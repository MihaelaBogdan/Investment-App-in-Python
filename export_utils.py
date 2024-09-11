import os
from datetime import datetime
import pandas as pd
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.drawing.image import Image as ExcelImage
from io import BytesIO

def export_to_excel(df, report_dir, future_df=None, figure=None):
    if df is None or df.empty:
        raise ValueError("Nu există date pentru a exporta.")

    
    df = df.copy()
    for col in df.select_dtypes(include=['datetime', 'datetimetz']).columns:
        df[col] = df[col].dt.tz_localize(None)

    if future_df is not None:
        future_df = future_df.copy()
        for col in future_df.select_dtypes(include=['datetime', 'datetimetz']).columns:
            future_df[col] = future_df[col].dt.tz_localize(None)

    if not os.path.exists(report_dir):
        try:
            os.makedirs(report_dir)
        except Exception as e:
            raise OSError(f"Nu s-a putut crea directorul {report_dir}: {e}")

    
    filename = os.path.join(report_dir, f"raport_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx")
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Date Acțiuni"

    
    for r in dataframe_to_rows(df, index=True, header=True):
        sheet.append(r)

    
    if future_df is not None and not future_df.empty:
        sheet_future = workbook.create_sheet(title="Predicții")
        for r in dataframe_to_rows(future_df, index=True, header=True):
            sheet_future.append(r)

    
    if figure:
        try:
            img = BytesIO()
            figure.savefig(img, format='png')
            img.seek(0)
            excel_img = ExcelImage(img)
            sheet.add_image(excel_img, 'H2')
        except Exception as e:
            raise RuntimeError(f"Nu s-a putut adăuga imaginea în fișierul Excel: {e}")

    
    try:
        workbook.save(filename)
        return filename
    except Exception as e:
        raise IOError(f"Nu s-a putut salva fișierul Excel: {e}")
