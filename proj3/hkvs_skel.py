#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'grupo043'
__author__ = 'nunosilva 44285'
__author__ = 'andrepeniche 44312'

import pickle as p
from hkvs_durable import DurableHKVS


class Skeleton:

    def __init__(self,f_size):
        self.durahkvs = DurableHKVS(f_size)

    def processMessage(self,msg):

        ret = []
        msg_unp = p.loads(msg)
        print 'Received %s' % msg_unp

        if(msg_unp[0] == '10'):
            ret=['11']
            try:
                ret.append(self.durahkvs.create(msg_unp[1],msg_unp[2]))
            except IndexError:
                ret.append('NOK')
            except UnboundLocalError:
                ret.append('NOK')

        elif(msg_unp[0] == '20'):
            ret=['21']
            try:
                ret.append(self.durahkvs.put(msg_unp[1],msg_unp[2],msg_unp[3]))
            except IndexError:
                ret.append('NOK')
            except UnboundLocalError:
                ret.append('NOK')

        elif(msg_unp[0] == '30'):
            ret=['31']
            try:
                ret.append(self.durahkvs.cas(msg_unp[1],msg_unp[2],msg_unp[3],msg_unp[4]))
            except IndexError:
                ret.append('NOK')
            except UnboundLocalError:
                ret.append('NOK')

        elif(msg_unp[0] == '40'):
            ret=['41']
            try:
                ret.append(self.durahkvs.remove(msg_unp[1]))
            except IndexError:
                ret.append('NOK')
            except UnboundLocalError:
                ret.append('NOK')

        elif(msg_unp[0] == '50'):
            ret=['51']
            ret.append(self.durahkvs.get(msg_unp[1]))

        elif(msg_unp[0] == '60'):
            ret=['61']
            try:
                ret.append(self.durahkvs.list(msg_unp[1]))
            except IndexError:
                ret.append('NOK')
            except UnboundLocalError:
                ret.append('NOK')

        msg_pronta_enviar = p.dumps(ret,-1)
        return msg_pronta_enviar