import pandas as pd
from sklearn.preprocessing import LabelEncoder

def LoadData(DATASET):
  df = None
  
  try:
    df = pd.read_csv(DATASET,sep=',')
    print(df)
  except:
    print('Load dataset Error!')
    
  return df
    
def DataTreat(data):
  #print(data.info())

  data.drop_duplicates(inplace=True)

  data.drop(columns=['availability','society','balcony'], inplace=True)

  data.dropna(inplace=True)

  lb = LabelEncoder()

  print(data.info())

  data['total_sqft'] = lb.fit_transform(data['total_sqft'])

  data['Room'] = data['size'].str.replace(r'[^0-9]','',regex=True)

  print(data['location'].value_counts())

  #print(data.head())

  #print(data.info())
DATASET = 'DataHouse.csv'
data = LoadData(DATASET)

if data is not None:
  DataTreat(data)