import pandas as pd

df = pd.read_csv("netflix_titles.csv")
print(df.isnull().mean() * 100)
