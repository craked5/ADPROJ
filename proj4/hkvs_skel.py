#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'grupo043'
__author__ = 'Nuno Silva 44285'
__author__ = 'Andre Peniche 44312'

import pickle as p
import os
import sys
import ssl
import socket as s
from hkvs_durable import DurableHKVS

class Skeleton:

    def __init__(self,f_size):
        self.durahkvs = DurableHKVS(f_size)
        self.list_servers = []
        self.ip = 0
        self.mode = ''

    #Processa a mensagem que vem do hkvs_server
    def processMessage(self,msg,ip):
        ret = []
        msg_unp = p.loads(msg)
        print 'Received %s' % msg_unp

        if msg_unp[0] == '10':
            ret=['11']
            try:
                ret.append(self.durahkvs.create(msg_unp[1],msg_unp[2]))
            except IndexError:
                ret.append('NOK')
            except UnboundLocalError:
                ret.append('NOK')

        elif msg_unp[0] == '20':
            ret=['21']
            try:
                ret.append(self.durahkvs.put(msg_unp[1],msg_unp[2],msg_unp[3]))
            except IndexError:
                ret.append('NOK')
            except UnboundLocalError:
                ret.append('NOK')

        elif msg_unp[0] == '30':
            ret=['31']
            try:
                ret.append(self.durahkvs.cas(msg_unp[1],msg_unp[2],msg_unp[3],msg_unp[4]))
            except IndexError:
                ret.append('NOK')
            except UnboundLocalError:
                ret.append('NOK')

        elif msg_unp[0] == '40':
            ret=['41']
            try:
                ret.append(self.durahkvs.remove(msg_unp[1]))
            except IndexError:
                ret.append('NOK')
            except UnboundLocalError:
                ret.append('NOK')

        elif msg_unp[0] == '50':
            ret=['51']
            ret.append(self.durahkvs.get(msg_unp[1]))

        elif msg_unp[0] == '60':
            ret=['61']
            try:
                ret.append(self.durahkvs.list(msg_unp[1]))
            except IndexError:
                ret.append('NOK')
            except UnboundLocalError:
                ret.append('NOK')

        elif msg_unp[0] == '70':
            ret=['71']
            try:
                path = 'rec_client2.req'
                rec_client2 = open(path, 'w')
                rec_client2.write(msg_unp[1])
                rec_client2.close()

                os.system('openssl x509 -req -in rec_client2.req -CA '
                          '../ca.pem -CAkey privkey.pem '
                          '-CAserial file.srl -out client2.pem')

                pem_client2 = open('client2.pem', 'r')
                pem_data = pem_client2.read()
                ret.append(pem_data)
            except IOError:
                print "Error writing .req or .pem file on server"

        elif msg_unp[0] is '80':
            if self.mode is not True or False:
                ret=['81']
                ret.append('NOK')
            else:
                ret=['81']
                ret.append('OK')

        elif msg_unp[0] == '90':
            #verifica se o server fica/continua o primario
            if msg_unp[1] is ip:
                ret=['91']
                self.list_servers = msg_unp[1]
                for i in msg_unp[2]:
                        self.list_servers.append(i)
                self.mode = 'primario'
                ret.append('OK')
            #no caso de nao ficar primario, mete-se o estado do server em backup
            else:
                ret = ['91']
                self.list_servers = msg_unp[1]
                for i in msg_unp[2]:
                        self.list_servers.append(i)
                self.mode = 'backup'
                ret.append('OK')

        msg_pronta_enviar = p.dumps(ret,-1)
        return msg_pronta_enviar

    def sendtobackup(self,ip,msg):
        back_sock = s.socket(s.AF_INET, s.SOCK_STREAM)
        temp_ip = ip.split(':')
        try:
            back_sock.connect((temp_ip[0],temp_ip[1]))
        except:
            return 0
        sslback_sock = ssl.wrap_socket(back_sock,
        ssl_version = ssl.PROTOCOL_TLSv1, cert_reqs = ssl.CERT_REQUIRED,
        ca_certs = '../ca.pem',
        keyfile = 'client.key',
        certfile = 'client.pem')

        env_pickled = p.dumps(msg, -1)

        size_env = sys.getsizeof(env_pickled)
        size_env = str(size_env)

        size_env_pickled = p.dumps(size_env,-1)
        sslback_sock.send(size_env_pickled+"\n")
        p.loads(sslback_sock.recv(1024))

        sslback_sock.send(env_pickled)

        msg_rec = sslback_sock.recv(2048)
        msg_rec = p.loads(msg_rec)
        sslback_sock.close()
        return msg_rec
