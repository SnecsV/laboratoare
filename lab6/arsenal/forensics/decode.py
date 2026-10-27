import re
import binascii
import argparse
import json
from pathlib import Path


def ghici_strat(s):
    if re.search(r"%[0-9a-fA-F]{2}", s):
        return "url"
    if re.fullmatch(r"[0-9a-fA-F]+", s) and len(s) % 2 == 0:
        return "hex"
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

    # A2

    print(ghici_strat("%2Fetc"))   # url
    print(ghici_strat("48656c6c6f"))  # hex
    print(ghici_strat("U2FsdXQ="))  # base64
    print(ghici_strat("Salut"))     # necunoscut
    print("\n")

    # A4

    # Un rezultat poate fi tot o codare. Decodează în buclă până iese text citibil (sau te oprești după câteva încercări, ca să nu intri în buclă infinită).
    val = (root / "probe" / "mesaj.txt").read_text(
        encoding="ascii"
    ).strip()
    for _ in range(8):
        strat, b = desfa(val)
        if not citibil(b):
            raise ValueError("mesajul nu mai este text citibil")

        text = b.decode("ascii")
        urmatorul_strat = ghici_strat(text)
        if urmatorul_strat == "necunoscut":
            print("mesaj ascuns:", text)
            break
        val = text
    print("\n")
        
    # A5

    date = (root / "probe" / "xor.bin").read_bytes()
    for k in range(256):
        clar = bytes(b ^ k for b in date)
        if citibil(clar):
            print("cheie:", k, "\n", clar.decode("ascii", errors="replace"))
            break
    print("\n")

    # A6

    import hashlib
    tinte = [
        tinta.strip()
        for tinta in (root / "probe" / "hashuri.txt").read_text(
            encoding="ascii"
        ).splitlines()
        if tinta.strip()
    ]
    gasite = [None] * len(tinte)
    ramase = set(range(len(tinte)))
    for cuv in (root / "probe" / "wordlist.txt").read_text(
        encoding="latin1"
    ).splitlines():
        cuv = cuv.strip()
        for index in tuple(ramase):
            tinta = tinte[index]
            if len(tinta) == 32:
                h = hashlib.md5(cuv.encode()).hexdigest()
            elif len(tinta) == 40:
                h = hashlib.sha1(cuv.encode()).hexdigest()
            elif len(tinta) == 64:
                h = hashlib.sha256(cuv.encode()).hexdigest()
            else:
                raise ValueError("hash necunoscut")
            if h == tinte[index]:
                gasite[index] = cuv
                ramase.remove(index)
        if not ramase:
            break

    for tinta, cuv in zip(tinte, gasite):
        print(len(tinta))   # 32 md5 / 40 sha1 / 64 sha256
        if cuv is not None:
            print("cuvantul este:", cuv)
         
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
