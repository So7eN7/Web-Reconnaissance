INTERESTING = [200, 301, 302, 401, 403, 500]

def analyze(result):
    if result and result["status"] in INTERESTING:
        return result
    return None

