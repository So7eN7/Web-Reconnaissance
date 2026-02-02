def analyze(cookie_header):
    findings = []
    if not cookie_header:
        return findings

    for cookie in cookie_header.split(","):
        if "HttpOnly" not in cookie:
            findings.append({
                "type": "Cookie",
                "issue": "Cookie missing HttpOnly",
                "severity": "High",
                "recommendation": "Add HttpOnly flag"
            })
        if "Secure" not in cookie:
            findings.append({
                "type": "Cookie",
                "issue": "Cookie missing Secure",
                "severity": "Medium",
                "recommendation": "Add Secure flag"
            })
    return findings

