def classify_service(port, banner, http_info=None):
    confidence = 0
    service = "Unknown"

    if port == 22 and "SSH" in banner:
        service = "SSH"
        confidence = 0.9

    elif port == 21 and "FTP" in banner:
        service = "FTP"
        confidence = 0.9

    elif port in [80, 443] and http_info:
        service = "HTTP"
        confidence = 0.95

    elif banner:
        service = "Generic TCP Service"
        confidence = 0.4
    
    return {
        "service": service,
        "confidence": confidence,
        "evidence": banner[:100]
    }
