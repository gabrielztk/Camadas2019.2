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
import time


# Serial Com Port
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports

#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM5"                  # Windows(variacao de)

def main():
    # Inicializa enlace ... variavel com possui todos os metodos e propriedades do enlace, que funciona em threading
    com = enlace(serialName) # repare que o metodo construtor recebe um string (nome)
    # Ativa comunicacao
    com.enable()
    
    packer = Packer()
    unpacker = Unpacker()

    file_num = 1

    # Log
    print("-------------------------")
    print("Comunicação inicializada")
    print("  porta : {}".format(com.fisica.name))
    print("-------------------------")
    
    while(True):


        if com.rx.getIsEmpty():
            time.sleep(0.01)

        else:

            dataRx, nRx = com.getData(Protocol.max_size)
            print(com.rx.getBufferLen())
            data, code, kind, total = unpacker.unpack(dataRx, first=True)
            print(com.rx.getBufferLen())
            total = int.from_bytes(total, byteorder=Protocol.byteorder)
            atual = 1
            print(com.rx.getBufferLen())

            if code not in Protocol.errors:
                print("-------------------------")
                print("Total de pacotes a receber : {}".format(total))
                print("Tipo de arquivo : {}".format(Protocol.from_kind[kind]))
                print("Código do envio : {}".format(code))
                print("-------------------------")

                recieved = data

                back = packer.pack(data, kind, code)
                com.sendData(back)
                while(com.tx.getIsBussy()):
                    pass

                while atual < total:
                    dataRx, nRx = com.getData(Protocol.max_size)
                    data, code, atual = unpacker.unpack(dataRx, first=False)
                    atual = int.from_bytes(atual, byteorder=Protocol.byteorder)

                    if code not in Protocol.errors:
                        print("-------------------------")
                        print("Pacote {} recebido".format(atual))
                        print("-------------------------")

                        recieved += data

                    else:

                        print("-------------------------")
                        print("Erro {}".format(code))
                        print("Aguardando reenvio")
                        print("-------------------------")

                        back = packer.pack(data, kind, code)
                        com.sendData(back)
                        while(com.tx.getIsBussy()):
                            pass

                print("-------------------------")
                print("Pacotes recebidos com sucesso")
                print("Salvando")
                print("-------------------------")
                
                to_save = unpacker.destuff(recieved)
                print(kind)
                print(Protocol.from_kind[kind])
                open("recieved{:02}".format(file_num) + Protocol.from_kind[kind],"wb").write(to_save)
                file_num += 1

                print("-------------------------")
                print("Aguardando novo envio")
                print("-------------------------")


            else:
                print("-------------------------")
                print("Erro {}".format(total))
                print("Aguardando reenvio")
                print("-------------------------")

                back = packer.pack(data, kind, code)
                com.sendData(back)
                while(com.tx.getIsBussy()):
                    pass

        

            


    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()