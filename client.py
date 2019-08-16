
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
import time
import os

path = "C:/Users/Samuel Porto/Desktop/Semestres/4° Semestre/CamadaFisica"

entries = os.listdir(path)

i = 1

print('Arquivos no diretório:')

for entry in entries:
    print('{0} - {1}'.format(i,entry))
    i+=1
    
a = int(input('Selecione o número do arquivo que voce deseja enviar: '))

selected = entries[a-1]

print('\nArquivo selecionado: {0}\n'.format(selected))

serialName = "COM12"
print("abriu com")

def main():
    # Inicializa enlace ... variavel com possui todos os metodos e propriedades do enlace, que funciona em threading
    com = enlace(serialName) # repare que o metodo construtor recebe um string (nome)
    # Ativa comunicacao
    com.enable()

    # Log
    print("-------------------------")
    print("Comunicação inicializada")
    print("  porta : {}".format(com.fisica.name))
    print("-------------------------")

    # Carrega dados
    print ("gerando dados para transmissao :")

    img = open(selected,"rb").read()
    
    img_len = len(img)
    
    txBuffer = (img_len).to_bytes(4, byteorder='big') + img
    
    txLen = len(txBuffer)

    # Transmite dado
    print("tentado transmitir .... {} bytes".format(txLen))
    
    start = time.time()
    
    com.sendData(txBuffer)

    while(com.tx.getIsBussy()):
        pass

    txSize = com.tx.getStatus()
 
    rxBuffer, nRx = com.getData(4)
    
    final = time.time() - start

    # log
    print ("Lido              {} bytes ".format(nRx))
    print ("Performance              {} bytes/segundo ".format(int.from_bytes(rxBuffer, byteorder='big')/final))
    
    print (rxBuffer)

    print(int.from_bytes(rxBuffer,'big'))

    # Encerra comunicação
    print("-------------------------")
    print("Comunicação encerrada")
    print("-------------------------")
    
    f = open("img_retorno.png","wb").write(rxBuffer)
    
    com.disable()

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
