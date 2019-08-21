#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from protocol import *
from unpacker import *
from math import ceil

class Packer(object):

    def __init__(self):
        
        self.payload = []
        self.header = Header()
        self.eop = EOP()
        self.stuffing = Stuffing()


    def pack(self, data, kind, code):

        self.data = data
        self.kind = kind
        self.code = code

        self.stuff()

        self.total = ceil(len(self.data)/Protocol.data_size)
        

        self.header.updateKind(kind)
        self.header.updateCode(code)
        self.header.updateTotal(self.total)
        self.header.update()

        self.sort()

        back = self.payload
        self.payload = []

        return back


    def sort(self):

        count = 1
        nData = Protocol.data_size

        while(count <= self.total):
            
            if (len(self.data)<Protocol.data_size):
                nData = len(self.data)

            self.header.updateSize(nData)
            self.header.updateAtual(count)
            self.header.update()
            
            self.current = self.data[:nData] + (0).to_bytes((Protocol.data_size - nData), byteorder=Protocol.byteorder) 
            self.data = self.data[nData:]
            self.payload.append(self.header.body + self.current + self.eop.body)
            count += 1


    def stuff(self):

        self.data = self.stuffing.stuff(self.data)

