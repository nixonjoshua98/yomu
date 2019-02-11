import requests

def sendRequest(url):
    headers = requests.utils.default_headers()
    
    try:
        page = requests.get(url, stream = True, timeout = 5, headers = headers)

    except Exception:
        return False

    else:
        if (page.status_code == 200):
            return page
        
        else:
            return False
