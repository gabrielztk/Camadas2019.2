#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from protocol import *

class Unpacker(object):

    def __init__(self):

        self.eop = EOP()
        self.stuffing = Stuffing()

    def unpack(self, package, first=False):

        data = bytearray()

        if self.eop.body in package:

            place = package.index(self.eop.body)

            if place == Protocol.header_size + Protocol.data_size:

                size = package[0]
                data = package[12:Protocol.header_size + size]
                code = package[6]

            else:
                code = Protocol.type_error

        else:

            code = Protocol.type_error

        if first == True:
            total = package[3:5]
            kind = package[5]
            server = package[7]
            return data, code, kind, total, server
            
        else:
            atual = package[1:3]
            return data, code, atual

    def destuff(self, data):

        return self.stuffing.destuff(data)


