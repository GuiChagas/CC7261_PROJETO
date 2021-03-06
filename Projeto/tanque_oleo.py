import socket
import threading
import random
from time import sleep
 

#O TANQUE, VAI TER UMA EXECUÇÃO SOLO (LOGICA INTERNA) 
#A CADA SEGUNDO,O ORQUESTRADOR CHAMA ELE 
#E ELE RETORNA 0.75L DE SAÍDA REFENTE AO TOTAL
#PARA LOGICA DOS 10 SEC USAR SLEEP

tanque_oleo = {
    "Armazenamento": 0.00
}

value_tanque = 0.00

def entrega_oleo():    
    global value_tanque

    while True:
        tanque_oleo["Armazenamento"] += random.uniform(1, 2)
        print(f"Valor total de armazenamento do tanque de óleo: {tanque_oleo['Armazenamento']}")
        sleep(10)


def client_handler(client):

    while 1:
        valor_vazao = 0.75
        
        
        if tanque_oleo["Armazenamento"] >= valor_vazao:
            tanque_oleo["Armazenamento"] -= valor_vazao
            sleep(1)
            client.send((str(valor_vazao)).encode())
            
        elif (tanque_oleo["Armazenamento"] < valor_vazao) and tanque_oleo["Armazenamento"] > 0:
            sleep(1)
            client.send((str(tanque_oleo["Armazenamento"])).encode())
            tanque_oleo["Armazenamento"] -= tanque_oleo["Armazenamento"]
        
        else:
            client.send(str(tanque_oleo["Armazenamento"]).encode())
        break

def main():
    threading.Thread(target= entrega_oleo, args=()).start()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 


    try:
        server.bind((socket.gethostname(), 50002))
    except:
        print("Não consegui a conectar")

    server.listen()

    while 1:
        conexao, addr = server.accept()
        threading.Thread(target= client_handler, args=(conexao, )).start()    
            

if __name__ == "__main__":
    main()