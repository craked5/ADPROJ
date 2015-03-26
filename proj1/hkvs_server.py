#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'nunosilva 44285'
__author__ = 'andrepeniche 44312'

from hkvs import HKVS
import socket as s
import sys
import pickle as p

HOST = ''
PORT = int (sys.argv[1])
dir = HKVS()
msgcliente = []
ret = []
sock = s.socket(s.AF_INET, s.SOCK_STREAM)
sock.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1)
sock.bind((HOST, PORT))
sock.listen(1)

while True:
    (conn_sock, addr) = sock.accept()
    print 'ligado a %s', addr
    try:
        msg = conn_sock.recv(1024)
        msg_unp = p.loads(msg)
        print 'recebi %s' % msg_unp

        if(msg_unp[0] == '10'):
            ret=['11']
            ret.append(dir.create(msg_unp[1],msg_unp[2]))
        elif(msg_unp[0] == '20'):
            ret=['21']
            ret.append(dir.put(msg_unp[1],msg_unp[2],msg_unp[3]))

        elif(msg_unp[0] == '30'):
            ret=['22']
            ret.append(dir.cas(msg_unp[1],msg_unp[2],msg_unp[3],msg_unp[4]))

        elif(msg_unp[0] == '40'):
            ret=['23']
            ret.append(dir.remove(msg_unp[1]))

        elif(msg_unp[0] == '50'):
            ret=['24']
            ret.append(dir.get(msg_unp[1]))

        elif(msg_unp[0] == '60'):
            ret=['25']
            ret.append(dir.list(msg_unp[1]))

        print dir.root
        msg_pronta_enviar = p.dumps(ret,-1)
        conn_sock.sendall(msg_pronta_enviar)
    except:
        conn_sock.close()

sock.close()