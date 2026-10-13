# Laborator: funcții, metode și importuri pe web
# Student: Gonța Marius
 
BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10  # secunde

import time

import requests as rq



# Exercitiul 21

def fetch(url, timeout=TIMEOUT):
    return rq.get(url, timeout=timeout)


response = fetch(BASE_URL)
print(response.status_code)

# Exercitiul 22

def get_status(url, timeout=TIMEOUT):
    response = rq.get(url, timeout=timeout)
    return response.status_code

print(get_status(BASE_URL))
time.sleep(1)  # Pauză de 1 secundă
print(get_status(BASE_URL + "/robots.txt"))
time.sleep(1)  # Pauză de 1 secundă
print(get_status(BASE_URL + "/sitemap.xml"))

# Exercitiul 23

def fetch(url, timeout=TIMEOUT):
    return rq.get(url, timeout=timeout)
response=fetch(BASE_URL)
print(response.status_code)
response=fetch(BASE_URL, timeout=3)
print(response.status_code)



# Exercitiul 24

def get_title(url, timeout=TIMEOUT):
    response = rq.get(url, timeout=timeout)
    start = response.text.find("<title>") + len("<title>")
    end = response.text.find("</title>")
    return response.text[start:end].strip()

titlu = get_title(BASE_URL)
print(titlu)


# Exercitiul 25

def get_title(html):
    """Returnează titlul paginii din șirul HTML."""
    start = html.find("<title>") + len("<title>")
    end = html.find("</title>")
    return html[start:end]

print(get_title.__doc__)  # afișează docstring-ul funcției


# Exercitiul 26

def get_status(url: str) -> int:
    """Returnează codul de stare HTTP al răspunsului pentru URL-ul dat."""
    response = rq.get(url, timeout=TIMEOUT)
    return response.status_code
print(get_status("https://cybercor.org"))  # Funcționează corect
# print(get_status(123))  
# Mă oprește o eroare de tip TypeError, deoarece funcția așteaptă un argument de tip str, dar a primit un int.

# Exercitiul 27

def page_exists(url):
    try:
        response = rq.get(url, timeout=TIMEOUT)
        return response.status_code == 200
    except rq.RequestException:
        return False
print(page_exists(ECHO_URL))
print(page_exists("https://this-domain-does-not-exist.invalid"))  

# Exercitiul 28

def check_paths(base, paths):
    """Verifică dacă paginile pentru căile date există pe serverul specificat."""
    result = {}
    for path in paths:
            response = rq.get(base + path , timeout=TIMEOUT)
            result[path] = response.status_code
       
    return result

print(check_paths(BASE_URL, ["/", "/robots.txt", "/sitemap.xml"]))

# Exercitiul 29

def get_header(url, name, default="Lipseste"):
    """Returnează valoarea unui header HTTP specificat pentru URL-ul dat."""
    response = rq.get(url, timeout=TIMEOUT)
    return response.headers.get(name, default)
print(get_header(BASE_URL, name="Server"))

# Exercitiul 30

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
  
print(security_headers(BASE_URL))


# Exercitiul 31
def score_headers(headers):
    """Calculează scorul de securitate pe baza header-elor de securitate."""
    total = len(headers)
    gasite=sum(headers.values())
    return print("Scorul:", gasite, "/", total, "headere de securitate găsite.")

score_headers(security_headers(BASE_URL))

# Exercitiul 32

def fetch_robots_txt(url):
    """Returnează conținutul fișierului robots.txt pentru URL-ul dat."""
    response = rq.get(url + "/robots.txt", timeout=TIMEOUT)
    if response.status_code == 200:
        return response.text
    else:
        return None
    
def disallowed_paths(robots_txt):
    """Returnează o listă cu căile interzise din fișierul robots.txt."""
    paths = []
    for line in robots_txt.splitlines():
        if line.startswith("Disallow:"):
            path = line.split(":", 1)[1].strip()
            paths.append(path)
    return paths
print(fetch_robots_txt(BASE_URL))
print(disallowed_paths(fetch_robots_txt(BASE_URL))) 

# Exercitiul 33

def response_times(*urls):
    """Returnează un dicționar cu timpii de răspuns pentru fiecare URL dat."""
    times = {}
    for url in urls:
        start=time.time()
        rq.get(url, timeout=TIMEOUT)
        end=time.time()

        times[url] = end - start
    return times
print(response_times(BASE_URL, ECHO_URL, "https://www.google.com"))

# Exercitiul 34

def log(message, **detalii):
    """Afișează un mesaj de log cu detalii suplimentare."""
    print(message, end="")
    for mes,det in detalii.items():
        print(f" | {mes}= {det}" , end="")
log("Verificat", url=BASE_URL, status=get_status(BASE_URL))   


