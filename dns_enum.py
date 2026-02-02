import dns.resolver

COMMON_SUBDOMAINS = [
    "www", "api", "dev", "test", "staging", "mail", "blog", "admin"
]

def enumerate_subdomains(domain):
    results = []
    for sub in COMMON_SUBDOMAINS:
        fqdn = f"{sub}.{domain}"
        try:
            answers = dns.resolver.resolve(fqdn, "A")
            ips = [a.to_text() for a in answers]
            results.append({
                "subdomain": fqdn,
                "ips": ips,
                "alive": True
            })
        except Exception:
            results.append({
                "subdomain": fqdn,
                "ips": [],
                "alive": False
            })
        
    return results

