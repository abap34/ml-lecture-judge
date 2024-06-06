# 問題作成用の CLIツール.
# gen {problem_name}: 問題作成
# test {problem_name} {solution}: テストケース作成
# check {problem_name}: 問題設定のチェック

import argparse
import os
import pathlib
import glob
import yaml

CONFIG = {"summary": ["title", "points"], "constraint": ["time", "memory"]}

PROBLEM_TEMPLATE = """\
# 概要
summary: 
  title: 
  points: 
  
# 制約
constraint:
  # 実行時間制限 (ミリ秒)
  time: 
  # メモリ制限 (MB)
  memory: 
"""


# 問題を作成する.
# problems/{problem_name} に問題ディレクトリを作成して、problem.yaml, solution.py, description.md, in, out ディレクトリを作成する.
def generate_problem(problem_name: str):
    print(f"Creating problem {problem_name}")
    if os.path.exists(f"problems/{problem_name}"):
        raise Exception(f"Problem {problem_name} already exists")

    os.makedirs(f"problems/{problem_name}")
    with open(f"problems/{problem_name}/problem.yaml", "w") as f:
        f.write(PROBLEM_TEMPLATE)

    with open(f"problems/{problem_name}/solution.py", "w") as f:
        f.write("# Solution")
    
    with open(f"problems/{problem_name}/description.md", "w") as f:
        f.write("# Description")

    print(f"Problem {problem_name} created")

    os.makedirs(f"problems/{problem_name}/in")
    os.makedirs(f"problems/{problem_name}/out")


# テストケースを生成する.
# problems/{problem_name}/in/*.in を読み込んで problems/{problem_name}/solution.py を実行して、out/*.out を生成する.
def generate_testcases(problem_name: str):
    print(f"Generating testcases for {problem_name}")
    if not os.path.exists(f"problems/{problem_name}"):
        raise Exception(f"Problem {problem_name} does not exist")

    if not os.path.exists(f"problems/{problem_name}/solution.py"):
        raise Exception(f"solution.py does not exist for problem {problem_name}")

    # in/*.in を読み込んで、out/*.out を生成する
    inputs = glob.glob(f"problems/{problem_name}/in/*.in")

    print(f"Generating testcases for {problem_name}. {len(inputs)} testcases found")

    for input_file in inputs:
        print(f"Generating testcase for {input_file}")
        output_file = input_file.replace("/in/", "/out/").replace(".in", ".out")

        os.system(f"python problems/{problem_name}/solution.py < {input_file} > {output_file}")

    print("Testcases generated")


# 問題設定をチェックする.
# problems/{problem_name}/problem.yaml が存在して正しい形式であるかをチェックする.
# description.md, solution.py が存在しているかをチェックする.
# in/*.in と out/*.out が対応しているかをチェックする.
def check_problem(problem_name: str):
    print(f"Checking problem {problem_name}")

    if not os.path.exists(f"problems/{problem_name}"):
        raise Exception(f"Problem {problem_name} does not exist")

    # problem.yaml のチェック.
    with open(f"problems/{problem_name}/problem.yaml") as f:
        summary = yaml.safe_load(f)

        for section, keys in CONFIG.items():
            if section not in summary:
                raise Exception(f"{section} is missing in problem.yaml")

            for key in keys:
                if key not in summary[section]:
                    raise Exception(f"{key} is missing in problem.yaml")

    inputs = glob.glob(f"problems/{problem_name}/in/*.in")
    outputs = glob.glob(f"problems/{problem_name}/out/*.out")

    if len(inputs) != len(outputs):
        raise Exception(
            f"Number of input and output files do not match for problem {problem_name}"
        )

    for input_file in inputs:
        output_file = input_file.replace("/in/", "/out/").replace(".in", ".out")
        if not os.path.exists(output_file):
            raise Exception(f"Output file {output_file} does not exist")
        
    if not os.path.exists(f"problems/{problem_name}/solution.py"):
        raise Exception(f"solution.py does not exist for problem {problem_name}")
    
    if not os.path.exists(f"problems/{problem_name}/description.md"):
        raise Exception(f"description.md does not exist for problem {problem_name}")

    print(f"Problem {problem_name} is valid")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["gen", "genout", "check"])
    parser.add_argument("problem_name")
    parser.add_argument("solution", nargs="?")
    args = parser.parse_args()

    if args.command == "gen":
        generate_problem(args.problem_name)
    elif args.command == "genout":
        generate_testcases(args.problem_name, pathlib.Path(args.solution))
    elif args.command == "check":
        check_problem(args.problem_name)
    else:
        raise Exception("Invalid command")


if __name__ == "__main__":
    main()