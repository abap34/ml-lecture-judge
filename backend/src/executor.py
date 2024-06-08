import argparse
from dataclasses import dataclass
from pathlib import Path
import subprocess
import os

import datetime
from typing import Literal
from dataclasses import dataclass
import json
from pathlib import Path


@dataclass
class Config:
    code_file: Path
    input_file: Path
    time: float
    memory: float


@dataclass
class Result:
    stdout: str
    stderr: str
    status: Literal["OK", "RE", "TLE", "MLE", "IE"]
    time: float
    memory: float

    def to_json(self):
        return json.dumps(self.__dict__)


def main(config: Config) -> Result:
    cmd = ["python", str(config.code_file)]
    try:
        start_time = datetime.datetime.now()
        result = subprocess.run(
            cmd,
            timeout=config.time / 1000,
            input=config.input_file.read_text(),
            check=True,  # CalledProcessError を発生させる
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        end_time = datetime.datetime.now()

        elapsed_time = end_time - start_time 


    except subprocess.TimeoutExpired as e:
        return Result(
            stdout="",
            stderr="",
            status="TLE",
            time=e.timeout,
            memory=0.0,
        )
    except subprocess.CalledProcessError as e:
        return Result(
            stdout="",
            stderr=e.stderr,
            status="RE",
            time=0.0,
            memory=0.0,
        )

    return Result(
        stdout=result.stdout,
        stderr=result.stderr,
        status="OK",
        time=elapsed_time.total_seconds(),
        memory=0.0,
    )


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--code", type=str, required=True)
    argparser.add_argument("--input", type=str, required=True)
    argparser.add_argument("--time", type=float, default=1.0)
    args = argparser.parse_args()

    config = Config(
        code_file=Path(args.code),
        input_file=Path(args.input),
        time=args.time,
        memory=256.0,
    )

    result = main(config)
    print(result.to_json())
