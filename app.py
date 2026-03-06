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
# Bagian 1: CSS (UNTUK KARTU & ESTETIKA)
# ==================================
st.markdown("""
<style>
    /* Mengatur background halaman */
    [data-testid="stAppViewContainer"] {
        background-color: #f8f9fa !important;
    }

    /* Hilangkan padding berlebih di atas */
    .block-container {
        padding-top: 2rem !important;
    }

    /* Gaya Kartu Login */
    .stColumn > div > div > div {
        /* Target kolom tengah untuk dijadikan kartu */
    }
    
    /* Tombol Login Teal */
    div.stButton > button {
        background-color: #1D976C !important;
        color: white !important;
        border-radius: 6px !important;
        font-weight: bold !important;
        border: none !important;
        width: 100%;
        height: 40px;
    }
    
    /* Input Style agar lebih compact */
    div[data-testid="stTextInput"] {
        margin-bottom: -15px;
    }

    /* Footer Text */
    .footer-text {
        text-align: center;
        font-size: 11px;
        color: #999;
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ==================================
# Bagian 2: LOGIKA LOGIN
# ==================================
if "login" not in st.session_state:
    st.session_state.login = False
    st.session_state.role = ""

# ==================================
# Bagian 3: TAMPILAN LOGIN (KARTU COMPACT)
# ==================================
if not st.session_state.login:
    
    # 1. LOGO SUMUT DI TENGAH (Kecil)
    col_s1, col_s2, col_s3 = st.columns([2, 0.4, 2])
    with col_s2:
        if os.path.exists("logo_sumut.png"):
            st.image(Image.open("logo_sumut.png"), use_container_width=True)
        else:
            st.write("LOGO")

    # 2. KARTU LOGIN (Ukuran Separuh/Kecil)
    # Gunakan perbandingan kolom agar kartu berada di tengah dan tidak terlalu lebar
    _, col_card, _ = st.columns([1.5, 2, 1.5]) 

  with col_card:
        # Kotak dengan gradasi biru (diatur via CSS)
        with st.container(border=True):
            # Layout Horizontal: Logo SI-PANDAI (Kiri), Form (Kanan)
            col_l, col_r = st.columns([0.8, 1.5])

            with col_l:
                st.write("") # Spasi atas logo
                if os.path.exists("logo_sipandai.png"):
                    st.image(Image.open("logo_sipandai.png"), use_container_width=True)
                else:
                    st.write("SI-PANDAI")

            with col_r:
                st.markdown("<h4>LOGIN USER</h4>", unsafe_allow_html=True)
                st.markdown("<p>Sistem Pemetaan ATS Disabilitas Sumatera Utara</p>", unsafe_allow_html=True)
                
                # Input dengan Ikon di dalam placeholder
                user = st.text_input("Username", placeholder="👤  Masukkan Username", label_visibility="collapsed")
                pwd = st.text_input("Password", type="password", placeholder="🔑  Masukkan Password", label_visibility="collapsed")
                
                if st.button("MASUK KE SISTEM"):
                    # Logika pengecekan (Dummy)
                    if user == "admin" and pwd == "admin":
                        st.session_state.login = True
                        st.session_state.role = "Admin"
                        st.rerun()
                    else:
                        st.error("Gagal Masuk", icon="⚠️")

    st.markdown('<div style="text-align:center; color:#999; font-size:10px; margin-top:15px;">© 2024 Dinas Pendidikan Provinsi Sumatera Utara</div>', unsafe_allow_html=True)
    st.stop()
# ==================================
# Bagian 4: DASHBOARD (SETELAH LOGIN)
# ==================================
st.title("Berhasil Login")
st.write(f"Selamat datang, **{st.session_state.role}**")
if st.button("Logout"):
    st.session_state.login = False
    st.rerun()


