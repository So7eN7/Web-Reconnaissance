WEIGHTS = {"High": 15, "Medium": 10, "Low": 5}

def calculate(findings):
    score = 100
    for f in findings:
        score -= WEIGHTS.get(f["severity"], 0)
    return max(score, 0)
