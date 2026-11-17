from dataclasses import dataclass, asdict
import json
 
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

p = Proces(3120, "update.exe", "ana", r"C:\Users\ana\AppData\Local\Temp\update.exe")
print(p.pid, p.nume)
print(p)
print(p.e_suspect())   # True (update.exe din Temp)
procese = procese_din_json("arsenal/windows/start/procese.json")
print("procese:", len(procese))
print("suspecte:", sum(1 for p in procese if p.e_suspect()))
