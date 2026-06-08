import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import json

# --- KONFIGURASI AWAL ---
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds_dict = json.loads(st.secrets["GOOGLE_SHEETS_CREDENTIALS"])
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)
SPREADSHEET_ID = '1GhL5zy_SYsoOCAOvvcTZO3-vXItrPvkIKNMk_w5oErY'

# --- FUNGSI AUTH ---
def authenticate(username, password):
    users_sheet = client.open_by_key(SPREADSHEET_ID).worksheet('users')
    users_data = pd.DataFrame(users_sheet.get_all_records())
    if users_data.empty: return False
    user_match = users_data[(users_data['username'] == username) & (users_data['password'] == password)]
    return not user_match.empty

def register(username, password):
    users_sheet = client.open_by_key(SPREADSHEET_ID).worksheet('users')
    users_sheet.append_row([username, password])

# --- LOGIKA APLIKASI ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("Login Monitoring Genset")
    tab1, tab2 = st.tabs(["Sign In", "Sign Up"])
    
    with tab1:
        user = st.text_input("Username", key="login_user")
        pwd = st.text_input("Password", type="password", key="login_pwd")
        if st.button("Sign In"):
            if authenticate(user, pwd):
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Username atau Password salah!")
                
    with tab2:
        new_user = st.text_input("Username Baru")
        new_pwd = st.text_input("Password Baru", type="password")
        if st.button("Sign Up"):
            if new_user and new_pwd:
                register(new_user, new_pwd)
                st.success("Akun berhasil dibuat! Silakan pindah ke tab Sign In.")
            else:
                st.warning("Mohon isi username dan password.")
    st.stop()

# --- DASHBOARD SETELAH LOGIN ---
st.title("Monitoring Genset Realtime")
if st.button("Log Out"):
    st.session_state.logged_in = False
    st.rerun()

try:
    sheet = client.open_by_key(SPREADSHEET_ID).worksheet('Sheet2')
    data = sheet.get_all_records()
    df = pd.DataFrame(data)
    st.dataframe(df)
except Exception as e:
    st.error(f"Terjadi kesalahan saat memuat data: {e}")
