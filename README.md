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

Actualização para a parte3 do projeto:
    Tudo esta feito de acordo com o enunciado.
    Foi introduzido uma nova funcao auth.
    Esta faz-se da seguinte forma: auth 'path'
        Exemplo: auth cliente2.req

Actualização para a parte4 do projeto:
    Devido a motivos maiores, a falta de tempo foi sentida na ultima parte do projeto.
    O projeto não funciona, devido a não conseguir-mos testar a tempo.
    O servico de configuração está feito, só que nao foi testado, logo nao sabemos se funciona.
    A parte da replicação está feita tambem, só que tambem nao conseguimos testar nada, logo não sabemos se funciona.
    A parte da segurança está totalmente por fazer.
    A razão pela qual o projeto nao funciona, e pelo que, como não conseguimos ir a faculdade, tentamos testar em VMs e
        elas nao estão a conseguir falar uma com a outra, não permitindo a comunicação entre servidores/config/clientes.
    O codigo está quase feito, espero que os Professores consiguam perceber a nossa lógica.

Muito obrigado pelo melhor projeto da faculdade.
Vamo-nos certificar que fazemos o projeto mesmo a data ja se ter excedido, visto que nos pensamos que isto é uma peça
fundamental para o nosso curriculo.