#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#####################################################
# Camada Física da Computação
#Carareto
#17/02/2018
#  Aplicação 
####################################################

print("comecou")

from enlace import Enlace
from protocol import Protocol
from packer import Packer
from unpacker import Unpacker
from ports import serial_ports
import time
from functions import select_port


# Serial Com Port
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports




#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
#serialName = "COM4"                  # Windows(variacao de)


serialName = select_port()


def main():
    # Inicializa enlace ... variavel com possui todos os metodos e propriedades do enlace, que funciona em threading
    com = Enlace(serialName) # repare que o metodo construtor recebe um string (nome)
    # Ativa comunicacao
    com.enable()
    com.rx.clearBuffer()


    my_server = Protocol.sever_number
    
    packer = Packer()
    unpacker = Unpacker()

    file_num = 1
    try_num = 1

    # Log
    print("-------------------------")
    print("Comunicação inicializada")
    print("  porta : {}".format(com.fisica.name))
    print("-------------------------")
    
    ocioso = True
    serverReady_message_sent = False
    count = 1

    while(True):

        # Server está ocioso
        if ocioso:
            dataRx = com.getData(Protocol.max_size, time.time())
            data, code, kind, total, server, client = unpacker.unpack(dataRx, first=True)
            client_number = client

            # Server checa se o código e número de server da mensagem estão certos
            if code == Protocol.type_client_call and server == my_server:
                # Log do server é inicializado
                log = open("log/fille{:02}log_try{:02}.txt".format(file_num, try_num),"w+")
                # Server deixa de estar ocioso
                ocioso = False
                print("-------------------------")
                print("Server chamado pelo client")
                print("-------------------------")
                log.write("Msg: {} – recebida: {} – remetente: {}\n".format(code, time.ctime(time.time()), client_number))

        # Server não está mais ociono mas ainda não mandou uma mensagem com Código 2   
        elif serverReady_message_sent == False:
            
            message = packer.pack_message(Protocol.type_server_ready, total, total, my_server, client_number)
            com.sendData(message)
            while(com.tx.getIsBussy()):
                pass
            
            serverReady_message_sent = True
            log.write("Msg: {} – enviada: {} – destinatário: {}\n".format(Protocol.type_server_ready, time.ctime(time.time()), client_number))

            print("-------------------------")
            print("Total de pacotes a receber : {}".format(total))
            print("Tipo de arquivo : {}".format(Protocol.from_kind[kind]))
            print("-------------------------")

            # Variáveis são iniciadas aqui para que não sejam mudadas indevidamente no loop de envio
            recieved = bytes()
            start = time.time()
            time_out_time = time.time()

        # Server recebe os pacotes e checa seus conteúdos
        else:

            # Enquanto todos os pacotes ainda não foram recebido, é checado se ainda não ocorreu um timeout
            if count <= total and (time.time() - time_out_time) < Protocol.great_timeout:
                dataRx = com.getData(Protocol.max_size, time.time())
                data, code, atual, client = unpacker.unpack(dataRx)

                print("-------------------------")
                print("Pacote aberto")
                print("Contador {} e atual {} e código {}".format(count, atual, code))
                print("-------------------------")

                log.write("Msg: {} – recebida: {} – remetente: {}\n".format(code, time.ctime(time.time()), client_number))

                # Se o pacote recebido conter o código certo e seu número bater com o esperado,
                # seu conteúdo é adicionado e uma mensagem de confirmação é enviada
                if code == Protocol.type_package_delivery and atual == count and client == client_number:
                    
                    print("-------------------------")
                    print("Pacote {} de {} recebido".format(atual, total))
                    print("-------------------------")

                    recieved += data
                    message = packer.pack_message(Protocol.type_package_ok, count, total, Protocol.sever_number, client_number)
                    com.sendData(message)
                    while(com.tx.getIsBussy()):
                        pass

                    count += 1
                    time_out_time = time.time()
                    log.write("Msg: {} – enviada: {} – destinatário: {}\n".format(Protocol.type_package_ok, time.ctime(time.time()), client_number))

                # Se o pacote recebido não conter o código certo eou seu número não bater com o esperado,
                # seu conteúdo é ignorado e uma mensage de erro com o pacote esperado é enviada
                else:
                    print("-------------------------")
                    print("Erro")
                    print("Aguardando reenvio")
                    print("-------------------------")

                    message = packer.pack_message(Protocol.type_error, count, total, Protocol.sever_number, client_number)
                    com.sendData(message)
                    while(com.tx.getIsBussy()):
                        pass

                    log.write("Msg: {} – enviada: {} – destinatário: {}\n".format(Protocol.type_error, time.ctime(time.time()), client_number))
                    
            # Quando todos os pacotes forem recebidos o stuffing, se houver, é removido e o arquivo salvo
            # O server volta para seu estado ocioso
            elif count > total:
                end = time.time() - start

                print("-------------------------")
                print("Pacotes recebidos com sucesso")
                print("Taxa de recepção: {:02}".format(total*Protocol.max_size/end))
                print("Salvando")
                print("-------------------------")
                
                to_save = unpacker.destuff(recieved)
                open("recieved/recieved{:02}".format(file_num) + Protocol.from_kind[kind],"wb").write(to_save)
                log.write("Salvo em: {}\n".format(time.ctime(time.time())))
                log.close()
                file_num += 1

                print("-------------------------")
                print("Aguardando novo envio")
                print("-------------------------")

                ocioso = True
                serverReady_message_sent = False
                com.rx.clearBuffer()
                count = 1
                try_num = 1

            # Se mais tempo que o estipulado para um timeout passou, o server volta para seu estado ocioso
            else:
                print("-------------------------")
                print("Timeout")
                print("Aguardando novo envio")
                print("-------------------------")
                message = packer.pack_message(Protocol.type_time_out, count, total, my_server, client_number)
                com.sendData(message)
                while(com.tx.getIsBussy()):
                    pass
                
                ocioso = True
                serverReady_message_sent = False
                count = 1
                log.write("Msg: {} – enviada: {} – destinatário: {}\n".format(Protocol.type_time_out, time.ctime(time.time()), client_number))
                log.close()


#so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()