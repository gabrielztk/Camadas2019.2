#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#pra_bytes = (50).to_bytes(4, byteorder=byteorder)
#de_bytes = int.from_bytes(bytes, byteorder=byteorder)

class Header(object):

    def __init__(self, atual, total, size, kind, code):

        # Tamnho do Payload
        self.size = (size).to_bytes(Protocol.size_size, byteorder=Protocol.byteorder)
        # Payload atual
        self.atual = (atual).to_bytes(Protocol.atual_size, byteorder=Protocol.byteorder)
        # Numero total de payloads
        self.total = (total).to_bytes(Protocol.total_size, byteorder=Protocol.byteorder)
        # Tamnho do Payload
        self.kind = (kind).to_bytes(Protocol.kind_size, byteorder=Protocol.byteorder)
        # Tipo de arquivo do payload
        self.code = (total).to_bytes(Protocol.code_size, byteorder=Protocol.byteorder)
        # Bytes livres
        self.free = (0).to_bytes(5, byteorder=Protocol.byteorder)
        # Concatendo os bytes na ordem desejada
        self.body = self.size + self.atual + self.total + self.kind + self.code + self.free
        # Tamanho do header
        self.h_size = len(self.body)

    def update(self):
        self.body = self.size + self.atual + self.total + self.kind + self.code + self.free

class EOP(object):

    def __init__(self):

        # \xa0
        self.n1 = (160).to_bytes(1, byteorder=Protocol.byteorder)
        # \xb1
        self.n2 = (177).to_bytes(1, byteorder=Protocol.byteorder)
        # \xc2
        self.n3 = (194).to_bytes(1, byteorder=Protocol.byteorder)
        # \xd3
        self.n4 = (211).to_bytes(1, byteorder=Protocol.byteorder)
        # Concatendo os bytes na ordem desejada
        self.body = self.n1 + self.n2 + self.n3 + self.n4



class Protocol(object):

    # Ordem de leitura dos bytes para conversão
    byteorder = "big"

    # Tamanho, em bytes dos componentes do header
    code_size = 1
    size_size = 1
    total_size = 2
    atual_size = 2
    kind_size = 1

    # Tamanho máximo de dados por payload
    data_size = 112
    max_size = 128

    # Códigos de identificação dos payloads
    payload_delivery = 1
    payload_error = 2
    payload_ok = 3

    # Códigos do tipo de arquivo dos payloads
    py = 1
    jpeg = 2

    # Dicionário com os tipos

    dic = {".py":py, ".jpeg":jpeg}
