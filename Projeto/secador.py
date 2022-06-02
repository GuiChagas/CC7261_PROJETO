import socket
import threading
import random
import json
from time import sleep
 

#O REATOR VAI RECEBER OS VALORES DE naOH, etOH
#A CADA SEGUNDO,O ORQUESTRADOR CHAMA ELE 
#E ELE RETORNA 0.75L DE SAÍDA REFENTE AO TOTAL
#PARA LOGICA DOS 10 SEC USAR SLEEP

secador = {
    "solucao_secador": 0,
    "perda_produto": 0
}

def client_handler(client, msg):

    print(f"Entrada no secador: {msg}")

    secador["solucao_secador"] = float(msg) * 0.995
    secador["perda_produto"] = float(msg) * 0.005

    print(f"Saída do secador: {secador['solucao_secador']}")
    print(f"Perda de produto do secador: {secador['perda_produto']}")

    sleep(5 * secador["solucao_secador"])    

    client.send(str.encode(json.dumps(secador)))        

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

    try:
        server.bind((socket.gethostname(), 50006))
    except:
        print("Não consegui a conectar")

    server.listen()

    while 1:
        conexao, addr = server.accept()
        msg = conexao.recv(1024).decode()
        threading.Thread(target= client_handler, args=(conexao, msg)).start()    
            

if __name__ == "__main__":
    main()