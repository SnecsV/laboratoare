# Laborator: funcții, metode și importuri pe web
# Student: Gonța Marius
 
BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10  # secunde

from fileinput import filename
import json
import time
import hashlib
import requests as rq 
import re
response = rq.get(BASE_URL, timeout=TIMEOUT)

# Exercitiul 35
import urllib.parse
def descompunere(url):
    """Descompune un URL în componentele sale."""
    rezultat = urllib.parse.urlparse(url)
    return {
        "scheme": rezultat.scheme,
        "netloc": rezultat.netloc,
        "path": rezultat.path,
        "query": rezultat.query,
        "fragment": rezultat.fragment
    }
# print(descompunere("https://cybercor.org/path?x=1#top"))

# Exercitiul 36

def compunerea(url, part):
    """Recompune un URL din componentele sale."""
    rezultat = urllib.parse.urljoin(url,part)
    return rezultat
# print(compunerea(BASE_URL, "/about"))
# print(compunerea(BASE_URL, "contact.html"))
# print(compunerea(BASE_URL, "../index.html"))

# Exercitiul 37

def extract_links(html):
    """Extrage toate link-urile dintr-o pagină web."""
    links=re.findall(r'href="([^"]+)"', html) 
    return list(set(links))
html=rq.get(BASE_URL).text
# print(extract_links(html))

# Exercitiul 38

def split_links(links, domain):
    """Împarte link-urile în absolute și relative."""
    interne = []
    externe = []
    for link in links:
        url=urllib.parse.urljoin(domain, link)
        if urllib.parse.urlparse(url).netloc == urllib.parse.urlparse(domain).netloc:
            interne.append(url)
        else:
            externe.append(url)
    return interne, externe
# print(split_links(extract_links(html), BASE_URL))

# Exercitiul 39 
from html.parser import HTMLParser
test_html = """
<html><body>
  <img src="/logo.png" alt="Logo">
  <IMG SRC="poza.jpg">
  <img alt="imagine fără src">
  <img src="https://cdn.example.com/banner.webp" />
  <a href="/despre">Aceasta nu este o imagine</a>
</body></html>
"""
class ImageFinder(HTMLParser):
    def __init__(self):
        super().__init__()
        self.images = []
 
    def handle_starttag(self, tag, attrs):
        if tag == "img":
            src = dict(attrs).get("src")
            if src:
                self.images.append(src)
finder = ImageFinder()  
finder.feed(test_html)
print(finder.images)
assert finder.images == [
    "/logo.png",                            # imagine obișnuită
    "poza.jpg",                             # tag scris cu majuscule
    "https://cdn.example.com/banner.webp",  # tag care se închide singur
], "Parserul nu a găsit exact imaginile așteptate"
print("Testul a trecut!")
finder = ImageFinder()
finder.feed(response.text)
print(len(finder.images), "imagini găsite")
for src in finder.images:
    print(src)

# Exercitiul 40

def page_fingerprint(url):
    """Returnează un fingerprint al paginii web pentru URL-ul dat."""
    return hashlib.sha256(response.content).hexdigest()
# print(page_fingerprint(BASE_URL))
# print(page_fingerprint(BASE_URL))  
# O sa fie diferite in cazul in care se va schimba continutul paginii între cele două apeluri

# Exercitiul 41

def salvare_headers(response, filename):
    """Salvează headerele HTTP într-un fișier JSON."""
    with open(filename, "w") as file:
          json.dump(dict(response.headers), file, indent=2)
    with open(filename, "r") as file:
          headers = json.load(file)
    return headers
# print(salvare_headers(response, "headers.json"))

# Exercitiul 42

def resolve(hostname):
    """Rezolvă un hostname în adresa sa IP."""
    import socket
    return socket.gethostbyname(hostname)
# print(resolve("cybercor.org"))  
# Ar trebui să returneze adresa IP a domeniului

# Exercitiul 43

def cert_days_left(hostname):
    """Returnează numărul de zile rămase până la expirarea certificatului SSL al unui hostname."""
    import ssl
    import socket
    import datetime

    context = ssl.create_default_context()
    with socket.create_connection((hostname, 443)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            cert = ssock.getpeercert()
    
    zile_ramase=cert['notAfter']
    return (ssl.cert_time_to_seconds(zile_ramase) - time.time()) / (24 * 60 * 60)  
# Convertim secunde în zile
# print(cert_days_left("cybercor.org"))  
# # Ar trebui să returneze numărul de zile rămase până la expirarea certificatului SSL











