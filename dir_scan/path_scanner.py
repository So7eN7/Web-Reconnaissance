import requests

def scan(base_url, path):
    url = f"{base_url.rstrip('/')}/{path}"
    try:
        r = requests.head(url, timeout=4, allow_redirects=False)
        return {"path": path, "url": url, "status": r.status_code}
    except Exception:
        return None

