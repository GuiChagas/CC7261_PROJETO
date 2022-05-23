import socket
import threading
import random
import json
from time import sleep
 

#O REATOR VAI RECEBER OS VALORES DE naOH, etOH
#A CADA SEGUNDO,O ORQUESTRADOR CHAMA ELE 
#E ELE RETORNA 0.75L DE SAÍDA REFENTE AO TOTAL
#PARA LOGICA DOS 10 SEC USAR SLEEP

reator = {
    "oleo": 0.00,
    "naOH": 0.00, 
    "etOH": 0.00,
    "mix": 0.00
}

def client_handler(client, msg):
    menor_elemento = 0
    parte_1 = 1.25
    parte_2 = 2.5

    print(f"MENSAGEM RECEBIDA: {msg}")
    print("")
    print(f"VALOR REATOR: {reator}")

    if msg != '':
        reator["naOH"] += msg["naOH"]
        reator["etOH"] += msg["etOH"]
        reator["oleo"] += msg["oleo"]
            
        if (reator["etOH"] < reator["naOH"]) and (reator["etOH"] < reator["oleo"]):
            menor_elemento = reator["etOH"]
        elif (reator["naOH"] < reator["etOH"]) and (reator["naOH"] < reator["oleo"]):
            menor_elemento = reator["naOH"]
        else:
            menor_elemento = reator["naOH"]
        
        if menor_elemento < parte_1 and menor_elemento > 0 and (reator["oleo"] >= (menor_elemento*2)):
            reator["etOH"] = menor_elemento
            reator["naOH"] = menor_elemento
            reator["oleo"] = (menor_elemento * 2)
            reator["mix"] = ((reator["etOH"] + reator["naOH"]) + reator["oleo"])
            client.send(str.encode(json.dumps(reator)))            
        elif menor_elemento >= parte_1 and (reator["oleo"] >= parte_2): 
            reator["etOH"] = parte_1
            reator["naOH"] = parte_1
            reator["oleo"] = parte_2
            reator["mix"] += ((reator["etOH"] + reator["naOH"]) + reator["oleo"])
            client.send(str.encode(json.dumps(reator)))    
        elif reator["oleo"] == menor_elemento:        
            reator["etOH"] = (menor_elemento / 2)
            reator["naOH"] = (menor_elemento / 2)
            reator["oleo"] = (menor_elemento * 4)
            reator["mix"] += ((reator["etOH"] + reator["naOH"]) + reator["oleo"])
            client.send(str.encode(json.dumps(reator)))
    sleep(menor_elemento * 4) #tempo de vazão

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

    try:
        server.bind((socket.gethostname(), 50004))
    except:
        print("Não consegui a conectar")

    server.listen()

    while 1:
        conexao, addr = server.accept()
        #print(conexao)
        msg = conexao.recv(1024).decode()
        threading.Thread(target= client_handler, args=(conexao, json.loads(msg))).start()    
            

if __name__ == "__main__":
    main()