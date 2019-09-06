#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#####################################################
# Camada Física da Computação
#Carareto
#17/02/2018
#  Aplicação 
####################################################

print("comecou")

from enlace import *
from protocol import *
from packer import *
from unpacker import *
from ports import *
import time
from functions import *


# Serial Com Port
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports




#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
#serialName = "COM4"                  # Windows(variacao de)

serialName = select_port()


def main():
    # Inicializa enlace ... variavel com possui todos os metodos e propriedades do enlace, que funciona em threading
    
    # Ativa comunicacao
    
    packer = Packer()
    unpacker = Unpacker()

    # Log
    
    
    run = True
    call = True
    serverReady_message_get = False
    count = 1

    while(run):

        if call:

            selected = select_file()

            print("-------------------------")
            print("Gerando dados para transmissao :")
            print("-------------------------")

            data = open(selected,"rb").read()
            delivery, total = packer.pack(data, get_kind(selected), Protocol.type_package_delivery, get_total=True)

            com = enlace(serialName) 
            com.enable()
            com.rx.clearBuffer()

            print("-------------------------")
            print("Chamando o server para tranferência de dados")
            print("-------------------------")

            message = packer.pack_message(Protocol.type_client_call, total, total, Protocol.sever_number)
            com.sendData(message)
            while(com.tx.getIsBussy()):
                pass

            call = False
            message_timeot = time.time()
            
            
        
        elif serverReady_message_get == False and (time.time() - message_timeot) < Protocol.great_timeout:
            
            dataRx = com.getData(Protocol.max_size, time.time())
            data, code, atual = unpacker.unpack(dataRx)

            if code == Protocol.type_server_ready:
                serverReady_message_get = True

                print("-------------------------")
                print("Server pronto, começando o envio")
                print("-------------------------")

                start = time.time()
                time_out_time = time.time()
                count = 1

        elif not call and serverReady_message_get == True:
            

            if count <= total and (time.time() - time_out_time) < Protocol.great_timeout:

                print("-------------------------")
                print("Envindo pacote {} de {}".format(count, total))
                print("-------------------------")
                com.sendData(delivery[count-1])
                while(com.tx.getIsBussy()):
                    pass
                
                dataRx = com.getData(Protocol.max_size, time.time())
                data, code, atual = unpacker.unpack(dataRx)

                if code == Protocol.type_package_ok and atual == count:
                    print("-------------------------")
                    print("Pacote {} de {} enviado com sucesso".format(count, total))
                    print("-------------------------")
                    count += 1
                    time_out_time = time.time()

                else:
                    print("-------------------------")
                    print("Erro")
                    print("-------------------------")

                    if 1 <= atual <= total:
                        count = atual
                    

            elif count > total:
                end = time.time() - start

                print("-------------------------")
                print("Pacotes enviados com sucesso")
                print("Taxa de recepção: {:02}".format(total*Protocol.max_size/end))
                print("-------------------------")

                print("-------------------------")
                go_on = input("Se desejar um novo envio digite sim, caso contrário outro caractere: ")
                print("-------------------------")

                call = True
                serverReady_message_get = False
                count = 1

                if go_on != "sim":
                    print("-------------------------")
                    print("Até mais!")
                    print("-------------------------")
                run = False
                

            else:
                print("-------------------------")
                print("O server não respondeu e um timeout ocorreu")
                print("-------------------------")
                com.disable()

                print("-------------------------")
                go_on = input("Se desejar um novo envio digite sim, caso contrário outro caractere: ")
                print("-------------------------")

                call = True
                serverReady_message_get = False
                count = 1

                if go_on != "sim":
                    print("-------------------------")
                    print("Até mais!")
                    print("-------------------------")
                    run = False


        else:
            print("-------------------------")
            print("O server não respondeu e um timeout ocorreu")
            print("-------------------------")
            com.disable()

            print("-------------------------")
            go_on = input("Se desejar um novo envio digite sim, caso contrário outro caractere: ")
            print("-------------------------")

            call = True
            serverReady_message_get = False
            count = 1

            if go_on != "sim":
                print("-------------------------")
                print("Até mais!")
                print("-------------------------")
                run = False
            


#so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()