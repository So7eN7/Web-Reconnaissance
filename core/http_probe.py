import requests

def probe(url):
    try:
        r = requests.get(url, timeout=5, allow_redirects=True)
        return {
            "url": r.url,
            "status": r.status_code,
            "headers": dict(r.headers),
            "cookies": r.headers.get("Set-Cookie", "")
        }
    except Exception:
        return None

