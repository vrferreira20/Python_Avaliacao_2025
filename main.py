import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder


def LoadData(DATASET):
    df = None
    try:
        df = pd.read_csv(DATASET, sep=',')
        print("Dataset carregado com sucesso!")
    except:
        print("Load dataset Error!")
    return df
    

def DataTreat(data):
    # ---- Limpeza inicial ----
    data.drop_duplicates(inplace=True)                  
    data.drop(columns=['availability','society'], inplace=True, errors='ignore') # Remove as colunas availability e society, que não são relevantes. errors='ignore' evita erro se alguma dessas colunas não existir.
    data.dropna(inplace=True)                           

    # ---- Trata total_sqft ----
    def convert_sgft(x): # 'x' representa o valor de cada coluna
        x = str(x) #Converte o valor para string (facilita o tratamento de ranges e textos).
        if '-' in x:
            a, b = x.split('-')
            return (float(a) + float(b)) / 2 #Caso x seja um intervalo (ex.: "2100-2850"), divide em dois valores e tira a média.
        
        elif 'Sq. Meter' in x:
            return float(x.replace('Sq. Meter','')) * 10.7639 #Caso esteja em m², remove o texto "Sq. Meter", transforma em número e converte para sqft (1 m² = 10.7639 sqft).
        
        elif 'Perch' in x:
            return float(x.replace('Perch','')) * 272.25 #Caso esteja em Perch (medida usada em alguns países), converte para sqft.
        
        else:
            try:
                return float(x)
            except:
                return None #Caso seja apenas um número (ex.: "2100"), converte para float. Se não conseguir converter, retorna None.


    data['total_sqft'] = data['total_sqft'].apply(convert_sgft) #Aplica a função convert em toda a coluna total_sqft, convertendo os valores para números. ->'apply(convert)' pega cada valor da coluna e passa como argumento para a função.
    #print(data['total_sqft'])

     # ---- Converte price ----
    data['price'] = (data['price'] * 100000) * 0.063 # Aprica uma conversão na coluna price. Motivo: O preço originalmente está em Lakh/Lac (uma unidade do sistema de numeração indiano), então converto ele primeiro para rúpias indianas (INR) e depois para Real (R$)
    #print(data['price'])

    # ---- Extrai número de quartos para uma nova coluna ----
    data['room'] = data['size'].str.extract(r'(\d+)').astype(float) # Usa um regex (é uma linguagem de padrões usada para encontrar e manipular textos), onde '\d+' extrai apenas os números na coluna size.

    lb = LabelEncoder()
    data['location'] = lb.fit_transform(data['location'])
    print(data.head())

    return data
def dispersao_grafico(data, x_col, y_col):
    plt.figure(figsize=(8,6))
    plt.scatter(data[x_col], data[y_col], color = 'blue', alpha=0.6) # Plota todos os pontos de uma vez, colorindo pela classe
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    plt.title(f'Dispersão Binomial: {x_col} x {y_col}')
    plt.show()

def distribuicao_preco(data):
    plt.figure(figsize=(8,6))
    sns.histplot(data=data, x="total_sqft" ,y="price", bins=60)
    #plt.yscale(value='linear')
    plt.title("Distribuição dos preços das casas")
    plt.show()

def boxplot_room_price(data):
    sns.boxplot(data=data, x="total_sqft", y="price")
    plt.xticks(rotation=45)
    plt.title("Distribuição de preço por número de quartos")
    plt.show()

#esse heatmap trás uma correlação não muito relevante
def correlacao_val_num(data):
    corr = data[["price", "total_sqft", "bath"]].corr()
    sns.heatmap(corr, annot=True, cmap="coolwarm")
    plt.yticks(rotation= 360)
    plt.title("Correlação entre variáveis numéricas")
    plt.show()

def preco_med (data):
    locations = data.groupby("location")["price"].mean().sort_values(ascending=False).head(10)
    sns.barplot(x=locations.values, y=locations.index, palette='viridis')
    plt.title("Top 10 localizações com maior preço médio")
    plt.show()

# ---------- Execução ----------
DATASET = 'DataHouse.csv'
data = LoadData(DATASET)

if data is not None:
    data = DataTreat(data)
    #dispersao_grafico(data, x_col='total_sqft', y_col='price')
    #distribuicao_preco(data)
    #boxplot_room_price(data)
    #correlacao_val_num(data)
    #preco_med(data)

