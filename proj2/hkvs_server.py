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
enviar = Skeleton()
sock = s.socket(s.AF_INET, s.SOCK_STREAM)
sock.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1)
sock.bind((HOST, PORT))
sock.listen(1)
SocketList = [sock]

#recall vai receber todos os dados que vai ser enviados ao servidor sem falhas
def recall(s, size):
    msg = ""
    while size > 0:
        frag = s.recv(size)
        size -= len(frag)
    msg += frag
    return msg

while True:
    R, W, X = sel.select(SocketList, [], [])
    print R
    for sckt in R:
        if sckt is sock:
            (conn_sock, addr) = sock.accept()
            print 'ligado a %s', addr
            SocketList.append(conn_sock)
        else:
            msg = recall(sckt,1800)
            if msg:
                temp = enviar.processMessage(msg)
                sckt.sendall(temp)
            else:
                sckt.close()
                SocketList.remove(sckt)
                print 'Cliente fechou ligação'
sock.close()