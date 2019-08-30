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


# Serial Com Port
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports




#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
#serialName = "COM4"                  # Windows(variacao de)

i = 1
print('Selecione uma porta para a comunicação')
ports = serial_ports()

for port in ports:
    print('{0} - {1}'.format(i,port))
    i+=1

p = int(input('Selecione o número da porta que deseja usar: '))
serialName = ports[p-1]


def main():
    # Inicializa enlace ... variavel com possui todos os metodos e propriedades do enlace, que funciona em threading
    com = enlace(serialName) # repare que o metodo construtor recebe um string (nome)
    # Ativa comunicacao
    com.enable()
    com.rx.clearBuffer()
    time.sleep(1)

    my_server = Protocol.sever_number
    
    packer = Packer()
    unpacker = Unpacker()

    file_num = 1

    # Log
    print("-------------------------")
    print("Comunicação inicializada")
    print("  porta : {}".format(com.fisica.name))
    print("-------------------------")
    
    ocioso = True
    serverReady_message_sent = False
    count = 1

    while(True):

        if ocioso:
            dataRx = com.getData(Protocol.max_size, time.time())
            data, code, kind, total, server = unpacker.unpack(dataRx, first=True)
            if code == Protocol.type_client_call and server == my_server:
                ocioso = False
            time.sleep(1)
        
        elif serverReady_message_sent == False:
            message = packer.pack_message(Protocol.type_server_ready, total, total, my_server)
            com.sendData(message)
            while(com.tx.getIsBussy()):
                pass
            serverReady_message_sent = True

            print("-------------------------")
            print("Total de pacotes a receber : {}".format(total))
            print("Tipo de arquivo : {}".format(Protocol.from_kind[kind]))
            print("-------------------------")

            recieved = bytes()
            start = time.time()
            time_out_time = time.time()

        else:
            if count <= total and (time.time() - time_out_time) < Protocol.great_timeout:

                dataRx = com.getData(Protocol.max_size, time.time())
                data, code, atual = unpacker.unpack(dataRx)

                if code == Protocol.type_package_delivery and atual == count:
                    print("-------------------------")
                    print("Pacote {} de {} recebido".format(atual, total))
                    print("-------------------------")

                    recieved += data
                    message = packer.pack_message(Protocol.type_package_ok, count, total, my_server)
                    com.sendData(message)
                    while(com.tx.getIsBussy()):
                        pass
                    count += 1

                else:
                    print("-------------------------")
                    print("Erro")
                    print("Aguardando reenvio")
                    print("-------------------------")

                    message = packer.pack_message(Protocol.type_error, count, total, my_server)
                    com.sendData(message)
                    while(com.tx.getIsBussy()):
                        pass

            elif count > total:
                end = time.time() - start

                print("-------------------------")
                print("Pacotes recebidos com sucesso")
                print("Taxa de recepção: {:02}".format(total*Protocol.max_size/end))
                print("Salvando")
                print("-------------------------")
                
                to_save = unpacker.destuff(recieved)
                open("recieved/recieved{:02}".format(file_num) + Protocol.from_kind[kind],"wb").write(to_save)
                file_num += 1

                print("-------------------------")
                print("Aguardando novo envio")
                print("-------------------------")

                ocioso = True
                serverReady_message_sent = False
                count = 1

            else:
                print("-------------------------")
                print("Timeout")
                print("Aguardando novo envio")
                print("-------------------------")
                message = packer.pack_message(Protocol.type_time_out, count, total, my_server)
                com.sendData(message)
                while(com.tx.getIsBussy()):
                    pass

                ocioso = True
                serverReady_message_sent = False
                count = 1


    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()