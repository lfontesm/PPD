# Relatório do primeiro trabalho de PPD

## Instruções para execução do programa
* Versão do python: `v3.9.5`
* Bibliotecas utilizadas: `numpy multiprocessing time`
* Alterar número de threads no código na variável `nThreadsGlobal`
* Executar no terminal: `python trabppd.py`

## Configurações do hardware utilizado
* CPU: AMD ryzen 7 2700 (3.2 GHz)
* RAM: 16Gb
* OS: Linux

## Gráfico geral de tempo a cada iteração
![grafico_iteracoes](https://user-images.githubusercontent.com/22310158/125137501-2e110f00-e0e3-11eb-8e1c-a91428353406.png)

## Tempo médio de execução por número de threads
![medias](https://user-images.githubusercontent.com/22310158/125138083-5fd6a580-e0e4-11eb-9069-befba319e6ba.jpg)

## Dados detalhados 
#### Tabela para k = 1
![k1](https://user-images.githubusercontent.com/22310158/125137837-daeb8c00-e0e3-11eb-82b7-1ffc6a4fa418.jpg)

#### Tabela para k = 2
![k2](https://user-images.githubusercontent.com/22310158/125137841-dd4de600-e0e3-11eb-9da0-ab762147ab18.jpg)

#### Tabela para k = 4
![k4](https://user-images.githubusercontent.com/22310158/125137846-dfb04000-e0e3-11eb-8c7d-1e6e836cc1e7.jpg)

#### Tabela para k = 8
![k8](https://user-images.githubusercontent.com/22310158/125137861-e76fe480-e0e3-11eb-837f-3f0770f2ae79.jpg)

## Conclusão

Os resultados estão coerentes com o que esperávamos. O algoritmo utilizado foi o _QuickSort_, o qual não é muito escalável para _multithreading/multiprocessing_. Dito isso, o resultado esperado para a atividade sugerida é que depois que cada processo finaliza a ordenação de uma parte do vetor de tamanho **n**, ele deve passar um vetor maior para o próximo processo, composto por dois vetores ordenados. Obviamente, isso é semi-equivalente a reordenação inteira de um vetor de tamanho **n*2** , resultando em uma acumulação do tempo de execução.

Note que caso a performance da atividade fosse prioridade, poderíamos ter utilizado um algoritmo mais amigável com paralelismo, como por exemplo, _MergeSort_.
