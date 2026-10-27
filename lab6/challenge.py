import hashlib
from pathlib import Path

from arsenal.forensics.decode import citibil, desfa, ghici_strat


HASH_ASTEPTAT = "8c4eb02d9dcef7d0ff91d8e4c7fea91b"


def rezolva(cale: Path) -> tuple[str, int, bytes]:
    continut = cale.read_text(encoding="ascii").strip()
    strat = ghici_strat(continut)
    if strat not in ("hex", "base64", "url"):
        raise ValueError(f"Strat de encoding necunoscut: {strat}")

    _, criptat = desfa(continut)
    for cheie in range(256):
        mesaj = bytes(octet ^ cheie for octet in criptat)
        if citibil(mesaj) and hashlib.md5(mesaj).hexdigest() == HASH_ASTEPTAT:
            return strat, cheie, mesaj

    raise ValueError("Nu a fost gasita cheia XOR")


if __name__ == "__main__":
    cale = Path(__file__).resolve().parent / "probe" / "challenge.bin"
    strat, cheie, mesaj = rezolva(cale)
    print("Strat detectat:", strat)
    print("Cheia XOR:", cheie)
    print("Mesajul:", mesaj.decode("ascii"))
    print("MD5:", hashlib.md5(mesaj).hexdigest())
