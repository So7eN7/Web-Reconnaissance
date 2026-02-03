from core.output import debug

def calculate(findings, services=None, paths=None):
    score = 100
    breakdown = []

    for f in findings:
        if f["severity"] == "High":
            penalty = 15
        elif f["severity"] == "Medium":
            penalty = 7
        elif f["severity"] == "Low":
            penalty = 3
        else:
            continue

        score -= penalty

        entry = {
            "category": f["type"],
            "penalty": penalty,
            "reason": f["issue"]
        }
        breakdown.append(entry)

        debug(
            f"[score] -{penalty}  {f['type']}: {f['issue']}"
        )

    if services:
        risky_ports = {21, 23, 25, 3306, 3389}
        for s in services:
            if s["port"] in risky_ports:
                penalty = 5
                score -= penalty
        
                entry = {
                    "category": "Service Exposure",
                    "penalty": penalty,
                    "reason": (
                        f"{s['classification']['service']}"
                        f"on port {s['port']}"
                    )
                }
                breakdown.append(entry)

                debug(
                    f"[score] -{penalty} Exposed service"
                    f"{s['classification']['service']}"
                    f"on port {s['port']}"
                )

    if paths:
        sensitive = {"admin", "login", "backup", ".git", ".env"}
        for p in paths:
            if p["path"].lower() in sensitive:
                penalty = 3 
                score -= penalty

                entry = {
                    "category": "Sensitive Path",
                    "penalty": penalty,
                    "reason": f"/{p['path']}"
                }
                breakdown.append(entry)

                debug(
                    f"[score] -{penalty} Sensitive path discovered /{p['path']}"
                )

    return max(score, 0), breakdown
