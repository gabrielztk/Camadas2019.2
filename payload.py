#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from protocol import *
from math import ceil

class Payload(object):

    def __init__(self, name, kind, code):

        self.data = open(name + kind, "rb").read()
        self.data = self.data + EOP().body
        self.kind = Protocol.dic[kind]
        self.code = code
        self.payload = []
        self.total = ceil(len(self.data)/Protocol.data_size)
        self.header = Header(1, self.total, 1, self.kind, self.code)
        self.eop = EOP()

        self.stuff()
        self.sort()



    def sort(self):

        count = 1
        nData = Protocol.data_size

        while(count <= self.total):
            
            if (len(self.data)<Protocol.data_size):
                nData = len(self.data)

            self.header.size = nData
            self.header.atual = count
            self.header.update()
            
            self.current = self.data[0:nData]
            self.data = self.data[nData:]
            self.payload.append(self.header.body + self.current + self.eop.body)
            count += 1

    def pop(self):
        return self.payload.pop(0)

    def isEmpty(self):

        if len(self.payload) > 0:
            return False
        else:
            return True

    def stuff(self):
        if self.eop.body in self.data:
            print("oi")

ddd = Payload("client", ".py", Protocol.payload_delivery)



