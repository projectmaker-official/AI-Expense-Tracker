from datetime import datetime
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# 🌐 Constants
GSHEET_SCOPE = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]
CREDENTIALS_PATH = "config/birthday.json"
SPREADSHEET_NAME = "birthday"

# ✅ Authentication & client initialization
def get_gspread_client():
    creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_PATH, GSHEET_SCOPE)
    return gspread.authorize(creds)

# 🧾 Check if current year sheet exists
def is_new_year_sheet_needed(spreadsheet):
    current_year = datetime.now().year
    return f"test-{current_year}" not in [s.title for s in spreadsheet.worksheets()]

# 🆕 Create sheet for new year with header
def create_new_year_sheet(spreadsheet, sheet_title):
    sheet = spreadsheet.add_worksheet(title=sheet_title, rows="1000", cols="26")
    sheet.append_row(["date", "month", "credit", "credit_details", "debit", "debit_details", "category"])
    return sheet

# 📥 Load current year's data
def load_data_from_gsheet():
    client = get_gspread_client()
    spreadsheet = client.open(SPREADSHEET_NAME)
    sheet_title = f"test-{datetime.now().year}"

    if is_new_year_sheet_needed(spreadsheet):
        worksheet = create_new_year_sheet(spreadsheet, sheet_title)
    else:
        worksheet = spreadsheet.worksheet(sheet_title)

    df = pd.DataFrame(worksheet.get_all_records())
    return df, worksheet, spreadsheet

# 🔄 Push updated DataFrame to Google Sheet
def update_data_to_gsheet(sheet, df):
    sheet.clear()
    data = [df.columns.tolist()] + df.values.tolist()
    sheet.update('A1', data)

# 📊 Load all yearly data from "test-" sheets
def load_yearly_data(spreadsheet):
    yearly_data = {}
    for sheet in spreadsheet.worksheets():
        if sheet.title.lower().startswith("test-"):
            df = pd.DataFrame(sheet.get_all_records())
            if not df.empty:
                df['year'] = sheet.title.split('-')[-1]
                df['credit'] = pd.to_numeric(df.get('credit', 0), errors='coerce').fillna(0)
                df['debit'] = pd.to_numeric(df.get('debit', 0), errors='coerce').fillna(0)
                yearly_data[sheet.title] = df
    return yearly_data
