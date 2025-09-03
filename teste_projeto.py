import pandas as pd

#Comando para ler o CSV
'''
data = pd.read_csv('bengaluru_house_prices.csv')
print (data)
'''
#Função de carregar os dados
def uploadData(nomeArquivo):
    data_up = None
    try:
        data_up = pd.read_csv(nomeArquivo, sep=',')

    except:
        print("Erro no upload de dados")
    
    return data_up

#Função para preparar os dados
def prepareData(p_data):
    print ('Preparando dados')
    
    # verificar informações rápidas do arquivo: tipos, nome, dados nulos
    #print(p_data.info())

    # retorna as primeiras 5 linhas do arquivo
    #print(p_data.head())

    # retorna as ultimas 5 linhas do arquivo
    #print(p_data.tail())

    # retorna uma estatistica básica sobre as colunas
    #print(p_data.describe())

    # remove os registros duplicados
    #p_data.drop_duplicates(inplace=True)
    #p_data.drop(columns=['bath', 'balcony'], inplace=True)
    #print(p_data)

    # remove os dados nulos do dataset
    #p_data.dropna(inplace=True)
    #print(p_data)

    # Selecionando apenas uma coluna
    #print(p_data['size'])

    # fatiamento para retornar multiplas linhas
    #print (p_data[0:2])

    # fatiamento para retornar uma linha específica com base no índice
    #print (p_data.loc[10])

    #Ordenamento do DataFrame por valores de uma ou mais colunas
    #p_data.sort_values(by=['size', 'price'], ascending=False, inplace=True)
    #print(p_data)

    #Mudando o nome das colunas
    #p_data.rename(columns={'price': 'preco'}, inplace = True)
    print(p_data)


#Espaço para definição do arquivo
NOMEARQUIVO = 'bengaluru_house_prices.csv'
data_nome = uploadData(NOMEARQUIVO)

if data_nome is not None:
    prepareData(data_nome)