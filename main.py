from dns_resolver import resolve_domain
from port_probe import probe_ports
from banner_grabber import grab_banner
from http_fingerprint import fingerprint_http
from tls_inspector import inspect_tls
from service_classifer import classify_service
from report_generator import generate_json_report, generate_html_report
from datetime import datetime 

def main(domain):
    ip = resolve_domain(domain)
    if not ip:
        print("Could not resolve domain")
        return
    
    services = []
    open_ports = probe_ports(ip)

    for entry in open_ports:
        port = entry["port"]
        banner = grab_banner(ip, port)

        http_info = None
        tls_info = None

        if port == 80:
            http_info = fingerprint_http(f"http://{domain}")
        elif port == 443:
            http_info = fingerprint_http(f"https://{domain}")
            tls_info = inspect_tls(ip)

        classification = classify_service(port, banner, http_info)

        services.append({
            "port": port,
            "banner": banner,
            "http_info": http_info,
            "tls_info": tls_info,
            "classification": classification
        })

    report = {
        "domain": domain,
        "ip": ip,
        "timestamp": datetime.utcnow().isoformat(),
        "services": services
    }

    generate_json_report(report)
    generate_html_report(report)
    print("Service scan completed.")


if __name__ == "__main__":
    target = input("Enter domain: ")
    main(target)

        
