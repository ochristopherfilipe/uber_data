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
st.write('')
# Configuração das abas
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Por que Usar?", "Como Usar", "Visualizando os Dados", "Gráficos", "Despesas", "Locais"])

with tab1:
    st.title('Por que usar?')
    st.markdown('''
    ## Descubra Mais Sobre Suas Viagens com a Uber!

    Você já se perguntou como seria interessante explorar suas próprias jornadas com a Uber? Bem, agora você pode! Este aplicativo foi criado com o objetivo de desvendar os mistérios por trás de suas viagens e despesas, oferecendo a você uma visão detalhada de suas aventuras nas estradas.

    ### A Origem da Ideia

    A ideia para este aplicativo surgiu da curiosidade e da necessidade de compreender melhor o impacto das viagens com a Uber em nossas vidas. Afinal, o serviço revolucionou a forma como nos movemos nas cidades, tornando o transporte mais conveniente do que nunca. Mas o que essas viagens realmente representam para nós? Quanto gastamos? Quais são nossos destinos mais frequentes?

    ### A Intenção por Trás do Aplicativo

    A intenção é simples: capacitar você com informações detalhadas sobre suas viagens. Ao entender suas despesas, padrões de viagem e destinos favoritos, você pode tomar decisões mais informadas e, quem sabe, até economizar algum dinheiro. Este aplicativo visa trazer clareza para o universo de viagens com a Uber, transformando dados em conhecimento.

    ### Por Que Você Deve Explorar Seus Dados da Uber?

    **Consciência Financeira:** Conhecer o quanto você gasta com a Uber pode ajudar na gestão de suas finanças pessoais. Saiba quanto você investe em mobilidade e ajuste seu orçamento de acordo.

    **Identificação de Padrões:** Descubra quando e para onde você viaja com mais frequência. Isso pode revelar informações valiosas sobre seus hábitos e preferências de deslocamento.

    **Melhoria na Tomada de Decisões:** Com dados em mãos, você pode tomar decisões mais informadas sobre suas viagens futuras. Optar por alternativas mais econômicas ou sustentáveis é mais fácil quando você conhece suas opções.

    **Aventura e Exploração:** Além de fins práticos, explorar seus dados pode ser uma jornada fascinante por si só. Descubra curiosidades sobre suas viagens que você nunca imaginou!

    Pronto para embarcar nessa jornada de descobertas? Carregue seu arquivo CSV da Uber na aba "Visualizando os Dados" e comece a explorar suas viagens. Este aplicativo está aqui para transformar dados em insights, e nós estamos empolgados para ajudar você a aproveitar ao máximo suas experiências com a Uber!

    Não espere mais. Descubra o poder dos seus próprios dados de viagem agora!
                
    ### Veja mais dos meus projetos:
                
    Clique aqui: [**Meu Portifólio**](https://ochristopherfilipe.github.io/portifolio/index.html) e saiba mais sobre projetos e **análises descritivas e preditivas superinteressantes**!

    ''')

with tab2:
    st.title('Como Usar')
    st.markdown(r''' 

Você pode solicitar seus dados pessoais. A LGPD garante o direito de acesso aos dados pessoais tratados pela Uber.
                
### Como solicitar:
##### 1. Acessando [Esse Link](https://help.uber.com/pt-BR/lite/riders/article/solicita%C3%A7%C3%A3o-de-dados-da-uber?nodeId=f1ba2cfb-2bd0-4d49-9e68-f980cdbc8829) e seguindo os passos nas imagens abaixo:

''')
    st.image('img/solicitacao_1.png', caption='Passo 1')
    st.markdown(r''' 

#### 2. Após clicar em solicitação de dados pessoais, clique em 'solicitar' na aba de *Baixe suas informações*
''')
    
    st.image('img/solicitacao_2.png', caption='Passo 2')
    st.markdown(r''' 

#### 3. Acesse usando sua conta (a mesma que você usa pra pedir Uber)
''')
    st.image('img/solicitacao_3.png', caption='Passo 3')
    st.markdown(r''' 

#### 4. Após realizar esses passos você será informado que pode levar de 1 a 2 dias para seus dados serem enviados ao seu email.
##### * Alguns momentos depois o seguinte email chega na sua caixa de entrada:
''')
    st.image('img/solicitacao_4.png', caption='Passo 4')
    st.markdown(r''' 
##### * Clique em 'Go To Download Page' e faça o download do seu arquivo ZIP

#### 5. Extraia o arquivo ZIP e ache o arquivo 'trips_data.csv'
''')
    st.image('img/solicitacao_5.png', caption='Passo 5')

    st.markdown(''' 
                #### Após baixar o arquivo ZIP, provavelmente esse será o caminho para seu arquivo:
                ''')
    st.markdown(r''' 
                #### c:\Users\[SEU USUÁRIO]\Downloads\Uber Data B1525343.zip\Uber Data\Rider\trips_data.csv
                ''')

with tab3:
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

with tab4:
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
        st.write("Carregue um arquivo CSV na aba 'Visualizando os Dados.'")



with tab5:
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
        st.write("Carregue um arquivo CSV na aba 'Visualizando os Dados.'")



with tab6:
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
        st.write("Carregue um arquivo CSV na aba 'Visualizando os Dados.'")