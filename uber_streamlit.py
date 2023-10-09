import plotly.express as px
import pandas as pd
import numpy as np
import streamlit as st
from geopy.distance import great_circle

# Define o df como None caso não carregue os arquivos

df = None

# Função para carregar os dados
def load_data(file_data):
    if file_data is not None:
        df = pd.read_csv(file_data)
        return df
    else:
        return None


# Configuração da página
st.set_page_config(
    page_title="Análise de Dados da Uber",
    page_icon="./img/UberIcon.png",
    layout="wide",
)

# Título e introdução
st.title('Análise dos seus dados da Uber')
st.markdown('1. Acesse o site da Uber e solicite seus dados.
  ou acesse [esse link](https://auth.uber.com/v2/?breeze_local_zone=phx7&next_url=https%3A%2F%2Fmyprivacy.uber.com%2Fprivacy%2Fexploreyourdata%2Fdownload&state=mBH_cSQedxK1Fzjp3Lqd6x6G7axt_m4--MebmYL_nx8%3D) para solicitar seus dados
<br>

Obs:** *Pode levar 1 ou 2 dias para liberarem seus dados para o seu email.*

<br>

2. Faça login na sua conta Uber.
3. Siga as instruções para solicitar e baixar seus dados. Você receberá um arquivo CSV com as informações das suas viagens.
4. Extraia o arquivo ZIP e encontre o arquivo "trips_data.csv". Esse é o arquivo que contém seus dados')

# Configuração das abas
tab1, tab2, tab3, tab4 = st.tabs(["Visualizando os dados", "Gráficos", "Despesas", "Locais"])

with tab1:
    # Upload do arquivo CSV na primeira aba
    file_data = st.file_uploader("Carregue o arquivo 'trips_data.csv'", type=["csv"])

    df = load_data(file_data)

    if df is not None and not df.empty:
        # Checkbox para mostrar detalhes do dataset
        if st.checkbox('Mostrar detalhes do dataset'):
            st.subheader('Preview dos Dados')
            st.write(df)

        st.markdown('---')

        # Excluindo a coluna 'Fare Currency'
        df = df.drop('Fare Currency', axis=1)

        # Removendo linhas com dados faltantes
        df = df.dropna()

        # Exibindo o número de viagens completas, canceladas por você ou pelo motorista
        st.write("Viagens completas, canceladas por você ou pelo motorista:")
        st.write(df['Trip or Order Status'].value_counts())

        st.markdown('---')

        # Exibindo o número de viagens por cidade
        st.write("Número de viagens por cidade:")
        st.write(df['City'].value_counts())

with tab2:
    st.title('Gráficos')

    if df is not None and not df.empty:

        # Criando categorias de gastos
        categories = [0, 5, 10, 15, 20, 30, float('inf')]
        labels = ['R$0 - R$5', 'R$6 - R$10', 'R$11-R$15', 'R$16-R$20', 'R$21-R$30', 'R$31-R$100']
    
        # Adicionando uma nova coluna ao DataFrame com as categorias
        df['Fare Category'] = pd.cut(df['Fare Amount'], bins=categories, labels=labels)
    
        # Contando quantos valores estão em cada categoria
        count_by_category = df['Fare Category'].value_counts().reset_index()
        count_by_category.columns = ['Valor Gasto por Viagem', 'Contagem de Viagens']
    
        # Ordenando as categorias do menor valor para o maior
        count_by_category = count_by_category.sort_values(by='Valor Gasto por Viagem')
    
        # Criando um gráfico de barras interativo
        fig = px.bar(count_by_category, x='Valor Gasto por Viagem', y='Contagem de Viagens',
                    title='Contagem de Viagens por Valor Gasto',
                    labels={'Valor Gasto por Viagem': 'Valor Gasto por Viagem', 'Contagem de Viagens': 'Contagem de Viagens'})
        fig.update_xaxes(type='category')
        st.plotly_chart(fig)
    
        # Contando quantas viagens estão em cada tipo de transporte
        contagem_por_transporte = df['Product Type'].value_counts().reset_index()
        contagem_por_transporte.columns = ['Tipo de transporte', 'Contagem']
    
        # Criando um gráfico de barras horizontais com Plotly
        fig = px.bar(contagem_por_transporte, x='Contagem', y='Tipo de transporte',
            orientation='h', text='Contagem',
            title='Distribuição de Tipos de Transporte')
        fig.update_traces(textposition='outside')
        fig.update_layout(xaxis_title='Contagem', yaxis_title='Tipo de transporte')
        st.plotly_chart(fig)
    
        # Definindo o formato da data e hora
        date_format = "%Y-%m-%d %H:%M:%S +0000 UTC"
    
        # Convertendo colunas para o formato datetime especificado
        df['Begin Trip Time'] = pd.to_datetime(df['Begin Trip Time'], format=date_format)
        df['Dropoff Time'] = pd.to_datetime(df['Dropoff Time'], format=date_format)
        df['Request Time'] = pd.to_datetime(df['Request Time'], format=date_format)
    
        # Criando colunas 'Duration' e 'Waiting Time'
        df['Duration'] = df['Dropoff Time'] - df['Begin Trip Time']
    
        # Convertendo a coluna 'Duration' para um tipo `str`
        df['Duration (minutes)'] = df['Duration'].apply(lambda duration: str(duration.total_seconds() // 60))
    
        # Convertendo a coluna 'Duration' para um tipo numérico
        df['Duration (minutes)'] = pd.to_numeric(df['Duration'].apply(lambda duration: str(duration.total_seconds() // 60)))
    
        # Função para criar as categorias de duração
        def categorize_duration(duration_minutes):
            if duration_minutes <= 5:
                return '0-5 minutos'
            elif duration_minutes <= 10:
                return '6-10 minutos'
            elif duration_minutes <= 20:
                return '11-20 minutos'
            elif duration_minutes <= 30:
                return '21-30 minutos'
            else:
                return '31 minutos ou mais'

        # Adicionando uma nova coluna 'Categoria' ao DataFrame
        df['Categoria'] = df['Duration (minutes)'].apply(categorize_duration)
    
        # Contando quantas viagens estão em cada categoria
        contagem_por_categoria = df['Categoria'].value_counts().reset_index()
        contagem_por_categoria.columns = ['Categoria', 'Contagem']
    
        # Criando um gráfico de pizza interativo com Plotly Express
        fig = px.pie(contagem_por_categoria, values='Contagem', names='Categoria', title='Distribuição da Duração das Viagens')
        fig.update_traces(textinfo='percent+label')
    
        # Exibindo o gráfico no Streamlit
        st.plotly_chart(fig)

    else:
        # Se df não estiver definido, exiba uma mensagem para o usuário
        st.write("Carregue um arquivo CSV na aba 1 para continuar.")



with tab3:
    st.title('Dados de Despesas:')


    if df is not None and not df.empty:
        # Calculando o valor total gasto
        valor_gasto = df['Fare Amount'].sum()
        st.subheader(f"Você já gastou R$ {valor_gasto:.2f} com Uber")

        st.markdown('---')

        # Calculando o valor médio gasto
        valor_medio = df['Fare Amount'].mean()
        st.subheader(f'O valor médio gasto em todas as viagens foi de R${valor_medio:.2f}')

        st.markdown('---')

        # Convertendo colunas para o formato datetime especificado
        df['Begin Trip Time'] = pd.to_datetime(df['Begin Trip Time'], format=date_format)
        df['Dropoff Time'] = pd.to_datetime(df['Dropoff Time'], format=date_format)

        # Calculando a duração média das viagens em minutos
        df['Duration'] = (df['Dropoff Time'] - df['Begin Trip Time']).dt.total_seconds() / 60
        duracao_media = df['Duration'].mean()
        st.subheader(f'A duração média de todas as viagens foi de {duracao_media:.0f} minutos')

        st.markdown('---')

        # Calculando o custo médio por quilômetro
        distancia = df['Distance (miles)'].sum() * 1.60934
        media_km_valor = valor_gasto / distancia
        st.subheader(f"Você gastou em média R$ {media_km_valor:.2f} por quilômetro")

        st.markdown('---')

        st.subheader(f"Você já percorreu {distancia:.2f} Km de Uber")

    else:
        # Se df não estiver definido, exiba uma mensagem para o usuário
        st.write("Carregue um arquivo CSV na aba 1 para continuar.")



with tab4:
    st.title('Locais:')
    
    if df is not None and not df.empty:        
        df = df.dropna()

        st.subheader('Local de onde você mais saiu:')
        endereco_mais_frequente = df['Begin Trip Address'].value_counts().idxmax()
        st.write(endereco_mais_frequente)
        
        st.subheader('Local onde você mais foi:')
        local_mais_frequente = df['Dropoff Address'].value_counts().idxmax()
        st.write(local_mais_frequente)

        st.markdown('---')

        st.subheader('Detalhes da viagem mais longa:')

        # Função para calcular a distância entre dois pontos de latitude e longitude
        def calcular_distancia(row):
            begin_coords = (row['Begin Trip Lat'], row['Begin Trip Lng'])
            dropoff_coords = (row['Dropoff Lat'], row['Dropoff Lng'])
            return great_circle(begin_coords, dropoff_coords).kilometers

        # Aplicar a função para calcular a distância para cada viagem e criar uma nova coluna 'Distância'
        df['Distance'] = df.apply(calcular_distancia, axis=1)

        # Encontrar a maior distância percorrida
        maior_distancia = df['Distance'].max()

        # Encontrar a linha correspondente à viagem mais longa
        viagem_mais_longa = df[df['Distance'] == maior_distancia]

        # Obter informações sobre a viagem mais longa
        valor_viagem = viagem_mais_longa['Fare Amount'].values[0]
        local_saida = viagem_mais_longa['Begin Trip Address'].values[0]
        local_chegada = viagem_mais_longa['Dropoff Address'].values[0]
        data_saida = viagem_mais_longa['Begin Trip Time'].values[0]
        data_chegada = viagem_mais_longa['Dropoff Time'].values[0]

        # Imprimir informações sobre a viagem mais longa
        st.write(f"- A maior distância percorrida foi de {maior_distancia:.2f} quilômetros.")
        st.write(f"- Valor da viagem: R$ {valor_viagem:.2f}")
        st.write(f"- Local de saída: {local_saida}")
        st.write(f"- Local de chegada: {local_chegada}")
        st.write(f"- Data e horário de saída: {data_saida}")
        st.write(f"- Data e horário de chegada: {data_chegada}")

        st.markdown('---')

        st.subheader("Todos os Pontos de Saída:")  # Adicione um título para o mapa
        
        # Crie um mapa com Plotly Express
        fig = px.scatter_mapbox(df,
                                lat="Begin Trip Lat",  # Substitua pelo nome correto da coluna de latitude
                                lon="Begin Trip Lng",  # Substitua pelo nome correto da coluna de longitude
                                hover_name="Begin Trip Address",  # Substitua pelo nome correto da coluna de rótulos
                                zoom=10)
        
        # Defina o layout do mapa
        fig.update_layout(mapbox_style="open-street-map")
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
        
        # Exiba o mapa no Streamlit
        st.plotly_chart(fig)

        st.markdown('---')

        st.subheader("Todos os Lugares aonde você foi:")  # Adicione um título para o mapa
        
        # Crie um mapa com Plotly Express
        fig = px.scatter_mapbox(df,
                                lat="Dropoff Lat",  # Substitua pelo nome correto da coluna de latitude
                                lon="Dropoff Lng",  # Substitua pelo nome correto da coluna de longitude
                                hover_name="Dropoff Address",  # Substitua pelo nome correto da coluna de rótulos
                                zoom=10)
        
        # Defina o layout do mapa
        fig.update_layout(mapbox_style="open-street-map")
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
        
        # Exiba o mapa no Streamlit
        st.plotly_chart(fig)
        
    else:
        # Se df não estiver definido, exiba uma mensagem para o usuário
        st.write("Carregue um arquivo CSV na aba 1 para continuar.")

