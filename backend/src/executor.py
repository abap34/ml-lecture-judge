import argparse
from dataclasses import dataclass
from pathlib import Path
import subprocess
import datetime
from typing import Literal
from dataclasses import dataclass
import json
from pathlib import Path
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
# debug も出力するように設定
logger.setLevel(logging.DEBUG)

@dataclass
class Config:
    code_file: Path
    input_file: Path
    time: float


@dataclass
class Result:
    stdout: str
    stderr: str
    status: Literal["OK", "RE", "TLE", "MLE", "IE"]
    time: float

    def to_json(self):
        return json.dumps(self.__dict__)


def main(config: Config) -> Result:
    logger.debug("This is executor.py...")

    cmd = ["python3", str(config.code_file)]

    logger.debug("cmd: %s", cmd)

    try:
        start_time = datetime.datetime.now()
        logger.debug("start_time: %s", start_time)
        logger.debug("start execution with:")
        logger.debug("input:\n%s", config.input_file.read_text())
        logger.debug("code:\n%s", config.code_file.read_text())
        logger.debug("timeout: %s", config.time / 1000)

        result = subprocess.run(
            cmd,
            timeout=config.time / 1000,
            input=config.input_file.read_text(),
            check=True,  # CalledProcessError を発生させる
            capture_output=True,
            text=True,
            encoding="utf-8",
        )

        logger.debug("Finished execution Successfully")
        logger.debug("stdout: %s", result.stdout)
        logger.debug("stderr: %s", result.stderr)
        end_time = datetime.datetime.now()
        
        elapsed_time = end_time - start_time 


    except subprocess.TimeoutExpired as e:
        logger.debug("TimeoutExpired!", exc_info=e, stack_info=True, extra={"stdout": e.stdout, "stderr": e.stderr})
        return Result(
            stdout=e.stdout,
            stderr=e.stderr,
            status="TLE",
            time=e.timeout,
        )
    except subprocess.CalledProcessError as e:
        logger.debug("CalledProcessError!", exc_info=e, stack_info=True, extra={"stdout": e.stdout, "stderr": e.stderr})
        return Result(
            stdout=e.stdout,
            stderr=e.stderr,
            status="RE",
            time=0.0,
        )
    except Exception as e:
        logger.debug("Unexpected Error!", exc_info=e, stack_info=True)
        return Result(
            stdout="",
            stderr=str(e),
            status="IE",
            time=0.0,
        )

    return Result(
        stdout=result.stdout,
        stderr=result.stderr,
        status="OK",
        time=elapsed_time.total_seconds(),
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
    )

    result = main(config)
    print(result.to_json())
