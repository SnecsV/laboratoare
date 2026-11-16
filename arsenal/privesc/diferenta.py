from enumerare import citeste_linii
def cai(fisier):
    return set(citeste_linii(fisier))
 
baza = cai("C:\\UTM\\arsenal\\privesc\\start\\baza_suid.txt")
acum = cai("C:\\UTM\\arsenal\\privesc\\start\\suid.txt")
print("baza:", len(baza), " acum:", len(acum))

noi = acum - baza
print(len(noi), "SUID noi fata de sistemul curat")
for c in sorted(noi):
    print(" ", c)

from enumerare import nume, GTFO
 
risc = {nume(c): ("mare" if nume(c) in GTFO else "normal") for c in noi}
periculoase = [c for c in sorted(noi) if nume(c) in GTFO]
print("periculoase NOI:", periculoase)

