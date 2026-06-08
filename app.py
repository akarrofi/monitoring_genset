import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import json

# 1. Konfigurasi akses Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds_dict = json.loads(st.secrets["GOOGLE_SHEETS_CREDENTIALS"])
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

# 2. Buka Spreadsheet (Ganti 'Nama_File_Sheets_Anda' dengan nama sheet Anda)
sheet = client.open('DSE 7320 MKII').worksheet('Sheet2')

# 3. Ambil data
data = sheet.get_all_records()
df = pd.DataFrame(data)

# 4. Tampilkan di Streamlit
st.title("Monitoring Genset Realtime")
st.dataframe(df) # Ini akan menampilkan data dalam bentuk tabel
