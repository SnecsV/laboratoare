


MAGIC = {b"\x89PNG": "PNG", b"%PDF": "PDF", b"PK\x03\x04": "ZIP"}
 
def tip(head):
    for semnatura, nume in MAGIC.items():
        if head.startswith(semnatura):
            return nume
    return "necunoscut"

import os, hashlib
 
def amprenta_fisier(cale):
    with open(cale, "rb") as f:      # "rb" = binar; with = inchide singur
        date = f.read()
    return {"nume": os.path.basename(cale),
            "tip": tip(date[:8]),
            "sha256": hashlib.sha256(date).hexdigest()[:16]}

def scaneaza(folder):
    rez = []
    for nume in sorted(os.listdir(folder)):
        cale = os.path.join(folder, nume)
        if os.path.isfile(cale):
            rez.append(amprenta_fisier(cale))
    return rez
 

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Scaneaza un folder si afiseaza amprentele fisierelor.")
    parser.add_argument("folder", help="Calea catre folderul de scanat")
    args = parser.parse_args()
    rezultate = scaneaza(args.folder)
    for rezultat in rezultate:
        print(f"{rezultat['nume']:14} {rezultat['tip']:11} {rezultat['sha256']}")

if __name__ == "__main__":
    main()


