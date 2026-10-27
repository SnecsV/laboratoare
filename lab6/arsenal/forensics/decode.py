import re
import binascii
import argparse
import json
from pathlib import Path


def ghici_strat(s):
    # TODO: daca are %xx -> "url"
    if re.search(r"%[0-9a-fA-F]{2}", s):
        return "url"
    # TODO: daca doar 0-9 a-f si lungime para -> "hex"
    if re.fullmatch(r"[0-9a-fA-F]+", s) and len(s) % 2 == 0:
        return "hex"
    # TODO: daca doar A-Za-z0-9+/= -> "base64"
    if re.fullmatch(r"[A-Za-z0-9+/=]+", s):
        return "base64"
    return "necunoscut"

# A3

import base64
from urllib.parse import unquote


def desfa(s):
    if not isinstance(s, str):
        raise TypeError("desfa asteapta un sir de caractere")

    strat = ghici_strat(s)

    if strat == "base64":
        try:
            return strat, base64.b64decode(s, validate=True)
        except (binascii.Error, ValueError) as exc:
            raise ValueError("sir Base64 invalid") from exc

    if strat == "hex":
        try:
            return strat, bytes.fromhex(s)
        except ValueError as exc:
            raise ValueError("sir hex invalid") from exc

    if strat == "url":
        return strat, unquote(s).encode()

    return strat, s.encode()

# A4

# Un rezultat poate fi tot o codare. Decodează în buclă până iese text citibil (sau te oprești după câteva încercări, ca să nu intri în buclă infinită).
def citibil(b):
    # TODO: True daca toti octetii sunt 32..126
    return all(32 <= c < 127 for c in b)

def main():
    print("\n")
    root = Path(__file__).resolve().parents[2]

    # A1

    s = "Salut"
    b = s.encode()          # bytes
    print(b, b[0])          # b"Salut" 83
    print(b.hex())          # 53616c7574
    print(bytes.fromhex(b.hex()))  # b"Salut"
    print("\n")
    # TODO: tipareste b.hex() si refa bytes din hex
    #       cu bytes.fromhex(...)

    # A2

    print(ghici_strat("%2Fetc"))   # url
    print(ghici_strat("48656c6c6f"))  # hex
    print(ghici_strat("U2FsdXQ="))  # base64
    print(ghici_strat("Salut"))     # necunoscut
    print("\n")

    # A4

    # Un rezultat poate fi tot o codare. Decodează în buclă până iese text citibil (sau te oprești după câteva încercări, ca să nu intri în buclă infinită).
    val = "NTM1OTU3NTk="
    for _ in range(8):
        strat, b = desfa(val)
        # TODO: daca citibil(b): opreste si tipareste
        if citibil(b):
            if strat == "hex":
                print("hex:", b.hex())
            elif strat == "base64":
                print("base64:", b.decode())
            else:
                print("alt:", b.decode())
            break
        #       altfel val = b.decode(); continua
        else:
            val = b.decode()
            continue
        
        
    # A5

    date = (root / "probe" / "xor.bin").read_bytes()
    for k in range(256):
        clar = bytes(b ^ k for b in date)
        # TODO: daca citibil(clar):
        #       print("cheie:", k, clar.decode())
        if citibil(clar):
            print("cheie:", k, clar.decode("ascii", errors="replace"))
            break
    print("\n")

    # A6

    import hashlib

    tinta = (root / "probe" / "hashuri.txt").read_text().splitlines()[0]
    print(len(tinta))   # 32 md5 / 40 sha1 / 64 sha256
    for cuv in (root / "probe" / "wordlist.txt").read_text(
        encoding="latin1"
    ).splitlines():
        cuv = cuv.strip()
        # TODO: daca hashlib.md5(cuv.encode()).hexdigest()
        #       == tinta: print("gasit:", cuv); break
        if hashlib.md5(cuv.encode()).hexdigest() == tinta:
            print("gasit:", cuv)
            print("\n")
            break

    # A7
    
    

    parser = argparse.ArgumentParser()
    parser.add_argument("intrare")       # șir sau cale
    parser.add_argument("--fisier", action="store_true")

    args = parser.parse_args()

    if args.fisier:
       date = Path(args.intrare).read_text(encoding="ascii", errors="replace")
    else:
       date = args.intrare

    strat, rezultat = desfa(date)

    try:
        rezultat_json = rezultat.decode("utf-8")
    except UnicodeDecodeError:
        rezultat_json = rezultat.hex()

    continut = {
        "strat": strat,
        "rezultat": rezultat_json,
}

    Path("arsenal/forensics/fisa.json").write_text(
    json.dumps(continut, ensure_ascii=False, indent=2),
    encoding="utf-8",
)

    print("Fisa salvată în arsenal/forensics/fisa.json")

if __name__ == "__main__":
    main()

