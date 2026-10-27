import base64
import hashlib

with open("mesaj.txt", "rb") as f:
    strat_b64_2 = f.read()

strat_b64_1 = base64.b64decode(strat_b64_2)
strat_hex = base64.b64decode(strat_b64_1)
clar = bytes.fromhex(strat_hex.decode())

print("Mesajul ascuns:", clar.decode())

# Verificare cu MD5
print("MD5:", hashlib.md5(clar).hexdigest())