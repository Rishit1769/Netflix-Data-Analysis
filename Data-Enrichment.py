import pandas as pd

df = pd.read_csv("netflix_titles.csv")

df["date_added"] = pd.to_datetime(df["date_added"].str.strip())

df["year_added"] = df["date_added"].dt.year

print(df["year_added"])