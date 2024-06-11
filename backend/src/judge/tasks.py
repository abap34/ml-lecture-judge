import os
import json
import shlex
import subprocess
from datetime import datetime
import docker
from celery import Celery
from typing import Literal, Union
import docker.types

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
            f"echo {code} > target_code.py && echo {input_data} > input.txt && python3 /app/executor.py --code target_code.py --input input.txt --time {time}",
        ]
    )

    return cmd


# コンテナ内で実行
# code: str  実行するコード
# input_data: str  標準入力
# timelimit: int  時間制限 (ms)
# memorylimit: int  メモリ制限 (MB)
def run(
    code: str, input_data: str, timelimit: int, memorylimit: int
) -> ExecutionResult:

    client = docker.from_env()
    try:
        log = client.containers.run(
            image="executor",
            command=build_command(code, input_data, timelimit),
            mem_limit=f"{memorylimit}m",
            pids_limit=128,
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
                finish_datetime=datetime.now(),
            )

    # 時間制限
    except docker.errors.ContainerError as e:
        return ExecutionResult(
            stdout=e.stderr.decode("utf-8"),
            stderr="",
            status="TLE",
            time=0.0,
            finish_datetime=datetime.now(),
        )

    # メモリ制限
    except docker.errors.APIError as e:
        return ExecutionResult(
            stdout="",
            stderr=str(e),
            status="MLE",
            time=0.0,
            finish_datetime=datetime.now(),
        )

    # 　予期せぬそのほかのエラー (ランタイムエラーは含まれない！. REは executor.py で処理される)
    except Exception as e:
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


def passed(
    output: str,
    expected: str,
    error_judge: bool,
    abs_error: Union[float, None],
    rel_error: Union[float, None],
) -> bool:
    if error_judge:
        try:
            # 出力を2次元配列と見なして各要素を誤差ジャッジ
            output_lines = output.splitlines()
            expected_lines = expected.splitlines()
            if len(output_lines) != len(expected_lines):
                return False
            for i in range(len(output_lines)):
                outputs = output_lines[i].split()
                expecteds = expected_lines[i].split()
                if len(outputs) != len(expecteds):
                    return False
                for j in range(len(outputs)):
                    output_float = float(outputs[j])
                    expected_float = float(expecteds[j])
                    
                    # 絶対誤差が abs_error 以下なら ok
                    if abs(output_float - expected_float) <= abs_error:
                        continue

                    # 相対誤差が rel_error 以下なら ok
                    if expected_float == 0:
                        if output_float == 0:
                            continue
                        else:
                            return False
                    else:
                        if abs((output_float - expected_float) / expected_float) <= rel_error:
                            continue
                        else :
                            return False

            return True
        except ValueError:
            # 出力が不正.
            return False
    else:
        # 通常のジャッジ
        return output == expected


@app.task(name="tasks.evaluate_code")
def evaluate_code(
    code: str,
    testcases: list[tuple[str, str]],
    timelimit: float,
    memorylimit: float,
    error_judge: bool = False,
    abs_error: Union[float, None] = None,
    rel_error: Union[float, None] = None,
) -> dict:
    # 誤差ジャッジするなら abs_error と rel_error はどちらも指定されている必要がある
    if error_judge and (abs_error is None or rel_error is None):
        raise ValueError(
            "abs_error and rel_error must be specified when error_judge is True"
        )

    ng_cases = 0
    ok_cases = 0

    max_time = -1
    for i, (input_data, output_data) in enumerate(testcases):
        # 実行
        result: ExecutionResult = run(
            code, input_data=input_data, timelimit=timelimit, memorylimit=memorylimit
        )
        status: ExecutionStatus = result.status

        # ノックアウトする
        if status != "OK":
            return Judgement(
                status=status,
                time=result.time,
                pass_cases=i,
            ).to_dict()

        max_time = max(max_time, result.time)

        # ジャッジ. ここはノックアウトしないことに注意
        # 誤差ジャッジなら floatで読んで誤差ジャッジする.
        # 出力が不正なら WA
        if passed(result.stdout, output_data, error_judge, abs_error, rel_error):
            ok_cases += 1
        else:
            ng_cases += 1

    if ng_cases == 0:
        return Judgement(status="AC", time=max_time, pass_cases=ok_cases).to_dict()
    else:
        return Judgement(status="WA", time=max_time, pass_cases=ok_cases).to_dict()
