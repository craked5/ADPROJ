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
        ca_certs = '/server/ca.pem',
        keyfile = '/client/client.key',
        certfile = '/client/client.pem')

    def disconnect(self):
        self.sslconn_sock.close()

    def receber(self):
        msg = self.sslconn_sock.recv(2048)
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

    def auth(self,mensagem):
        mensagem[0] = '70'
        req_name = mensagem[1]
        req = open(req_name,'r')
        req_data = req.read()
        mensagem[1] = req_data
        self.enviar(mensagem)
        pem_client2_data = self.receber()
        try:
            pem_name = req_name.replace('.req','.pem')
            pem_client2 = open(pem_name,'w')
            pem_client2.write(pem_client2_data[1])
            return "OK"
        except:
            print "NOK"

