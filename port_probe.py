import socket

SAFE_PORTS = {
    80: "HTTP",
    443: "HTTPS",
    22: "SSH",
    21: "FTP",
    25: "SMTP"
}

def probe_ports(ip, timeout=2):
    open_ports = []

    for port, service in SAFE_PORTS.items():
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)

        try:
            sock.connect((ip, port))
            open_ports.append({
                    "port": port,
                    "expected_service": service,
                    "open": True
                })
        except Exception:
            pass
        finally:
            sock.close()

    return open_ports
