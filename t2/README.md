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




## Comandos disponiveis

Nessa seção, serão descritos os comandos que podem ser utilizados pelo programa: 

- **```new```**  

   Gera um novo node_id, envia a mensagem de join para criação do respectivo node, adiciona-o na dht e calcula seus vizinhos.

- **```put <msg>```**  

   Gera uma chave aleatória e adiciona `<msg>` na dht na posição da chave gerada.  

- **```get <key>```**  

   Realiza uma busca na dht, na posição passada como argumento.

- **```show```**  

   Lista toda a hash, nesse caso, cada nó é responsável por exibir informações referentes à sua parte.

- **```remove <node_id>```**  

   Remove o respectivo nó da dht, recalcula os intervalos que os nós restantes são responsavéis e redistribui as chaves pertencentes ao nó removido.
   
   
 ## Mensagem de join
   A mensagem de join citada durante o comando `new` nada mais é do que o envio do node_id para todas as filas e então esperar para que todos os nós reconhecam este node_id como um novo nó e recalculem os seus vizinhos se necessário.
