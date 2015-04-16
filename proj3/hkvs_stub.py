#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'grupo043'
__author__ = 'nunosilva 44285'
__author__ = 'andrepeniche 44312'

import socket as s
import pickle

class remoteHKVS:

    def __init__(self):
        self.conn_sock = None


    def connect(self,host,port):
        self.conn_sock = s.socket(s.AF_INET, s.SOCK_STREAM)
        self.conn_sock.connect((host,port))

    def disconnect(self):
        self.conn_sock.close()

    def receber(self):
        msg = self.conn_sock.recv(1024)
        msg_unp = pickle.loads(msg)
        return msg_unp

    def enviar(self,env):
        env_p = pickle.dumps(env, -1)
        self.conn_sock.send(env_p)

    def create(self, mensagem):
        mensagem[0] = '10'
        self.enviar(mensagem)
        return self.receber()

    def put(self,mensagem):
        mensagem[0] = '20'
        self.enviar(mensagem)
        return self.receber()

    def cas(self,mensagem):
        mensagem[0] = '30'
        self.enviar(mensagem)
        return self.receber()

    def remove(self,mensagem):
        mensagem[0] = '40'
        self.enviar(mensagem)
        return self.receber()

    def get(self,mensagem):
        mensagem[0] = '50'
        self.enviar(mensagem)
        return self.receber()

    def list(self,mensagem):
        mensagem[0] = '60'
        self.enviar(mensagem)
        return self.receber()
