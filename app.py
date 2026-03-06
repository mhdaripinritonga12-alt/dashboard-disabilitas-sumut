import streamlit as st
import pandas as pd
from PIL import Image
import os

# ==================================
# Bagian 0: KONFIGURASI HALAMAN
# ==================================
st.set_page_config(
    page_title="Login SI-PANDAI SUMUT",
    layout="wide",
    page_icon="🔒"
)

# ==================================
# Bagian 1: CSS CUSTOM (MODERN DESIGN WITH BACKGROUND IMAGE)
# ==================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&display=swap');
    
    html, body, [data-testid="stWidgetLabel"] {
        font-family: 'Inter', sans-serif !important;
    }

    /* BACKGROUND HALAMAN DENGAN GAMBAR & OVERLAY */
    [data-testid="stAppViewContainer"] {
        background-image: linear-gradient(rgba(15, 32, 39, 0.8), rgba(32, 58, 67, 0.8)), 
                          url("https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&w=2072&auto=format&fit=crop");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    /* Hapus header default agar bersih */
    header {visibility: hidden;}

    /* KOTAK LOGIN: GLASSMORPHISM EFFECT */
    /* Membuat kotak terlihat semi-transparan seperti kaca */
    [data-testid="stVerticalBlockBorderWrapper"] > div {
        background: rgba(255, 255, 255, 0.9) !important;
        backdrop-filter: blur(10px); /* Efek blur di belakang kotak */
        border-radius: 24px !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        padding: 35px !important;
        box-shadow: 0px 20px 40px rgba(0,0,0,0.3) !important;
    }

    /* Judul & Teks */
    .login-title {
        color: #073642 !important;
        font-size: 26px !important;
        font-weight: 800 !important;
        margin-bottom: 2px !important;
    }
    
    .login-subtitle {
        color: #1D976C !important;
        font-size: 13px !important;
        font-weight: 600;
        margin-bottom: 25px !important;
    }

    /* Input Field Custom */
    div[data-testid="stTextInput"] input {
        border-radius: 12px !important;
        border: 1.5px solid #d1d9e0 !important;
        height: 45px !important;
    }

    /* Tombol Login Vibrant */
    div.stButton > button {
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%) !important;
        color: white !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        height: 50px;
        border: none !important;
        width: 100%;
        margin-top: 20px;
        box-shadow: 0px 4px 15px rgba(30, 60, 114, 0.4);
    }
    
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0px 8px 25px rgba(30, 60, 114, 0.5);
    }

    .logo-header {
        display: flex;
        justify-content: center;
        padding: 30px 0 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# ==================================
# Bagian 2: TAMPILAN LOGIN
# ==================================
if "login" not in st.session_state:
    st.session_state.login = False

if not st.session_state.login:
    
    # 1. LOGO SUMUT (DIPERBESAR & DI TENGAH)
    st.markdown('<div class="logo-header">', unsafe_allow_html=True)
    col_l1, col_l2, col_l3 = st.columns([2, 0.6, 2])
    with col_l2:
        if os.path.exists("logo_sumut.png"):
            st.image(Image.open("logo_sumut.png"), width=110)
    st.markdown('</div>', unsafe_allow_html=True)

    # 2. KARTU LOGIN (COMPACT HORIZONTAL)
    _, col_card, _ = st.columns([1.4, 2.6, 1.4]) 

    with col_card:
        with st.container(border=True):
            col_left, col_right = st.columns([1, 1.5])

            with col_left:
                st.write("") 
                if os.path.exists("logo_sipandai.png"):
                    st.image(Image.open("logo_sipandai.png"), use_container_width=True)

            with col_right:
                st.markdown('<div class="login-title">LOGIN USER</div>', unsafe_allow_html=True)
                st.markdown('<div class="login-subtitle">SI-PANDAI SUMUT</div>', unsafe_allow_html=True)
                
                username = st.text_input("Username", placeholder="👤  Username", label_visibility="collapsed")
                password = st.text_input("Password", type="password", placeholder="🔑  Password", label_visibility="collapsed")
                
                if st.button("MASUK KE DASHBOARD"):
                    # Logika Dummy (Ganti dengan pengecekan Excel Anda)
                    if username == "admin" and password == "admin":
                        st.session_state.login = True
                        st.rerun()
                    else:
                        st.error("Username/Password Salah")

    st.markdown('<p style="text-align:center; color:rgba(255,255,255,0.6); font-size:12px; margin-top:30px; font-weight:bold;">© 2026 Dinas Pendidikan Provinsi Sumatera Utara</p>', unsafe_allow_html=True)
    st.stop()

# ==================================
# DASHBOARD AREA
# ==================================
st.title("Selamat Datang, Anda Berhasil Masuk!")
if st.button("Keluar"):
    st.session_state.login = False
    st.rerun()
