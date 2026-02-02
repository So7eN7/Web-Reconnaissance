import socket

def resolve_domain(domain):
    try:
        ip = socket.gethostbyname(domain)
        return ip 
    except Exception:
        return None

