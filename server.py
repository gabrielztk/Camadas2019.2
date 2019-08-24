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

            start = time.time()
            dataRx = com.getData(Protocol.max_size, time.time())
            data, code, kind, total = unpacker.unpack(dataRx, first=True)
            total = int.from_bytes(total, byteorder=Protocol.byteorder)
            atual = 1
            count = 2

            if code in Protocol.sucess:
                print("-------------------------")
                print("Total de pacotes a receber : {}".format(total))
                print("Tipo de arquivo : {}".format(Protocol.from_kind[kind]))
                print("Código do envio : {}".format(code))
                print("Pacote {} recebido".format(atual))
                print("-------------------------")

                recieved = data
                back = packer.pack_return(code, atual)
                com.sendData(back)
                while(com.tx.getIsBussy()):
                    pass

                while atual < total:
                    dataRx = com.getData(Protocol.max_size, time.time())
                    data, code, atual = unpacker.unpack(dataRx)
                    atual = int.from_bytes(atual, byteorder=Protocol.byteorder)

                    if atual != count:
                        code = Protocol.package_incorrect_order



                    if code in Protocol.sucess:
                        print("-------------------------")
                        print("Pacote {} de {} recebido".format(atual, total))
                        print("-------------------------")

                        recieved += data
                        count += 1
                        

                    else:
                        print("-------------------------")
                        print("Erro {}".format(code))
                        print("Aguardando reenvio")
                        print("-------------------------")


                    back = packer.pack_return(code, atual)
                    com.sendData(back)
                    while(com.tx.getIsBussy()):
                        pass

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


            else:
                print("-------------------------")
                print("Erro {}".format(code))
                print("Aguardando reenvio")
                print("-------------------------")

                back = packer.pack_return(code, atual)
                com.sendData(back)
                while(com.tx.getIsBussy()):
                    pass

        

            


    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()