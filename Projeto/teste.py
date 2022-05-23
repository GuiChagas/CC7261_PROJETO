import threading
from time import sleep

def setInterval(func,time):
    e = threading.Event()
    while not e.wait(time):
        func()


def oi():
    print('oi')


reator = {
    "oleo": 0.00,
    "etOH": 0.00,
    "naOH": 0.00,
    "mix": 0.00,  
}

while True:
    reator["oleo"] += 1
    reator["naOH"] += 0.5
    reator["etOH"] += 0.25

    parte_1 = 1.25
    parte_2 = 2.5
    menor_elemento = 0

    if (reator["etOH"] < reator["naOH"]) and (reator["etOH"] < reator["oleo"]):
        menor_elemento += reator["etOH"]
    elif (reator["naOH"] < reator["etOH"]) and (reator["naOH"] < reator["oleo"]):
        menor_elemento += reator["naOH"]
    else:
        menor_elemento += reator["oleo"]
       
    if menor_elemento < parte_1 and menor_elemento > 0 and (reator["oleo"] >= (menor_elemento*2)):
        reator["etOH"] -= menor_elemento
        reator["naOH"] -= menor_elemento
        reator["oleo"] -= (menor_elemento * 2)
        reator["mix"] += ((reator["etOH"] + reator["naOH"]) + reator["oleo"])
    elif menor_elemento >= parte_1 and (reator["oleo"] != (menor_elemento)): 
        reator["etOH"] -= parte_1
        reator["naOH"] -= parte_1
        reator["oleo"] -= parte_2
        reator["mix"] += ((reator["etOH"] + reator["naOH"]) + reator["oleo"])

    print(f"VALOR MENOR ELEMENTO: {menor_elemento}")
    print(f"VALOR ETOH: {reator['etOH']}")
    print(f"VALOR NAOH: {reator['naOH']}")
    print(f"VALOR OLEO: {reator['oleo']}")
    print(f"VALOR MIX: {reator['mix']}")
    sleep(5)

