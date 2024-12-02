import pandas as pd

df = pd.read_excel('./resources/recommendations.xlsx')

print(df.loc[0]['Рекомендаци'])
