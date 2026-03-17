import requests

def check_sql_injection(url):
    payloads = ["' OR '1'='1", "'; DROP TABLE users--"]
    for p in payloads:
        try:
            r = requests.get(url + "?id=" + p, timeout=5)
            if "error" in r.text.lower() or "sql" in r.text.lower():
                return True
        except:
            pass
    return False

def check_xss(url):
    payload = "<script>alert(1)</script>"
    try:
        r = requests.get(url + "?q=" + payload, timeout=5)
        if payload in r.text:
            return True
    except:
        pass
    return False
