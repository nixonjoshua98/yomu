import requests


class ScrapperBase:

	@staticmethod
	def _send_request(url):
		headers = requests.utils.default_headers()

		headers["User-Agent"] = "Python"

		try:
			page = requests.get(url, stream=True, timeout=5, headers=headers)

		except requests.exceptions.RequestException as e:  # Should narrow it down
			return None

		else:
			return page if page.status_code == 200 else None

	@staticmethod
	def _str_to_num(num):
		"""
		10.0 	-> 10	<int>
		10.5 	-> 10.5<float>
		0 		-> 0	<int>
		0.0 	-> 0	<int>
		"""
		return float(num) if num.count(".") == 1 and not num.endswith(".0") else int(num.replace(".0", ""))
