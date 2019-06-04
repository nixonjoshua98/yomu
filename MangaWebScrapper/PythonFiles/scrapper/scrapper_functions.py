import requests


def send_request(url):
    headers = requests.utils.default_headers()

    try:
        page = requests.get(url, stream=True, timeout=5, headers=headers)

    except Exception:  # Should narrow it down
        return None

    else:
        return page if page.status_code == 200 else None
