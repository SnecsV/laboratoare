import argparse, json, os


 
def citeste_linii(cale):
    with open(cale, encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip() and not line.strip().startswith("#")]
 
cai = citeste_linii("./start/suid.txt")
print("linii SUID:", len(cai))

def nume(cale):
    return cale.rsplit("/", 1)[-1]
 
nume_unice = {nume(c) for c in cai}    # set comprehension
print("SUID distincte:", len(nume_unice))

GTFO = {"find", "vim.basic", "vim", "nmap", "cp", "bash",
        "less", "awk", "python3", "perl"}
 
def suid_constatari(cale):
    cai = citeste_linii(cale)
    return [{"cale": c, "nume": nume(c), "risc": "mare" if nume(c) in GTFO else "normal"} for c in sorted(cai, key=nume)]
 
suid = suid_constatari("./start/suid.txt")
mari = [c for c in suid if c["risc"] == "mare"]
print(len(suid), "SUID,", len(mari), "cu risc mare")
print(sorted(c["nume"] for c in mari))

def sudo_constatari(cale):
    out = []
    for ln in citeste_linii(cale):
        user, drept = ln.split(" : ", 1)   # despachetare in tuplu
        out.append({"user": user.strip(), "drept": drept.strip(),
                    "risc": "mare" if "NOPASSWD" in drept else "normal"})
    return out
 
def cron_constatari(cale):
    campuri = [ln.split() for ln in citeste_linii(cale)]
    constatari = []
    for c in campuri:
        comanda = " ".join(c[6:])
        executabile = {nume(token) for token in comanda.split()}
        risc = "mare" if executabile & GTFO else "normal"
        constatari.append({
            "user": c[5],
            "comanda": comanda,
            "risc": risc,
        })
    return constatari

def enumereaza(d):
    return {
        "suid": suid_constatari(os.path.join(d, "suid.txt")),
        "sudo": sudo_constatari(os.path.join(d, "sudo.txt")),
        "cron": cron_constatari(os.path.join(d, "crontab.txt")),
    }

def main():
    p = argparse.ArgumentParser()
    p.add_argument("capturi")
    p.add_argument("--json", action="store_true")
    a = p.parse_args()
    raport = enumereaza(a.capturi)
    if a.json:
        print(json.dumps(raport, indent=2, ensure_ascii=False)); return
    for categorie, lista in raport.items():
        mari = [c for c in lista if c.get("risc") == "mare"]
        print(f"{categorie}: {len(lista)} gasite, {len(mari)} cu risc mare")
    # TODO: utilizatorii implicati = multimea userilor din sudo REUNITA cu cei din cron
    utilizatori_implicati = {c["user"] for c in raport["sudo"]} | {c["user"] for c in raport["cron"]}
    print(f"Utilizatori implicati: {sorted(utilizatori_implicati)}")
    with open("enum.json", "w", encoding="utf-8") as f:
        json.dump(raport, f, indent=2, ensure_ascii=False)
    print("Raport salvat in enum.json")
 
if __name__ == "__main__":
    main()
