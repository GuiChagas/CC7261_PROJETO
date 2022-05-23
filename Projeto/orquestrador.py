import socket
import threading
import json
from time import sleep

orquestrador_dados = {
    "oleo": 0.00,
    "etOH": 0.00,
    "NaOH": 0.00,
    "reator": {
        "oleo": 0,
        "etOH": 0,
        "NaOH": 0,
        "mix": 0
    },
    "decantador": {    
        "glicerina":0,
        "etOH": 0,
        "solucao": 0,        
        "status": "disponivel"
    },
    "secador":{
        "solucao_pos_secador": 0,
        "envio_por": ""
    }
}

def listen_server_tanque_oleo(client):
    while 1:
        msg = client.recv(1024).decode()
        
        if msg != '':
            orquestrador_dados["oleo"] += float(msg) 
            print(f"RECEBIDA DE TANQUE OLEO: {msg}")
        break

def listen_server_tanque_NaetOH(client):

    while 1:
        msg = json.loads(client.recv(1024).decode())
    
        if msg != '':
            print(f"Quantidade recebida do tanque de NAOH/etOH: {msg['naOH']}")
            print(f"Quantidade recebida do tanque de NAOH/etOH: {msg['etOH']}")
            orquestrador_dados["NaOH"] += float(msg["naOH"])
            orquestrador_dados["etOH"] += float(msg["etOH"])
        break

def listen_server_reator(client):

    while 1:
        msg = json.loads(client.recv(1024).decode())

        print(f"RECEBIDA DE NAOH: {msg['naOH']}")
        print(f"RECEBIDA DE etOH: {msg['etOH']}")
        print(f"RECEBIDA DE OLEO: {msg['oleo']}")

        if msg != '':
            orquestrador_dados["reator"]["NaOH"] -= float(msg["naOH"])
            orquestrador_dados["reator"]["etOH"] -= float(msg["etOH"])
            orquestrador_dados["reator"]["oleo"] -= float(msg["oleo"])
            orquestrador_dados["reator"]["mix"] -= float(msg["mix"])

        break

def listen_server_decantador(client):
    while 1:
        msg = client.recv(1024).decode()
        
        if msg != '':
            orquestrador_dados["decantador"]["glicerina"] += float(msg["glicerina"]) 
            orquestrador_dados["decantador"]["etOH"] += float(msg["etOH"]) 
            orquestrador_dados["decantador"]["solucao"] += float(msg["solucao"]) 
            orquestrador_dados["decantador"]["status"] = "disponivel" 
            print(f"RECEBIDA DE TANQUE OLEO: {msg}")
        break



def orc_tanque_oleo():
    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        c.connect((socket.gethostname(), 50002))

        while 1:
            t = threading.Thread(target= listen_server_tanque_oleo, args=(c, ))
            t.start()
            t.join()
            sleep(1) #tempo de vazão
            break

    except:
        return print('Não foi possivel conectar ao servidor')

def orc_tanque_naetOH():
    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        c.connect((socket.gethostname(), 50003))
        while 1:
            t = threading.Thread(target= listen_server_tanque_NaetOH, args=(c, ))
            t.start()
            t.join()
            sleep(1) #tempo de vazão
            break

    except:
        return print('Não foi possivel conectar ao servidor')        

def orc_reator():
    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        if orquestrador_dados["decantador"]["status"] == "disponivel":
            c.connect((socket.gethostname(), 50004))
            reator_envio = {
                "oleo": 0.75,
                "naOH": 0.5,        
                "etOH": 0.25,
            }
            jserialize = json.dumps(reator_envio)
            
            c.send(str.encode(jserialize))

            while 1:
                t = threading.Thread(target= listen_server_reator, args=(c, ))
                t.start()
                t.join()
                sleep(1) #tempo de vazão
                break
        else: 
            sleep(5)

    except:
        return print('Não foi possivel conectar ao servidor')    

def orc_decantador():
    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        
        if orquestrador_dados["decantador"]["status"] == "disponivel":
            orquestrador_dados["decantador"]["status"] = "repouso"
            c.connect((socket.gethostname(), 50005))
            jserialize = json.dumps(orquestrador_dados["reator"])    
            c.send(str.encode(jserialize))

            while 1:
                t = threading.Thread(target= listen_server_decantador, args=(c, ))
                t.start()
                t.join()
                break

    except:
        return print('Não foi possivel conectar ao servidor')

def orc_secador(name):
    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        c.connect((socket.gethostname(), 50006))
        c.send(str.encode(orquestrador_dados["reator"][name]["solucao"]))

        while 1:
            t = threading.Thread(target= listen_server_decantador, args=(c, ))
            t.start()
            t.join()
            break

    except:
        return print('Não foi possivel conectar ao servidor')
def main():

    while True:
        #orc_tanque_oleo()  
        #orc_tanque_naetOH() #executar em uma thread
        orc_reator()

if __name__ == '__main__': 
    main() 