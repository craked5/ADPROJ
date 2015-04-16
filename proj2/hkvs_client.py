#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'grupo043'
__author__ = 'nunosilva 44285'
__author__ = 'andrepeniche 44312'

import sys

from hkvs_stub import remoteHKVS


HOST = sys.argv[1]
PORT = int (sys.argv[2])
a = remoteHKVS()
ret = 0
a.connect(HOST,PORT)
lista = []

try:
    while True:

        lista_keywords = ['create','put','cas','remove','get','list','exit']
        temp = raw_input()
        lista = temp.split(' ')

        if lista[0] in lista_keywords:
            if lista[0] == 'exit':
                a.disconnect()
                sys.exit()
            elif lista[0] == 'create':
                ret =  a.create(lista)
            elif lista[0] == 'put':
                ret = a.put(lista)
            elif lista[0] == 'cas':
                ret = a.cas(lista)
            elif lista[0] == 'remove':
                ret = a.remove(lista)
            elif lista[0] == 'get':
                ret = a.get(lista)
            elif lista[0] == 'list':
                ret = a.list(lista)
            print ret[1]
        else:
            print "Command Unknown, please type a valid command"
except KeyboardInterrupt:
    print 'Interrupted by the user'
a.disconnect()
sys.exit()



