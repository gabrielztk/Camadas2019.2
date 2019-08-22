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
            #print("EOP encontrado em {}".format(place))

            if place == Protocol.header_size + Protocol.data_size:

                size = package[0]

                data = package[12:Protocol.header_size + size]
                if package[6] not in Protocol.sucess:
                    code = Protocol.package_resend

                else:
                    code = Protocol.package_ok

            else:

                code = Protocol.package_eop_out_of_place

        else:

            code = Protocol.package_eop_not_found

        if first == True:
            kind = package[5]
            total = package[3:5]
            return data, code, kind, total
            
        else:
            atual = package[1:3]
            return data, code, atual

    def destuff(self, data):

        return self.stuffing.destuff(data)


