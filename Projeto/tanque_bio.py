import socket
import threading
import json
from time import sleep
 

#O REATOR VAI RECEBER OS VALORES DE naOH, etOH
#A CADA SEGUNDO,O ORQUESTRADOR CHAMA ELE 
#E ELE RETORNA 0.75L DE SAÍDA REFENTE AO TOTAL
#PARA LOGICA DOS 10 SEC USAR SLEEP

tanque_bio = {
    "solucao_final": 0
}

def client_handler(client, msg):

    tanque_bio["solucao_final"] += float(msg)
    print("")
    print(f"Quantidade de Biodiesel produzido: {tanque_bio['solucao_final']}")

    client.send(str.encode(json.dumps(tanque_bio)))            

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

    try:
        server.bind((socket.gethostname(), 50010))
    except:
        print("Não consegui a conectar")

    server.listen()

    while 1:
        conexao, addr = server.accept()
        msg = conexao.recv(1024).decode()
        threading.Thread(target= client_handler, args=(conexao, msg)).start()    
            

if __name__ == "__main__":
    main()