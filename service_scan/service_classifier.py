def classify(port, banner):
    if port == 22 and "SSH" in banner:
        return {"service": "SSH", "confidence": 0.9}
    if port in [80, 443]:
        return {"service": "HTTP", "confidence": 0.95}
    return {"service": "Unknown", "confidence": 0.4}

