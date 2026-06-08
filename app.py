import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import json

# Fungsi untuk mengecek password
def check_password():
    def password_entered():
        if st.session_state["password"] == "Genset123": # Ganti password Anda di sini
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # Halaman Login
        st.text_input("Masukkan Password", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        # Jika salah password
        st.text_input("Password Salah. Coba lagi:", type="password", on_change=password_entered, key="password")
        st.error("Password salah")
        return False
    else:
        # Jika benar, lanjut ke aplikasi
        return True

# PANGGIL FUNGSI INI
if not check_password():
    st.stop() # Menghentikan jalannya aplikasi jika belum login

# --- DI BAWAH INI ADALAH KODE MONITORING ANDA YANG TADI ---
# ... kode koneksi Google Sheets dll ...

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
