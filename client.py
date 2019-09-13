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
    com = Enlace(serialName) # repare que o metodo construtor recebe um string (nome)
    # Ativa comunicacao
    com.enable()
    com.rx.clearBuffer()
#    time.sleep(1)
    
    f= open("Log\LogClient.txt","w+")
    
    servidor = Protocol.sever_number
    client = Protocol.client_number

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
    code = Protocol.type_package_delivery

    delivery, total = packer.pack(data, kind, code, client, get_total=True)
    
#    data, code, kind, total, server = unpacker.unpack(delivery[0], first=True)
    
    
    contador = 1
    code = Protocol.type_client_call
    back = packer.pack_message(code, contador, total, servidor, client)
    
    while code != Protocol.type_server_ready:
        f.write("Tipo de mensagem: {} - enviada: {} - destinatário: {}\n".format(code,time.ctime(time.time()),servidor))
        com.sendData(back)
        
        while(com.tx.getIsBussy()):
            pass
        
        rxBuffer = com.getData(Protocol.max_size, time.time())
                
        response, code, atual, client = unpacker.unpack(rxBuffer)
        data1, code1, kind1, total1, server1, client1 = unpacker.unpack(rxBuffer, first=True)
        f.write("Tipo de mensagem: {} - enviada: {} - remetente: {}\n".format(code,time.ctime(time.time()),server1))

    # Transmite dado
    print("-------------------------")
    print("Total de pacotes para envio : {}".format(total))
    print("Tipo de arquivo : {}".format(Protocol.from_kind[kind]))
    print("Código do envio : {}".format(code))
    print("-------------------------")

    count = 1
    timer1 = time.time()
    timer2 = time.time()
    
    while count <= total:        
        start = time.time()
        com.sendData(delivery[count-1])
        
        data, code, kind, total, server4, client = unpacker.unpack(delivery[count-1], first=True)
        f.write("Tipo de mensagem: {} - enviada: {} - destinatário: {}\n".format(code,time.ctime(time.time()),servidor))


        while(com.tx.getIsBussy()):
            pass
        
        data, code, atual, client = unpacker.unpack(delivery[count-1])

        print("-------------------------")
        print('Enviando {0} de {1}'.format(count,total))
        print("-------------------------")
        
        out = False
        time_out = False
        
        while not out:
            rxBuffer = com.getData(Protocol.max_size, time.time())
    
            response, code, atual, client = unpacker.unpack(rxBuffer)
            data2, code2, kind2, total2, server2, client2 = unpacker.unpack(rxBuffer, first=True)
            f.write("Tipo de mensagem: {} - enviada: {} - remetente: {}\n".format(code,time.ctime(time.time()),server2))
        
            if code == Protocol.type_package_ok:
                print("-------------------------")
                print("Pacote enviado com sucesso")
                print("-------------------------")
                count +=1
                out = True
                timer1 = time.time()
                timer2 = time.time()
                
            elif time.time() - timer2 > 20:
                out = True
                time_out = True
                
                code = Protocol.type_time_out
                back = packer.pack_message(code2, contador, total2, server2, client2)
                
                com.rx.clearBuffer()
                com.sendData(back)
                
                while(com.tx.getIsBussy()):
                    pass
           
            elif time.time() - timer1 > 5:            
                com.sendData(delivery[count-1])
    
                while(com.tx.getIsBussy()):
                    pass
                
                timer1 = time.time()
                
                data, code, atual, client = unpacker.unpack(delivery[count-1])
                
                print("timeout timer1")
                
            elif code == Protocol.type_error:
                    print("erro {} esperado {}".format(code, atual))
                    count = atual
                    out = True
                    timer1 = time.time()
                    timer2 = time.time()
            else:
                pass
            
        if time_out:
            break
            
#        elif code == Protocol.package_incorrect_order:
#            count = atual
#            print("-------------------------")
#            print("Erro {}".format(code))
#            print("Reenviando pacote")
#            print("-------------------------")
#        else:
#            print("-------------------------")
#            print("Erro {}".format(code))
#            print("Reenviando pacote")
#            print("-------------------------")
            
    if time_out:
        print("-------------------------")
        print("TIME OUT")
        print("Comunicação encerrada")
        print("-------------------------")
    
    else:
        final = time.time() - start
    
        # log
        print("-------------------------")
        print ("Taxa de transmissão {} (bytes/segundo) ".format(len(delivery)*128/final))
        print ("OverHead {}".format(len(delivery)*128/len(data)))
        print("-------------------------")
        
        com.rx.clearBuffer()
    
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
    
    f.close()
    
    # f = open("img_retorno.png","wb").write(rxBuffer)
    
    com.disable()

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
