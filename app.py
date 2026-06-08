import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import json

# --- KONFIGURASI ---
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds_dict = json.loads(st.secrets["GOOGLE_SHEETS_CREDENTIALS"])
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)
SPREADSHEET_ID = '1GhL5zy_SYsoOCAOvvcTZO3-vXItrPvkIKNMk_w5oErY'

# --- FUNGSI ---
def check_login(user, pwd):
    ws = client.open_by_key(SPREADSHEET_ID).worksheet('users')
    df = pd.DataFrame(ws.get_all_records())
    if df.empty: return False
    # Mencocokkan kolom 'id' dan 'pass' sesuai sheet Anda
    match = df[(df['id'].astype(str) == str(user)) & (df['pass'].astype(str) == str(pwd))]
    return not match.empty

# --- APP FLOW ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("Login Monitoring")
    tab1, tab2 = st.tabs(["Sign In", "Sign Up"])
    
    with tab1:
        u = st.text_input("Username", key="u1")
        p = st.text_input("Password", type="password", key="p1")
        if st.button("Masuk"):
            if check_login(u, p):
                st.session_state.logged_in = True
                st.rerun()
            else: st.error("User atau Password salah!")
            
    with tab2:
        nu = st.text_input("Username Baru", key="u2")
        np = st.text_input("Password Baru", type="password", key="p2")
        fn = st.text_input("Nama Depan", key="fn")
        ln = st.text_input("Nama Belakang", key="ln")
        if st.button("Daftar"):
            if nu and np and fn and ln:
                # Menambahkan data ke kolom id, pass, fn, ln
                client.open_by_key(SPREADSHEET_ID).worksheet('users').append_row([nu, np, fn, ln])
                st.success("Akun berhasil dibuat! Silakan pindah ke tab Sign In.")
            else: st.warning("Mohon lengkapi semua kolom!")
    st.stop()

# --- DASHBOARD ---
st.title("Monitoring Genset Realtime")
if st.button("Log Out"): 
    st.session_state.logged_in = False
    st.rerun()

try:
    data = client.open_by_key(SPREADSHEET_ID).worksheet('Sheet2').get_all_records()
    st.dataframe(pd.DataFrame(data))
except Exception as e:
    st.error(f"Error memuat data: {e}")
