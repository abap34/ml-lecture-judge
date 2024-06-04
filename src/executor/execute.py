import sys
import traceback
import json

def main():
    try:
        user_code = sys.stdin.read()
        local_vars = {}
        exec(user_code, local_vars)
        result = local_vars.get('result', 'No result variable found')
        output = {"status": "success", "result": result}
    except Exception as e:
        output = {"status": "error", "error": str(e), "traceback": traceback.format_exc()}
    
    print(json.dumps(output))

if __name__ == "__main__":
    main()
