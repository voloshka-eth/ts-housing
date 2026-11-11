
import pandas as pd
from pathlib import Path

path = Path("..") / "data" / "rentals_clean.jsonl"

df = pd.read_json(path)

print("=== DATASET ===")
print("Apartments:", len(df))
print("Duplicates:", df["url"].duplicated().sum())

print("\n=== PRICES ===")
print(df["price"].describe())

print("\n=== AREAS ===")
print(df["area_m2"].describe())

print("\n=== PRICE PER M2 ===")
df["calculated_price_m2"] = df["price"] / df["area_m2"]
print(df["calculated_price_m2"].describe())

print("\n=== CITIES ===")
print(df.groupby("city_clean")["price"].agg(
    ["count", "median", "mean", "min", "max"]
).round(2))

print("\n=== LOCATION ACCURACY ===")
if "location_approximate" in df.columns:
    print(df["location_approximate"].value_counts(dropna=False))

print("\n=== SUSPICIOUS PRICES PER M2 ===")
suspicious = df[
    (df["calculated_price_m2"] < 15)
    | (df["calculated_price_m2"] > 250)
]

print("Suspicious listings:", len(suspicious))
print(suspicious[
    ["id", "city_clean", "price", "area_m2", "calculated_price_m2"]
].head(15).to_string(index=False))
