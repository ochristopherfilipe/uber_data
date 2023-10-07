import plotly.express as px
import pandas as pd
import numpy as np
import streamlit as st
import folium

# Configuração da página
st.set_page_config(
    page_title="Análise de Dados da Uber",
    page_icon="./img/UberIcon.png",
    layout="wide",
)

# Título e introdução
st.title('Análise dos seus dados da Uber')
st.write('Para acessar seus dados da Uber, você deve solicitar...pipipipopopo')

# Configuração das abas
tab1, tab2, tab3, tab4 = st.tabs(["Visualizando os dados", "Gráficos", "Valores", "Mapa"])

with tab1:
    # Função para carregar os dados
    @st.cache_data
    def load_data(file_data):
        if file_data is not None:
            df = pd.read_csv(file_data)
            return df

    # Upload do arquivo CSV na primeira aba
    file_data = st.file_uploader("Carregue o arquivo 'trips_data.csv'", type=["csv"])

    if file_data is not None:
        df = load_data(file_data)

        # Checkbox para mostrar detalhes do dataset
        if st.checkbox('Mostrar detalhes do dataset'):
            st.subheader('Preview dos Dados')
            st.write(df)

        # Excluindo a coluna 'Fare Currency'
        df = df.drop('Fare Currency', axis=1)

        # Removendo linhas com dados faltantes
        df = df.dropna()

        # Definindo o formato da data e hora
        date_format = "%Y-%m-%d %H:%M:%S +0000 UTC"

        # Convertendo colunas para o formato datetime especificado
        df['Begin Trip Time'] = pd.to_datetime(df['Begin Trip Time'], format=date_format)
        df['Dropoff Time'] = pd.to_datetime(df['Dropoff Time'], format=date_format)
        df['Request Time'] = pd.to_datetime(df['Request Time'], format=date_format)

        # Criando colunas 'Duration' e 'Waiting Time'
        df['Duration'] = df['Dropoff Time'] - df['Begin Trip Time']
        df['Waiting Time'] = df['Request Time'] - df['Begin Trip Time']

        # Exibindo o número de viagens completas, canceladas por você ou pelo motorista
        st.write("Viagens completas, canceladas por você ou pelo motorista")
        st.write(df['Trip or Order Status'].value_counts())

with tab2:
    st.title('Gráficos')

    # Use df do tab1 aqui para criar gráficos
    if 'df' in locals():
        # Criando categorias de gastos
        categories = [0, 5, 10, 15, 20, 30, float('inf')]
        labels = ['0-5', '6-10', '11-15', '16-20', '21-30', '31-50']

        # Adicionando uma nova coluna ao DataFrame com as categorias
        df['Fare Category'] = pd.cut(df['Fare Amount'], bins=categories, labels=labels)

        # Contando quantos valores estão em cada categoria
        count_by_category = df['Fare Category'].value_counts().reset_index()
        count_by_category.columns = ['Categoria de Gastos', 'Contagem de Viagens']

        # Criando um gráfico de barras interativo
        st.write("Contagem de Viagens por Valor Gasto:")
        fig = px.bar(count_by_category, x='Categoria de Gastos', y='Contagem de Viagens',
                    title='Contagem de Viagens por Valor Gasto',
                    labels={'Categoria de Gastos': 'Categoria de Gastos', 'Contagem de Viagens': 'Contagem de Viagens'})
        fig.update_xaxes(type='category')
        st.plotly_chart(fig)


with tab4:
    st.title('Mapa de Viagens')

    # Função para carregar os dados novamente
    @st.cache_data
    def load_data_tab4(file_data):
        if file_data is not None:
            df_tab4 = pd.read_csv(file_data)
            return df_tab4

    # Upload do arquivo CSV na quarta aba
    file_data_tab4 = st.file_uploader("Carregue o arquivo 'trips_data.csv' na aba 4", type=["csv"], key="tab4_file_uploader")

    if file_data_tab4 is not None:
        df_tab4 = load_data_tab4(file_data_tab4)

        st.write(df_tab4)

        df_tab4 = df_tab4.dropna()

        # Criar um mapa com Folium
        mapa = folium.Map(location=[-3.116481, -60.048106], zoom_start=12)

        # Adicionar marcadores ao mapa para cada ponto de início de viagem
        for i in range(len(df_tab4)):
            folium.Marker([df_tab4['Begin Trip Lat'].iloc[i], df_tab4['Begin Trip Lng'].iloc[i]],
                            popup=df_tab4['Begin Trip Address'].iloc[i]).add_to(mapa)

        # Exibir o mapa no Streamlit
        mapa