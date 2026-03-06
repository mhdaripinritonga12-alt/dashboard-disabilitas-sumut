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
# Bagian 1: CSS CUSTOM (BIRU LEMBUT GRADASI)
# ==================================
st.markdown("""
<style>
    /* Background halaman utama */
    [data-testid="stAppViewContainer"] {
        background-color: #f8f9fa !important;
    }

    /* KOTAK LOGIN: BIRU LEMBUT GRADASI PUTIH */
    [data-testid="stVerticalBlockBorderWrapper"] > div {
        background: linear-gradient(180deg, #e3f2fd 0%, #ffffff 100%) !important;
        border-radius: 20px !important;
        border: 1px solid #cde4f7 !important;
        padding: 25px !important;
        box-shadow: 0px 10px 20px rgba(0,0,0,0.05) !important;
    }

    /* TULISAN DI DALAM KOTAK (Diubah ke gelap agar kontras) */
    .stMarkdown h4 {
        color: #073642 !important; /* Biru Gelap */
        font-weight: 800 !important;
        margin-bottom: 0px !important;
    }
    .stMarkdown p {
        color: #34495e !important; /* Abu-abu Gelap */
        font-size: 12px !important;
        margin-bottom: 20px !important;
    }

    /* INPUT FIELD */
    div[data-testid="stTextInput"] input {
        border-radius: 10px !important;
        border: 1px solid #d1d9e0 !important;
        background-color: white !important;
        color: #333 !important;
    }

    /* TOMBOL LOGIN (Biru Profesional) */
    div.stButton > button {
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%) !important;
        color: white !important;
        border-radius: 10px !important;
        font-weight: bold !important;
        height: 45px;
        border: none !important;
        width: 100%;
        margin-top: 15px;
    }
    
    div.stButton > button:hover {
        opacity: 0.9;
        transform: scale(1.01);
    }

    /* Container Logo Sumut */
    .logo-sumut-container {
        display: flex;
        justify-content: center;
        padding-top: 10px;
        margin-bottom: 15px;
    }
</style>
""", unsafe_allow_html=True)

# ==================================
# Bagian 2: LOGIKA SESSION
# ==================================
if "login" not in st.session_state:
    st.session_state.login = False
    st.session_state.role = ""

# ==================================
# Bagian 3: TAMPILAN LOGIN
# ==================================
if not st.session_state.login:
    
    # 1. LOGO SUMUT (DIBESARKAN & DI TENGAH)
    st.markdown('<div class="logo-sumut-container">', unsafe_allow_html=True)
    col_s1, col_s2, col_s3 = st.columns([1.8, 0.4, 1.8]) # Kolom tengah diperlebar sedikit
    with col_s2:
        if os.path.exists("logo_sumut.png"):
            # Ukuran width dinaikkan ke 80 agar terlihat lebih gagah
            st.image(Image.open("logo_sumut.png"), width=80) 
    st.markdown('</div>', unsafe_allow_html=True)

    # 2. KARTU LOGIN (COMPACT)
    _, col_card, _ = st.columns([1.6, 2.2, 1.6]) 

    with col_card:
        with st.container(border=True):
            # Layout Horizontal
            col_l, col_r = st.columns([0.8, 1.5])

            with col_l:
                st.write("") # Spasi atas
                if os.path.exists("logo_sipandai.png"):
                    st.image(Image.open("logo_sipandai.png"), use_container_width=True)

            with col_r:
                # Judul menggunakan warna gelap
                st.markdown("<h4>LOGIN USER</h4>", unsafe_allow_html=True)
                st.markdown("<p>Sistem Pemetaan ATS Disabilitas</p>", unsafe_allow_html=True)
                
                # Input dengan Ikon
                user = st.text_input("Username", placeholder="👤  Username", label_visibility="collapsed")
                pwd = st.text_input("Password", type="password", placeholder="🔑  Password", label_visibility="collapsed")
                
                if st.button("MASUK SISTEM"):
                    if user == "admin" and pwd == "admin":
                        st.session_state.login = True
                        st.session_state.role = "Admin"
                        st.rerun()
                    else:
                        st.error("Gagal Login", icon="⚠️")

    st.markdown('<p style="text-align:center; color:#bbb; font-size:11px; margin-top:20px;">© 2024 Dinas Pendidikan Provinsi Sumatera Utara</p>', unsafe_allow_html=True)
    st.stop()

# ==================================
# Bagian 4: DASHBOARD
# ==================================
st.success(f"Selamat Datang, {st.session_state.role}")
if st.button("Logout"):
    st.session_state.login = False
    st.rerun()
