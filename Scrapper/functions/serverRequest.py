import requests

def sendRequest(url):
    headers = requests.utils.default_headers()
    
    headers["user-agent"] = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"
        )
    
    try:
        page = requests.get(url, stream = True, timeout = 5, headers = headers)

    except Exception:
        return False

    else:
        if (page.status_code == 200):
            return page
        
        else:
            return False
