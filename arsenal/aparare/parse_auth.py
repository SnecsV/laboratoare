import re
import argparse
TIPAR = re.compile(r"Failed password for (?:invalid user )?(\S+) from (\S+) port")
 
def esec(linie):
    m = TIPAR.search(linie)
    if m is None:
        return None
    else:
        return (m.group(1), m.group(2))
    
 


def citeste_esecuri(cale):
    esecuri = []
    try:
        f = open(cale, encoding="utf-8")
    except FileNotFoundError:
        print("nu gasesc", cale)
        return esecuri
    with f:
        for linie in f:
            r = esec(linie)
            if r is not None:
                esecuri.append({"user": r[0], "ip": r[1]})
    return esecuri
 


from collections import Counter
 
def pe_ip(esecuri):

    return Counter(e["ip"] for e in esecuri)
 

def afiseaza_rezumat(esecuri):
    print("esecuri:", len(esecuri))
    counts = pe_ip(esecuri)
    for ip, n in counts.most_common():
        print(f"  {ip}: {n}")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("cale", help="cale catre fisierul auth.log")
    args = p.parse_args()
    esecuri = citeste_esecuri(args.cale)
    afiseaza_rezumat(esecuri)


if __name__ == "__main__":
    main()