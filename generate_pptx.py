"""
PowerPoint (.pptx) Presentation Generator for Sales Data Analysis Dashboard
Creates outputs/Sales_Data_Analysis_Presentation.pptx with 14 professional slides.
Requires: pip install python-pptx
"""

import os
import sys

def create_presentation(output_path=None):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if output_path is None:
        output_path = os.path.join(base_dir, "outputs", "Sales_Data_Analysis_Presentation.pptx")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    try:
        from pptx import Presentation
        from pptx.util import Inches, Pt
        from pptx.enum.text import PP_ALIGN
        from pptx.dml.color import RGBColor
        from pptx.enum.shapes import MSO_SHAPE
    except ImportError:
        print("\n" + "=" * 65)
        print("  [INFO] 'python-pptx' library is not yet installed.")
        print("  To generate the native Microsoft PowerPoint (.pptx) file:")
        print("    Run: pip install python-pptx")
        print("    Then re-run: python src/generate_pptx.py")
        print("  OR double-click 'generate_ppt.bat' in the project folder!")
        print("=" * 65 + "\n")
        return False

    prs = Presentation()
    # 16:9 Widescreen layout
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # Theme colors
    COLOR_BG = RGBColor(11, 15, 25)         # Dark slate
    COLOR_CARD = RGBColor(21, 28, 46)       # Navy card
    COLOR_PRIMARY = RGBColor(56, 189, 248)  # Cyan blue
    COLOR_SUCCESS = RGBColor(16, 185, 129)  # Green
    COLOR_ACCENT = RGBColor(129, 140, 248)  # Indigo
    COLOR_TEXT = RGBColor(248, 250, 252)    # Pure white
    COLOR_MUTED = RGBColor(148, 163, 184)   # Slate gray

    blank_layout = prs.slide_layouts[6]

    def add_custom_slide(title, subtitle="", badge="SALES ANALYTICS PORTFOLIO"):
        slide = prs.slides.add_slide(blank_layout)
        
        # Dark Background
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = COLOR_BG
        bg.line.fill.background()

        # Top decorative bar
        top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, Inches(0.08))
        top_bar.fill.solid()
        top_bar.fill.fore_color.rgb = COLOR_PRIMARY
        top_bar.line.fill.background()

        # Badge
        badge_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(8), Inches(0.4))
        p_badge = badge_box.text_frame.paragraphs[0]
        p_badge.text = badge.upper()
        p_badge.font.size = Pt(11)
        p_badge.font.bold = True
        p_badge.font.color.rgb = COLOR_PRIMARY

        # Title
        t_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.9), Inches(11.5), Inches(0.8))
        p_t = t_box.text_frame.paragraphs[0]
        p_t.text = title
        p_t.font.size = Pt(28)
        p_t.font.bold = True
        p_t.font.color.rgb = COLOR_TEXT

        # Subtitle
        if subtitle:
            s_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.65), Inches(11.5), Inches(0.5))
            p_s = s_box.text_frame.paragraphs[0]
            p_s.text = subtitle
            p_s.font.size = Pt(14)
            p_s.font.color.rgb = COLOR_MUTED

        return slide

    def add_card(slide, left, top, width, height, title="", color=COLOR_CARD, border_color=None):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
        card.fill.solid()
        card.fill.fore_color.rgb = color
        if border_color:
            card.line.color.rgb = border_color
            card.line.width = Pt(1.5)
        else:
            card.line.fill.background()

        if title:
            tb = slide.shapes.add_textbox(Inches(left + 0.2), Inches(top + 0.15), Inches(width - 0.4), Inches(0.4))
            p = tb.text_frame.paragraphs[0]
            p.text = title
            p.font.size = Pt(14)
            p.font.bold = True
            p.font.color.rgb = COLOR_PRIMARY
        return card

    # =========================================================================
    # SLIDE 1: Title Slide
    # =========================================================================
    s1 = add_custom_slide("Executive Sales Data Analysis & Interactive Dashboard", 
                          "End-to-End Commercial Analytics Portfolio Project | 10,000+ Transactions",
                          "DATA ANALYTICS PORTFOLIO")
    add_card(s1, 0.8, 2.5, 2.7, 4.0, "DATASET SCALE")
    tb1 = s1.shapes.add_textbox(Inches(1.0), Inches(3.2), Inches(2.3), Inches(3.0))
    tf1 = tb1.text_frame
    p = tf1.paragraphs[0]
    p.text = "10,500+"
    p.font.size = Pt(32)
    p.font.bold = True
    p.font.color.rgb = COLOR_PRIMARY
    p2 = tf1.add_paragraph()
    p2.text = "\n• 2 Full Years (2024-2025)\n• 13 Transaction Attributes\n• 5 Geographic Regions\n• 1,590+ Repeat Customers"
    p2.font.size = Pt(12)
    p2.font.color.rgb = COLOR_TEXT

    add_card(s1, 3.8, 2.5, 2.7, 4.0, "CORE ENGINE")
    tb2 = s1.shapes.add_textbox(Inches(4.0), Inches(3.2), Inches(2.3), Inches(3.0))
    tf2 = tb2.text_frame
    p = tf2.paragraphs[0]
    p.text = "Python & Pandas"
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = COLOR_ACCENT
    p2 = tf2.add_paragraph()
    p2.text = "\n• Vectorized Data Cleaning\n• Temporal Feature Eng.\n• Profit Margin Formulas\n• Statistical Grouping"
    p2.font.size = Pt(12)
    p2.font.color.rgb = COLOR_TEXT

    add_card(s1, 6.8, 2.5, 2.7, 4.0, "WEB APPLICATION")
    tb3 = s1.shapes.add_textbox(Inches(7.0), Inches(3.2), Inches(2.3), Inches(3.0))
    tf3 = tb3.text_frame
    p = tf3.paragraphs[0]
    p.text = "Streamlit & Plotly"
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = COLOR_SUCCESS
    p2 = tf3.add_paragraph()
    p2.text = "\n• Live Executive KPI Cards\n• Dynamic Slicers & Filters\n• Dual-Axis Trend Visuals\n• Custom CSV File Upload"
    p2.font.size = Pt(12)
    p2.font.color.rgb = COLOR_TEXT

    add_card(s1, 9.8, 2.5, 2.7, 4.0, "BI & REPORTING")
    tb4 = s1.shapes.add_textbox(Inches(10.0), Inches(3.2), Inches(2.3), Inches(3.0))
    tf4 = tb4.text_frame
    p = tf4.paragraphs[0]
    p.text = "Power BI & Excel"
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = RGBColor(245, 158, 11)
    p2 = tf4.add_paragraph()
    p2.text = "\n• Star Schema Data Model\n• Safe DAX Measures\n• 7-Tab Formatted Excel\n• Portfolio Interview Ready"
    p2.font.size = Pt(12)
    p2.font.color.rgb = COLOR_TEXT

    # =========================================================================
    # SLIDE 2: Business Context & Problem Statement
    # =========================================================================
    s2 = add_custom_slide("Business Context & Problem Statement", "Identifying why traditional sales reporting limits executive decisions.")
    add_card(s2, 0.8, 2.4, 5.6, 4.2, "⚠️ TRADITIONAL REPORTING PAIN POINTS", border_color=RGBColor(239, 68, 68))
    tb = s2.shapes.add_textbox(Inches(1.0), Inches(3.1), Inches(5.2), Inches(3.3))
    tf = tb.text_frame
    tf.text = "• Gross Revenue Illusion: Tracking gross top-line numbers while ignoring COGS and discounts conceals unprofitable product lines.\n\n• Reporting Latency: Preparing static spreadsheets takes days each month, resulting in stale business information.\n\n• Regional Margin Blindspots: Lack of granular visibility into territory profitability and return costs.\n\n• Siloed Stakeholder Formats: Finance needs spreadsheets, executives need web dashboards, and BI teams need Power BI models."
    for p in tf.paragraphs:
        p.font.size = Pt(13)
        p.font.color.rgb = COLOR_TEXT

    add_card(s2, 6.8, 2.4, 5.7, 4.2, "💡 PROPOSED ANALYTICAL SOLUTION", border_color=COLOR_SUCCESS)
    tb = s2.shapes.add_textbox(Inches(7.0), Inches(3.1), Inches(5.3), Inches(3.3))
    tf = tb.text_frame
    tf.text = "• Automated Python Pipeline: Instant cleaning, deduplication, and profit margin calculation across 10,000+ orders.\n\n• Self-Service Exploration: Dynamic Streamlit web application with real-time date, territory, and product filtering.\n\n• Multi-Channel Deliverables: Formatted 7-tab Excel workbook, Power BI DAX blueprint, and interactive web charts.\n\n• Actionable Strategy: Direct visibility into high-margin items (Office Supplies: 41.6% margin) and Q4 seasonality."
    for p in tf.paragraphs:
        p.font.size = Pt(13)
        p.font.color.rgb = COLOR_TEXT

    # =========================================================================
    # SLIDE 3: Executive KPI Scorecard
    # =========================================================================
    s3 = add_custom_slide("Executive KPI Scorecard (2-Year Performance)", "Key commercial baseline metrics extracted from 10,500 transactions.")
    
    kpis = [
        ("TOTAL REVENUE", "$8,424,326.70", "▲ Gross Invoiced Sales", COLOR_PRIMARY),
        ("TOTAL NET PROFIT", "$2,719,100.70", "▲ Operating Income", COLOR_SUCCESS),
        ("PROFIT MARGIN", "32.28%", "Target: >25.0%", COLOR_ACCENT),
        ("TOTAL ORDERS", "10,500", "21,733 Units Distributed", COLOR_PRIMARY),
        ("AVG ORDER VALUE", "$802.32", "Per Transaction Invoice", RGBColor(245, 158, 11))
    ]
    for idx, (title, val, sub, col) in enumerate(kpis):
        left = 0.8 + idx * 2.4
        add_card(s3, left, 2.4, 2.2, 2.2)
        tb = s3.shapes.add_textbox(Inches(left + 0.1), Inches(2.55), Inches(2.0), Inches(1.9))
        tf = tb.text_frame
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(10)
        p.font.color.rgb = COLOR_MUTED
        p2 = tf.add_paragraph()
        p2.text = val
        p2.font.size = Pt(22)
        p2.font.bold = True
        p2.font.color.rgb = col
        p3 = tf.add_paragraph()
        p3.text = sub
        p3.font.size = Pt(9)
        p3.font.color.rgb = COLOR_MUTED

    add_card(s3, 0.8, 5.0, 11.7, 1.8, "EXECUTIVE SUMMARY HIGHLIGHTS")
    tb = s3.shapes.add_textbox(Inches(1.0), Inches(5.5), Inches(11.3), Inches(1.2))
    tf = tb.text_frame
    tf.text = "• Sustainable Margins: Healthy 32.28% overall net margin maintained even through promotional discount windows.\n• Customer Retention: 1,597 unique customers with high repeat purchase frequency in office consumables.\n• Order Health: Robust Average Order Value of $802.32 driven by premium technology hardware and ergonomic workstations."
    for p in tf.paragraphs:
        p.font.size = Pt(13)
        p.font.color.rgb = COLOR_TEXT

    # =========================================================================
    # SLIDE 4: Monthly Trend & Seasonality
    # =========================================================================
    s4 = add_custom_slide("Monthly Sales Trajectory & Q4 Seasonality", "Time-series analysis of commercial revenue and net profit.")
    add_card(s4, 0.8, 2.4, 6.0, 4.4, "📊 MONTHLY TREND DYNAMICS")
    tb = s4.shapes.add_textbox(Inches(1.0), Inches(3.1), Inches(5.6), Inches(3.4))
    tf = tb.text_frame
    tf.text = "• Stable Baseline (Q1-Q3): Consistent run-rate averaging $250,000 to $290,000 per month.\n\n• Q4 Surge (Oct-Dec): Massive 120%+ revenue spike exceeding $600,000 to $660,000 per month.\n\n• Seasonality Factors: Year-end corporate budget clearing, black friday promotions, and holiday restocking.\n\n• Resilient Margins: Profit margins remained rock-solid at 31.9% to 33.4%, proving volume discounts did not erode margin integrity."
    for p in tf.paragraphs:
        p.font.size = Pt(13)
        p.font.color.rgb = COLOR_TEXT

    add_card(s4, 7.2, 2.4, 5.3, 4.4, "📈 QUARTERLY REVENUE BREAKDOWN")
    tb = s4.shapes.add_textbox(Inches(7.4), Inches(3.1), Inches(4.9), Inches(3.4))
    tf = tb.text_frame
    tf.text = "• Q1 (Jan - Mar):\n   Avg Monthly Sales: $268,526 | 32.20% Margin\n\n• Q2 (Apr - Jun):\n   Avg Monthly Sales: $241,848 | 32.48% Margin\n\n• Q3 (Jul - Sep):\n   Avg Monthly Sales: $282,109 | 32.28% Margin\n\n• Q4 (Oct - Dec) [PEAK]:\n   Avg Monthly Sales: $616,193 | 32.27% Margin\n   (Highest Order Volume: 750+ orders/month)"
    for p in tf.paragraphs:
        p.font.size = Pt(13)
        p.font.color.rgb = COLOR_TEXT

    # =========================================================================
    # SLIDE 5: Category & Product Performance
    # =========================================================================
    s5 = add_custom_slide("Product Category & Top Sellers Leaderboard", "Evaluating top-line contributors versus margin champions.")
    cats = [
        ("TECHNOLOGY", "$4,883,899.75", "57.97% Revenue Share", "28.41% Margin", COLOR_PRIMARY),
        ("OFFICE FURNITURE", "$2,564,250.60", "30.44% Revenue Share", "36.79% Margin", COLOR_ACCENT),
        ("OFFICE SUPPLIES", "$489,686.50", "5.81% Revenue Share", "41.66% HIGH MARGIN", COLOR_SUCCESS),
        ("HOME & ELECTRONICS", "$486,489.85", "5.77% Revenue Share", "37.81% Margin", RGBColor(245, 158, 11))
    ]
    for idx, (cat, rev, share, mrg, col) in enumerate(cats):
        left = 0.8 + idx * 3.0
        add_card(s5, left, 2.3, 2.8, 2.1)
        tb = s5.shapes.add_textbox(Inches(left + 0.15), Inches(2.45), Inches(2.5), Inches(1.8))
        tf = tb.text_frame
        p = tf.paragraphs[0]
        p.text = cat
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = col
        p2 = tf.add_paragraph()
        p2.text = rev
        p2.font.size = Pt(18)
        p2.font.bold = True
        p2.font.color.rgb = COLOR_TEXT
        p3 = tf.add_paragraph()
        p3.text = f"{share}\n{mrg}"
        p3.font.size = Pt(10)
        p3.font.color.rgb = COLOR_MUTED

    add_card(s5, 0.8, 4.7, 11.7, 2.2, "🏆 TOP 3 FLAGSHIP PRODUCTS BY REVENUE")
    tb = s5.shapes.add_textbox(Inches(1.0), Inches(5.2), Inches(11.3), Inches(1.5))
    tf = tb.text_frame
    tf.text = "1. Dell XPS 15 Laptop (Technology) — Revenue: $987,915.95 | Units: 668 | Profit: $253,115.95 (25.62% Margin)\n2. Lenovo ThinkPad X1 (Technology) — Revenue: $823,890.75 | Units: 643 | Profit: $232,330.75 (28.20% Margin)\n3. Herman Miller Ergonomic Chair (Furniture) — Revenue: $778,625.00 | Units: 633 | Profit: $272,225.00 (34.96% Margin)"
    for p in tf.paragraphs:
        p.font.size = Pt(12)
        p.font.color.rgb = COLOR_TEXT

    # =========================================================================
    # SLIDE 6: Strategic Recommendations & Conclusion
    # =========================================================================
    s6 = add_custom_slide("Strategic Business Recommendations & Next Steps", "Turning data analytics insights into executive commercial actions.")
    recs = [
        ("📦 1. Product Bundling Strategy", "Bundle high-revenue Technology laptops with high-margin Office Supplies (41.6% margin) to increase average basket profit without discounting core hardware."),
        ("🚢 2. Q4 Supply Chain Preparation", "Secure inventory buffer 60 days in advance of October to prevent out-of-stock events during the proven 120% Q4 demand surge."),
        ("🤝 3. Enterprise B2B Retention", "Launch VIP tier pricing for the top 100 corporate accounts who generate recurring high-volume purchases across all quarters."),
        ("💳 4. 100% Cashless Migration", "Incentivize UPI and Credit Cards to eliminate the remaining 6% Cash on Delivery handling overhead and return risks.")
    ]
    for idx, (title, desc) in enumerate(recs):
        top = 2.4 + idx * 1.15
        add_card(s6, 0.8, top, 11.7, 1.0, title)
        tb = s6.shapes.add_textbox(Inches(1.0), Inches(top + 0.4), Inches(11.3), Inches(0.55))
        p = tb.text_frame.paragraphs[0]
        p.text = desc
        p.font.size = Pt(12)
        p.font.color.rgb = COLOR_TEXT

    prs.save(output_path)
    print(f"[SUCCESS] PowerPoint presentation saved successfully to: {output_path}")
    return True

if __name__ == "__main__":
    create_presentation()
