# Raport – Laboratorul 6: Informații invizibile (forensics și steganografie)

Toate analizele s-au făcut doar pe fișierele generate pentru laborator (`probe/`).

## Lucrarea A – Decoderul universal (`arsenal/forensics/decode.py`)

### Mesajul cu straturi (`probe/mesaj.txt`)
Mesajul avea trei straturi de codare: **base64 → base64 → hex**. Decodat strat cu strat (`probe/decoder.py`), textul clar este:

`FLAG{straturi_de_encoding}`

(MD5 al textului clar: `3c5b3be202456818308853d1f706cdda`.)

Exemplul din A4 (`NTM1OTU3NTk=`) se desface în două straturi, iar rezultatul final este `53595759`.

### XOR cu cheie de un octet (`probe/xor.bin`)
Prin forță brută pe cele 256 de chei, prima cheie care dă text citibil este **128** (0x80). Textul clar:

`Un singur octet tine tot secretul... gaseste-l! FLAG{xor_un_octet}`

### Hash-uri sparte prin dicționar (`probe/hashuri.txt`)
Toate cele 5 hash-uri au 32 de caractere, deci sunt **MD5**. Parolele găsite în `wordlist.txt`:

| Hash (MD5) | Parola |
|---|---|
| 5f4dcc3b5aa765d61d8327deb882cf99 | password |
| 8621ffdbc5698829397d97767ac13db3 | dragon |
| d8578edf8458ce06fbc5bb76a58c5ca4 | qwerty |
| 0d107d09f5bbe40cade3de5c71e9e9b7 | letmein |
| d0763edaa9d9bd2a9516280e9044d885 | monkey |

### Fișa JSON
`python arsenal/forensics/decode.py "U2FsdXQ="` salvează în `arsenal/forensics/fisa.json`:
`{"strat": "base64", "rezultat": "Salut"}`.

### Test
`teste/test_decode.py` – 4 teste, toate trec.

## Lucrarea B – Forensics pe fișiere și steganografie (`arsenal/forensics/forensics.py`)

### B1. Tipul real al fișierelor (magic bytes)
| Fișier | Primii octeți | Tip real |
|---|---|---|
| `foto.jpg` | `ff d8 ff e0` | jpeg |
| `ascuns.png` | `89 50 4e 47` | png |
| `stego.png` | `89 50 4e 47` | png |

### B2. Strings
În `ascuns.png` apar `secret.txt` și textul `FLAG{ascuns_prin_carving}`, plus semnătura `PK` – indiciu că în coada fișierului este o arhivă ZIP.

### B3. Metadate EXIF și GPS (`foto.jpg`)
- Producător / model: **Apple / iPhone 13**
- Data: **2026:09:14 10:30:00**
- GPS: **47° 1′ 0″ N, 28° 51′ 27″ E** → **47.016667, 28.8575** (zona Chișinău, Republica Moldova)

### B4. File carving
Semnătura `PK\x03\x04` se află la octetul **782** din `ascuns.png`. Arhiva extrasă (`gasit.zip`) conține `secret.txt`:

`FLAG{ascuns_prin_carving}`

### B5–B6. Steganografie LSB
Mesajul `FLAG{ascuns_in_pixeli}` (terminat cu un octet 0) a fost ascuns în ultimii biți ai canalelor R, G, B din `foto.jpg` și salvat ca `stego.png` (PNG, fără pierderi). Dezvăluirea citește LSB-urile, le grupează câte 8 și se oprește la primul octet 0. Mesajul recuperat:

`FLAG{ascuns_in_pixeli}`

## Opțional – `probe/challenge.bin`
Conform `challenge_hint.txt`: un strat de base64 peste un XOR cu cheie de un octet, cu verificare MD5 `8c4eb02d9dcef7d0ff91d8e4c7fea91b`. Pași: decodare base64, apoi XOR cu toate cele 256 de chei și comparare MD5 a rezultatului. Cheia este **128**, iar textul clar este:

`FLAG{lant_complet_despicat}`

(MD5 coincide cu cel din indiciu.)
