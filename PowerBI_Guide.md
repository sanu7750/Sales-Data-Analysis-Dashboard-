# 📊 Power BI Dashboard Guide – Sales Data Analysis

This guide provides step-by-step instructions for replicating the **Sales Data Analysis Dashboard** in **Microsoft Power BI Desktop**. It is designed to be portfolio-ready, professional, and easy to follow.

---

## 🏗️ 1. Project Overview & Architecture

- **Data Source:** `data/cleaned_sales_data.csv` (or `data/sales_data.csv`)
- **Report Canvas:** 16:9 widescreen layout (`1920 x 1080` or `1280 x 720`)
- **Theme Palette:** Modern Executive Slate
  - Primary Accent: `#38BDF8` (Sky Blue)
  - Success/Profit: `#10B981` (Emerald Green)
  - Secondary/Tech: `#6366F1` (Indigo)
  - Background: `#0F172A` (Dark Slate) or `#F8FAFC` (Clean Modern Light)

---

## 📥 2. Step-by-Step Data Import & Power Query

1. Open **Power BI Desktop**.
2. Click **Get Data** > **Text/CSV**.
3. Browse and select `E:\Sales Data Analysis Dashboard\data\cleaned_sales_data.csv`.
4. Click **Transform Data** to open the **Power Query Editor**.
5. Verify column data types:
   - `Order ID`: Text
   - `Order Date`: Date
   - `Customer ID`: Text
   - `Product Name`: Text
   - `Category`: Text
   - `Region`: Text
   - `City`: Text
   - `Quantity`: Whole Number
   - `Unit Price`: Fixed Decimal Number (`$`)
   - `Sales`: Fixed Decimal Number (`$`)
   - `Cost`: Fixed Decimal Number (`$`)
   - `Profit`: Fixed Decimal Number (`$`)
   - `Payment Mode`: Text
6. Click **Close & Apply**.

---

## 📐 3. Core DAX Measures Table

Create a dedicated measures table:
1. In Home ribbon, click **Enter Data**.
2. Name the table `_Measures` and click **Load**.
3. Right-click `_Measures` > **New Measure** and add the following DAX calculations:

### 1. Total Revenue
```dax
Total Revenue = SUM('cleaned_sales_data'[Sales])
```

### 2. Total Cost
```dax
Total Cost = SUM('cleaned_sales_data'[Cost])
```

### 3. Total Profit
```dax
Total Profit = SUM('cleaned_sales_data'[Profit])
```

### 4. Overall Profit Margin (%)
```dax
Profit Margin % = 
DIVIDE([Total Profit], [Total Revenue], 0) * 100
```

### 5. Total Orders
```dax
Total Orders = DISTINCTCOUNT('cleaned_sales_data'[Order ID])
```

### 6. Units Sold
```dax
Total Units Sold = SUM('cleaned_sales_data'[Quantity])
```

### 7. Average Order Value (AOV)
```dax
Average Order Value = 
DIVIDE([Total Revenue], [Total Orders], 0)
```

### 8. Total Active Customers
```dax
Total Customers = DISTINCTCOUNT('cleaned_sales_data'[Customer ID])
```

### 9. Top-line Target Indicator
```dax
Profit Health Status = 
IF([Profit Margin %] >= 25, "🟢 Healthy (>25%)", 
IF([Profit Margin %] >= 15, "🟡 Moderate (15-25%)", "🔴 Low Margin (<15%)"))
```

---

## 🎨 4. Canvas Layout & Visual Setup

```
+----------------------------------------------------------------------------------------------------+
|  [LOGO]  EXECUTIVE SALES ANALYTICS DASHBOARD                             [Date Range Slicer]        |
+----------------------------------------------------------------------------------------------------+
|  [KPI 1]          |  [KPI 2]          |  [KPI 3]          |  [KPI 4]          |  [KPI 5]            |
|  Total Revenue    |  Total Profit     |  Total Orders     |  Units Sold       |  Avg Margin %       |
|  $1,245,820       |  $384,210         |  10,500           |  24,800           |  30.84%             |
+---------------------------------------+------------------------------------------------------------+
|  VISUAL 1: Monthly Trend              |  VISUAL 2: Category Breakdown                              |
|  (Line & Clustered Column Chart)      |  (Donut Chart & Treemap)                                   |
|  Revenue bars + Profit line           |  Revenue share by Product Category                         |
+---------------------------------------+------------------------------------------------------------+
|  VISUAL 3: Regional Performance       |  VISUAL 4: Top 10 Best-Selling Products                   |
|  (Clustered Bar Chart)                |  (Horizontal Bar Chart with Top N filter)                  |
|  Sales & Profit by Region             |  Ranked by Revenue                                         |
+---------------------------------------+------------------------------------------------------------+
|  SLICERS (Side/Bottom):  [Region]     [Category]     [Payment Mode]     [Product Search]           |
+----------------------------------------------------------------------------------------------------+
```

---

## 📊 5. Visual Configuration Guide

### 1. KPI Cards (Top Banner)
- Visual type: **Card (New)** or **Multi-Row Card**
- Data fields:
  - `[Total Revenue]` (formatted as Currency `$#,##0`)
  - `[Total Profit]` (formatted as Currency `$#,##0`)
  - `[Total Orders]` (formatted as `#,##0`)
  - `[Total Units Sold]` (formatted as `#,##0`)
  - `[Profit Margin %]` (formatted as `0.00%`)

### 2. Monthly Revenue & Profit Trend
- Visual type: **Line and Clustered Column Chart**
- **X-axis:** `cleaned_sales_data[Order Date]` (Hierarchy: Year > Month) or `[Year_Month]`
- **Column Y-axis:** `[Total Revenue]`
- **Line Y-axis:** `[Total Profit]`
- **Formatting:** Enable Data labels, set line stroke width to 3, column color to Blue (`#38BDF8`), line to Emerald (`#10B981`).

### 3. Revenue by Category
- Visual type: **Donut Chart**
- **Legend:** `cleaned_sales_data[Category]`
- **Values:** `[Total Revenue]`
- **Detail Labels:** Category & Percent of total

### 4. Regional Commercial Performance
- Visual type: **Clustered Bar Chart** (Horizontal)
- **Y-axis:** `cleaned_sales_data[Region]`
- **X-axis:** `[Total Revenue]`
- **Tooltips:** `[Total Profit]`, `[Profit Margin %]`, `[Total Orders]`
- **Sorting:** Sort descending by `[Total Revenue]`

### 5. Top 10 Best-Selling Products
- Visual type: **Clustered Bar Chart** (Horizontal)
- **Y-axis:** `cleaned_sales_data[Product Name]`
- **X-axis:** `[Total Revenue]`
- **Filter:** In the Filters pane under `Product Name` > Filter Type: **Top N** > Show top **10** items by `[Total Revenue]`.

### 6. Payment Mode Share
- Visual type: **Pie Chart** or **Treemap**
- **Category:** `cleaned_sales_data[Payment Mode]`
- **Values:** `[Total Orders]` or `[Total Revenue]`

---

## 🎛️ 6. Interactive Slicers

1. **Date Range Slicer:**
   - Field: `cleaned_sales_data[Order Date]`
   - Style: **Between** (slider with start and end date pickers)
2. **Region Slicer:**
   - Field: `cleaned_sales_data[Region]`
   - Style: **Tile** or **Dropdown**
3. **Category Slicer:**
   - Field: `cleaned_sales_data[Category]`
   - Style: **Dropdown** (with multi-select enabled)
4. **Product Search Slicer:**
   - Field: `cleaned_sales_data[Product Name]`
   - Style: **Dropdown** with search bar enabled

---

## 💡 7. Portfolio Presentation Tips for Interviews

When presenting this project in a portfolio or technical interview:
1. **Explain the Business Context:** Frame the project as an executive analytics dashboard for leadership to make inventory, pricing, and regional expansion decisions.
2. **Discuss Data Quality Steps:** Highlight how duplicate entries were handled, data types validated, and missing values addressed.
3. **Demonstrate DAX Proficiency:** Walk through the DAX measures (`DIVIDE` safety, `DISTINCTCOUNT`, profit margin formulas).
4. **Highlight Key Business Insights:**
   - Technology drives top-line revenue but office supplies deliver steady, high-margin transactions.
   - Q4 demonstrates clear seasonal growth.
   - Cashless checkout (Credit Cards + UPI) dominates payment preferences.
