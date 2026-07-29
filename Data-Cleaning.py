import os
import pandas as pd


# =========================================================
# 1. LOAD THE DATASET
# =========================================================

df = pd.read_csv("netflix_titles.csv")

print("=" * 60)
print("DATASET LOADED SUCCESSFULLY")
print("=" * 60)

print(f"Original number of rows: {df.shape[0]}")
print(f"Original number of columns: {df.shape[1]}")


# =========================================================
# 2. STANDARDIZE COLUMN NAMES
# =========================================================

df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

print("\nColumn names:")
print(df.columns.tolist())


# =========================================================
# 3. CHECK MISSING VALUES
# =========================================================

print("\n" + "=" * 60)
print("MISSING VALUES BEFORE CLEANING")
print("=" * 60)

missing_values = df.isna().sum()
print(missing_values)

missing_percentage = (df.isna().sum() / len(df)) * 100

missing_report = pd.DataFrame({
    "missing_values": missing_values,
    "missing_percentage": missing_percentage.round(2)
})

print("\nMissing-value report:")
print(missing_report)


# =========================================================
# 4. CHECK AND REMOVE DUPLICATE ROWS
# =========================================================

print("\n" + "=" * 60)
print("DUPLICATE CHECK")
print("=" * 60)

duplicate_count = df.duplicated().sum()

print(f"Duplicate rows found: {duplicate_count}")

df = df.drop_duplicates()

print(f"Rows after removing duplicates: {len(df)}")


# =========================================================
# 5. RENAME COLUMNS
# =========================================================

df = df.rename(
    columns={
        "listed_in": "genres"
    }
)

print("\nColumns after renaming:")
print(df.columns.tolist())


# =========================================================
# 6. CLEAN TEXT COLUMNS
# =========================================================

text_columns = [
    "show_id",
    "type",
    "title",
    "director",
    "cast",
    "country",
    "rating",
    "duration",
    "genres",
    "description"
]

for column in text_columns:
    if column in df.columns:
        df[column] = df[column].astype("string").str.strip()


# =========================================================
# 7. HANDLE MISSING TEXT VALUES
# =========================================================

columns_to_fill = {
    "director": "Unknown",
    "cast": "Unknown",
    "country": "Unknown",
    "rating": "Unknown",
    "duration": "Unknown",
    "genres": "Unknown",
    "description": "No description available"
}

for column, replacement_value in columns_to_fill.items():
    if column in df.columns:
        df[column] = df[column].fillna(replacement_value)


# =========================================================
# 8. CLEAN AND CONVERT DATE_ADDED
# =========================================================

if "date_added" in df.columns:
    df["date_added"] = df["date_added"].astype("string").str.strip()

    df["date_added"] = pd.to_datetime(
        df["date_added"],
        format="%B %d, %Y",
        errors="coerce"
    )

print("\nDate column datatype:")
print(df["date_added"].dtype)

invalid_dates = df["date_added"].isna().sum()

print(f"Missing or invalid dates: {invalid_dates}")


# =========================================================
# 9. CREATE DATE-BASED COLUMNS
# =========================================================

df["year_added"] = df["date_added"].dt.year
df["month_added"] = df["date_added"].dt.month
df["day_added"] = df["date_added"].dt.day
df["month_name"] = df["date_added"].dt.month_name()
df["day_name"] = df["date_added"].dt.day_name()


# =========================================================
# 10. CLEAN RELEASE_YEAR
# =========================================================

df["release_year"] = pd.to_numeric(
    df["release_year"],
    errors="coerce"
)

invalid_release_years = df["release_year"].isna().sum()

print(f"Missing or invalid release years: {invalid_release_years}")

df["release_year"] = df["release_year"].astype("Int64")


# =========================================================
# 11. SPLIT DURATION INTO NUMBER AND UNIT
# =========================================================

df["duration_number"] = (
    df["duration"]
    .str.extract(r"(\d+)", expand=False)
)

df["duration_number"] = pd.to_numeric(
    df["duration_number"],
    errors="coerce"
)

df["duration_unit"] = (
    df["duration"]
    .str.extract(r"([A-Za-z]+)", expand=False)
    .str.lower()
)


# =========================================================
# 12. CREATE CONTENT AGE
# =========================================================

df["content_age_at_addition"] = (
    df["year_added"] - df["release_year"]
)

df.loc[
    df["content_age_at_addition"] < 0,
    "content_age_at_addition"
] = pd.NA


# =========================================================
# 13. CREATE GENRE COUNT
# =========================================================

df["genre_count"] = (
    df["genres"]
    .str.split(",")
    .str.len()
)

df.loc[
    df["genres"] == "Unknown",
    "genre_count"
] = 0


# =========================================================
# 14. CREATE CAST COUNT
# =========================================================

df["cast_count"] = (
    df["cast"]
    .str.split(",")
    .str.len()
)

df.loc[
    df["cast"] == "Unknown",
    "cast_count"
] = 0


# =========================================================
# 15. STANDARDIZE TYPE VALUES
# =========================================================

df["type"] = df["type"].str.title()

valid_types = ["Movie", "Tv Show"]

invalid_type_rows = ~df["type"].isin(valid_types)

print(
    f"Rows containing unexpected content types: "
    f"{invalid_type_rows.sum()}"
)


# =========================================================
# 16. CHECK FOR DUPLICATE SHOW IDS
# =========================================================

duplicate_show_ids = df["show_id"].duplicated().sum()

print(f"Duplicate show IDs: {duplicate_show_ids}")

if duplicate_show_ids > 0:
    df = df.drop_duplicates(
        subset="show_id",
        keep="first"
    )


# =========================================================
# 17. RESET THE INDEX
# =========================================================

df = df.reset_index(drop=True)


# =========================================================
# 18. FINAL VALIDATION
# =========================================================

print("\n" + "=" * 60)
print("FINAL DATASET INFORMATION")
print("=" * 60)

df.info()

print("\nMissing values after cleaning:")
print(df.isna().sum())

print("\nDuplicate rows after cleaning:")
print(df.duplicated().sum())

print("\nFirst five cleaned rows:")
print(df.head())

print("\nFinal dataset dimensions:")
print(f"Rows: {df.shape[0]}")
print(f"Columns: {df.shape[1]}")


# =========================================================
# 19. EXPORT THE CLEANED DATASET
# =========================================================

output_directory = "output"
output_file = os.path.join(
    output_directory,
    "cleaned_netflix_titles.csv"
)

os.makedirs(
    output_directory,
    exist_ok=True
)

df.to_csv(
    output_file,
    index=False
)

print("\n" + "=" * 60)
print("CLEANING COMPLETED")
print("=" * 60)

print(f"Cleaned dataset saved to: {output_file}")
