
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


# Serial Com Port
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports

#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM4"                  # Windows(variacao de)
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
    
    while(True):
        if com.rx.getIsEmpty():
            time.sleep(0.00001)
        else:

            sizeBuffer, nRx = com.getData(4)
            size = int.from_bytes(sizeBuffer, byteorder='big')


            rxBuffer, nRx = com.getData(size)

            com.sendData(sizeBuffer)
        
            # espera o fim da transmissão
            while(com.tx.getIsBussy()):
                pass
            
            f = open("recived_img.png","wb").write(rxBuffer)
            print(size)


    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()