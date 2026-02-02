SECURITY_HEADERS = {
    "Content-Security-Policy": "High",
    "Strict-Transport-Security": "High",
    "X-Frame-Options": "Medium",
    "X-Content-Type-Options": "Medium",
    "Referrer-Policy": "Low"
}

def analyze(headers):
    findings = []
    for h, sev in SECURITY_HEADERS.items():
        if h not in headers:
            findings.append({
                "type": "Header",
                "issue": f"Missing {h}",
                "severity": sev,
                "recommendation": f"Add {h} header"
            })
    return findings

