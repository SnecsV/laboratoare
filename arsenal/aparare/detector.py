def suspecti(counts, prag=10):
    if prag < 1:
        raise ValueError(f"prag invalid: {prag} (cel putin 1)")
    return [(ip, n) for ip, n in counts.most_common() if n >= prag]
 
from collections import Counter


import argparse, json
from collections import Counter
from arsenal.aparare.parse_auth import afiseaza_rezumat, citeste_esecuri
 
def main():
    p = argparse.ArgumentParser()
    p.add_argument("log")
    p.add_argument("--prag", type=int, default=10)
    p.add_argument("--json", action="store_true")
    a = p.parse_args()
    esecuri = citeste_esecuri(a.log)
    counts = Counter(e["ip"] for e in esecuri)
    sus = suspecti(counts, a.prag)
    if a.json:
        print(json.dumps({
            "esecuri": esecuri,
            "pe_ip": counts,
            "suspecti": sus,
        }, indent=2, ensure_ascii=False))
    else:
        afiseaza_rezumat(esecuri)
        print("suspecti:")
        for ip, n in sus:
            print(f" {ip} ({n} incercari) BRUTE FORCE")

if __name__ == "__main__":
    main()
