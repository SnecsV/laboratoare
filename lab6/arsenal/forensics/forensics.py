from pathlib import Path


root = Path(__file__).resolve().parents[2]
probe = root / "probe"

# B1

def tip_real(cale):
    cap = open(cale, "rb").read(8)
    if cap.startswith(b"%PDF"):
        return "pdf"
    elif cap.startswith(b"\x89PNG"):
        return "png"
    elif cap.startswith(b"\xff\xd8"):
        return "jpeg"
    elif cap.startswith(b"PK\x03\x04"):
        return "zip/docx"
    return cap.hex()
print(tip_real(probe / "foto.jpg"))
print ("\n")

# B2

import re
date = (probe / "ascuns.png").read_bytes()
for m in re.findall(rb"[ -~]{4,}", date):
    print(m.decode())
    print("\n")

# B3

from PIL import Image
from PIL.ExifTags import TAGS
exif = Image.open(probe / "foto.jpg")._getexif() or {}
for id, val in exif.items():
    print(TAGS.get(id, id), "=", val)
if 34853 in exif:
    gps_info = exif[34853]
    lat_gms = gps_info.get(2)  # Latitude
    lon_gms = gps_info.get(4)  # Longitude
    lon=float(lon_gms[0]+(lon_gms[1])/60+(lon_gms[2])/3600)
    lat=float(lat_gms[0]+(lat_gms[1])/60+(lat_gms[2])/3600)
    if lat and lon:
        print("Latitude:", lat)
        print("Longitude:", lon)
print("\n")
# B4

import zipfile
date = (probe / "ascuns.png").read_bytes()
i = date.find(b"PK\x03\x04")
if i != -1:
    arhiva_gasita = probe / "gasit.zip"
    arhiva_gasita.write_bytes(date[i:])
    print("arhiva extrasa de la octetul", i)
    with zipfile.ZipFile(arhiva_gasita, "r") as arhiva:
        arhiva.extractall(probe / "extras")
        print("fisiere extrase:", arhiva.namelist())
print("\n")

# B5

from PIL import Image
img = Image.open(probe / "foto.jpg").convert("RGB")
px = list(img.get_flattened_data())
mesaj = b"FLAG{ascuns_in_pixeli}"
biti = "".join(f"{x:08b}" for x in mesaj) + "00000000"
if len(biti) > len(px) * 3:
    raise ValueError("Mesajul nu incape in pixelii imaginii")

px_nou = []
pozitie_bit = 0
for pixel in px:
    canale = list(pixel)
    for index in range(len(canale)):
        if pozitie_bit < len(biti):
            canale[index] = (canale[index] & ~1) | int(biti[pozitie_bit])
            pozitie_bit += 1
    px_nou.append(tuple(canale))

img.putdata(px_nou)
img.save(probe / "stego.png")

# B6

px = list(Image.open(probe / "stego.png").convert("RGB").get_flattened_data())
biti = "".join(f"{r & 1}{g & 1}{b & 1}" for (r, g, b) in px)

mesaj_bytes = bytearray()
for pozitie in range(0, len(biti) - 7, 8):
    octet = int(biti[pozitie:pozitie + 8], 2)
    if octet == 0:
        break
    mesaj_bytes.append(octet)

print(mesaj_bytes.decode("ascii"))
