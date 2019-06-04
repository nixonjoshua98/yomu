def remove_trailing_zeros_if_zero(n):
    if is_float(n):
        if str(n).count(".") == 0 or str(n).endswith(".0"):
            return int(n)
        else:
            return float(n)
    return n


def remove_nasty_chars(s):
    try:
        return "".join([i for i in s if i not in ':\\/|*"><?.,'])
    except TypeError:
        return s


def is_float(f) -> bool:
    try:
        float(f)
    except ValueError:
        return False
    else:
        return True
