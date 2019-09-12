#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from ports import serial_ports
from protocol import Protocol
def select_file():
    import os
    path = os.getcwd()
    entries = os.listdir(path)

    i = 1
    print('Arquivos no diretório:')

    for entry in entries:
        print('{0} - {1}'.format(i,entry))
        i+=1
        
    a = int(input('Selecione o número do arquivo que voce deseja enviar: '))
    if 1 <= a <= len(entries):
        selected = entries[a-1]
    else:
        selected = False

    print('\nArquivo selecionado: {0}\n'.format(selected))
    return selected

def select_port():
    i = 1
    print('Selecione uma porta para a comunicação')
    ports = serial_ports()

    for port in ports:
        print('{0} - {1}'.format(i,port))
        i+=1

    p = int(input('Selecione o número da porta que deseja usar: '))
    return ports[p-1]

def get_kind(file_name):
        type_file = '.'+file_name.split('.')[-1]
        return Protocol.to_kind[type_file]