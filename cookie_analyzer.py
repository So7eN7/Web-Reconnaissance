def analyze_cookies(headers):
    findings = []
    cookies = headers.get("Set-Cookie", "")

    if not cookies:
        return findings

    cookie_list = cookies.split(",")

    for cookie in cookie_list:
        if "Secure" not in cookie:
            findings.append({
                "issue": "Cookie missing Secure flag",
                "severity": "Medium",
                "recommendation": "Add secure flag to cookies"
            })

        if "HttpOnly" not in cookie:
            findings.append({
                "issue": "Cookie missing HttpOnly flag",
                "severity": "High",
                "recommendation": "Add HttpOnly flag to cookies"
            })

        if "SameSite" not in cookie:
            findings.append({
                "issue": "Cookie missing SameSite attribute",
                "severity": "Low",
                "recommendation": "Set SameSite attribute"
            })

    return findings
