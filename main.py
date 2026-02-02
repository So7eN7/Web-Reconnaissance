from core.dns_enum import enumerate_subdomains
from core.http_probe import probe
from core.header_analyzer import analyze as header_analyze
from core.cookie_analyzer import analyze as cookie_analyze
from core.scoring import calculate

from service_scan.port_probe import scan as port_scan
from service_scan.banner_grabber import grab
from service_scan.service_classifier import classify

from dir_scan.path_wordlist import COMMON_PATHS
from dir_scan.path_scanner import scan as path_scan
from dir_scan.response_analyzer import analyze as path_analyze

from reports.report_generator import generate_json_report, generate_html_report
from datetime import datetime
import socket

def main(domain):
    findings = []
    services = []
    paths = []

    subs = enumerate_subdomains(domain)

    for sub in subs:
        if not sub["alive"]:
            continue

        url = f"http://{sub['subdomain']}"
        http = probe(url)
        if not http:
            continue

        findings += header_analyze(http["headers"])
        findings += cookie_analyze(http["cookies"])

        try:
            ip = socket.gethostbyname(sub["subdomain"])
            ports = port_scan(ip)

            for p in ports:
                banner = grab(ip, p)
                services.append({
                    "subdomain": sub["subdomain"],
                    "port": p,
                    "classification": classify(p, banner)
                })
        except Exception:
            pass


        for path in COMMON_PATHS:
            r = path_scan(url, path)
            a = path_analyze(r)
            if a:
                paths.append(a)

    score = calculate(findings)

    report = {
        "domain": domain,
        "timestamp": datetime.now().astimezone().isoformat(),
        "score": score,
        "subdomains": subs,
        "findings": findings,
        "services": services,
        "paths": paths
    }

    generate_json_report(report)
    generate_html_report(report)

    print("Recon complete")
    print(f"Security score: {score}/100")

if __name__ == "__main__":
    target = input("Enter domain: ")
    main(target)

