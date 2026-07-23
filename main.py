import pandas as pd

df = pd.read_csv('netflix_titles.csv')

# 1. Dataset Exploration
head = df.head()
print(head.to_string())
