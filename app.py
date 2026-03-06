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
# Bagian 1: CSS CUSTOM (MODERN DESIGN)
# ==================================
st.markdown("""
<style>
    /* Menggunakan Font yang lebih modern */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&display=swap');
    
    html, body, [data-testid="stWidgetLabel"] {
        font-family: 'Inter', sans-serif !important;
    }

    /* Background Halaman */
    [data-testid="stAppViewContainer"] {
        background-color: #f0f4f8 !important;
    }

    /* KOTAK LOGIN: BIRU LEMBUT GRADASI PUTIH (LINEAR) */
    [data-testid="stVerticalBlockBorderWrapper"] > div {
        background: linear-gradient(180deg, #e3f2fd 0%, #ffffff 100%) !important;
        border-radius: 24px !important; /* Lebih bulat agar modern */
        border: 1px solid rgba(255, 255, 255, 0.8) !important;
        padding: 35px !important;
        box-shadow: 0px 20px 40px rgba(0,0,0,0.05) !important;
    }

    /* Teks Judul LOGIN USER (Warna Biru Navy Tua) */
    .login-title {
        color: #0d47a1 !important;
        font-size: 24px !important;
        font-weight: 800 !important;
        margin-bottom: 2px !important;
        letter-spacing: -0.5px;
    }
    
    .login-subtitle {
        color: #546e7a !important;
        font-size: 13px !important;
        margin-bottom: 25px !important;
    }

    /* STYLE INPUT FIELD */
    div[data-testid="stTextInput"] input {
        border-radius: 12px !important;
        border: 1.5px solid #d1d9e0 !important;
        padding: 12px !important;
        background-color: white !important;
        transition: 0.3s;
    }
    
    div[data-testid="stTextInput"] input:focus {
        border-color: #1e88e5 !important;
        box-shadow: 0 0 0 3px rgba(30, 136, 229, 0.1) !important;
    }

    /* TOMBOL LOGIN (Vibrant Blue) */
    div.stButton > button {
        background: linear-gradient(90deg, #1565c0 0%, #1e88e5 100%) !important;
        color: white !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        height: 48px;
        border: none !important;
        width: 100%;
        margin-top: 20px;
        box-shadow: 0px 4px 15px rgba(21, 101, 192, 0.3);
    }
    
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0px 6px 20px rgba(21, 101, 192, 0.4);
    }

    /* Logo Sumut di atas */
    .logo-header {
        display: flex;
        justify-content: center;
        padding: 40px 0 20px 0;
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
    col_l1, col_l2, col_l3 = st.columns([2, 0.5, 2])
    with col_l2:
        if os.path.exists("logo_sumut.png"):
            # Ukuran dinaikkan ke 100 agar lebih dominan
            st.image(Image.open("logo_sumut.png"), width=100) 
    st.markdown('</div>', unsafe_allow_html=True)

    # 2. KARTU LOGIN (COMPACT HORIZONTAL)
    _, col_card, _ = st.columns([1.5, 2.5, 1.5]) 

    with col_card:
        with st.container(border=True):
            # Layout Horizontal: Logo Kiri, Form Kanan
            col_left, col_right = st.columns([1, 1.4])

            with col_left:
                st.write("") # Spasi vertikal agar logo rata tengah
                if os.path.exists("logo_sipandai.png"):
                    st.image(Image.open("logo_sipandai.png"), use_container_width=True)

            with col_right:
                # Judul & Subjudul
                st.markdown('<div class="login-title">LOGIN USER</div>', unsafe_allow_html=True)
                st.markdown('<div class="login-subtitle">Akses Dashboard SI-PANDAI SUMUT</div>', unsafe_allow_html=True)
                
                # Form Input
                username = st.text_input("Username", placeholder="👤  Username", label_visibility="collapsed")
                password = st.text_input("Password", type="password", placeholder="🔑  Password", label_visibility="collapsed")
                
                if st.button("MASUK KE DASHBOARD"):
                    if username == "admin" and password == "admin":
                        st.session_state.login = True
                        st.rerun()
                    else:
                        st.error("Credential Salah")

    st.markdown('<p style="text-align:center; color:#adb5bd; font-size:11px; margin-top:30px;">Dinas Pendidikan Provinsi Sumatera Utara © 2026</p>', unsafe_allow_html=True)
    st.stop()

# --- Dashboard Sederhana ---
st.title("Selamat Datang di Dashboard!")
if st.button("Keluar"):
    st.session_state.login = False
    st.rerun()

