import streamlit as st

st.title("Sistem Monitoring Genset")
st.write("Selamat datang! Silakan login terlebih dahulu.")

user = st.text_input("ID Pegawai")
pwd = st.text_input("Password", type="password")

if st.button("Login"):
    if user == "admin" and pwd == "12345":
        st.success("Berhasil Login!")
        st.balloons()
    else:
        st.error("ID atau Password salah.")
