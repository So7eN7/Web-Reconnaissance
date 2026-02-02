def score_path(finding):
    if finding["status_code"] == 200:
        return 0.9

    if finding["status_code"] in [301, 302]:
        return 0.7

    if finding["status_code"] == [401, 403]:
        return 0.8

    if finding["status_code"] == 500:
        return 0.6

    return 0.3
