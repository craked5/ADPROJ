#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'grupo043'
__author__ = 'Nuno Silva 44285'
__author__ = 'Andre Peniche 44312'

import sys

from hkvs_stub import stubHKVS

ret_connect = 0
a = stubHKVS()
ret = 0
lista = []
count_conns = 0
lista_keywords = ['create','put','cas','remove','get','list','exit','auth']
list_servers = sys.argv
list_servers = list_servers.split(' ')

while count_conns is not 2:
    for adrs in list_servers:
        adrs_temp = adrs.split(':')
        ret_connect = a.connect(adrs_temp[0],adrs_temp[1])
        if ret_connect != 0:
            break
    count_conns += 1

try:
    while True:
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
            elif lista[0] == 'auth':
                ret = a.auth(lista)
            print ret
        else:
            print "Command Unknown, please type a valid command"
except KeyboardInterrupt:
    print 'Interrupted by the user'
a.disconnect()
sys.exit()



