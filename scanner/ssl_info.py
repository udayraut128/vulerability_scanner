import ssl, socket

def get_ssl_info(hostname):
    try:
        ctx = ssl.create_default_context()
        with ctx.wrap_socket(socket.socket(), server_hostname=hostname) as s:
            s.connect((hostname, 443))
            cert = s.getpeercert()
            return {
                "Issuer": cert.get("issuer"),
                "Expiry": cert.get("notAfter")
            }
    except:
        return "No SSL Info"
