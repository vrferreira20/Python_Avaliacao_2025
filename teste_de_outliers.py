import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Carregando o dataset
data = pd.read_csv("DataHouse.csv")

#print(data.shape)
#print(data.columns)

Q1 = data["price"].quantile(0.25)
Q3 = data["price"].quantile(0.75)
IQR = Q3 - Q1

# Mantém apenas os valores dentro do intervalo
data = data[(data["price"] >= Q1 - 1.5*IQR) & (data["price"] <= Q3 + 1.5*IQR)], inplace=True

print(data.shape)

plt.figure(figsize=(8,5))
sns.boxplot(y=data["price"])
plt.show()
