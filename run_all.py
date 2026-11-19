"""
End-to-End Sales Analytics Pipeline Runner
Executes data generation (10,500+ records), data cleaning,
statistical EDA analysis, and multi-sheet Excel report generation.
"""

import os
import sys

# Ensure src directory is in Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from generate_data import generate_sales_data
from data_cleaning import clean_data
from analysis import run_analysis
from export_excel import generate_excel_report

def run_pipeline(num_rows=10500):
    print("=" * 65)
    print("      🚀 SALES DATA ANALYSIS & DASHBOARD PIPELINE")
    print("=" * 65)

    base_dir = os.path.dirname(current_dir)
    raw_data_path = os.path.join(base_dir, "data", "sales_data.csv")
    cleaned_data_path = os.path.join(base_dir, "data", "cleaned_sales_data.csv")
    outputs_dir = os.path.join(base_dir, "outputs")
    excel_path = os.path.join(outputs_dir, "sales_analysis_report.xlsx")

    # Step 1: Generate Raw Data if missing or less than 10,000 rows
    print("\n[STEP 1/4] Checking and Generating Sales Dataset...")
    needs_generation = True
    if os.path.exists(raw_data_path):
        with open(raw_data_path, "r", encoding="utf-8") as f:
            line_count = sum(1 for _ in f)
        if line_count >= num_rows:
            print(f"  Existing dataset contains {line_count - 1:,} rows. Skipping regeneration.")
            needs_generation = False
        else:
            print(f"  Existing dataset has {line_count - 1:,} rows. Expanding to {num_rows:,} rows...")

    if needs_generation:
        generate_sales_data(num_rows, raw_data_path)

    # Step 2: Data Cleaning & Preprocessing
    print("\n[STEP 2/4] Cleaning Dataset & Feature Engineering...")
    clean_data(raw_data_path, cleaned_data_path)

    # Step 3: Statistical Analysis & Power BI Summaries
    print("\n[STEP 3/4] Performing Exploratory Data Analysis (EDA)...")
    run_analysis(cleaned_data_path, outputs_dir)

    # Step 4: Multi-sheet Excel Report Generation
    print("\n[STEP 4/4] Creating Multi-Sheet Excel Workbook...")
    generate_excel_report(excel_path)

    print("\n" + "=" * 65)
    print("      🎉 PIPELINE COMPLETED SUCCESSFULLY!")
    print("=" * 65)
    print(f"  📁 Raw Data:       {raw_data_path}")
    print(f"  📁 Cleaned Data:   {cleaned_data_path}")
    print(f"  📁 Excel Report:   {excel_path}")
    print(f"  📁 Power BI Guide: {os.path.join(outputs_dir, 'PowerBI_Guide.md')}")
    print(f"  📊 Dashboard:      Run 'run_dashboard.bat' or 'streamlit run dashboard/app.py'")
    print("=" * 65)

if __name__ == "__main__":
    run_pipeline(10500)
