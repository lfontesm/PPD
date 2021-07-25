# Trabalho 1.2 de PPD

Biblioteca(s) externa(s) utilizada(s): Numpy
Versão do python: Python 3.8.10

### Como rodar?
* Para mudar o número de threads executadas no programa, mudar a variável K;
* Na pasta _servidor_, rode o comando `python servidor.py` para rodar o servidor que escutará na porta 8000;
* Em seguida, na pasta _cliente_, rode o comando `python servidor.py` para iniciar a conexão cliente/servidor.

### É necessário implementar algum controle de concorrência no acesso aos métodos e à tabela hash por parte dos diferentes clientes?
Não. Como a tabela hash está armazenada no servidor, não existe acesso simultâneo à tabela hash, portanto não é necessário controle de concorrência, já que do jeito que implementamos o trabalho, os processos compartilham a mesma conexão HTTP.
