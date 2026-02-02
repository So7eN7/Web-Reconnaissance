import argparse
import os
import socket
import time
from datetime import datetime
from tqdm import tqdm

from core.dns_enum import enumerate_subdomains
from core.http_probe import probe
from core.header_analyzer import analyze as header_analyze
from core.cookie_analyzer import analyze as cookie_analyze
from core.scoring import calculate
from core.output import info, success, warning, error, header, debug, configure

from service_scan.port_probe import scan as port_scan
from service_scan.banner_grabber import grab
from service_scan.service_classifier import classify

from dir_scan.path_wordlist import COMMON_PATHS
from dir_scan.path_scanner import scan as path_scan
from dir_scan.response_analyzer import analyze as path_analyze

from reports.report_generator import generate_json_report, generate_html_report

def run_scan(domain, run_headers, run_services, run_dirs, 
             output_dir, timeout, rate_limit, quiet, verbose):
    findings = []
    services = []
    paths = []

    header("Starting Reconnaissance")
    info(f"Target domain: {domain}")
    info(f"Timeout: {timeout}s | Rate limit: {rate_limit}s")

    subdomains = enumerate_subdomains(domain)
    success(f"Subdomains discovered: {len(subdomains)}")

    iterable = subdomains if quiet else tqdm(subdomains, desc="Scanning subdomains")

    for sub in iterable:
        if not sub["alive"]:
            debug(f"{sub['subdomain']} not reachable")
            continue

        info(f"Scanning {sub['subdomain']}")
        base_url = f"http://{sub['subdomain']}"

        http = probe(base_url, timeout=timeout)
        time.sleep(rate_limit)

        if not http:
            warning("HTTP probe failed")
            continue

        if run_headers:
            findings.extend(header_analyze(http["headers"]))
            findings.extend(cookie_analyze(http["cookies"]))

        if run_services:
            try:
                ip = socket.gethostbyname(sub["subdomain"])
                open_ports = port_scan(ip, timeout=timeout)

                for port in open_ports:
                    banner = grab(ip, port)
                    services.append({
                        "subdomain": sub["subdomain"],
                        "ip": ip,
                        "port": port,
                        "classification": classify(port, banner)
                    })
                    time.sleep(rate_limit)
            except Exception:
                warning("Service scan failed")

        if run_dirs:
            for path in COMMON_PATHS:
                result = path_scan(base_url, path)
                analysis = path_analyze(result)
                if analysis:
                    analysis["subdomain"] = sub["subdomain"]
                    paths.append(analysis)
                time.sleep(rate_limit)

    score = calculate(findings)

    report = {
        "domain": domain,
        "timestamp": datetime.now().astimezone().isoformat(),
        "score": score,
        "subdomains": subdomains,
        "findings": findings,
        "services": services,
        "paths": paths
    }

    os.makedirs(output_dir, exist_ok=True)
    os.chdir(output_dir)

    generate_json_report(report)
    generate_html_report(report)

    header("Reconnaissance completed")
    info(f"Target: {domain}")
    success(f"Security Score: {score}/100")
    success(f"Findings: {len(findings)}")
    success(f"Services identified: {len(services)}")
    success(f"Paths discovered: {len(paths)}")
    info(f"Reports saved to: {output_dir}")

def main():
    parser = argparse.ArgumentParser(
        description="Simple Passive Web Reconnaissance Tool"
    )

    subparsers = parser.add_subparsers(dest="command")
    scan = subparsers.add_parser("scan", help="Run passive reconnaissance")

    scan.add_argument("domain", help="Target domain (example.com)")
    scan.add_argument("--headers", action="store_true", help="HTTP header & cookie analysis")
    scan.add_argument("--services", action="store_true", help="Passive service recognition")
    scan.add_argument("--dirs", action="store_true", help="Passive directory discovery")
    scan.add_argument("--all", action="store_true", help="Run all modules (default)")
    scan.add_argument("--out", default="reports", help="Output directory")
    scan.add_argument("--timeout", type=int, default=5, help="Request timeout (seconds)")
    scan.add_argument("--rate-limit", type=float, default=0.5, help="Delay between requests (seconds)")
    scan.add_argument("--quiet", action="store_true", help="Minimal output")
    scan.add_argument("--verbose", action="store_true", help="Verbose output")

    args = parser.parse_args()

    if args.command != "scan":
        parser.print_help()
        return

    configure(quiet=args.quiet, verbose=args.verbose)

    run_headers = args.all or args.headers or not any([args.headers, args.services, args.dirs])
    run_services = args.all or args.services or not any([args.headers, args.services, args.dirs])
    run_dirs = args.all or args.dirs or not any([args.headers, args.services, args.dirs])

    run_scan(
        domain=args.domain,
        run_headers=run_headers,
        run_services=run_services,
        run_dirs=run_dirs,
        output_dir=args.out,
        timeout=args.timeout,
        rate_limit=args.timeout,
        quiet=args.quiet,
        verbose=args.verbose
    )


if __name__ == "__main__":
    main()
