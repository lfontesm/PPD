# Trabalho Final (T2)

Este arquivo apresenta a documentação referente ao trabalho final da disciplina Processamento Paralelo e Distribuido.

## Colaboradores:

[@elcineyjr](https://github.com/elcineyjr) (Elciney Júnior)  
[@lfontesm](https://github.com/lfontesm)   (Leonardo Fontes)  
[@luanripax](https://github.com/luanripax) (Luan Thome)

_____________

## Dependências

* Docker
* docker-compose


## Como rodar?




## Funcionamento 




## Comandos

Nessa seção, serão descritos os comandos que podem ser utilizados pelo programa: 

- **```new()```**  

   Gera um novo node, seu respectivo node_id, adiciona-o na dht e calcula seus vizinhos.  

- **```put(msg)```**  

   Gera um valor aleatório, e adiciona a mensagem passada como argumento na dht.  

- **```get(key)```**  

   Realiza uma busca na dht, na posição passada como argumento.

- **```show()```**  

   Lista toda a hash, nesse caso, cada nó é responsável por exibir informações referentes à sua parte.

- **```remove(node_id)```**  

   Remove o respectivo nó da dht e recalcula os vizinhos considerando a redistribuição dos valores.
