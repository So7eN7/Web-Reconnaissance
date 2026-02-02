INTERESTING_STATUSES = {
    200: "Accessible resource",
    301: "Redirected resource",
    302: "Redirected resource",
    401: "Authentication required",
    403: "Forbidden (resource exists)",
    500: "Server error (possible misconfiguration)"
}

def analyze_response(result):
    if not result:
        return None

    status = result["status_code"]

    if status in INTERESTING_STATUSES:
        return {
            "path": result["path"],
            "url": result["url"],
            "status_code": status,
            "meaning": INTERESTING_STATUSES[status]
        }

    return None
