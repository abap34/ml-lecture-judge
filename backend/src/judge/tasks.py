import os
import json
import shlex
import subprocess
from datetime import datetime
import docker
from celery import Celery
from typing import Literal
import docker.types
import logging

logging.basicConfig(
    level=logging.DEBUG,  
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        # logging.FileHandler("/app/logs/debug.log"), 
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")

app = Celery("tasks", broker=REDIS_URL, backend=REDIS_URL)

ExecutionStatus = Literal["OK", "RE", "TLE", "MLE", "IE"]


class ExecutionResult:
    def __init__(
        self,
        stdout: str,
        stderr: str,
        status: ExecutionStatus,
        time: float,
        finish_datetime: datetime,
    ):
        self.stdout = stdout
        self.stderr = stderr
        self.status = status
        self.time = time
        self.finish_datetime = finish_datetime

    @staticmethod
    def from_json(data: dict):
        return ExecutionResult(
            stdout=data["stdout"],
            stderr=data["stderr"],
            status=data["status"],
            time=data["time"],
            finish_datetime=datetime.now(),
        )

    def to_dict(self):
        return {
            "stdout": self.stdout,
            "stderr": self.stderr,
            "status": self.status,
            "time": self.time,
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
    cmd = subprocess.list2cmdline(
        [
            "/bin/sh",
            "-c",
            f"echo {code} > code.py && echo {input_data} > input.txt && python3 /app/executor.py --code code.py --input input.txt --time {time}",
        ]
    )

    logger.debug("cmd: %s", cmd)

    return cmd

# コンテナ内で実行
# code: str  実行するコード
# input_data: str  標準入力
# timelimit: int  時間制限 (ms)
# memorylimit: int  メモリ制限 (MB)
def run(code: str, input_data: str, timelimit: int, memorylimit: int) -> ExecutionResult:
    logger.debug("This is run function...")

    client = docker.from_env()
    try:
        # CPU使用率 20% 
        logger.debug("timelimit: %s", timelimit)
        logger.debug("memorylimit: %s", memorylimit)

        log = client.containers.run(
            image="executor",
            command=build_command(code, input_data, timelimit),
            # cpu_quota=cpu_quota,
            # cpu_period=cpu_period,
            # mem_limit=f"{memorylimit}m",
            # pids_limit=64,
            stdout=True,
            stderr=True,
        )

        stdout = log.decode("utf-8")

        try:
            logger.debug("Parsing the result...")
            return ExecutionResult.from_json(json.loads(stdout))

        except json.JSONDecodeError:
            logger.debug("Failed to parse the result. value: %s", stdout)
            return ExecutionResult(
                stdout="",
                stderr="Failed to parse the result. value: " + stdout,
                status="IE",
                time=0.0,
                finish_datetime=datetime.now(),
            )

    # 時間制限
    except docker.errors.ContainerError as e:
        logger.debug("ContainerError!", exc_info=e, stack_info=True)
        return ExecutionResult(
            stdout=e.stderr.decode("utf-8"),
            stderr="",
            status="TLE",
            time=0.0,
            finish_datetime=datetime.now(),
        )

    # メモリ制限
    except docker.errors.APIError as e:
        logger.debug("APIError!", exc_info=e, stack_info=True)
        return ExecutionResult(
            stdout="",
            stderr=str(e),
            status="MLE",
            time=0.0,
            finish_datetime=datetime.now(),
        )

    # 　予期せぬそのほかのエラー (ランタイムエラーは含まれない！. REは executor.py で処理される)
    except Exception as e:
        logger.debug("Unexpected error!", exc_info=e, stack_info=True)
        return ExecutionResult(
            stdout="",
            stderr=str(e),
            status="IE",
            time=0.0,
            finish_datetime=datetime.now(),
        )
    finally:
        client.close()



JudgeResult = Literal["WJ", "AC", "WA", "RE", "TLE", "MLE", "IE"]

class Judgement:
    def __init__(self, status: JudgeResult, time: float, pass_cases: int):
        self.status = status
        self.time = time
        self.pass_cases = pass_cases

    def to_dict(self):
        return {
            "status": self.status,
            "time": self.time,
            "pass_cases": self.pass_cases,
        }

    def to_json(self):
        return json.dumps(self.to_dict())


@app.task(name="tasks.evaluate_code")
def evaluate_code(code: str, testcases: list[tuple[str, str]], timelimit: float, memorylimit: float) -> Judgement:
    for i, (input_data, output_data) in enumerate(testcases):
        logger.debug(f"Case {i}: {input_data}  -> {output_data}")


        # 実行！
        result: ExecutionResult = run(code, input_data=input_data, timelimit=timelimit, memorylimit=memorylimit)
        status: ExecutionStatus = result.status

        # ノックアウトする
        if status != "OK":
            return Judgement(
                status=status,
                time=result.time,
                pass_cases=i,
            ).to_dict()
        
        # ジャッジ. ここもノックアウトする
        if result.stdout.strip() != output_data.strip():
            return Judgement(
                status="WA",
                time=result.time,
                pass_cases=i,
            ).to_dict()
        

    return Judgement(
        status="AC",
        time=result.time,
        pass_cases=i,
    ).to_dict()