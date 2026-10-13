# Laborator: funcții, metode și importuri pe web
# Student: Gonța Marius
 
BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10  # secunde



# Exercitiul 1
import requests 
print(requests.__version__)
import urllib.request #urllib este biblioteca interna Python, requests este biblioteca externa care trebuie instalata

# Exercitiul 2
response=requests.get(BASE_URL, timeout=TIMEOUT)  #importeaza toata biblioteca requests, mai clara originea functiei
print(response.status_code)
                
from requests import get
response=get(BASE_URL, timeout=TIMEOUT)           #importeaza doar functia get, sintaxa mai scurta
print(response.status_code)

# Exercitiul 3
import requests as rq
response=rq.get(BASE_URL, timeout=TIMEOUT)        #aliasul usureaza citirea in cazul in care este folosita prescurtarea intuitiva 
print(response.status_code)                       #a cuvantului, de exemplu rq este evident prescurtarea requests, in caz contrar
                                                 #aliasul va fi inteles doar de cel care il predefineste

# Exercitiul 4 
import urllib.request
try:
    response=urllib.request.urlopen(BASE_URL, timeout=TIMEOUT)
    print(response.status)
    caractere=response.read().decode("utf-8")
    print(caractere[:200])
except Exception as e:
    print(f"Eroare la accesarea URL-ului: {e}")

# Exercitiul 5
print(dir(requests)) #ConnectTimeout este o clasa, status_codes este un modul si  get este o functie

# Exercitiul 6
help(requests.get)
response=requests.get(BASE_URL,timeout=TIMEOUT)
print(response.status_code)

# Exercitiul 7
import time 
timp1=time.perf_counter() 
print(timp1)
response=requests.get(BASE_URL, timeout=TIMEOUT)
timp2=time.perf_counter()
print(timp2)
durata=timp2-timp1
print(durata)
print(response.elapsed)

# Exercitiul 8
try:
    import bs4
    print("bs4 version:", bs4.__version__)
except ImportError:
    print("Instalați modulul cu: pip install beautifulsoup4")












