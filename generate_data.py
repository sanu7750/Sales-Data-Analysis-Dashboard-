"""
Sales Data Generator
Generates 10,000+ realistic sales records for data analytics, EDA, and business dashboards.
"""

import csv
import os
import random
from datetime import datetime, timedelta

# Set random seed for reproducibility
random.seed(42)

# Catalog of products with realistic prices and profit margins
PRODUCT_CATALOG = {
    "Technology": {
        "Apple MacBook Air M2": (999.00, 720.00),
        "Dell XPS 15 Laptop": (1499.00, 1100.00),
        "Lenovo ThinkPad X1": (1299.00, 920.00),
        "Apple iPhone 15 Pro": (1099.00, 780.00),
        "Samsung Galaxy S24 Ultra": (1199.00, 840.00),
        "iPad Pro 11-inch": (799.00, 560.00),
        "Sony WH-1000XM5 Headphones": (399.00, 260.00),
        "Logitech MX Master 3S Mouse": (99.00, 55.00),
        "Samsung 32\" 4K Curved Monitor": (449.00, 310.00),
        "Keychron Mechanical Keyboard": (110.00, 60.00),
    },
    "Office Furniture": {
        "Herman Miller Ergonomic Chair": (1250.00, 800.00),
        "Steelcase Gesture Office Chair": (1100.00, 720.00),
        "Ergonomic Mesh Swivel Chair": (280.00, 160.00),
        "Electric Height Adjustable Standing Desk": (599.00, 360.00),
        "L-Shaped Executive Corner Desk": (450.00, 270.00),
        "Solid Pine 5-Shelf Bookcase": (199.00, 110.00),
        "Heavy-Duty 3-Drawer Filing Cabinet": (165.00, 95.00),
        "Mobile Under-Desk Pedestal": (130.00, 75.00),
    },
    "Office Supplies": {
        "Multipurpose Copy Paper (Box of 10 Reams)": (48.00, 26.00),
        "Parker Premium Stainless Ballpoint Pen": (35.00, 16.00),
        "Heavy Duty Desktop Stapler & Punch Set": (28.00, 12.00),
        "Fellowes Cross-Cut Paper Shredder": (145.00, 85.00),
        "Self-Adhesive Sticky Notes (Pack of 12)": (15.00, 6.00),
        "Dry Erase Whiteboard 36x24": (55.00, 28.00),
        "Expanding File Folder Organizer": (22.00, 9.00),
        "Thermal Label Printer & Rolls": (180.00, 105.00),
    },
    "Home & Electronics": {
        "Dyson V12 Cordless Vacuum": (649.00, 430.00),
        "Philips Smart Hue Lighting Starter Kit": (169.00, 98.00),
        "Nespresso Vertuo Coffee Machine": (189.00, 115.00),
        "Bose SoundLink Bluetooth Speaker": (149.00, 88.00),
        "Anker 100W Fast Multi-Port Charger": (65.00, 32.00),
        "Ember Temperature Control Smart Mug": (129.00, 72.00),
        "Ergonomic Memory Foam Footrest": (42.00, 20.00),
    }
}

REGIONS_CITIES = {
    "North": ["New York", "Chicago", "Boston", "Philadelphia", "Minneapolis"],
    "South": ["Atlanta", "Dallas", "Houston", "Miami", "Austin"],
    "East": ["Washington D.C.", "Baltimore", "Charlotte", "Richmond", "Pittsburgh"],
    "West": ["San Francisco", "Seattle", "Los Angeles", "Denver", "Portland"],
    "Central": ["Kansas City", "Indianapolis", "Columbus", "St. Louis", "Detroit"]
}

PAYMENT_MODES = ["Credit Card", "Debit Card", "UPI", "Net Banking", "Cash on Delivery"]
PAYMENT_WEIGHTS = [0.42, 0.22, 0.18, 0.12, 0.06]

def generate_sales_data(num_rows=10500, output_path=None):
    """Generate realistic sales dataset and save to CSV."""
    if output_path is None:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        output_path = os.path.join(base_dir, "data", "sales_data.csv")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    start_date = datetime(2024, 1, 1)
    end_date = datetime(2025, 12, 31)
    total_days = (end_date - start_date).days

    # Customer pool (around 1,500 distinct repeat customers)
    customer_pool = [f"CUST-{10000 + i}" for i in range(1600)]

    fieldnames = [
        "Order ID",
        "Order Date",
        "Customer ID",
        "Product Name",
        "Category",
        "Region",
        "City",
        "Quantity",
        "Unit Price",
        "Sales",
        "Cost",
        "Profit",
        "Payment Mode"
    ]

    records = []
    
    # Weight categories realistically
    cat_choices = list(PRODUCT_CATALOG.keys())
    cat_weights = [0.38, 0.26, 0.22, 0.14]

    for i in range(1, num_rows + 1):
        order_id = f"ORD-{2024 + (i % 2):04d}-{100000 + i}"
        
        # Slight seasonal weighting towards Q4 (Oct-Dec)
        day_offset = random.randint(0, total_days)
        # Introduce Q4 holiday boost
        if random.random() < 0.25:
            # Shift towards holiday months (Oct, Nov, Dec)
            day_offset = random.choice([
                random.randint(270, 364),   # 2024 Q4
                random.randint(635, 729)    # 2025 Q4
            ])
            day_offset = min(day_offset, total_days)
            
        order_date = start_date + timedelta(days=day_offset)
        customer_id = random.choice(customer_pool)

        category = random.choices(cat_choices, weights=cat_weights)[0]
        products_in_cat = PRODUCT_CATALOG[category]
        product_name = random.choice(list(products_in_cat.keys()))
        unit_price, base_cost = products_in_cat[product_name]

        # Quantity: most orders are 1-3, office supplies have higher quantity
        if category == "Office Supplies":
            quantity = random.choices([1, 2, 3, 4, 5, 8, 10, 15, 20], 
                                      weights=[0.30, 0.25, 0.15, 0.10, 0.08, 0.05, 0.04, 0.02, 0.01])[0]
        elif category == "Technology":
            quantity = random.choices([1, 2, 3, 4, 5], 
                                      weights=[0.65, 0.22, 0.08, 0.03, 0.02])[0]
        else:
            quantity = random.choices([1, 2, 3, 4, 6], 
                                      weights=[0.55, 0.25, 0.12, 0.05, 0.03])[0]

        # Occasional volume discount (5% - 15%) for large quantities
        discount_pct = 0.0
        if quantity >= 10:
            discount_pct = 0.15
        elif quantity >= 5:
            discount_pct = 0.10
        elif random.random() < 0.15:
            discount_pct = 0.05

        sales = round((unit_price * quantity) * (1 - discount_pct), 2)
        cost = round(base_cost * quantity, 2)
        profit = round(sales - cost, 2)

        region = random.choice(list(REGIONS_CITIES.keys()))
        city = random.choice(REGIONS_CITIES[region])
        payment_mode = random.choices(PAYMENT_MODES, weights=PAYMENT_WEIGHTS)[0]

        records.append({
            "Order ID": order_id,
            "Order Date": order_date.strftime("%Y-%m-%d"),
            "Customer ID": customer_id,
            "Product Name": product_name,
            "Category": category,
            "Region": region,
            "City": city,
            "Quantity": quantity,
            "Unit Price": f"{unit_price:.2f}",
            "Sales": f"{sales:.2f}",
            "Cost": f"{cost:.2f}",
            "Profit": f"{profit:.2f}",
            "Payment Mode": payment_mode
        })

    # Sort chronological by Order Date
    records.sort(key=lambda r: r["Order Date"])

    # Write to CSV
    with open(output_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

    print(f"[SUCCESS] Generated {len(records)} sales records.")
    print(f"[OUTPUT] Saved to: {output_path}")
    return output_path

if __name__ == "__main__":
    generate_sales_data(10500)
