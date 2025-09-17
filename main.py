import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split


def LoadData(DATASET):
    data = None
    try:
        data = pd.read_csv(DATASET, sep=',')
        print("Dataset carregado com sucesso!")
    except:
        print("Load dataset Error!")
    return data
    

def DataTreat(data):
    # ---- Limpeza inicial ----
    data.drop_duplicates(inplace=True)                  
    data.drop(columns=['availability','society'], inplace=True, errors='ignore') # Remove as colunas availability e society, que não são relevantes. errors='ignore' evita erro se alguma dessas colunas não existir.
    data.dropna(inplace=True)                           
    # -------------------------------------------------------------------

    # ---- Trata convert_sqm ----
    def convert_sqm(x):  # 'x' representa o valor de cada célula
        x = str(x)  # Converte para string para facilitar o tratamento
    
        if '-' in x:  # Caso seja um intervalo, pega a média
            a, b = x.split('-')
            return (float(a) + float(b)) / 2
    
        elif 'Sq. Meter' in x:  # Já está em m², só remove o texto
            return float(x.replace('Sq. Meter',''))
    
        elif 'Perch' in x:  # Converte de Perch para m²
            return float(x.replace('Perch','')) * 25.2929  # 1 Perch ≈ 25.2929 m²
    
        else:
            try:
                return float(x)  # Se já for número, retorna como float
            except:
                return None  # Caso não consiga converter


    data['total_sqm'] = data['total_sqft'].apply(convert_sqm) #Aplica a função convert em toda a coluna convert_sqm, convertendo os valores para números. ->'apply(convert)' pega cada valor da coluna e passa como argumento para a função.
    #print(data['convert_sqm'])

    # -------------------------------------------------------------------

    # ---- Converte price ----
    data['price'] = (data['price'] * 100000) * 0.063 # Aprica uma conversão na coluna price. Motivo: O preço originalmente está em Lakh/Lac (uma unidade do sistema de numeração indiano), então converto ele primeiro para rúpias indianas (INR) e depois para Real (R$)
    #print(data['price'])

    # -------------------------------------------------------------------

    # ---- Remove OutLiers ----
    def remove_outliers_iqr(data, column):
        Q1 = data[column].quantile(0.25) # Calcula o 1º quartil (25%)
        Q3 = data[column].quantile(0.75) # Calcula o 2º quartil (75%)
        IQR = Q3 - Q1                    # Intervalo interquartílico (Q3 - Q1)
    
        # Mantém apenas linhas em que o valor da coluna esteja dentro dos limites:
        data_clean = data[(data[column] >= Q1 - 1.5 * IQR) & (data[column] <= Q3 + 1.5 * IQR)]

        #Por que 1.5?
        #O IQR mede a dispersão do meio dos dados (entre o 25% e 75%).
        #Multiplicar por 1.5 significa que aceita valores até 1.5 vezes a “largura normal” dos dados antes de chamar de outlier.

        return data_clean

    print("Antes:", data.shape)
    for column in ["price", "bath", "total_sqm"]:
        data = remove_outliers_iqr(data, column)
    print("Depois:", data.shape)


    # ---- Extrai número de quartos para uma nova coluna ----
    data['room'] = data['size'].str.extract(r'(\d+)').astype(float) # Usa um regex (é uma linguagem de padrões usada para encontrar e manipular textos), onde '\d+' extrai apenas os números na coluna size.

    data.drop(columns=['size','total_sqft'], inplace=True, errors='ignore')

    data['Price_per_M²'] =  data['price']/data['total_sqm']

    #lb = LabelEncoder()
    #data['location'] = lb.fit_transform(data['location'])

    #print(data.head())

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
    sns.histplot(data=data, x="total_sqm", y="price", bins=60)
    #plt.yscale(value='linear')
    plt.title("Distribuição dos preços das casas")
    plt.show()

def boxplot_room_price(data):
    sns.boxplot(data=data, x="Price_per_M²", y="room")
    plt.title("Distribuição de preço por número de quartos")
    plt.show()

def correlacao_val_num(data):
    corr = data[["price", "total_sqm", "bath"]].corr()
    sns.heatmap(corr, annot=True, cmap="coolwarm")
    plt.yticks(rotation= 360)
    plt.title("Correlação entre variáveis numéricas")
    plt.show()

def preco_med (data):
    locations = data.groupby("location")["price"].mean().sort_values(ascending=False).head(10)
    sns.barplot(x=locations.values, y=locations.index, palette='viridis')
    plt.title("Top 10 localizações com maior preço médio")
    plt.show()

def lmplot_graph (data): #  O gráfico mostra como o preço por metro quadrado varia em função do tipo da área
    sns.lmplot(data=data,x="price",y="Price_per_M²",palette="muted", hue="area_type",
    ci=None,height=4,scatter_kws={"s": 50, "alpha": 1})
    plt.yticks(rotation= 360)
    plt.show()

def conj_treino_teste(data):
    # Variável dependente (coluna 'price' no dataset original)
    y = data['price'].values  

    # Variáveis independentes (todas menos 'price')
    x = data.drop(columns=['price']).values
    #print(x)
    # Dividindo os dados em conjuntos de treino e teste
    x_treinamento, x_teste, y_treinamento, y_teste = train_test_split(x, y, test_size=0.3, random_state=12)

    return x_treinamento, x_teste, y_treinamento, y_teste

# ---------- Execução ----------
DATASET = 'DataHouse.csv'
data = LoadData(DATASET)

if data is not None:
    data = DataTreat(data)
    #dispersao_grafico(data, x_col='Price_per_M²', y_col='price')
    #distribuicao_preco(data)
    #boxplot_room_price(data)
    #correlacao_val_num(data)
    preco_med(data)
    #lmplot_graph(data)
    #conj_treino_teste(data)

