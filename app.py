import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import json

# 1. Konfigurasi akses (Sudah benar)
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds_dict = json.loads(st.secrets["GOOGLE_SHEETS_CREDENTIALS"])
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

# 2. GANTI DENGAN SPREADSHEET ID (Jauh lebih stabil daripada pakai Nama)
# Copy ID dari URL spreadsheet Anda (kumpulan huruf/angka di antara /d/ dan /edit)
SPREADSHEET_ID = '1GhL5zy_SYsoOCAOvvcTZO3-vXItrPvkIKNMk_w5oErY' 

try:
    # Membuka dengan ID
    sheet = client.open_by_key(SPREADSHEET_ID).worksheet('Sheet2')
    
    # 3. Ambil data
    data = sheet.get_all_records()
    df = pd.DataFrame(data)

    # 4. Tampilkan di Streamlit
    st.title("Monitoring Genset Realtime")
    st.dataframe(df)

except Exception as e:
    st.error(f"Terjadi kesalahan saat memuat data: {e}")
    st.write("Pastikan Spreadsheet ID sudah benar dan bot email sudah di-Share sebagai Editor.")
