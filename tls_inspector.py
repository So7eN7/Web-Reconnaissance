import ssl
import socket
from cryptography import x509
from cryptography.hazmat.backends import default_backend

def inspect_tls(ip, port=443):
    try:
        context = ssl.create_default_context()
        sock = socket.create_connection((ip, port))
        ssock = context.wrap_socket(sock, server_hostname=ip)

        cert_bin = ssock.getpeercert(binary_form=True)
        cert = x509.load_der_x509_certificate(cert_bin, default_backend())

        return {
            "issuer": cert.issuer.rfc4514_string(),
            "subject": cert.subject.rfc4514_string(),
            "not_before": cert.not_valid_before.isoformat(),
            "not_after": cert.not_valid_after.isoformat(),
            "signiture_algorithm": cert.signiture_hash_algorithm.name
        }
    except Exception:
        return None
