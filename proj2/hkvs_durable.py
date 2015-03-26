#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'nunosilva 44285'
__author__ = 'andrepeniche 44312'

from hkvs_impl import HKVS
import sys as s
import time
import os

class DurableHKVS:

    def __init__(self):
        self.hkvs = HKVS()
        self.cont = 0
        self.f = open('dhkvs-log-atual.txt', 'w')

    def copy(self, Atual1, Destino1):
        atual = open(Atual1, 'r')
        destino = open(Destino1, 'w')
        reader = atual.read()
        destino.write(reader)
        atual.close()
        destino.close()

    def logMessage(self,type,conc):
        if self.cont > 100:
            self.copy('dhkvs-log-atual.txt', 'dhkvs-log-'+int(time.time())+'.txt')
            self.f = open('dhkvs-log-atual.txt', 'w')
            self.cont = 0
        else:
            self.f.write('Fez '+type+' e foi '+conc+'\n')
            self.f.flush()
            os.fsync(self.f.fileno())
            self.cont += 1


    def create(self, path, name):
        r = self.hkvs.create(path,name)
        self.logMessage('create',r)
        print self.f
        return r

    def put(self, path, name, value):
        r = self.hkvs.put(path,name,value)
        self.logMessage('put',r)
        return r

    def cas(self,path, name, cur_val, new_val):
        r = self.hkvs.put(path,name,cur_val,new_val)
        self.logMessage('cas',r)
        return r

    def remove(self, path):
        r = self.hkvs.remove(path)
        self.logMessage('remove',r)
        return r

    def get(self, path):
        return self.hkvs.get()

    def list(self, path):
        return self.hkvs.list()