import dns.resolver

COMMON_SUBDOMAINS = ["www", "api", "dev", "test", "staging", "mail"]

def enumerate_subdomains(domain):
    results = []
    for sub in COMMON_SUBDOMAINS:
        fqdn = f"{sub}.{domain}"
        try:
            answers = dns.resolver.resolve(fqdn, "A")
            results.append({
                "subdomain": fqdn,
                "ips": [a.to_text() for a in answers],
                "alive": True
            })
        except Exception:
            results.append({
                "subdomain": fqdn,
                "ips": [],
                "alive": False
            })
    return results
