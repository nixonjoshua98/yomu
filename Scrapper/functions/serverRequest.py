import requests

def sendRequest(url):
    headers = requests.utils.default_headers()

    headers["user-agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
    
    try:
        page = requests.get(url, stream = True, timeout = 5, headers = headers)

    except Exception:
        return False

    else:
        if (page.status_code == 200):
            return page
        
        else:
            return False
