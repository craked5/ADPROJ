#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'nuno silva 44285'
__author__ = 'andre peniche 44312'

#from hkvs_impl import HKVS
import socket as s
import sys
import select as sel

from hkvs_skel import Skeleton

HOST = ''
PORT = int (sys.argv[1])
skel_enviar = Skeleton(20)
sock = s.socket(s.AF_INET, s.SOCK_STREAM)
sock.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1)
sock.bind((HOST, PORT))
sock.listen(1)
SocketList = [sock]

#recall vai receber todos os dados que vai ser enviados ao servidor sem falhas
#a funcao recvall nao foi posta em implementacao devido a duvidas na mesma.
#def recvall(s, size):
    #msg = ""
    #while size > 0:
        #frag = s.recv(size)
        #size -= len(frag)
        #msg += frag
    #return msg

try:
    while True:
        R, W, X = sel.select(SocketList, [], [])
        for sckt in R:
            if sckt is sock:
                (conn_sock, addr) = sock.accept()
                print 'Connected to %s', addr
                SocketList.append(conn_sock)
            else:
                msg = sckt.recv(2048)
                if msg:
                    temp = skel_enviar.processMessage(msg)
                    sckt.sendall(temp)
                else:
                    sckt.close()
                    SocketList.remove(sckt)
                    print 'Client closed the connection'
except KeyboardInterrupt:
    print "Interrupted by the user"
sock.close()