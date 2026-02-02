import socket

def grab_banner(ip, port, timeout=2):
    try:
        sock = socket.socket()
        sock.settimeout(timeout)
        sock.connect((ip, port))

        if port in [80, 443]:
            sock.send(b"HEAD / HTTP1,1\r\nHost: test\r\n\r\n")

        banner = sock.recv(1024).decode(errors="ignore").strip()
        sock.close()
        return banner
    except Exception:
        return ""
