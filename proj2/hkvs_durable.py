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
        try:
            self.f = open('dhkvs-log-atual.txt', 'a')
        except:
            IOError
        print self.f.mode
        print self.f.name

    def copy(self, atual_arg, destino_arg):
        atual = open(atual_arg, 'r')
        destino = open(destino_arg, 'w')
        reader = atual.read()
        destino.write(reader)
        atual.close()
        destino.close()

    def logMessage(self,comando):
        if self.cont > 100:
            try:
                self.copy('dhkvs-log-atual.txt', 'dhkvs-log-'+int(time.time())+'.txt')
                self.f = open('dhkvs-log-atual.txt', 'a')
                self.cont = 0
            except IOError:
                print "nao foi possivel guardar o ficheiro"
        try:
            self.f.write(comando)
            self.f.flush()
            os.fsync(self.f.fileno())
            self.cont += 1
        except IOError:
            return False
        return True

    def create(self, path, name):
        r = self.hkvs.create(path,name)
        self.logMessage('create em ' +path+ r +'\n')

        print self.f
        print self.cont
        return r

    def put(self, path, name, value):
        r = self.hkvs.put(path,name,value)
        self.logMessage('put ' + path + ' ' + name + ' ' + value + r +'\n')
        return r

    def cas(self,path, name, cur_val, new_val):
        r = self.hkvs.put(path,name,cur_val,new_val)
        self.logMessage('cas ' + path + ' ' + name + ' ' + cur_val + ' ' + new_val + r +'\n')
        return r

    def remove(self, path):
        r = self.hkvs.remove(path)
        self.logMessage('remove em ' +path+ r + '\n')
        return r

    def get(self, path):
        return self.hkvs.get()

    def list(self, path):
        return self.hkvs.list()