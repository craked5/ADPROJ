#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'grupo043'
__author__ = 'nunosilva 44285'
__author__ = 'andrepeniche 44312'

from hkvs_impl import HKVS
import os
import pickle as p
import os.path

class DurableHKVS:

    def __init__(self,max_count):
        self.cont = 0
        self.max_count = max_count
        try:
            self.f = open('/Users/nunosilva/Desktop/trabalhopython/dhkvs-log.txt', 'a')
        except IOError:
            print "Error opening the log file"

        #se existir of ficheiro dhkvs-ckpt-tmp.p e se sim recupera a hkvs-temp
        if os.path.isfile('/Users/nunosilva/Desktop/trabalhopython/dhkvs-ckpt-tmp.p') is True:
            self.hkvs = self.checkpointToHkvs('/Users/nunosilva/Desktop/trabalhopython/dhkvs-ckpt-tmp.p')
            self.f.truncate(0)
            os.rename('/Users/nunosilva/Desktop/trabalhopython/dhkvs-ckpt-tmp.p', '/Users/nunosilva/Desktop/trabalhopython/dhkvs-ckpt.p')
        #se nao existir dhkvs-ckpt-tmp.p
        elif os.path.isfile('/Users/nunosilva/Desktop/trabalhopython/dhkvs-ckpt-temp.p') is False:
            #ve se existe o dhkvs-ckpt.p e se sim recupera a hkvs e recupera o log file
            if os.path.isfile('/Users/nunosilva/Desktop/trabalhopython/dhkvs-ckpt.p') is True:
                self.hkvs = self.checkpointToHkvs('/Users/nunosilva/Desktop/trabalhopython/dhkvs-ckpt.p')
                self.logFileRecover()
            #se nao instancia uma hkvs nova e recupera o logfile
            else:
                self.hkvs = HKVS()
                self.logFileRecover()

        print self.hkvs.root
        print self.cont

    #ve se o contador de escrita do log esta igual ao maximo:
        #se sim chama o ckptCreation() para fazer reset e guardar tudo
        #se nao escreve uma linha para o log com a operacao certa
    def logMessage(self,comando):
        if self.cont == self.max_count:
            try:
                self.ckptCreation()
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

    #cria um checkpoint e faz reset ao logfile e ao contador de escrita do logfile
    def ckptCreation(self):
        check = open('/Users/nunosilva/Desktop/trabalhopython/dhkvs-ckpt-tmp.p', 'a')
        p.dump(self.hkvs,check,-1)
        check.flush()
        os.fsync(check.fileno())
        check.close()
        self.f.truncate(0)
        os.rename('/Users/nunosilva/Desktop/trabalhopython/dhkvs-ckpt-tmp.p', '/Users/nunosilva/Desktop/trabalhopython/dhkvs-ckpt.p')
        self.cont = 0

    #faz o recuperamento do log para a nova instancia do servidor
    def logFileRecover(self):
        lista_keywords = ['create','put','cas','remove','get','list']

        try:
            file_temp = open('/Users/nunosilva/Desktop/trabalhopython/dhkvs-log.txt', 'r')
        except IOError:
            print "Error opening the log file in function logFileRecover"

        #separa o texto em linhas
        lines = [line.rstrip('\n') for line in file_temp]

        #itera nas linhas e faz a operacao correspondente a primeira palavra em cada linha do ciclo
        #tambem incrementa o contador de linhas no log
        for l in lines:
            line_temp = l.split(' ')
            try:
                if line_temp[0] in lista_keywords:
                    if line_temp[0] == 'create':
                        self.hkvs.create(line_temp[1],line_temp[2])
                        self.cont += 1
                    elif line_temp[0] == 'put':
                        self.hkvs.put(line_temp[1],line_temp[2],line_temp[3])
                        self.cont += 1
                    elif line_temp[0] == 'cas':
                        self.hkvs.cas(line_temp[1],line_temp[2],line_temp[3],line_temp[4])
                        self.cont += 1
                    elif line_temp[0] == 'remove':
                        self.hkvs.remove(line_temp[1])
                        self.cont += 1
                    elif line_temp[0] == 'get':
                        self.hkvs.get(line_temp[1])
                        self.cont += 1
                    elif line_temp[0] == 'list':
                        self.hkvs.list(line_temp[1])
                        self.cont += 1
            except:
                print "erro ao ler linha " + str(l)

    def checkpointToHkvs(self, file):
        hkvs_temp = p.load(open(file, 'r'))
        return hkvs_temp