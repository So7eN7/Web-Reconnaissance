from path_wordlist import COMMON_PATHS
from path_scanner import scan_path
from response_analyzer import analyze_response
from confidence_scoring import score_path
from report_generator import generate_json_report, generate_html_report
from datetime import datetime 

def main(base_url):
    findings = []

    for path in COMMON_PATHS:
        result = scan_path(base_url, path)
        analysis = analyze_response(result)

        if analysis:
            analysis["confidence"] = score_path(analysis)
            findings.append(analysis)

    report = {
        "target": base_url,
        "timestamp": datetime.utcnow().isoformat(),
        "results": findings
    }

    generate_json_report(report)
    generate_html_report(report)

    print("Directory scan complete.")
    print(f"Findings: {len(findings)}")

if __name__ == "__main__":
    target = input("Enter base URL: ")
    main(target)
