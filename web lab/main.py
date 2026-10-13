# Laborator: funcții, metode și importuri pe web
# Student: Gonța Marius
 
BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10  # secunde

#import requests as rq

# Exercitiul 44

import json

import webtools
print(webtools.get_title(BASE_URL))

# Exercitiul 45
from webtools import get_title
from webtools import security_headers
# Daca main.py ar avea o functie get_title, aceasta ar fi apelata in locul functiei din webtools.py.

# Exercitiul 46

# Autotestul lucreaza doar in primul caz deoarece webtools.py este folosit direct
# pe cand in al doilea caz webtools este importat.

# Exercitiul 47

from webtools import DEFAULT_HEADERS
print(DEFAULT_HEADERS)

# Exercitiul 48
import argparse
from webtools import get_status
parser=argparse.ArgumentParser()
parser.add_argument("url")
args=parser.parse_args()
print(get_status(args.url))

# Exercitiul 49
import csv
from datetime import datetime
from part3_functions import check_paths as cp
rezultat=cp()
with open("report.csv" , "w") as file:
    WRITER=csv.writer(file)
    WRITER.writerow(["Path", "Status" , "Checked_At"])
    for path, status in rezultat.items():
        WRITER.writerow([path, status, datetime.now().isoformat()])
print("Raportul a fost salvat în report.csv")

# Exercitiul 50
def site_report(url):
    """Generează un raport al site-ului și îl salvează într-un fișier CSV."""
    from part3_functions import check_paths as cp
    from datetime import datetime
    import csv
    # Cod de stare si URL final
    r=webtools.fetch(url)
    status_code=r.status_code
    # Titlu
    title=webtools.get_title(url)
    # Adresa IP
    ip_address=webtools.resolve(url)
    # Redirecționări
    redirects=[]
    for redirect in r.history:  
        redirects.append((redirect.status_code, redirect.url))
    # Scorul de securitate
    headers=webtools.security_headers(url)
    security_score=sum(headers.values())
    # Zile rămase până la expirarea certificatului SSL
    days_left=webtools.cert_days_left(url)
    # Legaturi externe si interne
    external_links, internal_links=webtools.extract_links(url)
    # Caile interzise din robots.txt
    robots_txt=webtools.fetch_robots_txt(url)
    disallowed_paths=webtools.disallowed_paths(robots_txt)
    # Afisarea raportului
    print(f"Raport pentru {url}:")
    print(f"Cod de stare: {status_code}")   
    print(f"Titlu: {title}")
    print(f"Adresa IP: {ip_address}")
    print(f"Redirecționări: {redirects}")
    if redirects:
        for redirect in redirects:
            print(f" {redirect[0]} -> {redirect[1]}")
    print(f"Scor de securitate: {security_score} din {len(headers)} headere de securitate găsite.")
    print(f"Zile rămase până la expirarea certificatului SSL: {days_left:.2f}")
    print(f"Legături externe: {external_links}")
    print(f"Legături interne: {internal_links}")
    print(f"Căi interzise din robots.txt: {disallowed_paths}")
    raport_json = {
            "url": url,
            "status_code": status_code,
            "title": title,
            "ip_address": ip_address,
            "redirects": redirects,
            "security_score": security_score,
            "days_left_ssl": days_left,
            "external_links": external_links,
            "internal_links": internal_links,
            "disallowed_paths": disallowed_paths
        }
    with open("report.json", "w") as file:
        json.dump(raport_json, file)
    print("Raportul a fost salvat în report.json")

    
    