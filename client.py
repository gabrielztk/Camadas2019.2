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
import os

path = os.getcwd()
entries = os.listdir(path)

i = 1
print('Arquivos no diretório:')

for entry in entries:
    print('{0} - {1}'.format(i,entry))
    i+=1
    
a = int(input('Selecione o número do arquivo que voce deseja enviar: '))
selected = entries[a-1]

print('\nArquivo selecionado: {0}\n'.format(selected))

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
    time.sleep(1)

    packer = Packer()
    unpacker = Unpacker()

    # Log
    print("-------------------------")
    print("Comunicação inicializada")
    print("  porta : {}".format(com.fisica.name))
    print("-------------------------")

    # Carrega dados
    print ("Gerando dados para transmissao :")

    data = open(selected,"rb").read()
    
    type_file = '.'+selected.split('.')[-1]
    kind = Protocol.to_kind[type_file]
    code = Protocol.package_delivery

    delivery = packer.pack(data, kind, code)
    
    data, code, kind, total = unpacker.unpack(delivery[0], first=True)

    total = int.from_bytes(total, byteorder = Protocol.byteorder)

    # Transmite dado
    print("-------------------------")
    print("Total de pacotes para envio : {}".format(total))
    print("Tipo de arquivo : {}".format(Protocol.from_kind[kind]))
    print("Código do envio : {}".format(code))
    print("-------------------------")

    start = time.time()
    count = 1
    while count <= total:
        com.sendData(delivery[count-1])

        while(com.tx.getIsBussy()):
            pass

        print("-------------------------")
        print('Enviando {0} de {1}'.format(count,total))
        print("-------------------------")
    
        rxBuffer = com.getData(Protocol.max_size, time.time())

        response, code, atual = unpacker.unpack(rxBuffer)

        if code in Protocol.sucess:
            print("-------------------------")
            print("Pacote enviado com sucesso")
            print("-------------------------")
            count +=1
        elif code == Protocol.package_incorrect_order:
            count = atual
            print("-------------------------")
            print("Erro {}".format(code))
            print("Reenviando pacote")
            print("-------------------------")
        else:
            print("-------------------------")
            print("Erro {}".format(code))
            print("Reenviando pacote")
            print("-------------------------")
    
    final = time.time() - start

    # log
    print("-------------------------")
    print ("Taxa de transmissão {} (bytes/segundo) ".format(len(delivery)*128/final))
    print ("OverHead {}".format(len(delivery)*128/len(data)))
    print("-------------------------")

    print("-------------------------")
    print("Comunicação encerrada")
    print("-------------------------")
    
    # f = open("img_retorno.png","wb").write(rxBuffer)
    
    com.disable()

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
