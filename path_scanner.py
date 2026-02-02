import requests

def scan_path(base_url, path):
    url = f"{base_url.rstrip('/')}/{path}"

    try:
        r = requests.head(url, timeout=4, allow_redirects=False)
        return {
            "path": path,
            "url": url,
            "status_code": r.status_code,
            "headers": dict(r.headers)
        }
    except Exception:
        return None
    
