#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'grupo043'
__author__ = 'nunosilva 44285'
__author__ = 'andrepeniche 44312'

class HKVS:

    def __init__(self):
        self.root = {}

# Cria uma diretoria com o nome name no caminho path, caso não
# exista nenhum elemento com esse nome. Retorna ‘OK’ ou ‘NOK’ em
# caso de sucesso ou fracasso da operação, respetivamente.
    def create(self, path, name):

        elems = path.split("/")
        while '' in elems:
            elems.remove('')

        temproot = self.root

        for k in elems:
            if k in temproot:
                temproot = temproot[k]
            else:
                return "NOK"
        if temproot.has_key(name):
            return "NOK"
        else:
            temproot[name]={}
            return "OK"

# Cria uma entrada com o nome name e valor value especificados, numa
# diretoria definida pelo caminho path. Caso exista outra entrada
# com o mesmo nome, o valor associado é substituído; caso exista uma
# diretoria com o mesmo nome a operação falha. Retorna ‘OK’ ou ‘NOK’
# em caso de sucesso ou fracasso da operação, respetivamente.
    def put(self, path, name, value):
        elems = path.split("/")
        while '' in elems:
            elems.remove('')

        temproot = self.root

        for k in elems:
            if k in temproot:
                temproot = temproot[k]
            else:
                return "NOK"
        if temproot.has_key(name):
            if type(temproot[name]) == dict:
                return "NOK"
        else:
            temproot[name] = value
            return "OK"


# Exatamente igual a put, mas apenas substitui o valor associado a
# nome se o valor antigo corresponde a cur_val.
    def cas(self, path, nome, cur_val, new_val):
        elems = path.split("/")
        while '' in elems:
            elems.remove('')

        temproot = self.root

        for k in elems:
            if k in temproot:
                temproot = temproot[k]
            else:
                return "NOK"
        if temproot.has_key(nome):
            if type(temproot[nome]) == dict:
                return "NOK"
            elif temproot[nome] == cur_val:
                temproot[nome] = new_val
                return "OK"
            else:
                return "NOK"
        else:
            return "NOK"

# Remove o último elemento do caminho path se o elemento for uma
# entrada.
# Caso este elemento seja uma diretoria, ele só é apagado se a
# diretoria estiver vazia. Retorna ‘OK’ ou ‘NOK’ em caso de sucesso
# ou fracasso da operação, respectivamente.
    def remove(self, path):
        elems = path.split("/")
        while '' in elems:
            elems.remove('')

        temproot = self.root

        if len(elems) < 1:
            if self.root == {}:
                return "OK"
            else:
                return 'NOK'

        removido = elems.pop()

        for k in elems:
            if k in temproot:
                temproot = temproot[k]
            else:
                return "NOK"
        if type(temproot[removido]) == type({}):
            if len(temproot[removido]) == 0:
                del temproot[removido]
                return "OK"
            else:
                return "NOK"
        elif type(temproot[removido]) != dict:
            del temproot[removido]
            return "OK"
        else:
            return "NOK"

# Retorna o valor associado ao ultimo elemento da path; se este
# elemento for uma diretoria, retorna uma mensagem de erro
# ‘Diretoria’.
    def get(self, path):

        elems = path.split("/")
        while '' in elems:
            elems.remove('')
        temproot = self.root

        if len(elems) < 1:
            return 'Diretorio'

        removido = elems.pop(len(elems)-1)

        for k in elems:
            if k in temproot:
                temproot = temproot[k]
            else:
                return "NOK"
        if type(temproot[removido]) == dict:
            return "Diretoria"
        else:

            return temproot[removido]

# Retorna a lista com os elementos dentro do ultimo elemento da
# path, se este for uma diretoria. Se o elemento for uma entrada,
# retorna ‘Entrada’
    def list(self, path):

        elems = path.split("/")
        while '' in elems:
            elems.remove('')
        temproot = self.root

        if len(elems) < 1:
            return self.root

        removido = elems.pop(len(elems)-1)

        for k in elems:
            if k in temproot:
                temproot = temproot[k]
            else:
                return "NOK"
        if type(temproot[removido]) == dict:
            return temproot[removido]
        else:
            return "Entrada"