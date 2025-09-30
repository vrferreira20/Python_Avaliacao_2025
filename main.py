import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split


def loaddata(DATASET):
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
    data.drop(columns=['availability', 'society'], inplace=True,
              errors='ignore')  # Remove as colunas availability e society, que não são relevantes. errors='ignore' evita erro se alguma dessas colunas não existir.
    data.dropna(inplace=True)

    # -------------------------------------------------------------------

    # ---- Tratamento do convert_sqm ----
    def convert_sqm(v_col):  # 'v_col' representa o valor de cada célula
        v_col = str(v_col)  # Converte para string para facilitar o tratamento

        if '-' in v_col:  # Caso seja um intervalo, pega a média
            a, b = v_col.split('-')
            return (float(a) + float(b)) / 2

        elif 'Sq. Meter' in v_col:  # Já está em m², só remove o texto
            return float(v_col.replace('Sq. Meter', ''))

        elif 'Perch' in v_col:  # Converte de Perch para m²
            return float(v_col.replace('Perch', '')) * 25.2929  # 1 Perch ≈ 25.2929 m²

        else:
            try:
                return float(v_col) / 10.764  # Se já for número, retorna como float e convertendo para metro quadrado
            except:
                return None  # Caso não consiga converter

    data['total_sqm'] = data['total_sqft'].apply(
        convert_sqm)  # Aplica a função convert em toda a coluna convert_sqm, convertendo os valores para números. ->'apply(convert)' pega cada valor da coluna e passa como argumento para a função.
    data = data[data['total_sqm'].notna()]  # Remove linhas que não foram convertidas
    data['total_sqm'] = data['total_sqm'].round(3)

    # -------------------------------------------------------------------

    # ---- Traduz area_type ----
    def traduz_a_type(v_col):
        mapa = {
            "super built-up area": "Zona Densamente Urbanizada",
            "plot area": "Terreno/Parcela de terra",
            "built-up area": "Área construída/edificada",
            "carpet area": "Área útil líquida"
        }
        v_col = " ".join(
            str(v_col).lower().split())  # Força a ser uma string, coloca em minúsculo, remove espaços extras no início, fim ou no meio.
        return mapa.get(v_col, None)  # Caso a chave não exista retorna o valor como ausente que mais tarde é excluido

    data['tipo_area'] = data['area_type'].apply(traduz_a_type)
    data = data[data['tipo_area'].notna()]

    # -------------------------------------------------------------------

    # ---- Converte price ----
    data['price'] = (data['price'] * 100000) * 0.063  # Aplica uma conversão na coluna price. Motivo: O preço originalmente está em Lakh/Lac (uma unidade do sistema de numeração indiano), então converto ele primeiro para rúpias indianas (INR) e depois para Real (R$)

    # -------------------------------------------------------------------
    # print(data['price'])

    # ---- Remove OutLiers ----
    def remove_outliers_iqr(data, column):
        Q1 = data[column].quantile(0.25)  # Calcula o 1º quartil (25%)
        Q3 = data[column].quantile(0.75)  # Calcula o 2º quartil (75%)
        IQR = Q3 - Q1  # Intervalo interquartílico (Q3 - Q1)

        # Mantém apenas linhas em que o valor da coluna esteja dentro dos limites:
        data_clean = data[(data[column] >= Q1 - 1.5 * IQR) & (data[column] <= Q3 + 1.5 * IQR)]

        # Por que 1.5?
        # O IQR mede a dispersão do meio dos dados (entre o 25% e 75%).
        # Multiplicar por 1.5 significa que aceita valores até 1.5 vezes a “largura normal” dos dados antes de chamar de outlier.

        return data_clean

    print("Antes:", data.shape)
    for column in ["price", "bath", "total_sqm"]:
        data = remove_outliers_iqr(data, column)
    print("Depois:", data.shape)
    # ----------------------------------------------------------------  ---

    # ---- Extrai número de quartos para uma nova coluna ----
    data['room'] = data['size'].str.extract(r'(\d+)').astype(
        float)  # Usa um regex (é uma linguagem de padrões usada para encontrar e manipular textos), onde '\d+' extrai apenas os números na coluna size.

    # ---- Converte os valores que não precisam ser decimais em inteiro ----

    data['room'] = data['room'].astype(int)
    data['bath'] = data['bath'].astype(int)
    data['balcony'] = data['balcony'].astype(int)

    # ---- Dropa as colunas não mais utilizadas ----
    data.drop(columns=['size', 'total_sqft', 'area_type'], inplace=True, errors='ignore')

    # ---- Gera o preço por Metro Quadrado ----
    data['Price_per_M²'] = data['price'] / data['total_sqm']
    data['Price_per_M²'] = data['Price_per_M²'].round(2)

    # lb = LabelEncoder()
    # data['location'] = lb.fit_transform(data['location'])

    # print(data.head())
    # ---- Faz o download do data set final com todas as sua aplicações ----

    data.to_csv('DataHouseTreated.csv', index=False)

    print(data.info())

    return data

def dispersao_grafico(data, x_col, y_col):
    plt.figure(figsize=(8, 6))
    plt.scatter(data[x_col], data[y_col], color='blue', alpha=0.6)
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    plt.title(f'Dispersão: {x_col} x {y_col}')
    plt.show()

def distribuicao_preco(data):
    plt.figure(figsize=(8, 6))
    sns.histplot(data=data, x="price", multiple='stack', bins=60)
    # plt.yscale(value='linear')
    plt.title("Distribuição dos preços das casas")
    plt.show()

def boxplot(data):
    top_locations = data['location'].value_counts().nlargest(10).index
    data_top = data[data['location'].isin(top_locations)]


    plt.figure(figsize=(10, 6))
    sns.boxplot(x="location", y="Price_per_M²", data=data_top)
    plt.title("Preço do metro Quadrado X Pelas localizações mais frequentes")
    plt.ylabel("Preço por M²")
    plt.xlabel("Localização")
    plt.xticks(rotation=45)
    plt.show()

def correlacao_val_num(data):
    corr = data[["price", "total_sqm", "bath"]].corr()
    sns.heatmap(corr, annot=True, cmap="coolwarm")
    plt.yticks(rotation=360)
    plt.title("Correlação entre variáveis numéricas")
    plt.show()

def preco_med(data):
    locations = data.groupby("location")["price"].mean().sort_values(ascending=False).head(10)
    sns.barplot(x=locations.values, y=locations.index, palette='viridis')
    plt.title("Top 10 localizações com maior preço médio")
    plt.show()

def lmplot_graph(data):
    sns.lmplot(
    data=data, 
    x="price", 
    y="Price_per_M²",
    hue="tipo_area",     # cores diferentes para cada tipo de área
    col="tipo_area",     # cria um gráfico separado para cada tipo de área
    col_wrap=2,          # organiza em até 2 colunas
    height=4,            # tamanho de cada facet
    scatter_kws={"s": 20, "alpha": 0.7}  # estética dos pontos
    )

    plt.show()

def conj_treino_teste(data):
    # Variável dependente (coluna 'price' no dataset original)
    y = data['price'].values

    # Variáveis independentes (todas menos 'price')
    x = data.drop(columns=['price']).values
    # print(x)
    # Dividindo os dados em conjuntos de treino e teste
    x_treinamento, x_teste, y_treinamento, y_teste = train_test_split(x, y, test_size=0.3, random_state=42)

    return x_treinamento, x_teste, y_treinamento, y_teste

def scatterplot(data):
    data['NDC'] = data['room'] + data['bath'] + data['balcony'] / 3

    sns.relplot(data, x='total_sqm', y='price', hue='NDC')
    plt.xlabel('Área Total (sqm)')
    plt.ylabel('Preço')
    plt.show()

# ---------- Execução ----------
DATASET = 'DataHouse.csv'
data = loaddata(DATASET)

if data is not None:
    data = DataTreat(data)
    # dispersao_grafico(data, x_col='Price_per_M²', y_col='price')
    # distribuicao_preco(data)
    #boxplot(data)
    #scatterplot(data)
    # correlacao_val_num(data)
    # preco_med(data)
    lmplot_graph(data)
    # conj_treino_teste(data)