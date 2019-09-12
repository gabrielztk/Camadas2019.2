#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from protocol import *

class Unpacker(object):

    def __init__(self):

        self.eop = EOP()
        self.stuffing = Stuffing()

    def unpack(self, package, first=False):

        data = Protocol.empty_package

        if self.eop.body in package:

            place = package.index(self.eop.body)

            if place == Protocol.header_size + Protocol.data_size:

                size = package[0]
                code = package[6]
                if code != Protocol.type_error:
                    data = package[12:Protocol.header_size + size]

            else:
                code = Protocol.type_error
                

        else:
            code = Protocol.type_error

        if first == True:
            total = int.from_bytes(package[3:5], byteorder=Protocol.byteorder)
            kind = package[5]

            server = package[7]
            client = package[8]

            return data, code, kind, total, server, client
            
        else:
            client = package[8]
            atual = int.from_bytes(package[1:3], byteorder=Protocol.byteorder)
            return data, code, atual, client

    def destuff(self, data):

        return self.stuffing.destuff(data)


