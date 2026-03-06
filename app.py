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
# Bagian 1: CSS CUSTOM (GLASSMORPHISM PREMIUM)
# ==================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&display=swap');
    
    html, body, [data-testid="stWidgetLabel"] {
        font-family: 'Inter', sans-serif !important;
    }

    /* BACKGROUND HALAMAN */
    [data-testid="stAppViewContainer"] {
        background-image: linear-gradient(rgba(10, 25, 30, 0.7), rgba(20, 45, 55, 0.7)), 
                          url("https://images.unsplash.com/photo-1557683316-973673baf926?q=80&w=2029&auto=format&fit=crop");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    header {visibility: hidden;}

    /* KOTAK LOGIN UTAMA (PUTIH SEMI-TRANSPARAN) */
    [data-testid="stVerticalBlockBorderWrapper"] > div {
        background: rgba(255, 255, 255, 0.15) !important; /* Putih Transparan */
        backdrop-filter: blur(15px); /* Efek Kaca Blur */
        -webkit-backdrop-filter: blur(15px);
        border-radius: 20px !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        padding: 30px !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37) !important;
    }

    /* CONTAINER LOGO SI-PANDAI (PUTIH SEMI-TRANSPARAN DI DALAM) */
    .logo-sipandai-box {
        background: rgba(255, 255, 255, 0.2);
        padding: 20px;
        border-radius: 15px;
        display: flex;
        justify-content: center;
        align-items: center;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 10px;
    }

    /* Teks Judul & Subtitle */
    .login-title {
        color: #ffffff !important;
        font-size: 26px !important;
        font-weight: 800 !important;
        text-shadow: 1px 1px 4px rgba(0,0,0,0.3);
    }
    
    .login-subtitle {
        color: #00d2ff !important; /* Biru Cerah agar kontras di kaca */
        font-size: 13px !important;
        font-weight: 600;
        margin-bottom: 25px !important;
    }

    /* Input Field Custom (Transparan dengan border putih) */
    div[data-testid="stTextInput"] input {
        background-color: rgba(255, 255, 255, 0.9) !important;
        border-radius: 10px !important;
        border: none !important;
        height: 45px !important;
        color: #333 !important;
    }

    /* Tombol Login Vibrant */
    div.stButton > button {
        background: linear-gradient(90deg, #00d2ff 0%, #3a7bd5 100%) !important;
        color: white !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        height: 48px;
        border: none !important;
        width: 100%;
        margin-top: 15px;
    }
    
    div.stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0px 5px 20px rgba(0,210,255,0.4);
    }

    .logo-sumut-header {
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
    
    # 1. LOGO SUMUT (DI TENGAH ATAS)
    st.markdown('<div class="logo-sumut-header">', unsafe_allow_html=True)
    col_t1, col_t2, col_t3 = st.columns([2, 0.4, 2])
    with col_t2:
        if os.path.exists("logo_sumut.png"):
            st.image(Image.open("logo_sumut.png"), width=80)
    st.markdown('</div>', unsafe_allow_html=True)

    # 2. KARTU LOGIN GLASSMORPHISM
    _, col_card, _ = st.columns([1.5, 2.5, 1.5]) 

    with col_card:
        with st.container(border=True):
            col_l, col_r = st.columns([1, 1.4])

            with col_l:
                # Bungkus Logo SI-PANDAI dalam kotak transparan
                st.markdown('<div class="logo-sipandai-box">', unsafe_allow_html=True)
                if os.path.exists("logo_sipandai.png"):
                    st.image(Image.open("logo_sipandai.png"), use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)

            with col_r:
                st.markdown('<div class="login-title">LOGIN USER</div>', unsafe_allow_html=True)
                st.markdown('<div class="login-subtitle">SI-PANDAI SUMUT</div>', unsafe_allow_html=True)
                
                # Ikon Row
                user = st.text_input("Username", placeholder="👤  Masukkan Username", label_visibility="collapsed")
                pwd = st.text_input("Password", type="password", placeholder="🔑  Masukkan Password", label_visibility="collapsed")
                
                if st.button("MASUK SISTEM"):
                    if user == "admin" and pwd == "admin":
                        st.session_state.login = True
                        st.rerun()
                    else:
                        st.error("Gagal Masuk")

    st.markdown('<p style="text-align:center; color:rgba(255,255,255,0.5); font-size:11px; margin-top:25px;">Dinas Pendidikan Provinsi Sumatera Utara © 2026</p>', unsafe_allow_html=True)
    st.stop()

# ==================================
# DASHBOARD SETELAH LOGIN
# ==================================
st.title("Dashboard SI-PANDAI SUMUT")
if st.button("Keluar"):
    st.session_state.login = False
    st.rerun()
