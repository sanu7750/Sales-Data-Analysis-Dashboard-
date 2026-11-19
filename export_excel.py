"""
Multi-Sheet Excel Report Generator
Generates outputs/sales_analysis_report.xlsx with 7 dedicated business sheets:
1. Raw Sales Data
2. Cleaned Data
3. Monthly Sales
4. Category Analysis
5. Regional Analysis
6. Top Products
7. KPI Summary
"""

import os
import csv
import zipfile

try:
    import pandas as pd
    import openpyxl
    OPENPYXL_AVAILABLE = True
except ImportError:
    OPENPYXL_AVAILABLE = False

def create_native_xlsx(filename, sheets_dict):
    """
    Creates a compliant Microsoft Excel (.xlsx) file using Python standard library.
    Allows generating genuine multi-sheet workbooks without requiring third-party libraries.
    """
    wb_xml = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>']
    wb_xml.append('<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets>')
    
    wb_rels = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>']
    wb_rels.append('<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">')
    
    content_types = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>']
    content_types.append('<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">')
    content_types.append('<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>')
    content_types.append('<Default Extension="xml" ContentType="application/xml"/>')
    content_types.append('<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>')

    sheet_files = {}
    
    for idx, (name, rows) in enumerate(sheets_dict.items(), 1):
        wb_xml.append(f'<sheet name="{name}" sheetId="{idx}" r:id="rId{idx}"/>')
        wb_rels.append(f'<Relationship Id="rId{idx}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet{idx}.xml"/>')
        content_types.append(f'<Override PartName="/xl/worksheets/sheet{idx}.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>')
        
        s_xml = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>']
        s_xml.append('<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><sheetData>')
        for r_idx, row in enumerate(rows, 1):
            s_xml.append(f'<row r="{r_idx}">')
            for c_idx, val in enumerate(row, 1):
                col_letter = chr(64 + c_idx) if c_idx <= 26 else f'A{chr(64 + c_idx - 26)}'
                cell_ref = f'{col_letter}{r_idx}'
                if isinstance(val, (int, float)):
                    s_xml.append(f'<c r="{cell_ref}"><v>{val}</v></c>')
                else:
                    clean_str = str(val).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                    s_xml.append(f'<c r="{cell_ref}" t="inlineStr"><is><t>{clean_str}</t></is></c>')
            s_xml.append('</row>')
        s_xml.append('</sheetData></worksheet>')
        sheet_files[f'xl/worksheets/sheet{idx}.xml'] = ''.join(s_xml)
        
    wb_xml.append('</sheets></workbook>')
    wb_rels.append('</Relationships>')
    content_types.append('</Types>')
    
    pkg_rels = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/></Relationships>'

    with zipfile.ZipFile(filename, 'w', zipfile.ZIP_DEFLATED) as z:
        z.writestr('[Content_Types].xml', ''.join(content_types))
        z.writestr('_rels/.rels', pkg_rels)
        z.writestr('xl/workbook.xml', ''.join(wb_xml))
        z.writestr('xl/_rels/workbook.xml.rels', ''.join(wb_rels))
        for path, data in sheet_files.items():
            z.writestr(path, data)

def read_csv_rows(path, max_rows=None):
    """Utility to read a CSV file into list of row lists."""
    if not os.path.exists(path):
        return []
    rows = []
    with open(path, mode="r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for idx, row in enumerate(reader):
            if max_rows and idx > max_rows:
                break
            rows.append(row)
    return rows

def generate_excel_report(output_xlsx_path=None):
    """
    Assembles the complete multi-sheet Excel report.
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if output_xlsx_path is None:
        output_xlsx_path = os.path.join(base_dir, "outputs", "sales_analysis_report.xlsx")

    os.makedirs(os.path.dirname(output_xlsx_path), exist_ok=True)

    data_dir = os.path.join(base_dir, "data")
    outputs_dir = os.path.join(base_dir, "outputs")

    raw_csv = os.path.join(data_dir, "sales_data.csv")
    cleaned_csv = os.path.join(data_dir, "cleaned_sales_data.csv")
    monthly_csv = os.path.join(outputs_dir, "monthly_sales.csv")
    cat_csv = os.path.join(outputs_dir, "category_analysis.csv")
    reg_csv = os.path.join(outputs_dir, "regional_analysis.csv")
    top_csv = os.path.join(outputs_dir, "top_products.csv")
    kpi_csv = os.path.join(outputs_dir, "kpi_summary.csv")

    if OPENPYXL_AVAILABLE:
        print("[INFO] Generating formatted Excel report via pandas and openpyxl...")
        with pd.ExcelWriter(output_xlsx_path, engine="openpyxl") as writer:
            if os.path.exists(kpi_csv):
                pd.read_csv(kpi_csv).to_excel(writer, sheet_name="KPI Summary", index=False)
            if os.path.exists(monthly_csv):
                pd.read_csv(monthly_csv).to_excel(writer, sheet_name="Monthly Sales", index=False)
            if os.path.exists(cat_csv):
                pd.read_csv(cat_csv).to_excel(writer, sheet_name="Category Analysis", index=False)
            if os.path.exists(reg_csv):
                pd.read_csv(reg_csv).to_excel(writer, sheet_name="Regional Analysis", index=False)
            if os.path.exists(top_csv):
                pd.read_csv(top_csv).to_excel(writer, sheet_name="Top Products", index=False)
            if os.path.exists(cleaned_csv):
                pd.read_csv(cleaned_csv).head(5000).to_excel(writer, sheet_name="Cleaned Data", index=False)
            if os.path.exists(raw_csv):
                pd.read_csv(raw_csv).head(5000).to_excel(writer, sheet_name="Raw Sales Data", index=False)

        print(f"[SUCCESS] Multi-sheet Excel workbook created at: {output_xlsx_path}")
        return output_xlsx_path

    else:
        print("[INFO] Generating native multi-sheet Excel report (.xlsx)...")
        sheets_dict = {
            "KPI Summary": read_csv_rows(kpi_csv),
            "Monthly Sales": read_csv_rows(monthly_csv),
            "Category Analysis": read_csv_rows(cat_csv),
            "Regional Analysis": read_csv_rows(reg_csv),
            "Top Products": read_csv_rows(top_csv),
            "Cleaned Data": read_csv_rows(cleaned_csv, max_rows=3000),
            "Raw Sales Data": read_csv_rows(raw_csv, max_rows=3000),
        }
        create_native_xlsx(output_xlsx_path, sheets_dict)
        print(f"[SUCCESS] Multi-sheet Excel workbook created at: {output_xlsx_path}")
        return output_xlsx_path

if __name__ == "__main__":
    generate_excel_report()
