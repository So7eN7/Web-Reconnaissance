SECURITY_HEADERS = {
    "Content-Security-Policy": "High",
    "Strict-Transport-Security": "High",
    "X-Frame-Options": "Medium",
    "X-Content-Type-Options": "Medium",
    "Referrer-Policy": "Low"
}

def analyze_headers(headers):
    findings = []

    for header, severity in SECURITY_HEADERS.items():
        if header not in headers:
            findings.append({
                "issue": f"Missing {header}",
                "severity": severity,
                "recommendation": f"Add {header} header" 
            })

    return findings


