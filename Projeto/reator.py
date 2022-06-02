import socket
import threading
import random
import json
from time import sleep
 

#O REATOR VAI RECEBER OS VALORES DE naOH, etOH
#A CADA SEGUNDO,O ORQUESTRADOR CHAMA ELE 
#E ELE RETORNA 0.75L DE SAÍDA REFENTE AO TOTAL
#PARA LOGICA DOS 10 SEC USAR SLEEP


def client_handler(client, msg):
    reator = {
        "oleo": 0.0,
        "naOH": 0.0, 
        "etOH": 0.00,
        "mix": 0.00,
        "ciclo": 0
    }

    menor_elemento = 0
    parte_1 = 1.25
    parte_2 = 2.5

    if msg != '' and (msg["etOH"] > 0 and msg["naOH"] > 0 and msg["oleo"] > 0):            
        if (msg["etOH"] < msg["naOH"]) and (msg["etOH"] < msg["oleo"]):
            menor_elemento = msg["etOH"]
            print("")
            print(f"MENOR ELEMENTO DO REATOR etOH: {menor_elemento}")
        elif (msg["naOH"] < msg["etOH"]) and (msg["naOH"] < msg["oleo"]):
            print("")
            menor_elemento = msg["naOH"]
            print(f"MENOR ELEMENTO DO REATOR naOH: {menor_elemento}")
        else:
            print("")
            menor_elemento = msg["oleo"]
            print(f"MENOR ELEMENTO DO REATOR oleo: {menor_elemento}")

        print("")
        print(f"FORAA - Valores recebidos do orquestrador: {msg}")
        print(f"FORAA - Valores do elementos no reator: {reator}")
        if menor_elemento < parte_1 and menor_elemento > 0 and (float(round(msg["oleo"], 2)) >= (menor_elemento*2)):
            reator["etOH"] = menor_elemento
            reator["naOH"] = menor_elemento
            reator["oleo"] = (menor_elemento * 2)
            reator["mix"] = ((reator["etOH"] + reator["naOH"]) + reator["oleo"])
            reator["ciclo"] = 1
            sleep(menor_elemento * 4)
            
            print("")
            print(f"IF 1 - Valores recebidos do orquestrador: {msg}")
            print(f"IF 1 - Valores do elementos no reator: {reator}")

            client.send(str.encode(json.dumps(reator)))            
        elif menor_elemento >= parte_1 and (msg["oleo"] >= parte_2): 

            print("")
            print(f"IF 2 - Valores recebidos do orquestrador: {msg}")
            print(f"IF 2 BEFORE - Valores do elementos no reator: {reator}")

            reator["etOH"] = parte_1
            reator["naOH"] = parte_1
            reator["oleo"] = parte_2
            reator["mix"] = 5
            reator["ciclo"] = 1
            print(f"IF 2 AFTER - Valores do elementos no reator: {reator}")

            sleep(1)
            client.send(str.encode(json.dumps(reator)))    
        elif msg["oleo"] == menor_elemento:
            if menor_elemento <= parte_2:
                print("")  
                print(f"IF 3 - Valores recebidos do orquestrador: {msg}")
                print(f"IF 3 - BEFORE Valores do elementos no reator: {reator}")            

                reator["etOH"] = menor_elemento / 2
                reator["naOH"] = menor_elemento / 2
                reator["oleo"] = menor_elemento 
                reator["mix"] = ((reator["etOH"] + reator["naOH"]) + reator["oleo"])
                reator["ciclo"] = 1

                print(f"IF 3 - AFTER Valores do elementos no reator: {reator}")            
                
                sleep(menor_elemento * 4)
                client.send(str.encode(json.dumps(reator)))
            else:
                print("")
                print(f"IF 4 - Valores recebidos do orquestrador: {msg}")
                print(f"IF 4 - BEFORE Valores do elementos no reator: {reator}")            

                reator["etOH"] = parte_1
                reator["naOH"] = parte_1
                reator["oleo"] = parte_2
                reator["mix"] = 5
                reator["ciclo"] = 1

                print(f"IF 4 - AFTER Valores do elementos no reator: {reator}")            
                sleep(1)    
                client.send(str.encode(json.dumps(reator)))
        else:
            reator["etOH"] = menor_elemento / 2
            reator["naOH"] = menor_elemento / 2
            reator["oleo"] =  menor_elemento
            reator["mix"] = ((reator["etOH"] + reator["naOH"]) + reator["oleo"])
            reator["ciclo"] = 1

            
            print("")
            print(f"IF 5 - Valores recebidos do orquestrador: {msg}")
            print(f"IF 5 - Valores do elementos no reator: {reator}")

            sleep(menor_elemento * 4)
            client.send(str.encode(json.dumps(reator)))            

    else:
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
        msg = conexao.recv(1024).decode()
        threading.Thread(target= client_handler, args=(conexao, json.loads(msg))).start()    
            

if __name__ == "__main__":
    main()