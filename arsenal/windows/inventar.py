import argparse
from dataclasses import dataclass, asdict
import json
from operator import inv
 
@dataclass
class Proces:
    pid: int
    nume: str
    user: str
    cale: str
 


CAI_SUSPECTE = ("\\Temp\\", "\\Roaming\\")
 
@dataclass
class Proces:
    pid: int; nume: str; user: str; cale: str
    def e_suspect(self):
        for cale_suspect in CAI_SUSPECTE:
            if cale_suspect in self.cale:
                return True
        return False

SUSPECTE_ID = {4625, 1102, 7045}
 
@dataclass
class Eveniment:
    id: int; nivel: str; sursa: str; cont: str; mesaj: str
    def e_suspect(self):
        if self.id in SUSPECTE_ID or self.nivel == "critical":
            return True
        return False

def procese_din_json(cale):
    with open(cale, encoding="utf-8") as f:
     return [Proces(**d) for d in json.load(f)]

@dataclass
class Inventar:
    procese: list
    @classmethod
    def din_json(cls, cale):
        with open(cale, encoding="utf-8") as f:
            return cls([Proces(**d) for d in json.load(f)])
    def __len__(self):
        return len(self.procese)

    def suspecte(self):
        return [p for p in self.procese if p.e_suspect()]

    def pe_user(self):
        d = {}
        for p in self.procese:
            d.setdefault(p.user, []).append(p.nume)
        return d

def evenimente_din_json(cale):
    with open(cale, encoding="utf-8") as f:
        return [Eveniment(**d) for d in json.load(f)]
def main():
    print("\n\nAfișări sarcinile A:")
    p = Proces(3120, "update.exe", "ana", r"C:\Users\ana\AppData\Local\Temp\update.exe")
    print(p.pid, p.nume)
    print(p)
    print(p.e_suspect())   # True (update.exe din Temp)
    procese = procese_din_json("arsenal/windows/start/procese.json")
    print("procese:", len(procese))
    print("suspecte:", sum(1 for p in procese if p.e_suspect()))
    inv = Inventar.din_json("arsenal/windows/start/procese.json")
    print("procese:", len(inv))
    for p in inv.suspecte():
        print(f"  [{p.pid}] {p.nume}  {p.cale}")
    print(inv.pe_user())
    print("\n\nAfișări sarcinile B:")
    p = argparse.ArgumentParser()
    p.add_argument("capturi")
    p.add_argument("--json", action="store_true")
    a = p.parse_args()
    inv = Inventar.din_json(a.capturi + "/procese.json")
    ev = evenimente_din_json(a.capturi + "/evenimente.json")
    alarma = [e for e in ev if e.e_suspect()]
    if a.json:
        raport = {
            "procese_suspecte": [asdict(p) for p in inv.suspecte()],
            "evenimente_suspecte": [asdict(e) for e in alarma],
        }
        with open(a.capturi + "/raport.json", "w", encoding="utf-8") as f:
            json.dump(raport, f, ensure_ascii=False, indent=2)
        print(json.dumps(raport, ensure_ascii=False, indent=2))
    else:
        print(f"procese suspecte: {len(inv.suspecte())}")
        for p in inv.suspecte():
            print(f"  [{p.pid}] {p.nume}  {p.cale}")
        print(f"evenimente suspecte: {len(alarma)}")
        for e in alarma:
            print(f"  [{e.id}] {e.nivel}  {e.sursa}  {e.cont}  {e.mesaj}")
    print("\n\n")

if __name__ == "__main__":
    main()
