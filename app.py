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
# Bagian 1: CSS CUSTOM (SUMUT BACKGROUND & GLASSMORPHISM)
# ==================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&display=swap');
    
    html, body, [data-testid="stWidgetLabel"] {
        font-family: 'Inter', sans-serif !important;
    }

    /* BACKGROUND PEMANDANGAN SUMUT DENGAN OVERLAY GELAP */
    [data-testid="stAppViewContainer"] {
        background-image: linear-gradient(rgba(0, 0, 0, 0.65), rgba(0, 0, 0, 0.65)), 
                          url("https://images.unsplash.com/photo-1571746243149-6012b84299ec?q=80&w=2000&auto=format&fit=crop");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    header {visibility: hidden;}

    /* KOTAK LOGIN: PUTIH SEMI-TRANSPARAN (GLASSMORPHISM) */
    [data-testid="stVerticalBlockBorderWrapper"] > div {
        background: rgba(255, 255, 255, 0.12) !important; /* Putih Transparan Tipis */
        backdrop-filter: blur(20px); /* Efek Blur Kaca */
        -webkit-backdrop-filter: blur(20px);
        border-radius: 25px !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        padding: 40px !important;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.5) !important;
    }

    /* WADAH LOGO SI-PANDAI (SEMI-TRANSPARAN) */
    .logo-sipandai-box {
        background: rgba(255, 255, 255, 0.15);
        padding: 25px;
        border-radius: 20px;
        display: flex;
        justify-content: center;
        align-items: center;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 10px;
    }

    /* Teks Judul & Subtitle */
    .login-title {
        color: #ffffff !important;
        font-size: 28px !important;
        font-weight: 800 !important;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.5);
    }
    
    .login-subtitle {
        color: #00e5ff !important; /* Biru Neon agar menyala di latar gelap */
        font-size: 14px !important;
        font-weight: 700;
        margin-bottom: 30px !important;
        letter-spacing: 1px;
    }

    /* Input Field (Sangat Bersih) */
    div[data-testid="stTextInput"] input {
        background-color: rgba(255, 255, 255, 0.95) !important;
        border-radius: 12px !important;
        border: none !important;
        height: 48px !important;
        color: #222 !important;
        font-weight: 500;
    }

    /* Tombol Login Vibrant */
    div.stButton > button {
        background: linear-gradient(90deg, #00d2ff 0%, #3a7bd5 100%) !important;
        color: white !important;
        border-radius: 12px !important;
        font-weight: 800 !important;
        height: 52px;
        border: none !important;
        width: 100%;
        margin-top: 20px;
        text-transform: uppercase;
        letter-spacing: 1px;
        box-shadow: 0px 5px 20px rgba(0, 210, 255, 0.4);
    }
    
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0px 8px 30px rgba(0, 210, 255, 0.6);
    }

    /* Logo Sumut di Atas */
    .logo-sumut-header {
        display: flex;
        justify-content: center;
        padding: 50px 0 20px 0;
    }
</style>
""", unsafe_allow_html=True)

# ==================================
# Bagian 2: TAMPILAN LOGIN
# ==================================
if "login" not in st.session_state:
    st.session_state.login = False

if not st.session_state.login:
    
    # 1. LOGO SUMUT (TENGAH ATAS - UKURAN PAS)
    st.markdown('<div class="logo-sumut-header">', unsafe_allow_html=True)
    col_t1, col_t2, col_t3 = st.columns([2, 0.4, 2])
    with col_t2:
        # Menggunakan logo_sumut.png dengan ukuran yang diperbesar namun tetap aman
        if os.path.exists("logo_sumut.png"):
            st.image(Image.open("logo_sumut.png"), width=90)
    st.markdown('</div>', unsafe_allow_html=True)

    # 2. KARTU LOGIN GLASSMORPHISM (HORIZONTAL)
    _, col_card, _ = st.columns([1.2, 2.8, 1.2]) 

    with col_card:
        with st.container(border=True):
            col_l, col_r = st.columns([1, 1.3])

            with col_l:
                # Kotak logo SI-PANDAI semi-transparan
                st.markdown('<div class="logo-sipandai-box">', unsafe_allow_html=True)
                if os.path.exists("logo_sipandai.png"):
                    st.image(Image.open("logo_sipandai.png"), use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)

            with col_r:
                st.markdown('<div class="login-title">LOGIN USER</div>', unsafe_allow_html=True)
                st.markdown('<div class="login-subtitle">SI-PANDAI SUMUT</div>', unsafe_allow_html=True)
                
                # Baris User & Password
                user = st.text_input("Username", placeholder="👤  Username", label_visibility="collapsed")
                pwd = st.text_input("Password", type="password", placeholder="🔑  Password", label_visibility="collapsed")
                
                if st.button("MASUK SISTEM"):
                    if user == "admin" and pwd == "admin":
                        st.session_state.login = True
                        st.rerun()
                    else:
                        st.error("Gagal Login")

    st.markdown('<p style="text-align:center; color:rgba(255,255,255,0.6); font-size:12px; margin-top:30px; font-weight:700;">DINAS PENDIDIKAN PROVINSI SUMATERA UTARA © 2026</p>', unsafe_allow_html=True)
    st.stop()

# ==================================
# HALAMAN DASHBOARD (SETELAH LOGIN)
# ==================================
st.title("Berhasil Masuk ke Dashboard SI-PANDAI")
if st.button("Logout"):
    st.session_state.login = False
    st.rerun()
