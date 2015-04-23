# ADPROJ

O servidor é executado da maneira que esta descrita no enunciado, server.py “port”.
O cliente é executado da maneira que esta descrita no enunciado, client.py “ip” “port”.

Depois no client, os comandos são desta forma:
“função” “path” “args” …

A lista de comandos disponiveis e: create, put, cas, remove, get, list, exit, auth

Ex:

create tree/ tree1

put tree/tree1/ X Y

Actualização para a parte2 do projeto:
	Nesta parte do projeto foi feito tudo o pedido excepto a implementação da função recvall().

Actualização para a parte2 do projeto:
    Tudo esta feito de acordo com o enunciado.
    Foi introduzido uma nova funcao auth.
    Esta faz-se da seguinte forma: auth 'path'
        Exemplo: auth cliente2.req