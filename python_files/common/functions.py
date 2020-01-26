
def remove_trailing_zeroes(s: str):
	s = str(s)

	return int(s) if s.count(".") == 0 or s.endswith(".0") else float(s)