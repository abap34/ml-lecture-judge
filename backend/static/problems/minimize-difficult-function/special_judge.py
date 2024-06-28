def special_judger(
    output: str,
    expected: str,
    error_judge: bool,
    abs_error,
    rel_error,
    max_point: int,
) -> tuple[bool, int]:
    try:
        import math
        target = float(expected.strip())
        out = float(output.strip()) 
        
        # out が NaN とかだったら弾く
        if math.isnan(out):
            return False, 0

        # 絶対誤差
        abs_err = abs(out - target)
        if abs_err <= 0.001:
            return True, 1000

        # 相対誤差
        if target != 0:
            rel_err = abs(abs_err / target)
            if rel_err <= 0.001:
                return True, 1000   
        
        # どちらもダメだったら
        return True, max(0, math.ceil(1000 * (1 - 50 * abs(out - target))))
    except ValueError as e:
        print(e)
        return False, 0
