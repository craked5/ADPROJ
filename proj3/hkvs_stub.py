#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'grupo043'
__author__ = 'nunosilva 44285'
__author__ = 'andrepeniche 44312'

import socket as s
import pickle
import sys
import ssl

class remoteHKVS:

    def __init__(self):
        self.conn_sock = None

    def connect(self,host,port):
        self.conn_sock = s.socket(s.AF_INET, s.SOCK_STREAM)
        self.conn_sock.connect((host,port))

        self.sslconn_sock = ssl.wrap_socket(self.conn_sock,
        ssl_version = ssl.PROTOCOL_TLSv1, cert_reqs = ssl.CERT_REQUIRED,
        ca_certs = '/Users/nunosilva/Desktop/adcerts/ca.pem', keyfile = '/Users/nunosilva/Desktop/adcerts/client.key', certfile = '/Users/nunosilva/Desktop/adcerts/client.pem')

    def disconnect(self):
        self.sslconn_sock.close()

    def receber(self):
        msg = self.sslconn_sock.recv(1024)
        msg_unp = pickle.loads(msg)
        return msg_unp

    def enviar(self,env):
        env_pickled = pickle.dumps(env, -1)

        size_env = sys.getsizeof(env_pickled)
        size_env = str(size_env)

        size_env_pickled = pickle.dumps(size_env,-1)
        self.sslconn_sock.send(size_env_pickled+"\n")
        pickle.loads(self.sslconn_sock.recv(1024))

        self.sslconn_sock.send(env_pickled)

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
