#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'nunosilva 44285'
__author__ = 'andrepeniche 44312'

from hkvs_impl import HKVS
import time as t
import os

class DurableHKVS:

    def __init__(self,max_count):
        self.path = '/Users/nunosilva/Desktop/dhkvs-log-atual.txt'
        self.hkvs = HKVS()
        self.cont = 0
        self.max_count = max_count
        try:
            self.f = open(self.path, 'a')
        except IOError:
            print "Error opening the file"

    def logMessage(self,comando):
        if self.cont == self.max_count:
            try:
                time_created = t.strftime('%H:%M:%S', t.gmtime())
                os.rename(self.path, '/Users/nunosilva/Desktop/dhkvs-log-'+ time_created +'.txt' )
                self.f = open(self.path, 'a')
                self.cont = 0
            except IOError:
                print "Error writing to file"
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
        temp = self.logMessage('create ' +path+ ' ' + name+ ' ' +r +'\n')
        if temp == True:
            return r
        else:
            print "Error saving to file"

    def put(self, path, name, value):
        r = self.hkvs.put(path,name,value)
        temp = self.logMessage('put ' + path + ' ' + name + ' ' + value + ' ' + r +'\n')
        if temp == True:
            return r
        else:
            print "Error saving to file"

    def cas(self,path, name, cur_val, new_val):
        r = self.hkvs.put(path,name,cur_val,new_val)
        temp = self.logMessage('cas ' + path + ' ' + name + ' ' + cur_val + ' ' + new_val + ' ' +r +'\n')
        if temp == True:
            return r
        else:
            print "Error saving to file"

    def remove(self, path):
        r = self.hkvs.remove(path)
        temp = self.logMessage('remove ' +path+ ' ' +r + '\n')
        if temp == True:
            return r
        else:
            print "Error saving to file"

    def get(self, path):
        return self.hkvs.get()

    def list(self, path):
        return self.hkvs.list()