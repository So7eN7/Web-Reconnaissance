import requests

def probe_http(url):
    try:
        response = requests.get(
            url,
            timeout = 5,
            allow_redirects = True
        )
        return {
            "url": response.url,
            "status_code": response.status_code,
            "headers": dict(response.headers),
            "cookies": response.cookies.get_dict()
        }
    except Exception:
        return None
