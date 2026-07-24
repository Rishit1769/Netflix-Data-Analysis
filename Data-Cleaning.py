import pandas as pd

df = pd.read_csv("netflix_titles.csv")
print(df.isnull().sum())
print(df.isnull().mean() * 100)
print(df.duplicated().sum())

print(df.rename(columns={
    "listed_in": "genres",
    "description": "about"
}, inplace=True))
print(df)

df["date_added"] = df["date_added"].str.strip()

df["date_added"] = pd.to_datetime(
    df["date_added"],
    format="%B %d, %Y"
)
print(df)

df["year_added"] = df["date_added"].dt.year
df["month_added"] = df["date_added"].dt.month
df["day_added"] = df["date_added"].dt.day

print(df[df["director"].isnull()])

print(df.info())
print(df.isnull().sum())
