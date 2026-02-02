import requests

def probe(url, timeout=5):
    try:
        r = requests.get(url, timeout=timeout, allow_redirects=True)
        return {
            "url": r.url,
            "status": r.status_code,
            "headers": dict(r.headers),
            "cookies": r.headers.get("Set-Cookie", "")
        }
    except Exception:
        return None

