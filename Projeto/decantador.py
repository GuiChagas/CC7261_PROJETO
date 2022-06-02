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
    decantador = {
        "glicerina":0,
        "etOH": 0,
        "solucao": 0,
        "ciclo": 0,
        "status": ""
    }

    decantador["glicerina"] = float(msg["mix"]) * 0.01
    decantador["etOH"] = float(msg["mix"]) * 0.03
    decantador["solucao"] = float(msg["mix"]) * 0.96
    decantador["ciclo"] = 1
    decantador["status"] = "repouso"
    
    print(f"Valores decantador: {decantador}")

    sleep(5)
    decantador["status"] = "disponivel"
    client.send(str.encode(json.dumps(decantador)))            
             

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

    try:
        server.bind((socket.gethostname(), 50005))
    except:
        print("Não consegui a conectar")

    server.listen()

    while 1:
        conexao, addr = server.accept()
        msg = conexao.recv(1024).decode()
        threading.Thread(target= client_handler, args=(conexao, json.loads(msg))).start()    
            

if __name__ == "__main__":
    main()