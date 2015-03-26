#!/usr/bin/env python
# -*- coding: utf-8 -*-
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

while True:

    temp = raw_input()
    lista = temp.split(' ')

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

a.disconnect()
sys.exit()



