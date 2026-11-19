"""
Data Cleaning & Preprocessing Module
Handles loading, missing values, duplicates, type conversions, and feature engineering.
"""

import os
from datetime import datetime

try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False
    import csv

def clean_data(input_path=None, output_path=None):
    """
    Cleans raw sales dataset:
    - Verifies columns and data types
    - Checks and handles null/missing values
    - Removes duplicate orders
    - Formats dates and extracts Year, Month, Year-Month, Quarter
    - Computes Profit Margin percentage
    - Saves cleaned dataset to data/cleaned_sales_data.csv
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if input_path is None:
        input_path = os.path.join(base_dir, "data", "sales_data.csv")
    if output_path is None:
        output_path = os.path.join(base_dir, "data", "cleaned_sales_data.csv")

    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Sales dataset not found at: {input_path}. Please run src/generate_data.py first.")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    if PANDAS_AVAILABLE:
        print("[INFO] Loading data with Pandas...")
        df = pd.read_csv(input_path)

        initial_rows = len(df)
        print(f"[INFO] Initial record count: {initial_rows}")

        # 1. Deduplication
        df.drop_duplicates(inplace=True)
        print(f"[INFO] Dropped {initial_rows - len(df)} duplicate records.")

        # 2. Handle Missing Values
        # Numeric columns fill with 0 or median
        numeric_cols = ["Quantity", "Unit Price", "Sales", "Cost", "Profit"]
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

        # Categorical columns fill with mode / Unknown
        categorical_cols = ["Order ID", "Customer ID", "Product Name", "Category", "Region", "City", "Payment Mode"]
        for col in categorical_cols:
            if col in df.columns:
                df[col] = df[col].fillna("Unknown").astype(str).str.strip()

        # 3. Date Parsing & Feature Engineering
        df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
        # Remove records where date is completely invalid
        df = df.dropna(subset=["Order Date"])

        df["Year"] = df["Order Date"].dt.year
        df["Month"] = df["Order Date"].dt.month
        df["Month_Name"] = df["Order Date"].dt.strftime("%b")
        df["Year_Month"] = df["Order Date"].dt.strftime("%Y-%m")
        df["Quarter"] = "Q" + df["Order Date"].dt.quarter.astype(str)
        df["Day_of_Week"] = df["Order Date"].dt.day_name()

        # 4. Computed Business Metrics
        df["Profit Margin %"] = df.apply(
            lambda r: round((r["Profit"] / r["Sales"] * 100), 2) if r["Sales"] > 0 else 0.0,
            axis=1
        )

        # 5. Sort chronologically
        df.sort_values(by="Order Date", inplace=True)
        df.reset_index(drop=True, inplace=True)

        # Save cleaned dataset
        df.to_csv(output_path, index=False)
        print(f"[SUCCESS] Cleaned data saved ({len(df)} rows) to: {output_path}")
        return df

    else:
        # Fallback pure-python cleaning if pandas is not yet installed
        print("[INFO] Pandas not detected. Performing cleaning using standard Python...")
        with open(input_path, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            raw_rows = list(reader)

        seen_orders = set()
        cleaned_rows = []

        for row in raw_rows:
            order_id = row.get("Order ID", "").strip()
            if not order_id or order_id in seen_orders:
                continue
            seen_orders.add(order_id)

            # Date handling
            order_date_str = row.get("Order Date", "").strip()
            try:
                dt = datetime.strptime(order_date_str, "%Y-%m-%d")
            except ValueError:
                continue

            try:
                sales = float(row.get("Sales", 0))
                profit = float(row.get("Profit", 0))
            except ValueError:
                sales, profit = 0.0, 0.0

            margin = round((profit / sales * 100), 2) if sales > 0 else 0.0

            row["Year"] = str(dt.year)
            row["Month"] = f"{dt.month:02d}"
            row["Month_Name"] = dt.strftime("%b")
            row["Year_Month"] = dt.strftime("%Y-%m")
            row["Quarter"] = f"Q{(dt.month - 1) // 3 + 1}"
            row["Day_of_Week"] = dt.strftime("%A")
            row["Profit Margin %"] = f"{margin:.2f}"

            cleaned_rows.append(row)

        cleaned_rows.sort(key=lambda r: r["Order Date"])

        fieldnames = list(cleaned_rows[0].keys())
        with open(output_path, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(cleaned_rows)

        print(f"[SUCCESS] Cleaned data saved ({len(cleaned_rows)} rows) to: {output_path}")
        return cleaned_rows

if __name__ == "__main__":
    clean_data()
