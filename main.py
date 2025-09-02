import pandas as pd

def LoadData(DATASET):
  df = None
  
  try:
    df = pd.read_csv(DATASET,sep=',',encoder='utf8')
    print(df)
  except:
    print('Load dataset Error!')
    
  return df
    
def DataTreat(data)
  print(data.info())

DATASET = 'insurance.csv'
data = LoadData(DATASET)
