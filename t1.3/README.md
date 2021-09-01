# Trabalho 1.3

## Colaboradores:

[@elcineyjr](https://github.com/elcineyjr) (Elciney Júnior)  
[@lfontesm](https://github.com/lfontesm)   (Leonardo Fontes)  
[@luanripax](https://github.com/luanripax) (Luan Thome)

_____________

## Dependencias
* Docker
* docker-compose
* nc (netcat).*

\* Geralmente vem por padrao em algumas distribuicoes linux

### Como rodar?

Primeiro tenha certeza de que o seu daemon docker esteja rodando:
Com *init*:
```bash
sudo /etc/init.d/docker start
```

Com *systemd*
```bash
sudo systemctl start docker
```

Depois disso, basta rodar o script **startup.sh** como sudo:
```bash
sudo sh startup.sh
```
O script pode demorar um pouco para executar, mas quando terminar voce estara dentro do container contendo a versao de python e as bibliotecas utilizadas.

## Dentro do docker

Dentro do docker, rode 
```bash
python <script.py> <key>,<value>
```
para utilizar o metodo put, e
```bash
python <script.py> <key>
```
para utilizar o metodo get

#### Mensagens de log
Por padrao, estamos utilizando o comando
```bash
tail -f messages.log
```
para imprimir as mensagens de log na tela. Se o comando nao estiver funcionando ou se a saida no terminal estiver bugada, basta abrir uma nova sessao no mesmo diretorio, e rodar o mesmo comando acima e a saida se comportara melhor (junto com isso voce pode comentar a linha 7 em **startup.sh**).

