import requests
from bs4 import BeautifulSoup

def crawl_site(url):
    """
    Crawl the given URL and return all links and forms found.
    """
    try:
        r = requests.get(url, timeout=5)
        soup = BeautifulSoup(r.text, "html.parser")

        # Collect all links
        links = [a.get("href") for a in soup.find_all("a", href=True)]

        # Collect all forms
        forms = []
        for form in soup.find_all("form"):
            form_details = {
                "action": form.get("action"),
                "method": form.get("method", "get").lower(),
                "inputs": []
            }
            for input_tag in form.find_all("input"):
                form_details["inputs"].append({
                    "name": input_tag.get("name"),
                    "type": input_tag.get("type", "text"),
                    "value": input_tag.get("value", "")
                })
            forms.append(form_details)

        return {"links": links, "forms": forms}
    except Exception as e:
        return {"error": str(e)}
