import socket

SAFE_PORTS = [21, 22, 25, 80, 443]

def scan(ip, timeout=2):
    open_ports = []
    for port in SAFE_PORTS:
        s = socket.socket()
        s.settimeout(timeout)
        try:
            s.connect((ip, port))
            open_ports.append(port)
        except Exception:
            pass
        finally:
            s.close()
    return open_ports

