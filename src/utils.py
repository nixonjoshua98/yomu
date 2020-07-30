import time


def print_time(f):
	def decorator(*args, **kwargs):
		start = time.time()

		f(*args, **kwargs)

		end = time.time()

		print(f"{f.__name__} - {round(end - start, 5):.5f}s.")

	return decorator


def get(ls, **kwargs):
	for ele in ls:
		if all(str(ele[k]) == str(v) for k, v in kwargs.items()):
			return ele
	return None
