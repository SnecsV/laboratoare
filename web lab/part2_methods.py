# Laborator: funcții, metode și importuri pe web
# Student: Gonța Marius
 
BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10  # secunde

import requests as rq


# Exercitiul 9

response=rq.get(BASE_URL,timeout=TIMEOUT) 
print(response.status_code)  #atribut
print(response.ok)           #atribut
print(response.url)          #atribut
print(response.encoding)     #atribut

#toate sunt atribute deoarece metodele sunt urmate de ()

# Exercitiul 10
response=rq.get(BASE_URL, timeout=TIMEOUT)
response.raise_for_status
try:
    response=rq.get(BASE_URL + "/this-page-does-not-exist", timeout=TIMEOUT)
    response.raise_for_status
except response.HTTPError:
   print("Pagina nu a fost gasita")

# Exercitiul 11

response=rq.get(BASE_URL,timeout=TIMEOUT)
for nume, valoare in response.headers.items():
     print(nume, ":", valoare)

# Exercitiul 12

response=rq.get(BASE_URL,timeout=TIMEOUT)
print(response.headers.get("Server" , "Lipseste"))
print(response.headers.get("Content-Type" , "Lipseste")) 
#observ ca indiferent daca folosesc majuscule sau minuscule valorile vor fi
#aceleasi, deci HTTP u nu e case sensitive 
print(response.headers.get("content-type"))       

# Exercitiul 13
response=rq.get(BASE_URL,timeout=TIMEOUT)
numar=response.text.lower().count("cyber")  
#lower() se foloseste pentru a transforma majuscule in minuscule, returnand un string
#iar string ca tip de date are optiunea de count()
print(numar)  

# Exercitiul 14

response=rq.get(BASE_URL,timeout=TIMEOUT)
start=response.text.find("<title>") + len("<title>")
end=response.text.find("</title>")
titlu=response.text[start:end].strip()
print(titlu)

# Exercitiul 15

response=rq.get(BASE_URL,timeout=TIMEOUT)
linii=response.text.splitlines()
print("Numar de linii:", len(linii))
max=max(linii, key=len)

# Exercitiul 16

response=rq.get(BASE_URL,timeout=TIMEOUT)
if response.url.startswith("https://"):
    print ("Conexiune securizata")
else:
    print ("Conexiune nesecurizata")

# Exercitiul 17

response=rq.get("http://cybercor.org ",timeout=TIMEOUT)
for redirect in response.history:
    print(redirect.status_code, redirect.url)

print("URL final:", response.url)

# Exercitiul 18

response=rq.head(BASE_URL,timeout=TIMEOUT)
print(len(response.content)) 
#0 deoarece HEAD nu returneaza continutul paginii, doar header-ul
response=rq.get(BASE_URL,timeout=TIMEOUT)
print(len(response.content)) #returneaza lungimea continutului paginii

# Exercitiul 19

response=rq.get(BASE_URL,timeout=TIMEOUT)
if response.cookies:
    for cookie in response.cookies:
        print( "Nume:", cookie.nume)
        print( "Secure:", cookie.secure)
else:
    print("Nu exista cookies")

# Exercitiul 20

session = rq.Session()
session.headers.update({"User-Agent": "WebLab-Snecs"})
response = session.get(ECHO_URL + "/headers", timeout=TIMEOUT)    
print(response.json())  #json() este o metoda care returneaza un dictionar




    
