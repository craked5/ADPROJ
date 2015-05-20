#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'grupo043'
__author__ = 'Nuno Silva 44285'
__author__ = 'Andre Peniche 44312'

import socket as s
import sys
import os
import thread as t
import select as sel
import pickle as p
import ssl
from hkvs_skel import Skeleton

skel = Skeleton(5)
list_normal_ops = ['10','20','30','40','50','60','70']
command = "ifconfig | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -Eo '([0-9]*\.){3}[0-9]*' | grep -v '127.0.0.1'"
temp = os.popen(command).read()
temp2 = temp.split('\n')
HOST = temp2[0]
PORT = int (sys.argv[1])
CONFIG_PORT = raw_input('Qual a porta de config (9000-9100)?')
print "o ip deste servidor eh " + str(HOST)
print "a porta normal deste servidor eh " + str(PORT)
print "a porta para falar com o config e " + str(CONFIG_PORT)

print "WELCOME TO DA SERVER, WAITING FOR CONFIGURE"

#recall vai receber todos os dados que vai ser enviados ao servidor sem falhas
def recvall(s, size):
    msg = ""
    while size > 0:
        frag = s.recv(1024)
        size -= sys.getsizeof(frag)
        msg += frag
    return msg

def config():
    while True:
        try:
            config_sock = s.socket(s.AF_INET, s.SOCK_STREAM)
            config_sock.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1)
            config_sock.bind((HOST, PORT))
            config_sock.listen(3)
            (config_conn_sock, config_addr) = config_sock.accept()

            sslconn_sock = ssl.wrap_socket(conn_sock, server_side = True,
                        ssl_version = ssl.PROTOCOL_TLSv1, cert_reqs = ssl.CERT_REQUIRED,
                        ca_certs = 'ca.pem',
                        keyfile = 'server.key',
                        certfile = 'server.pem')

            while True:
                try:
                    config_mess = config_conn_sock.recv(2048)
                    if config_mess[0] is '80':
                        temp_config = skel.processMessage(config_mess)
                        config_conn_sock.sendall(p.dumps(temp_config))
                    elif config_mess[0] is '90':
                        temp_config = skel.processMessage(config_mess,HOST+':'+PORT)
                        config_conn_sock.sendall(p.dumps(temp_config))
                except:
                    print "A rececao ou as ops falharam, tentando restaurar"
        except:
            print "Tentando restaurar do erro"
            continue

#Server vai inicialmente estar em modo neutro quando e executado,
#esperando uma ligacao do config para saber o seu papel.
#Depois pode ficar em modo primario ou backup.

#Agora faz-se a socket para falar com o config e trata-se
#da primeira config do server atraves de uma thread para
#a o server estar sempre ligado ao config

try:
    t.start_new_thread(config())
except:
    print "Thread falhou, servidor sem ligacao ao config"


try:
    while True:
            sock = s.socket(s.AF_INET, s.SOCK_STREAM)
            sock.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1)
            sock.bind((HOST, PORT))
            sock.listen(3)
            SocketList = [sock]

            while True:
                R, W, X = sel.select(SocketList, [], [])
                for sckt in R:
                    if sckt is sock:
                        (conn_sock, addr) = sock.accept()
                        ip_prim = skel.list_servers[0]
                        ip_prim = ip_prim[0]

                        if skel.mode is 'backup':
                            if ip_prim is not addr[0]:
                                sckt.close()

                        sslconn_sock = ssl.wrap_socket(conn_sock, server_side = True,
                        ssl_version = ssl.PROTOCOL_TLSv1, cert_reqs = ssl.CERT_REQUIRED,
                        ca_certs = 'ca.pem',
                        keyfile = 'server.key',
                        certfile = 'server.pem')

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
                                if msg[0] in list_normal_ops:
                                    temp = skel.processMessage(msg)
                                    if skel.mode is 'primario':
                                        for ips in skel.list_servers:
                                            t.start_new_thread(skel.sendtobackup(ips,msg))
                                    sckt.sendall(temp)
                                else:
                                    sckt.sendall(p.dumps('Invalid Command, try again.',-1))
                            else:
                                sckt.close()
                                SocketList.remove(sckt)
                                print 'SIze is not equal'
except KeyboardInterrupt:
    print "Interrupted by the user"
sock.close()
