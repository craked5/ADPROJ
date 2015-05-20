#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Grupo 043'
__author__ = 'Nuno Silva 44285'
__author__ = 'Andre Peniche 44312'

import socket as s
import pickle
import sys
import ssl
import time

class config_stub:
    def __init__(self):
        self.conn_sock = None

    def connect(self,host,port):
        self.conn_sock = s.socket(s.AF_INET, s.SOCK_STREAM)
        try:
            self.conn_sock.connect((host,port))
        except:
            return 0
        self.sslconn_sock = ssl.wrap_socket(self.conn_sock,
        ssl_version = ssl.PROTOCOL_TLSv1, cert_reqs = ssl.CERT_REQUIRED,
        ca_certs = '../ca.pem',
        keyfile = 'config.key',
        certfile = 'config.pem')

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

    def is_alive(self, mensagem):
        mensagem[0] = '80'
        self.enviar(mensagem)
        return self.receber()

    def reconfigure(self,mensagem):
        mensagem[0] = '90'
        self.enviar(mensagem)
        return self.receber()

class config_client:

    hosts = sys.argv
    lista = hosts.split(' ')
    a = config_stub()
    T = 2.000
    K = 3
    K_temp = 3

    try:
        while True:
            for ips in lista:
                temp_ip = ips.split(':')
                a.connect(temp_ip[0],temp_ip[1])
                ret =  a.is_alive(lista)
                if ret[1] is 'NOK':
                    if K_temp is 3:
                        temp = raw_input('Insert new list of servers to reconfigure:')
                        lista_nova = temp.split(' ')
                        ret2 = a.reconfigure(lista_nova)
                        print 'new config: ' + ret2[1]
                        K_temp = 0
                    else:
                        K_temp += 1
                time.sleep(2.500)
    except KeyboardInterrupt:
        print 'Interrupted by the user'
    a.disconnect()
    sys.exit()