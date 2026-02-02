import socket

def grab(ip, port):
    try:
        s = socket.socket()
        s.settimeout(2)
        s.connect((ip, port))
        if port in [80, 443]:
            s.send(b"HEAD / HTTP/1.1\r\nHost: test\r\n\r\n")
        banner = s.recv(1024).decode(errors="ignore")
        s.close()
        return banner.strip()
    except Exception:
        return ""

