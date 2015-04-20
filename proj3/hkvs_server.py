#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'grupo043'
__author__ = 'nuno silva 44285'
__author__ = 'andre peniche 44312'

#from hkvs_impl import HKVS
import socket as s
import sys
import select as sel
import pickle as p

from hkvs_skel import Skeleton

HOST = ''
PORT = int (sys.argv[1])
skel_enviar = Skeleton(5)
sock = s.socket(s.AF_INET, s.SOCK_STREAM)
sock.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1)
sock.bind((HOST, PORT))
sock.listen(1)
SocketList = [sock]

#recall vai receber todos os dados que vai ser enviados ao servidor sem falhas
#a funcao recvall nao foi posta em implementacao devido a duvidas na mesma.
def recvall(s, size):
    msg = ""
    while size > 0:
        frag = s.recv(1024)
        size -= sys.getsizeof(frag)
        msg += frag
        print msg
    return msg

try:
    while True:
        R, W, X = sel.select(SocketList, [], [])
        for sckt in R:
            if sckt is sock:
                (conn_sock, addr) = sock.accept()
                print 'Connected to %s', addr
                SocketList.append(conn_sock)
            else:
                rec_size=sckt.recv(512)
                tamanho=int(p.loads(rec_size))
                sckt.sendall(p.dumps("SIZEOK",-1))
                msg=recvall(sckt,tamanho)
                if tamanho == sys.getsizeof(msg):
                    temp = skel_enviar.processMessage(msg)
                    sckt.sendall(temp)
                else:
                    sckt.close()
                    SocketList.remove(sckt)
                    print 'Client closed the connection'
except KeyboardInterrupt:
    print "Interrupted by the user"
sock.close()