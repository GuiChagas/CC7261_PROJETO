import socket
import threading
import random
import json
from time import sleep
 

#O TANQUE, VAI TER UMA EXECUÇÃO SOLO (LOGICA INTERNA) 
#A CADA SEGUNDO,O ORQUESTRADOR CHAMA ELE 
#E ELE RETORNA 1L DE SAÍDA REFENTE AO TOTAL
#RECEBE POR SEGUNDO 0.5L DE NaOH E 0.25L DE etOH

tanque_naetOH = {
    "naOH": 0.5, 
    "etOH": 0.25
}

def entrega_componentes():    

    while True:
        sleep(1)
        print("")
        print(f"Entrada de naOH: {tanque_naetOH['naOH']}")
        print(f"Entrada de etOH: {tanque_naetOH['etOH']}")


def client_handler(client):

    while 1:  
        jserialize = json.dumps(tanque_naetOH)
        sleep(1)        
        client.send(str.encode(jserialize))
        break

def main():
    threading.Thread(target= entrega_componentes, args=()).start()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

    try:
        server.bind((socket.gethostname(), 50003))
    except:
        print("Não consegui a conectar")

    server.listen()

    while 1:
        conexao, addr = server.accept()
        threading.Thread(target= client_handler, args=(conexao, )).start()    
            

if __name__ == "__main__":
    main()