import pandas as pd

df = pd.read_csv('netflix_titles.csv')

# 1. Dataset Exploration
print(df.head())
print(df.tail())
print(df.sample())
print(df.info())
# print(df.describe())
print(df.shape)
print(df.columns)
print(df.mean(numeric_only=True))
print(df.index)
print(df.dtypes)
