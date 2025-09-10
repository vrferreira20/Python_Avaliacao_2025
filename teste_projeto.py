import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder


#Comando para ler o CSV
#Função de carregar os dados
def uploadData(NOMEARQUIVO):
    df = None
    try:
        df = pd.read_csv(NOMEARQUIVO, sep=',')
    except:
        print("Erro no upload de dados")
    
    return df

#Função para preparar os dados
def prepareData(data):
    print ('Preparando dados')

    lb = LabelEncoder()
    # verificar informações rápidas do arquivo: tipos, nome, dados nulos
    #print(data.info())

    # retorna as primeiras 5 linhas do arquivo
    #print(p_data.head())

    # retorna as ultimas 5 linhas do arquivo
    #print(p_data.tail())

    # retorna uma estatistica básica sobre as colunas
    #print(p_data.describe())

    #remove os registros duplicados
    data.drop_duplicates(inplace=True)
    data.drop(columns=['balcony','availability','society'], inplace=True)

    # remove os dados nulos do dataset
    #p_data.dropna(inplace=True)
    #print(p_data)
    # Selecionando apenas uma coluna
    #print(p_data['size'])
    # fatiamento para retornar multiplas linhas
    #print (p_data[0:2]
    # fatiamento para retornar uma linha específica com base no índice
    #print (p_data.loc[10])

    #Ordenamento do DataFrame por valores de uma ou mais colunas
    #p_data.sort_values(by=['size', 'price'], ascending=False, inplace=True)
    #print(p_data)
    #Mudando o nome das colunas
    #p_data.rename(columns={'price': 'preco'}, inplace = True)

    # Usa um regex (é uma linguagem de padrões usada para encontrar e manipular textos), onde '\d+' extrai apenas os números na coluna size.
    data['room'] = data['size'].str.extract(r'(\d+)').astype(float)

    data['location'] = lb.fit_transform(data['location'])

    data.drop(columns=['size'], inplace=True)

    #print(data['location'].value_counts())

    #print(data.info())

    #print(data.head())

    return data

def heatMap(data):
    df = (data[['price','room','bath']].corr())
    sns.heatmap(df, annot=True, cmap="viridis", cbar=True)
    plt.show()

#Espaço para definição do arquivo
NOMEARQUIVO = 'DataHouse.csv'
data = uploadData(NOMEARQUIVO)

if data is not None:
    prepareData(data)
    heatMap(data)