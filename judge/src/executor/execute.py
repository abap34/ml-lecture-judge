import sys

def main():
    code = sys.stdin.read()
    exec(code)

if __name__ == "__main__":
    main()