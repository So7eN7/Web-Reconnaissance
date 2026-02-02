SEVERITY_SCORES = {
    "High": 15,
    "Medium": 10,
    "Low": 5
}

def calculate_score(findings):
    score = 100
    for f in findings:
        score -= SEVERITY_SCORES.get(f["severity"], 0)

    return max(score, 0)
