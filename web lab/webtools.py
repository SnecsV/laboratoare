# Laborator: funcții, metode și importuri pe web
# Student: Gonța Marius
 
BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10  # secunde
DEFAULT_HEADERS = {"User-Agent": "WebLab-Gonța Marius"} 

import requests as rq



def fetch(url, timeout=TIMEOUT):
    return rq.get(url, headers=DEFAULT_HEADERS, timeout=timeout)

def get_status(url, timeout=TIMEOUT):
    response = rq.get(url, timeout=timeout)
    return response.status_code

def get_title(url, timeout=TIMEOUT):
    response = rq.get(url, timeout=timeout)
    start = response.text.find("<title>") + len("<title>")
    end = response.text.find("</title>")
    return response.text[start:end].strip()

def security_headers(url):
    """Returnează un dicționar cu header-ele de securitate pentru URL-ul dat."""
    response = rq.get(url, timeout=TIMEOUT)
    headers = [
        "Strict-Transport-Security",
        "Content-Security-Policy",
        "X-Content-Type-Options",
        "X-Frame-Options",
        "Referrer-Policy",
    ]
    return {header: header in response.headers for header in headers}

def site_report(url, timeout=TIMEOUT):
    from part3_functions import score_headers
    from part4_modules import cert_days_left
    from part4_modules import split_links
    from part4_modules import extract_links
    from part3_functions import disallowed_paths
    """Returnează un dicționar cu informații despre site-ul dat."""
    response = rq.get(url, timeout=timeout)
    return {
        "status_code": response.status_code,
        "Title": get_title(url, timeout),
        "Adresa IP": response.raw._connection.sock.getpeername()[0],
        "Redictări": response.history,
        "Scor securitate": score_headers(url),
        "Zile până la expirarea certificatului": cert_days_left(url),
        "Legaturi": split_links(extract_links(response.text), url),
        "Cai interzise": disallowed_paths(url)
  }

with open("report.json", "w") as file:
    import json
    json.dump(site_report(BASE_URL), file, indent=4)
with open("report.json", "r") as file:
    import json
    data=json.load(file)
    print(json.dumps(data, indent=4))

#if __name__ == "__main__":
    # print("Autotest:", get_status("https://cybercor.org"))