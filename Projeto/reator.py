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
    "oleo": 0.0,
    "naOH": 0.0, 
    "etOH": 0.00,
    "mix": 0.00
}

def client_handler(client, msg):
    menor_elemento = 0
    parte_1 = 1.25
    parte_2 = 2.5

    print(f"Valores recebidos do orquestrador: {msg}")
    print("")
    print(f"Valores do elementos no reator: {reator}")

    if msg != '':            
        if (msg["etOH"] < msg["naOH"]) and (msg["etOH"] < msg["oleo"]):
            menor_elemento = msg["etOH"]
        elif (msg["naOH"] < msg["etOH"]) and (msg["naOH"] < msg["oleo"]):
            menor_elemento = msg["naOH"]
        else:
            menor_elemento = msg["naOH"]
        
        if menor_elemento < parte_1 and menor_elemento > 0 and (msg["oleo"] >= (menor_elemento*2)):
            reator["etOH"] = menor_elemento
            reator["naOH"] = menor_elemento
            reator["oleo"] = (menor_elemento * 2)
            reator["mix"] = ((msg["etOH"] + msg["naOH"]) + msg["oleo"])
            sleep(menor_elemento * 4)
            
            client.send(str.encode(json.dumps(reator)))            
        elif menor_elemento >= parte_1 and (msg["oleo"] >= parte_2): 
            reator["etOH"] = parte_1
            reator["naOH"] = parte_1
            reator["oleo"] = parte_2
            reator["mix"] += ((msg["etOH"] + msg["naOH"]) + msg["oleo"])
            sleep(5)
            
            client.send(str.encode(json.dumps(reator)))    
        elif msg["oleo"] == menor_elemento:        
            reator["etOH"] = (menor_elemento / 2)
            reator["naOH"] = (menor_elemento / 2)
            reator["oleo"] = (menor_elemento * 4)
            reator["mix"] += ((msg["etOH"] + msg["naOH"]) + msg["oleo"])
            sleep(menor_elemento * 4)

            client.send(str.encode(json.dumps(reator)))
        
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