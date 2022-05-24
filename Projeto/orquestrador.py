from ast import Break
import socket
import threading
import json
from time import sleep

orquestrador_dados = {
    "oleo": 0.00,
    "etOH": 0.00,
    "naOH": 0.00,
    "reator": {
        "oleo": 0,
        "etOH": 0,
        "naOH": 0,
        "mix": 0
    },
    "decantador": {    
        "glicerina":0,
        "etOH": 0,
        "solucao": 0,        
        "status": "disponivel"
    },
    "tanque_glicerina":{
        "glicerina":0
    },
    "secador":{
        "solucao_pos_secador": 0    
    },
    "tanque_lavagem_1": 0,
    "tanque_lavagem_2": 0,
    "tanque_lavagem_3": 0,
    "tanque_bio": 0
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
            orquestrador_dados["naOH"] += float(msg["naOH"])
            orquestrador_dados["etOH"] += float(msg["etOH"])
        break

def listen_server_reator(client):

    while 1:
        msg = json.loads(client.recv(1024).decode())
        
        print(f"Valor de oleo recebido do reator: {msg['oleo']}")
        print(f"Valor de naOH recebido do reator: {msg['naOH']}")
        print(f"Valor de etOH recebido do reator: {msg['etOH']}")

        if msg != '':
            orquestrador_dados["reator"]["naOH"] -= float(msg["naOH"])
            orquestrador_dados["reator"]["etOH"] -= float(msg["etOH"])
            orquestrador_dados["reator"]["oleo"] -= float(msg["oleo"])
            orquestrador_dados["reator"]["mix"] = float(msg["mix"])

            orc_decantador()
            break

def listen_server_decantador(client):
    while 1:
        msg = json.loads(client.recv(1024).decode())

        print(f"Valor de glicerina recebido do decantador: {msg['glicerina']}")
        print(f"Valor de etOH recebido do decantador: {msg['etOH']}")
        print(f"Valor de solucao recebido do decantador: {msg['solucao']}")
        print(f"Valor de status recebido do decantador: {msg['status']}")

        if msg != '':
            orquestrador_dados["decantador"]["glicerina"] += float(msg["glicerina"]) 
            orquestrador_dados["decantador"]["etOH"] += float(msg["etOH"]) 
            orquestrador_dados["decantador"]["solucao"] += float(msg["solucao"]) 
            orquestrador_dados["decantador"]["status"] = "disponivel"
            x = threading.Thread(target= orc_secador, args=("decantador", ))
            x.start()
            x.join()
            #orc_secador("decantador")
            #threading.Thread(target= orc_tanque_lavagem_1, args=()).start()
            #orc_tanque_lavagem_1()
            break

def listen_server_tanque_glicerina(client):
    while 1:
        msg = client.recv(1024).decode()
        
        if msg != '':
            orquestrador_dados["tanque_glicerina"]["glicerina"] = float(msg["glicerina"]) 
            print(f"Total tanque de glicerina: {msg}")
        break

def listen_server_tanque_oleo(client):
    while 1:
        msg = client.recv(1024).decode()
        
        if msg != '':
            orquestrador_dados["oleo"] += float(msg) 
            print(f"RECEBIDA DE TANQUE OLEO: {msg}")
        break

def listen_server_secador(client, name):
    while 1:
        msg = json.loads(client.recv(1024).decode())  
        if msg != '':        
            if name == "decantador":
                print(f"Recebida do secador do decantador (etOH): {msg}")
                orquestrador_dados["etOH"] += float(msg["solucao_secador"])
                    
            elif name == "lavagem":
                orquestrador_dados["tanque_bio"] += float(msg["solucao_secador"])
                print(f"Recebida do secador da lavagem (Solução Final): {msg}")
        break        

def listen_server_tanque_lavagem_1(client):
    while 1:
        msg = client.recv(1024).decode()
        
        if msg != '':
            print(f"Valor recebido do tanque de lavagem 1: {msg}")
            orquestrador_dados["tanque_lavagem_1"] += float(msg) 
            orc_tanque_lavagem_2()
        break    

def listen_server_tanque_lavagem_2(client):
    while 1:
        msg = client.recv(1024).decode()
        
        if msg != '':
            print(f"Valor recebido do tanque de lavagem 2: {msg}")

            orquestrador_dados["tanque_lavagem_2"] += float(msg) 
            orc_tanque_lavagem_3()
        break  

def listen_server_tanque_lavagem_3(client):
    while 1:
        msg = client.recv(1024).decode()
        
        if msg != '':
            print(f"Valor recebido do tanque de lavagem 3: {msg}")

            orquestrador_dados["tanque_lavagem_3"] += float(msg) 
            orc_secador("lavagem")
        break  

def listen_server_tanque_bio(client):
    while 1:
        msg = client.recv(1024).decode()
        
        if msg != '':
            orquestrador_dados["tanque_bio"] += float(msg) 
            print(f"No tanque de bio-diesel: {msg}")
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
            
            orquestrador_dados["reator"]["oleo"] += 0.75
            orquestrador_dados["reator"]["naOH"] += 0.5
            orquestrador_dados["reator"]["etOH"] += 0.25
            
            jserialize = json.dumps(orquestrador_dados["reator"])
            
            c.send(str.encode(jserialize))

            while 1:
                t = threading.Thread(target= listen_server_reator, args=(c, ))
                t.start()
                t.join()
                sleep(1) #tempo de vazão
                break
        else: 
            print("Reator está em repouso")
            sleep(10)

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
        if name == "decantador":
            print(f"ENVIANDO ETOH: {orquestrador_dados['decantador']['etOH']}")
            c.send(str.encode(str(orquestrador_dados["decantador"]["etOH"])))
        
        elif name == "lavagem":
            c.send(str.encode(str(orquestrador_dados["lavagem"]["solucao"])))


        while 1:
            t = threading.Thread(target= listen_server_secador, args=(c, name))
            t.start()
            t.join()
            break

    except:
        return print('Não foi possivel conectar ao servidor')        

def orc_tanque_glicerina():
    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        c.connect((socket.gethostname(), 50011))
        jserialize = json.dumps(orquestrador_dados["decantador"]["glicerina"])    
        c.send(str.encode(jserialize))

        while 1:
            t = threading.Thread(target= listen_server_tanque_glicerina, args=(c, ))
            t.start()
            t.join()
            sleep(1) #tempo de vazão
            break

    except:
        return print('Não foi possivel conectar ao servidor')

def orc_tanque_lavagem_1():
    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        c.connect((socket.gethostname(), 50007))
        c.send(str.encode(str(orquestrador_dados["decantador"]["solucao"])))
        while 1:
            t = threading.Thread(target= listen_server_tanque_lavagem_1, args=(c, ))
            t.start()
            t.join()
            sleep(1) #tempo de vazão
            break

    except:
        return print('Não foi possivel conectar ao servidor')

def orc_tanque_lavagem_2():
    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        c.connect((socket.gethostname(), 50008))
        c.send(str.encode(str(orquestrador_dados["tanque_lavagem_1"])))

        while 1:
            t = threading.Thread(target= listen_server_tanque_lavagem_2, args=(c, ))
            t.start()
            t.join()
            sleep(1) #tempo de vazão
            break

    except:
        return print('Não foi possivel conectar ao servidor')

def orc_tanque_lavagem_3():
    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        c.connect((socket.gethostname(), 50009))
        c.send(str.encode(str(orquestrador_dados["tanque_lavagem_2"])))

        while 1:
            t = threading.Thread(target= listen_server_tanque_lavagem_3, args=(c, ))
            t.start()
            t.join()
            sleep(1) #tempo de vazão
            break

    except:
        return print('Não foi possivel conectar ao servidor')        

def orc_tanque_bio():
    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        c.connect((socket.gethostname(), 50010))

        while 1:
            t = threading.Thread(target= listen_server_tanque_bio, args=(c, ))
            t.start()
            t.join()
            sleep(1) #tempo de vazão
            break

    except:
        return print('Não foi possivel conectar ao servidor')

def main():

    while True:
        #threading.Thread(target= orc_tanque_oleo, args=()).start()
        #threading.Thread(target= orc_tanque_naetOH, args=()).start()
        #orc_tanque_oleo()  
        #orc_tanque_naetOH() #executar em uma thread
        #if (orquestrador_dados["oleo"] != 0) and (orquestrador_dados["etOH"] != 0) and (orquestrador_dados["naOH"] != 0):
        orc_reator()

if __name__ == '__main__': 
    main() 