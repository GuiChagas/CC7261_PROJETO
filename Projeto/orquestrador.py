import socket
import threading
from threading import Thread
import json
import time
from time import sleep

orquestrador_dados = {
    "oleo": 0.00,
    "etOH": 0.00,
    "naOH": 0.00,
    "reator": {
        "oleo": 0,
        "etOH": 0,
        "naOH": 0,
        "mix": 0,
        "ciclos": 0
    },
    "decantador": {    
        "glicerina":0,
        "etOH": 0,
        "solucao": 0,
        "ciclos": 0,        
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
    "tanque_bio": 0,
    "emulsao": 0,
    "perda_total_produto": 0
}

def listen_server_tanque_oleo(client):
    while 1:
        msg = client.recv(1024).decode()
        
        if msg != '' and msg != None:
            if float(msg) != 0:
                orquestrador_dados["oleo"] += float(msg) 
                print("")
                print(f"Valor recebido da tanque de óleo: {msg}")
        break

def listen_server_tanque_NaetOH(client):

    while 1:
        msg = json.loads(client.recv(1024).decode())
    
        if msg != '' and msg != None:
            print("")
            print(f"Quantidade recebida do tanque de NAoh/etOH (NAoh): {msg['naOH']}")
            print(f"Quantidade recebida do tanque de NAoh/etOH (etOH): {msg['etOH']}")
            orquestrador_dados["naOH"] += float(msg["naOH"])
            orquestrador_dados["etOH"] += float(msg["etOH"])
        break

def listen_server_reator(client):

    while 1:
        msg = json.loads(client.recv(1024).decode())
    
        if msg != '' and msg != None:
            print("")
            print(f"Valor de oleo recebido do reator: {msg['oleo']}")
            print(f"Valor de naOH recebido do reator: {msg['naOH']}")
            print(f"Valor de etOH recebido do reator: {msg['etOH']}")
                      

            orquestrador_dados["reator"]["mix"] += float(msg["mix"])
            orquestrador_dados["reator"]["ciclos"] += float(msg["ciclo"])

            if (orquestrador_dados["reator"]["oleo"] - float(msg["oleo"])) < 0:
                orquestrador_dados["reator"]["oleo"] = 0
            else:
                orquestrador_dados["reator"]["oleo"] -= float(msg["oleo"])

            if (orquestrador_dados["reator"]["naOH"] - float(msg["naOH"])) < 0:
                orquestrador_dados["reator"]["naOH"] = 0
            else:
                orquestrador_dados["reator"]["naOH"] -= float(msg["naOH"])

            if (orquestrador_dados["reator"]["etOH"] - float(msg["etOH"])) < 0:
                orquestrador_dados["reator"]["etOH"] = 0
            else:
                orquestrador_dados["reator"]["etOH"] -= float(msg["etOH"])
                        
            print("")
            print("Valores do reator :")
            print(orquestrador_dados["reator"])
            print("")     
         
            
            if orquestrador_dados["reator"]["mix"] > 0 and orquestrador_dados["decantador"]["status"] == "disponivel":
                threading.Thread(target= orc_decantador, args=()).start()
                # x = threading.Thread(target= orc_decantador, args=())
                # x.start()
                # x.join()
                # orc_decantador()
            break

def listen_server_decantador(client):
    while 1:
        msg = json.loads(client.recv(1024).decode())


        print("")
        print(f"Valor de glicerina recebido do decantador: {msg['glicerina']}")
        print(f"Valor de etOH recebido do decantador: {msg['etOH']}")
        print(f"Valor de solucao recebido do decantador: {msg['solucao']}")
        print(f"Valor de status recebido do decantador: {msg['status']}")


        if msg != '' and msg != None:
            orquestrador_dados["decantador"]["etOH"] = float(msg["etOH"]) 
            orquestrador_dados["decantador"]["glicerina"] = float(msg["glicerina"]) 
            orquestrador_dados["decantador"]["solucao"] += float(msg["solucao"]) 
            orquestrador_dados["decantador"]["ciclos"] += float(msg["ciclo"]) 
            orquestrador_dados["decantador"]["status"] = "disponivel"

            print("")
            print("Valores do decantador :")        
            print(orquestrador_dados["decantador"])
            print("")

            sleep(msg['solucao'])

            if float(msg["etOH"]) > 0:
                threading.Thread(target= orc_secador, args=("decantador", )).start()
                # x = threading.Thread(target= orc_secador, args=("decantador", ))
                # x.start()
                # x.join()
            if float(msg["glicerina"]) > 0:
                threading.Thread(target= orc_tanque_glicerina, args=()).start()
                # y = threading.Thread(target= orc_tanque_glicerina, args=())
                # y.start()
                # y.join()
            if float(msg["solucao"]) > 0:
                threading.Thread(target= orc_tanque_lavagem_1, args=()).start()
                # z = threading.Thread(target= orc_tanque_lavagem_1, args=())
                # z.start()
                # z.join()            
            break

def listen_server_secador(client, name):
    while 1:
        msg = json.loads(client.recv(1024).decode())  
        if msg != '' and msg != None:        
            if name == "decantador":
                print(f"Recebida do secador do decantador (etOH): {msg}")
                orquestrador_dados["etOH"] += float(msg["solucao_secador"])
                orquestrador_dados["perda_total_produto"] += float(msg["perda_produto"])
                
                    
            elif name == "lavagem":
                orquestrador_dados["perda_total_produto"] += float(msg["perda_produto"])
                threading.Thread(target= orc_tanque_bio, args=(msg["solucao_secador"], )).start()
                # x = threading.Thread(target= orc_tanque_bio, args=(msg["solucao_secador"], ))
                # x.start()
                # x.join()
                #orc_tanque_bio(msg["solucao_secador"])

        break   

def listen_server_tanque_glicerina(client):
    while 1:
        msg = json.loads(client.recv(1024).decode())
        
        if msg != '' and msg != None:
            orquestrador_dados["tanque_glicerina"]["glicerina"] = float(msg["glicerina"])
            print(f"Total tanque de glicerina: {msg}")
        break

def listen_server_tanque_lavagem_1(client):
    while 1:
        msg = json.loads(client.recv(1024).decode())
        
        if msg != '' and msg != None:
            print(f"Valor recebido do tanque de lavagem 1: {msg}")
            orquestrador_dados["tanque_lavagem_1"] = float(msg["solucao"])
            orquestrador_dados["emulsao"] += float(msg["emulsao"])
            sleep(1)
            x = threading.Thread(target= orc_tanque_lavagem_2, args=())
            x.start()
            x.join()            
            #orc_tanque_lavagem_2()
        break    

def listen_server_tanque_lavagem_2(client):
    while 1:
        msg = json.loads(client.recv(1024).decode())
        
        if msg != '' and msg != None:
            print(f"Valor recebido do tanque de lavagem 2: {msg}")
            orquestrador_dados["tanque_lavagem_2"] = float(msg["solucao"]) 
            orquestrador_dados["emulsao"] += float(msg["emulsao"])

            sleep(1)
            x = threading.Thread(target= orc_tanque_lavagem_3, args=())
            x.start()
            x.join() 
            #orc_tanque_lavagem_3()
        break  

def listen_server_tanque_lavagem_3(client):
    while 1:
        msg = json.loads(client.recv(1024).decode())
        
        if msg != '' and msg != None:
            print(f"Valor recebido do tanque de lavagem 3: {msg}")
            orquestrador_dados["tanque_lavagem_3"] = float(msg["solucao"])
            orquestrador_dados["emulsao"] += float(msg["emulsao"])

            sleep(1)
            x = threading.Thread(target= orc_secador, args=("lavagem", ))
            x.start()
            x.join() 

            #orc_secador("lavagem")
        break  

def listen_server_tanque_bio(client):
    while 1:
        msg = json.loads(client.recv(1024).decode())
        
        if msg != '' and msg != None:
            orquestrador_dados["tanque_bio"] = float(msg["solucao_final"])
            print(f"No tanque de bio-diesel: {msg}")
            print("")
            print(f"{orquestrador_dados}")
            print("")
        break  

def orc_tanque_oleo():
    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        c.connect((socket.gethostname(), 50002))

        while 1:
            t = threading.Thread(target= listen_server_tanque_oleo, args=(c, ))
            t.start()
            t.join()
            sleep(1)
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
            sleep(1)
            break

    except:
        return print('Não foi possivel conectar ao servidor')        

def orc_reator():
    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        if orquestrador_dados["decantador"]["status"] == "disponivel":
            if orquestrador_dados["etOH"] >= 1.25:

                orquestrador_dados["reator"]["etOH"] += 1.25
                orquestrador_dados["etOH"] -= 1.25
            else:
                orquestrador_dados["reator"]["etOH"] += orquestrador_dados["etOH"] 
                orquestrador_dados["etOH"] = 0
            if orquestrador_dados["naOH"] >= 1.25:
                orquestrador_dados["reator"]["naOH"] += 1.25
                orquestrador_dados["naOH"] -= 1.25
            else:
                orquestrador_dados["reator"]["naOH"] += orquestrador_dados["naOH"] 
                orquestrador_dados["naOH"] = 0

            if orquestrador_dados["oleo"] >= 2.5:
                orquestrador_dados["reator"]["oleo"] += 2.5
                orquestrador_dados["oleo"] -= 2.5                   
            else:
                orquestrador_dados["reator"]["oleo"] +=  orquestrador_dados["oleo"]
                orquestrador_dados["oleo"] = 0
            
            print(f"DEPOIS: {orquestrador_dados['reator']}")
            jserialize = json.dumps(orquestrador_dados["reator"])
            c.connect((socket.gethostname(), 50004))
            c.send(str.encode(jserialize))

            while 1:
                t = threading.Thread(target= listen_server_reator, args=(c, ))
                t.start()
                t.join()
                break
        else: 
            print("decantador está em repouso")

    except:
        return print('Não foi possivel conectar ao servidor')    

def orc_decantador():
    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        
        if orquestrador_dados["decantador"]["status"] == "disponivel":
            if orquestrador_dados["reator"]["mix"] <= 10:
                orquestrador_dados["decantador"]["status"] = "repouso"
                jserialize = json.dumps(orquestrador_dados["reator"])    
               
                
                c.connect((socket.gethostname(), 50005))
                c.send(str.encode(jserialize))
                
                orquestrador_dados["reator"]["mix"] = 0
                while 1:
                    t = threading.Thread(target= listen_server_decantador, args=(c, ))
                    t.start()
                    t.join()
                    break
            else:
                orquestrador_dados["decantador"]["status"] = "repouso"
                c.connect((socket.gethostname(), 50005))
                
                jserialize = orquestrador_dados["reator"]
                jserialize["mix"] = 10 
                c.send(str.encode(json.dumps(jserialize)))
                orquestrador_dados["reator"]["mix"] -= 10

                while 1:
                    t = threading.Thread(target= listen_server_decantador, args=(c, ))
                    t.start()
                    t.join()
                    break
        else:
            print('Decantador está em repouso')
    except:
        return print('Não foi possivel conectar ao servidor')

def orc_secador(name):
    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        c.connect((socket.gethostname(), 50006))
        if name == "decantador":
            print(f"ENVIANDO ETOH: {orquestrador_dados['decantador']['etOH']}")
            c.send(str.encode(str(orquestrador_dados["decantador"]["etOH"])))
            orquestrador_dados["decantador"]["etOH"] -= orquestrador_dados["decantador"]["etOH"]
        
        elif name == "lavagem":
            c.send(str.encode(str(orquestrador_dados["tanque_lavagem_3"])))


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
        c.send(str.encode(str(orquestrador_dados["decantador"]["glicerina"])))
        orquestrador_dados["decantador"]["glicerina"] -= orquestrador_dados["decantador"]["glicerina"] 
        
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
        orquestrador_dados["decantador"]["solucao"] -= orquestrador_dados["decantador"]["solucao"] 
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

def orc_tanque_bio(value):
    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        c.connect((socket.gethostname(), 50010))
        c.send(str.encode(str(value)))
        while 1:
            t = threading.Thread(target= listen_server_tanque_bio, args=(c, ))
            t.start()
            t.join()
            sleep(1) #tempo de vazão
            break

    except:
        return print('Não foi possivel conectar ao servidor')

class ServerThread(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        while True:
            orc_tanque_oleo()
            orc_tanque_naetOH()

def main():
    
    start = time.time()
    while True:
        end = time.time()
        if end-start < 3600:
            threading.Thread(target= orc_tanque_oleo, args=()).start()
            sleep(1)
            threading.Thread(target= orc_tanque_naetOH, args=()).start()
            sleep(1)
            if (orquestrador_dados["naOH"] > 0) and (orquestrador_dados["etOH"] > 0) and (orquestrador_dados["oleo"] > 0) and (orquestrador_dados["decantador"]["status"] == "disponivel"):
                sleep(1)
                threading.Thread(target= orc_reator, args=()).start()
if __name__ == '__main__': 
    main() 