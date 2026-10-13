import requests 

SITES = [
    # Pagini obișnuite (Părțile 2, 3 și 4)
    "https://example.com",
    "https://httpbin.org/html",
    "https://httpbin.org/json",
    "https://httpbin.org/status/200",
    "https://httpbin.org/redirect/1",
    "https://httpbin.org/delay/2",
    # Pagini care eșuează
    "https://httpbin.org/status/404",
    "https://httpbin.org/status/500",
    "https://httpbin.org/delay/10",
    "http://this-site-does-not-exist.invalid",
    # Anteturi de securitate (Partea 5)
    "https://httpbin.org/response-headers?X-Frame-Options=DENY&X-Content-Type-Options=nosniff",
    "https://httpbin.org/response-headers?x-frame-options=DENY",
    # Răspunde aleatoriu cu 200 sau 500 (Partea 6)
    "https://httpbin.org/status/200,500",
]

SECURITY_HEADERS = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
]


def build_url(host, path):
    """Returnează o adresă completă, de exemplu https://example.com/login."""
    if path.startswith("/"):
        return host + path
    else:
        return host + "/" + path


def is_https(url):
    """Returnează True dacă adresa începe cu https://, altfel False."""
    if url.startswith("https://"):
        return True
    else:
        return False


def show_response(url):
    """Trimite un GET la url și afișează statusul și Content-Type."""
    import requests
    response=requests.get(url)
    print("Status:", response.status_code)
    print("Content-Type:", response.headers.get("Content-Type"))


def check_site(url):
    """Returnează un dicționar cu: status, content_type, length, server."""
    try:
        response = requests.get(url, timeout=5)
        return {
            "status": response.status_code,
            "content_type": response.headers.get("Content-Type"),
            "length": len(response.content),
            "server": response.headers.get("Server"),
        }
    except requests.RequestException:
        return {"status": None, "error": "Eroare la cerere"}
    except Exception:
        return {"status": response.status_code, "content_type": response.headers.get("Content-Type"), "length": len(response.content), "server": "Lipseste"}



def scan_sites():
    """Verifică toate site-urile din SITES, afișează-le pe cele care merg și un rezumat."""
    lista_siteuri = []
    succes=0
    esuate=0
    for site in SITES:
        result = check_site(site)
        if result["status"] == 200:
            succes+=1
        else:
            esuate+=1
        lista_siteuri.append((site,result["status"],len(result["content_type"])))
    lista_siteuri.sort(key=len, reverse=True)
    print("Lista site-urilor sortate după lungimea Content-Type:")
    for site in lista_siteuri:
        print(site, len(site))
    print("\nRezumat:")
    for status in lista_siteuri:
        if status[1] == 200:
            site = status[0]
            print(site)
            succes+=1
        else:
            esuate+=1
    print("Merg:",succes,"| Nu merg:",esuate)

def check_headers(url):
    """Returnează un dicționar cu: present, missing, score."""
    headers = {
        "Strict-Transport-Security", 
        "Content-Security-Policy", 
        "X-Content-Type-Options",
        "X-Frame-Options",
    }
    missing = set()
    present = set()
    response= requests.get(url, timeout=5)
    present = set()
    try:
        for header in headers:
            if header in response.headers:
                present.add(header)
            else:
                missing.add(header)
        score=len(present)/len(headers)*100
        return  {print("Present:", list(present),"\nMissing:", list(missing), "\nScore:",  int(score))}
    except requests.RequestException:
        return  {"status": None, "error": "Cerere eșuată"}
check_headers("https://httpbin.org/response-headers?X-Frame-Options=DENY&X-Content-Type-Options=nosniff")
    
        

def retry_check(url, attempts=3):
    """Încearcă de cel mult `attempts` ori; returnează un dicționar cu: status, attempts."""
    for i in range(attempts):
        try:
            response = requests.get(url, timeout=5)
            if response.status_code < 500:
                return {"status": response.status_code, "attempts": i + 1}
            elif response.status_code > 500:
                continue
        except requests.RequestException:
            continue
    return {"status": response.status_code, "attempts": i + 1}
    
