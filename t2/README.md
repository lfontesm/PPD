# Trabalho Final (T2)

Este arquivo apresenta a documentação referente ao trabalho final da disciplina Processamento Paralelo e Distribuido.

## Colaboradores:

[@elcineyjr](https://github.com/elcineyjr) (Elciney Júnior)  
[@lfontesm](https://github.com/lfontesm)   (Leonardo Fontes)  
[@luanripax](https://github.com/luanripax) (Luan Thome)

_____________

## Known Bugs
Reconhecemos que o melhor jeito de implementar concorrência e comunicação entre pai e filho é pelo uso de sinais. Porém, devido à falta de tempo ocasionada por uma outra matéria, não conseguimos ter o tempo necessário para deixar o código do jeito que gostaríamos. Dito isso, as vezes algum nó pode não atribuir o predecessor e sucessor de forma correta durante a entrada de um nó na DHT. Esse bug é corrigido quando um nó sai ou quando um nó entra

## Dependências

* Docker
* pika

## Como rodar

Primeiro é necessário que o _daemon_ do docker esteja rodando, para ativá-lo, execute:

Com _init_:

```bash
sudo /etc/init.d/docker start
```

Com _systemd_:

```bash
sudo systemctl start docker
```

Após isso basta subir o container oficial do RabbitMQ:

```bash
docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.9.5-management
```

Agora é necessário subir o servidor de DHT. Para tal, em outro terminal, rode o comando

```bash
python3 dht.py
```

Agora o servidor DHT está escutando por novos comandos.

Para interagir com o servidor DHT, utilize o comando

```bash
python3 interact.py <cmd>
```

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
