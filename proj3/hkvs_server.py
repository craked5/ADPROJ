#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'grupo043'
__author__ = 'nuno silva 44285'
__author__ = 'andre peniche 44312'

import socket as s
import sys
import select as sel
import pickle as p
import ssl
from hkvs_skel import Skeleton

HOST = ''
PORT = int (sys.argv[1])
skel_enviar = Skeleton(5)
sock = s.socket(s.AF_INET, s.SOCK_STREAM)
sock.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1)
sock.bind((HOST, PORT))
sock.listen(1)
SocketList = [sock]

print "WELCOME TO DA SERVER"

#recall vai receber todos os dados que vai ser enviados ao servidor sem falhas
#a funcao recvall nao foi posta em implementacao devido a duvidas na mesma.
def recvall(s, size):
    msg = ""
    while size > 0:
        frag = s.recv(1024)
        size -= sys.getsizeof(frag)
        msg += frag
    return msg

try:
    while True:
        R, W, X = sel.select(SocketList, [], [])
        for sckt in R:
            if sckt is sock:
                (conn_sock, addr) = sock.accept()

                sslconn_sock = ssl.wrap_socket(conn_sock, server_side = True,
                ssl_version = ssl.PROTOCOL_TLSv1, cert_reqs = ssl.CERT_REQUIRED,
                ca_certs = '/server/ca.pem',
                keyfile = '/server/server.key',
                certfile = '/server/server.pem')

                print 'Connected to %s', addr
                SocketList.append(sslconn_sock)
            else:
                rec_size=sckt.recv(512)
                if rec_size == '':
                    sckt.close()
                    SocketList.remove(sckt)
                    print 'Client closed the connection ' + '%s', addr
                else:
                    tamanho=int(p.loads(rec_size))
                    sckt.sendall(p.dumps("SIZE_CONFIRMED",-1))
                    msg=recvall(sckt,tamanho)

                    if tamanho == sys.getsizeof(msg):
                        temp = skel_enviar.processMessage(msg)
                        sckt.sendall(temp)
                    else:
                        sckt.close()
                        SocketList.remove(sckt)
                        print 'SIze is not equal'
except KeyboardInterrupt:
    print "Interrupted by the user"
sock.close()