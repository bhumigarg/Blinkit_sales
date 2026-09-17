"""
Blinkit Sales Analysis in Python
Follows the business requirements from the tutorial:
  KPIs   -> Total Sales, Average Sales, Number of Items Sold, Average Rating
  Charts -> Sales by Fat Content, Sales by Item Type, Fat Content by Outlet
            (stacked), Sales by Outlet Establishment Year, Sales by Outlet
            Size, Sales by Outlet Location

Run: python blinkit_analysis.py
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # non-interactive backend: save PNGs instead of opening windows
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

HERE = Path(__file__).parent
DATA_PATH = HERE / "data" / "BlinkIT Grocery Data.csv"

# ---------------------------------------------------------------------------
# 1. Import raw data
# ---------------------------------------------------------------------------
df = pd.read_csv(DATA_PATH)

print(f"Size of data: {df.shape}")
print(f"Columns: {list(df.columns)}")
print(df.dtypes)

# ---------------------------------------------------------------------------
# 2. Data cleaning
# ---------------------------------------------------------------------------
# Item Fat Content has inconsistent labels: LF/low fat -> Low Fat, reg -> Regular
print("\nUnique values before cleaning:", df["Item Fat Content"].unique())

df["Item Fat Content"] = df["Item Fat Content"].replace(
    {"LF": "Low Fat", "low fat": "Low Fat", "reg": "Regular"}
)

print("Unique values after cleaning:", df["Item Fat Content"].unique())

# ---------------------------------------------------------------------------
# 3. KPIs
# ---------------------------------------------------------------------------
total_sales = df["Sales"].sum()
average_sales = df["Sales"].mean()
number_of_items_sold = df["Sales"].count()
average_ratings = df["Rating"].mean()

print(f"\nTotal Sales: ${total_sales:,.1f}")
print(f"Average Sales: ${average_sales:,.1f}")
print(f"Number of Items Sold: {number_of_items_sold:,.0f}")
print(f"Average Ratings: {average_ratings:,.1f}")

# ---------------------------------------------------------------------------
# 4. Charts
# ---------------------------------------------------------------------------

# 4.1 Total sales by fat content -> pie chart
sales_by_fat = df.groupby("Item Fat Content")["Sales"].sum()

plt.pie(
    sales_by_fat,
    labels=sales_by_fat.index,
    autopct="%1.1f%%",
    startangle=90,
)
plt.title("Sales by Fat Content")
plt.axis("equal")
plt.tight_layout()
plt.savefig(HERE / "charts_sales_by_fat_content.png")
plt.close()

# 4.2 Total sales by item type -> bar chart
sales_by_type = df.groupby("Item Type")["Sales"].sum().sort_values(ascending=False)

plt.figure(figsize=(10, 6))
bars = plt.bar(sales_by_type.index, sales_by_type.values)
plt.xticks(rotation=-90)
plt.xlabel("Item Type")
plt.ylabel("Total Sales")
plt.title("Total Sales by Item Type")
for bar in bars:
    height = bar.get_height()
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        height,
        f"{height:,.0f}",
        ha="center",
        va="bottom",
        fontsize=8,
    )
plt.tight_layout()
plt.savefig(HERE / "charts_sales_by_item_type.png")
plt.close()

# 4.3 Fat content by outlet for total sales -> grouped bar chart
sales_by_fat_outlet = (
    df.groupby(["Outlet Location Type", "Item Fat Content"])["Sales"].sum().unstack()
)

ax = sales_by_fat_outlet.plot(kind="bar", figsize=(10, 6))
plt.xlabel("Outlet Location Tier")
plt.ylabel("Total Sales")
plt.title("Fat Content by Outlet for Total Sales")
plt.tight_layout()
plt.savefig(HERE / "charts_fat_content_by_outlet.png")
plt.close()

# 4.4 Total sales by outlet establishment year -> line chart
sales_by_year = df.groupby("Outlet Establishment Year")["Sales"].sum().sort_index()

plt.figure(figsize=(9, 5))
plt.plot(sales_by_year.index, sales_by_year.values, marker="o", linestyle="--")
plt.xlabel("Outlet Establishment Year")
plt.ylabel("Total Sales")
plt.title("Total Sales by Outlet Establishment")
plt.tight_layout()
plt.savefig(HERE / "charts_sales_by_establishment_year.png")
plt.close()

# 4.5 Sales by outlet size -> pie chart
sales_by_size = df.groupby("Outlet Size")["Sales"].sum()

plt.figure(figsize=(4, 4))
plt.pie(sales_by_size, labels=sales_by_size.index, autopct="%1.1f%%", startangle=90)
plt.title("Sales by Outlet Size")
plt.axis("equal")
plt.tight_layout()
plt.savefig(HERE / "charts_sales_by_outlet_size.png")
plt.close()

# 4.6 Sales by outlet location -> horizontal bar chart
sales_by_location = (
    df.groupby("Outlet Location Type")["Sales"].sum().sort_values(ascending=False)
)

plt.figure(figsize=(8, 3))
sns.barplot(x=sales_by_location.values, y=sales_by_location.index)
plt.title("Sales by Outlet Location")
plt.xlabel("Total Sales")
plt.ylabel("Outlet Location Type")
plt.tight_layout()
plt.savefig(HERE / "charts_sales_by_outlet_location.png")
plt.close()

print("\nAll charts saved as PNG files in", HERE)
