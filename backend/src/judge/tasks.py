import os
import json
import shlex
import subprocess
from datetime import datetime
import docker
from celery import Celery


REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")

app = Celery("tasks", broker=REDIS_URL, backend=REDIS_URL)


class ExecutionResult:
    def __init__(
        self,
        stdout: str,
        stderr: str,
        status: str,
        time: float,
        memory: float,
        finish_datetime: datetime,
    ):
        self.stdout = stdout
        self.stderr = stderr
        self.status = status
        self.time = time
        self.memory = memory
        self.finish_datetime = finish_datetime

    @staticmethod
    def from_json(data: dict):
        return ExecutionResult(
            stdout=data["stdout"],
            stderr=data["stderr"],
            status=data["status"],
            time=data["time"],
            memory=data["memory"],
            finish_datetime=datetime.now(),
        )

    def to_dict(self):
        return {
            "stdout": self.stdout,
            "stderr": self.stderr,
            "status": self.status,
            "time": self.time,
            "memory": self.memory,
            "finish_datetime": self.finish_datetime.isoformat(),
        }

    def to_json(self):
        return json.dumps(self.to_dict())


def build_command(code, input_data, time):
    # quote して攻撃を防ぐ
    code = shlex.quote(code)
    input_data = shlex.quote(input_data)
    time = shlex.quote(str(time))

    # /bin/sh を挟まないと && が使えないので使う.
    # list2cmdline でコードの内部の特殊文字もエスケープする
    return subprocess.list2cmdline(
        [
            "/bin/sh",
            "-c",
            f"echo {code} > code.py && echo {input_data} > input.txt && python /app/executor.py --code code.py --input input.txt --time {time}",
        ]
    )


def run(code: str, input_data: str, time: float, memory: float) -> ExecutionResult:
    client = docker.from_env()
    try:
        log = client.containers.run(
            image="executor_image",
            command=build_command(code, input_data, time),
            cpu_period=1000000,  # 1000ms
            mem_limit=f"{memory}m",
            pids_limit=4,
            stdout=True,
            stderr=True,
        )

        stdout = log.decode("utf-8")

        try:
            return ExecutionResult.from_json(json.loads(stdout))

        except json.JSONDecodeError:
            return ExecutionResult(
                stdout="",
                stderr="Failed to parse the result. value: " + stdout,
                status="IE",
                time=0.0,
                memory=0.0,
                finish_datetime=datetime.now(),
            )

    # 時間制限
    except docker.errors.ContainerError as e:
        return ExecutionResult(
            stdout=e.stderr.decode("utf-8"),
            stderr="",
            status="TLE",
            time=0.0,
            memory=0.0,
            finish_datetime=datetime.now(),
        )

    # メモリ制限
    except docker.errors.APIError as e:
        return ExecutionResult(
            stdout="",
            stderr=str(e),
            status="MLE",
            time=0.0,
            memory=0.0,
            finish_datetime=datetime.now(),
        )

    # 　予期せぬそのほかのエラー (ランタイムエラーは含まれない！. REは executor.py で処理される)
    except docker.errors.DockerException as e:
        return ExecutionResult(
            stdout="",
            stderr=str(e),
            status="IE",
            time=0.0,
            memory=0.0,
            finish_datetime=datetime.now(),
        )
    finally:
        client.close()


@app.task(name="tasks.evaluate_code")
def evaluate_code(code: str, submission_time: str):
    # 20s
    result = run(code, input_data="hogehoge", time=2000.0, memory=256.0)

    return {
        "submission_time": submission_time,
        "result": result.to_dict(),
    }
