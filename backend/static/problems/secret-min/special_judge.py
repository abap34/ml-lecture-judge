def special_judger(
    output: str,
    expected: str,
    error_judge: bool,
    abs_error,
    rel_error,
    max_point: int,
) -> tuple[bool, int]:
    try:
        
        secreat_num = 34
        int_output = int(output.strip())
        
        if not (-10**3 <= int_output <= 10**3):
            return False, 0
        
        return True, max(0, 10 - (int_output - secreat_num) ** 2)
    except ValueError as e:
        print(e)
        return False, 0
