import pandas as pd

df = pd.read_csv("netflix_titles.csv")

df["date_added"] = pd.to_datetime(df["date_added"])