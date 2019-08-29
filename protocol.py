#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#pra_bytes = (50).to_bytes(4, byteorder=byteorder)
#de_bytes = int.from_bytes(bytes, byteorder=byteorder)


class Header(object):

    def __init__(self):

        # Tamanho do Payload
        self.size = (0).to_bytes(Protocol.size_size, byteorder=Protocol.byteorder)
        # Payload atual
        self.atual = (0).to_bytes(Protocol.atual_size, byteorder=Protocol.byteorder)
        # Numero total de payloads
        self.total = (0).to_bytes(Protocol.total_size, byteorder=Protocol.byteorder)
        # Tipo do arquivo
        self.kind = (0).to_bytes(Protocol.kind_size, byteorder=Protocol.byteorder)
        # Tipo de arquivo do payload
        self.code = (0).to_bytes(Protocol.code_size, byteorder=Protocol.byteorder)
        # Bytes livres
        self.free = (0).to_bytes(5, byteorder=Protocol.byteorder)
        # Concatendo os bytes na ordem desejada
        self.body = self.size + self.atual + self.total + self.kind + self.code + self.free
        # Tamanho do header
        self.length = len(self.body)

    def update(self):
        self.body = self.size + self.atual + self.total + self.kind + self.code + self.free

    def updateSize(self, size):
        self.size = (size).to_bytes(Protocol.size_size, byteorder=Protocol.byteorder)

    def updateAtual(self, atual):
        self.atual = (atual).to_bytes(Protocol.atual_size, byteorder=Protocol.byteorder)

    def updateTotal(self, total):
        self.total = (total).to_bytes(Protocol.total_size, byteorder=Protocol.byteorder)

    def updateKind(self, kind):
        self.kind = (kind).to_bytes(Protocol.kind_size, byteorder=Protocol.byteorder)

    def updateCode(self, code):
        self.code = (code).to_bytes(Protocol.code_size, byteorder=Protocol.byteorder)


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
        # Tamanho do EOP
        self.length = len(self.body)

class StuffedEOP(object):

    def __init__(self):

        # \xa0
        self.n1 = (160).to_bytes(1, byteorder=Protocol.byteorder)
        # \xb1
        self.n2 = (177).to_bytes(1, byteorder=Protocol.byteorder)
        # \xc2
        self.n3 = (194).to_bytes(1, byteorder=Protocol.byteorder)
        # \xd3
        self.n4 = (211).to_bytes(1, byteorder=Protocol.byteorder)
        # Stuffing
        self.stuff = (0).to_bytes(1, byteorder=Protocol.byteorder)
        # Concatendo os bytes na ordem desejada
        self.body = self.stuff + self.n1 + self.stuff + self.n2 + self.stuff + self.n3 + self.stuff + self.n4
        # Tamanho
        self.length = len(self.body)

class Stuffing(object):

    def __init__(self):

        self.eop = EOP().body
        self.stuffeop = StuffedEOP().body

    def stuff(self, data):

        self.data = data

        while(self.eop in self.data):

            place = self.data.index(self.eop)
            p1 = self.data[:place] + bytes([0x00])
            p2 = self.data[place:place+1] + bytes([0x00])
            p3 = self.data[place+1:place+2] + bytes([0x00])
            p4 = self.data[place+2:place+3] + bytes([0x00])
            p5 = self.data[place+3:]

            self.data = p1 + p2 + p3 + p4 + p5

        return self.data

    def destuff(self, data):

        self.data = data

        while(self.stuffeop in self.data):

            place = self.data.index(self.stuffeop)
            p1 = self.data[:place]
            p2 = self.data[place+1:place+2]
            p3 = self.data[place+4:place+5]
            p4 = self.data[place+6:place+7]
            p5 = self.data[place+8:]

            self.data = p1 + p2 + p3 + p4 + p5

        return self.data


class Protocol(object):

    # Ordem de leitura dos bytes para conversão
    byteorder = "big"

    # Tamanho, em bytes dos componentes do header
    size_size = 1
    atual_size = 2
    total_size = 2
    kind_size = 1
    code_size = 1
    # Tamnho total do Header e do EOP

    header_size = 12
    eop_size = 4

    # Tamanho máximo de dados por payload
    max_size = 128
    data_size = max_size - (header_size + eop_size)

    # Códigos de identificação dos payloads
    package_delivery = 25
    package_ok = 55
    package_eop_out_of_place = 160
    package_eop_not_found = 220
    package_resend = 255
    package_incorrect_order = 245
    package_timeout = 100

    # Lista com códigos de erro
    errors = [package_eop_out_of_place, package_eop_not_found, package_timeout, package_incorrect_order]
    sucess = [package_delivery, package_ok]

    # Códigos do tipo de arquivo dos payloads
    py = 1
    jpg = 2
    png = 3

    # Dicionário com os tipos
    to_kind = {".py":py, ".jpg":jpg, ".png":png}
    from_kind = {py:".py", jpg:".jpg", png:".png"}

    # Pacote vazio
    empty_package = (0).to_bytes(data_size, byteorder=byteorder)

    # Time-out
    timeout = 2.5

