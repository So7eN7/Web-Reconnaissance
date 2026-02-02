from dns_enum import enumerate_subdomains
from http_probe import probe_http
from header_analyzer import analyze_headers
from cookie_analyzer import analyze_cookies
from scoring import calculate_score
from report_generator import generate_json_report, generate_html_report
from datetime import datetime 

def main(domain):
    subdomains = enumerate_subdomains(domain)
    all_findings = []

    for sub in subdomains:
        if not sub["alive"]:
            continue

        url = f"http://{sub['subdomain']}"
        result = probe_http(url)

        if not result:
            continue

        header_findings = analyze_headers(result["headers"])
        cookie_findings = analyze_cookies(result["headers"])

        all_findings.extend(header_findings)
        all_findings.extend(cookie_findings)

    score = calculate_score(all_findings)

    report_data = {
        "domain": domain,
        "timestamp": datetime.utcnow().isoformat(),
        "subdomains": subdomains,
        "findings": all_findings,
        "score": score
    }

    generate_json_report(report_data)
    generate_html_report(report_data)

    print("Scan completed")
    print(f"Security score: {score}/100")
    print("Reports generated in reports/")

if __name__ == "__main__":
    target = input("Enter domain (example.com): ")
    main(target)
