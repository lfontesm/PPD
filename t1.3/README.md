# Trabalho 1.3

## Colaboradores:

[@elcineyjr](https://github.com/elcineyjr) (Elciney Júnior)  
[@lfontesm](https://github.com/lfontesm)   (Leonardo Fontes)  
[@luanripax](https://github.com/luanripax) (Luan Thome)

_____________

## Dependências
* Docker
* docker-compose
* nc (netcat).*

\* Geralmente vem por padrão em algumas distribuições Linux

## Como rodar?

Primeiro tenha certeza de que o seu daemon docker esteja rodando:

Com *init*:
```bash
sudo /etc/init.d/docker start
```

Com *systemd*
```bash
sudo systemctl start docker
```

Depois disso, basta buildar a imagem e rodar o script **startup.sh** como sudo:
```bash
sudo docker build -t ppd .
sudo sh startup.sh
```
\* O docker build será necessário apenas na primeira vez que você rodar o trabalho.

O script pode demorar um pouco para executar, mas quando terminar voce estará dentro do container contendo a versão de python e as bibliotecas utilizadas.

### Dentro do docker

Dentro do docker, rode 
```bash
python interact.py 
```

Como os nodes são gerados ao inicializar o container, logo para se gerar novos nodes, o container deverá ser reinicializado.

## Mensagens de log
Os logs estão sendo escritos no arquivo **messages.log**
