import requests, socket, ipaddress

def get_server_info(url):
    try:
        r = requests.get(url, timeout=5)
        return r.headers.get("Server", "Unknown")
    except:
        return "Unknown"

def check_ip_type(url):
    try:
        hostname = url.split("//")[-1].split("/")[0]
        ip = socket.gethostbyname(hostname)
        ip_type = "Private" if ipaddress.ip_address(ip).is_private else "Public"
        return ip, ip_type
    except:
        return None, "Error"

def is_safe(url):
    try:
        r = requests.get(url, timeout=5)
        https = url.startswith("https")
        has_csp = "Content-Security-Policy" in r.headers
        if https and has_csp:
            return "Likely Safe"
        else:
            return "Potentially Unsafe"
    except:
        return "Error"
