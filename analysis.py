"""
Exploratory Data Analysis (EDA) & Business KPI Engine
Performs aggregation, trend analysis, category/regional breakdowns,
and exports Power BI-ready summaries.
"""

import os
import csv
from collections import defaultdict

try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False

def run_analysis(cleaned_data_path=None, outputs_dir=None):
    """
    Performs full exploratory data analysis and exports summaries:
    - Overall KPI metrics
    - Monthly sales & profit trends
    - Category-wise performance
    - Regional breakdown
    - Top 10 best-selling products
    - Payment mode distribution
    - Customer leaderboard
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if cleaned_data_path is None:
        cleaned_data_path = os.path.join(base_dir, "data", "cleaned_sales_data.csv")
    if outputs_dir is None:
        outputs_dir = os.path.join(base_dir, "outputs")

    os.makedirs(outputs_dir, exist_ok=True)

    if not os.path.exists(cleaned_data_path):
        # If cleaned data does not exist, run data_cleaning first
        from data_cleaning import clean_data
        clean_data()

    if PANDAS_AVAILABLE:
        print("[INFO] Performing analysis using Pandas...")
        df = pd.read_csv(cleaned_data_path)

        # 1. Overall KPIs
        total_revenue = float(df["Sales"].sum())
        total_cost = float(df["Cost"].sum())
        total_profit = float(df["Profit"].sum())
        total_orders = int(df["Order ID"].nunique())
        total_quantity = int(df["Quantity"].sum())
        overall_margin = round((total_profit / total_revenue * 100), 2) if total_revenue > 0 else 0.0
        avg_order_value = round((total_revenue / total_orders), 2) if total_orders > 0 else 0.0
        unique_customers = int(df["Customer ID"].nunique())

        kpis = {
            "Total Revenue ($)": [round(total_revenue, 2)],
            "Total Cost ($)": [round(total_cost, 2)],
            "Total Profit ($)": [round(total_profit, 2)],
            "Overall Profit Margin (%)": [overall_margin],
            "Total Orders": [total_orders],
            "Total Units Sold": [total_quantity],
            "Average Order Value ($)": [avg_order_value],
            "Unique Customers": [unique_customers]
        }
        kpi_df = pd.DataFrame(kpis)
        kpi_df.to_csv(os.path.join(outputs_dir, "kpi_summary.csv"), index=False)

        # 2. Monthly Trend Analysis
        monthly_df = df.groupby(["Year", "Month", "Year_Month"]).agg(
            Revenue=("Sales", "sum"),
            Cost=("Cost", "sum"),
            Profit=("Profit", "sum"),
            Order_Count=("Order ID", "nunique"),
            Quantity_Sold=("Quantity", "sum")
        ).reset_index()
        monthly_df["Profit_Margin_%"] = (monthly_df["Profit"] / monthly_df["Revenue"] * 100).round(2)
        monthly_df.sort_values(by="Year_Month", inplace=True)
        monthly_df.to_csv(os.path.join(outputs_dir, "monthly_sales.csv"), index=False)

        # 3. Category Analysis
        cat_df = df.groupby("Category").agg(
            Revenue=("Sales", "sum"),
            Profit=("Profit", "sum"),
            Units_Sold=("Quantity", "sum"),
            Total_Orders=("Order ID", "nunique")
        ).reset_index()
        cat_df["Revenue_Share_%"] = (cat_df["Revenue"] / total_revenue * 100).round(2)
        cat_df["Profit_Margin_%"] = (cat_df["Profit"] / cat_df["Revenue"] * 100).round(2)
        cat_df.sort_values(by="Revenue", ascending=False, inplace=True)
        cat_df.to_csv(os.path.join(outputs_dir, "category_analysis.csv"), index=False)

        # 4. Regional Analysis
        region_df = df.groupby("Region").agg(
            Revenue=("Sales", "sum"),
            Profit=("Profit", "sum"),
            Total_Orders=("Order ID", "nunique"),
            Units_Sold=("Quantity", "sum")
        ).reset_index()
        region_df["Profit_Margin_%"] = (region_df["Profit"] / region_df["Revenue"] * 100).round(2)
        region_df.sort_values(by="Revenue", ascending=False, inplace=True)
        region_df.to_csv(os.path.join(outputs_dir, "regional_analysis.csv"), index=False)

        # 5. Top 10 Best-Selling Products
        top_prod_df = df.groupby(["Product Name", "Category"]).agg(
            Revenue=("Sales", "sum"),
            Profit=("Profit", "sum"),
            Units_Sold=("Quantity", "sum")
        ).reset_index()
        top_prod_df["Profit_Margin_%"] = (top_prod_df["Profit"] / top_prod_df["Revenue"] * 100).round(2)
        top_prod_df.sort_values(by="Revenue", ascending=False, inplace=True)
        top_10_products = top_prod_df.head(10)
        top_10_products.to_csv(os.path.join(outputs_dir, "top_products.csv"), index=False)

        # 6. Payment Mode Distribution
        payment_df = df.groupby("Payment Mode").agg(
            Transactions=("Order ID", "count"),
            Revenue=("Sales", "sum")
        ).reset_index()
        payment_df["Transaction_Share_%"] = (payment_df["Transactions"] / len(df) * 100).round(2)
        payment_df.sort_values(by="Revenue", ascending=False, inplace=True)
        payment_df.to_csv(os.path.join(outputs_dir, "payment_mode_analysis.csv"), index=False)

        # 7. Customer Insights (Top 10 Customers)
        cust_df = df.groupby("Customer ID").agg(
            Total_Spend=("Sales", "sum"),
            Total_Profit=("Profit", "sum"),
            Order_Count=("Order ID", "nunique"),
            Units_Bought=("Quantity", "sum")
        ).reset_index()
        cust_df.sort_values(by="Total_Spend", ascending=False, inplace=True)
        top_customers = cust_df.head(10)
        top_customers.to_csv(os.path.join(outputs_dir, "top_customers.csv"), index=False)

        print("[SUCCESS] All analysis summaries exported to outputs/ folder!")
        return {
            "kpis": kpi_df,
            "monthly": monthly_df,
            "category": cat_df,
            "region": region_df,
            "top_products": top_10_products,
            "payment": payment_df,
            "top_customers": top_customers
        }

    else:
        # Pure Python fallback
        print("[INFO] Pandas not detected. Performing aggregation with Python standard library...")
        with open(cleaned_data_path, mode="r", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))

        total_revenue = sum(float(r["Sales"]) for r in rows)
        total_cost = sum(float(r["Cost"]) for r in rows)
        total_profit = sum(float(r["Profit"]) for r in rows)
        total_quantity = sum(int(r["Quantity"]) for r in rows)
        order_ids = set(r["Order ID"] for r in rows)
        total_orders = len(order_ids)
        customer_ids = set(r["Customer ID"] for r in rows)
        unique_customers = len(customer_ids)
        overall_margin = round((total_profit / total_revenue * 100), 2) if total_revenue > 0 else 0.0
        avg_order_value = round((total_revenue / total_orders), 2) if total_orders > 0 else 0.0

        # Export KPI Summary
        kpi_path = os.path.join(outputs_dir, "kpi_summary.csv")
        with open(kpi_path, mode="w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["Metric", "Value"])
            w.writerow(["Total Revenue ($)", f"{total_revenue:.2f}"])
            w.writerow(["Total Cost ($)", f"{total_cost:.2f}"])
            w.writerow(["Total Profit ($)", f"{total_profit:.2f}"])
            w.writerow(["Overall Profit Margin (%)", f"{overall_margin:.2f}"])
            w.writerow(["Total Orders", total_orders])
            w.writerow(["Total Units Sold", total_quantity])
            w.writerow(["Average Order Value ($)", f"{avg_order_value:.2f}"])
            w.writerow(["Unique Customers", unique_customers])

        # Monthly aggregation
        monthly = defaultdict(lambda: {"Revenue": 0.0, "Cost": 0.0, "Profit": 0.0, "Quantity": 0, "Orders": set()})
        for r in rows:
            ym = r.get("Year_Month", r["Order Date"][:7])
            monthly[ym]["Revenue"] += float(r["Sales"])
            monthly[ym]["Cost"] += float(r["Cost"])
            monthly[ym]["Profit"] += float(r["Profit"])
            monthly[ym]["Quantity"] += int(r["Quantity"])
            monthly[ym]["Orders"].add(r["Order ID"])

        monthly_path = os.path.join(outputs_dir, "monthly_sales.csv")
        with open(monthly_path, mode="w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["Year_Month", "Revenue", "Cost", "Profit", "Quantity_Sold", "Order_Count", "Profit_Margin_%"])
            for ym in sorted(monthly.keys()):
                m = monthly[ym]
                margin = round((m["Profit"] / m["Revenue"] * 100), 2) if m["Revenue"] > 0 else 0.0
                w.writerow([ym, f"{m['Revenue']:.2f}", f"{m['Cost']:.2f}", f"{m['Profit']:.2f}", m["Quantity"], len(m["Orders"]), margin])

        # Category aggregation
        cat_data = defaultdict(lambda: {"Revenue": 0.0, "Profit": 0.0, "Quantity": 0, "Orders": set()})
        for r in rows:
            c = r["Category"]
            cat_data[c]["Revenue"] += float(r["Sales"])
            cat_data[c]["Profit"] += float(r["Profit"])
            cat_data[c]["Quantity"] += int(r["Quantity"])
            cat_data[c]["Orders"].add(r["Order ID"])

        cat_path = os.path.join(outputs_dir, "category_analysis.csv")
        with open(cat_path, mode="w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["Category", "Revenue", "Profit", "Units_Sold", "Total_Orders", "Revenue_Share_%", "Profit_Margin_%"])
            for c, d in sorted(cat_data.items(), key=lambda x: x[1]["Revenue"], reverse=True):
                rev_share = round((d["Revenue"] / total_revenue * 100), 2) if total_revenue > 0 else 0.0
                margin = round((d["Profit"] / d["Revenue"] * 100), 2) if d["Revenue"] > 0 else 0.0
                w.writerow([c, f"{d['Revenue']:.2f}", f"{d['Profit']:.2f}", d["Quantity"], len(d["Orders"]), rev_share, margin])

        # Regional aggregation
        reg_data = defaultdict(lambda: {"Revenue": 0.0, "Profit": 0.0, "Quantity": 0, "Orders": set()})
        for r in rows:
            reg = r["Region"]
            reg_data[reg]["Revenue"] += float(r["Sales"])
            reg_data[reg]["Profit"] += float(r["Profit"])
            reg_data[reg]["Quantity"] += int(r["Quantity"])
            reg_data[reg]["Orders"].add(r["Order ID"])

        reg_path = os.path.join(outputs_dir, "regional_analysis.csv")
        with open(reg_path, mode="w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["Region", "Revenue", "Profit", "Units_Sold", "Total_Orders", "Profit_Margin_%"])
            for reg, d in sorted(reg_data.items(), key=lambda x: x[1]["Revenue"], reverse=True):
                margin = round((d["Profit"] / d["Revenue"] * 100), 2) if d["Revenue"] > 0 else 0.0
                w.writerow([reg, f"{d['Revenue']:.2f}", f"{d['Profit']:.2f}", d["Quantity"], len(d["Orders"]), margin])

        # Top 10 Products
        prod_data = defaultdict(lambda: {"Category": "", "Revenue": 0.0, "Profit": 0.0, "Quantity": 0})
        for r in rows:
            p = r["Product Name"]
            prod_data[p]["Category"] = r["Category"]
            prod_data[p]["Revenue"] += float(r["Sales"])
            prod_data[p]["Profit"] += float(r["Profit"])
            prod_data[p]["Quantity"] += int(r["Quantity"])

        top_prod_path = os.path.join(outputs_dir, "top_products.csv")
        with open(top_prod_path, mode="w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["Product Name", "Category", "Revenue", "Profit", "Units_Sold", "Profit_Margin_%"])
            sorted_prods = sorted(prod_data.items(), key=lambda x: x[1]["Revenue"], reverse=True)[:10]
            for p, d in sorted_prods:
                margin = round((d["Profit"] / d["Revenue"] * 100), 2) if d["Revenue"] > 0 else 0.0
                w.writerow([p, d["Category"], f"{d['Revenue']:.2f}", f"{d['Profit']:.2f}", d["Quantity"], margin])

        print("[SUCCESS] All analysis summaries exported to outputs/ folder!")
        return None

if __name__ == "__main__":
    run_analysis()
