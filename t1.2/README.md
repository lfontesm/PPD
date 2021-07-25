# Trabalho 1.2 de PPD

Biblioteca(s) externa(s) utilizada(s): Numpy
Versão do python: Python 3.8.10

### Como rodar?
* Para mudar o número de threads executadas no programa, mudar a variável K;
* Na pasta _servidor_, rode o comando `python servidor.py` para rodar o servidor que escutará na porta 8000;
* Em seguida, na pasta _cliente_, rode o comando `python servidor.py` para iniciar a conexão cliente/servidor.

### É necessário implementar algum controle de concorrência no acesso aos métodos e à tabela hash por parte dos diferentes clientes?
Devido a característica do servidor de ser single-threaded e do cliente utilizar uma única conexão TCP, independente da paralelização feita, temos um único acesso aos métodos e à tabela hash por vez. Logo, não é necessário controle de concorrência no servidor.