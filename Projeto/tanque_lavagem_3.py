import socket
import threading
import random
import json
from time import sleep
 

#O REATOR VAI RECEBER OS VALORES DE naOH, etOH
#A CADA SEGUNDO,O ORQUESTRADOR CHAMA ELE 
#E ELE RETORNA 0.75L DE SAÍDA REFENTE AO TOTAL
#PARA LOGICA DOS 10 SEC USAR SLEEP

tanque_lavagem = {
    "emulsao": 0,
    "solucao": 0
}

def client_handler(client, msg):

    tanque_lavagem["solucao_secador"] = float(msg["solucao"]) * 0.975
    tanque_lavagem["emulsao"] = float(msg["solucao"]) * 0.025
    client.send(str.encode(json.dumps(tanque_lavagem)))

    if tanque_lavagem["emulsao"] >= 1.5:
        tanque_lavagem["emulsao"] = 1.5

    sleep(1)     

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

    try:
        server.bind((socket.gethostname(), 50009))
    except:
        print("Não consegui a conectar")

    server.listen()

    while 1:
        conexao, addr = server.accept()
        print(conexao)
        msg = conexao.recv(1024).decode()
        threading.Thread(target= client_handler, args=(conexao, msg)).start()    
            

if __name__ == "__main__":
    main()