# Análise de Dados da Uber

Este é um aplicativo Streamlit para análise de dados das suas viagens com a Uber. Você pode carregar seus dados da Uber e explorar várias informações, como gastos, tipos de transporte utilizados, locais de partida e chegada, e muito mais.

## Como Baixar seus Dados da Uber

1. Acesse o site da Uber e solicite seus dados.
  ou acesse [esse link](https://auth.uber.com/v2/?breeze_local_zone=phx7&next_url=https%3A%2F%2Fmyprivacy.uber.com%2Fprivacy%2Fexploreyourdata%2Fdownload&state=mBH_cSQedxK1Fzjp3Lqd6x6G7axt_m4--MebmYL_nx8%3D) para solicitar seus dados
<br>

Obs:** *Pode levar 1 ou 2 dias para liberarem seus dados para o seu email.*

<br>

2. Faça login na sua conta Uber.
3. Siga as instruções para solicitar e baixar seus dados. Você receberá um arquivo CSV com as informações das suas viagens.
4. Extraia o arquivo ZIP e encontre o arquivo "trips_data.csv". Esse é o arquivo que contém seus dados

## Como Executar o Aplicativo

1. Acesse [ESSE LINK](https://uberdata.streamlit.app/)
2. Faça o upload do arquivo "trips_data.csv"
3. Navegue pelas abas vendo detalhes de gastos, viagens, locais, e outros.

# Funcionalidades do Aplicativo

## Visualizando os Dados
* Carregue o arquivo CSV de viagens da Uber.
* Visualize detalhes do dataset, incluindo informações sobre as viagens.

  
## Gráficos

* Veja gráficos interativos que mostram a contagem de viagens por valor gasto e tipo de transporte.
* Explore a distribuição da duração das viagens.


## Despesas
* Saiba o valor total gasto em viagens com a Uber.
* Descubra o valor médio gasto por viagem.
* Veja a duração média de suas viagens.
* Calcule o custo médio por quilômetro.

  
## Locais
* Descubra de onde você mais saiu e para onde mais foi com a Uber.
* Encontre detalhes sobre a viagem mais longa.
* Visualize todos os pontos de partida e chegada em mapas interativos.
