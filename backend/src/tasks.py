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


def build_command(code, input_data, time, prehook_code):
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
            f"echo {prehook_code} > prehook_code.py && python3 prehook_code.py && echo {code} > target_code.py && echo {input_data} > input.txt && python3 /app/executor.py --code target_code.py --input input.txt --time {time}",
        ]
    )

    return cmd


# コンテナ内で実行
# code: str  実行するコード
# input_data: str  標準入力
# timelimit: int  時間制限 (ms)
# memorylimit: int  メモリ制限 (MB)
def run(
    code: str, input_data: str, timelimit: int, memorylimit: int, prehook_code: str = "",
) -> ExecutionResult:

    client = docker.from_env()
    try:
        log = client.containers.run(
            image="executor",
            command=build_command(code, input_data, timelimit, prehook_code),
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
    def __init__(self, status: JudgeResult, time: float, pass_cases: int, point: int = 0):
        self.status = status
        self.time = time
        self.pass_cases = pass_cases
        self.point = point

    def to_dict(self):
        return {
            "status": self.status,
            "time": self.time,
            "pass_cases": self.pass_cases,
            "point": self.point,
        }

    def to_json(self):
        return json.dumps(self.to_dict())


def normaljudge(
    output: str,
    expected: str,
    error_judge: bool,
    abs_error: Union[float, None],
    rel_error: Union[float, None],
    max_point: int,
) -> tuple[bool, int]:
    if error_judge:
        try:
            # 出力を2次元配列と見なして各要素を誤差ジャッジ
            output_lines = output.splitlines()
            expected_lines = expected.splitlines()
            if len(output_lines) != len(expected_lines):
                return (False, 0)
            for i in range(len(output_lines)):
                outputs = output_lines[i].split()
                expecteds = expected_lines[i].split()
                if len(outputs) != len(expecteds):
                    return (False, 0)
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
                            return (False, 0)
                    else:
                        if abs((output_float - expected_float) / expected_float) <= rel_error:
                            continue
                        else:
                            return (False, 0)

            return (True, max_point)
        except ValueError:
            # 出力が不正.
            return (False, 0)
    else:
        # 通常のジャッジ
        if output == expected:
            return (True, max_point)
        else:
            return (False, 0)


@app.task(name="tasks.evaluate_code")
def evaluate_code(
    code: str,
    testcases: list[dict[str, str]],
    timelimit: float,
    memorylimit: float,
    error_judge: bool = False,
    prehook_code: str = "",
    special_judge_code: str = "",
    abs_error: Union[float, None] = None,
    rel_error: Union[float, None] = None,
    max_point: int | str = 100    # "スペシャルジャッジ"　とかも飛んでくる
) -> dict:
    
    special_judge = special_judge_code != ""

    # 誤差ジャッジするなら abs_error と rel_error はどちらも指定されている必要がある
    if error_judge and (abs_error is None or rel_error is None):
        raise ValueError(
            "abs_error and rel_error must be specified when error_judge is True"
        )
    
    judger = normaljudge  # デフォルトでnormaljudgeを設定


    def special_judger(*args, **kwargs):
        raise NotImplementedError("Special judge is not implemented! Please override this function in special_judge_code")

    local_vars = {}
    
    if special_judge:
        print("Special judge is enabled")
        print("Special judge code: ", special_judge_code)
        exec(special_judge_code, globals(), local_vars)  # special_judge_codeを実行してjudger関数をローカル名前空間に定義
        special_judger = local_vars.get("special_judger")
        if not special_judger:
            raise RuntimeError("Special judge function not defined in special_judge_code")

    

    ng_cases = 0
    ok_cases = 0
    sum_point = 0

    max_time = -1
    for i, testcase in enumerate(testcases):
        input_data = testcase["input"]
        output_data = testcase["output"]
        # 実行
        result: ExecutionResult = run(
            code, 
            input_data=input_data, 
            timelimit=timelimit, 
            memorylimit=memorylimit, 
            prehook_code=prehook_code
        )


        status: ExecutionStatus = result.status

        # ノックアウトする
        if status != "OK":
            print(
                "Error occured while running the code. status: ",
                result.to_json()
            )
            return Judgement(
                status=status,
                time=result.time,
                pass_cases=i,
            ).to_dict()

        max_time = max(max_time, result.time)

        # ジャッジ. ここはノックアウトしないことに注意
        # 誤差ジャッジなら floatで読んで誤差ジャッジする.
        # 出力が不正なら WA
        if not special_judge:
            passed, point = judger(result.stdout, output_data, error_judge, abs_error, rel_error, max_point)
        else:
            passed, point = special_judger(result.stdout, output_data, error_judge, abs_error, rel_error, max_point)
        
        sum_point += point
        if passed:
            print("Test case", i, "passed")
            ok_cases += 1
        else:
            print("Test case", i, "failed")
            ng_cases += 1

    if ng_cases == 0:
        if special_judge:
            return Judgement(status="AC", time=max_time, pass_cases=ok_cases, point=sum_point).to_dict()
        else:
            return Judgement(status="AC", time=max_time, pass_cases=ok_cases, point=max_point).to_dict()
    else:
        return Judgement(status="WA", time=max_time, pass_cases=ok_cases, point=0).to_dict()    
    


        
    