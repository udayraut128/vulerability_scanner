import requests

def get_geo_location(ip):
    try:
        r = requests.get(f"https://ipinfo.io/{ip}/json", timeout=5)
        return r.json()
    except:
        return {}
