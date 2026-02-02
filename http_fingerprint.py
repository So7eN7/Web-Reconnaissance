import requests

def fingerprint_http(url):
    try:
        r = requests.get(url, timeout=4)
        return {
            "server": r.headers.get("Server", ""),
            "x_powered_by": r.headers.get("X-Powered-By", ""),
            "status_code": r.status_code,
            "headers": dict(r.headers)
        }
    except Exception:
        return None

