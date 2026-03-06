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
# Bagian 1: CSS CUSTOM (GRADASI BIRU & ICON)
# ==================================
st.markdown("""
<style>
    /* Mengatur latar belakang halaman */
    [data-testid="stAppViewContainer"] {
        background-color: #f0f2f6 !important;
    }

    /* KOTAK LOGIN BIRU GRADASI */
    .stColumn > div > div > div[data-testid="stVerticalBlock"] {
        /* Ini akan menargetkan container di dalam kolom */
    }
    
    /* Custom Card Style untuk Container */
    [data-testid="stVerticalBlockBorderWrapper"] > div {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%) !important;
        border-radius: 15px !important;
        border: none !important;
        padding: 10px !important;
        color: white !important;
    }

    /* Mengatur Teks Putih di Dalam Kartu */
    .stMarkdown h4, .stMarkdown p {
        color: white !important;
    }

    /* Tombol Login (Teal agar kontras dengan biru) */
    div.stButton > button {
        background-color: #00d2ff !important;
        color: #002147 !important;
        border-radius: 8px !important;
        font-weight: bold !important;
        border: none !important;
        width: 100%;
        height: 42px;
        transition: 0.3s;
    }
    
    div.stButton > button:hover {
        background-color: #ffffff !important;
        transform: scale(1.02);
    }

    /* Logo Sumut agar tidak terpotong */
    .logo-top {
        padding-top: 10px;
        display: flex;
        justify-content: center;
    }

    /* Menghilangkan label input agar bersih */
    label[data-testid="stWidgetLabel"] {
        display: none;
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
    
    # 1. LOGO SUMUT (DITENGAH & LEBIH KECIL)
    # Menggunakan kolom rasio tinggi agar pas di tengah
    st.markdown('<div class="logo-top">', unsafe_allow_html=True)
    col_s1, col_s2, col_s3 = st.columns([2, 0.3, 2])
    with col_s2:
        if os.path.exists("logo_sumut.png"):
            st.image(Image.open("logo_sumut.png"), width=55) # Ukuran diperkecil agar tidak terpotong
    st.markdown('</div>', unsafe_allow_html=True)

    st.write("") # Spasi

    # 2. KARTU LOGIN (UKURAN COMPACT/SEPARUH)
    _, col_card, _ = st.columns([1.6, 2, 1.6]) 

    with col_card:
        # Menggunakan Container dengan Border (CSS akan mengubahnya jadi Biru Gradasi)
        with st.container(border=True):
            # Layout Horizontal: Logo Kiri, Form Kanan
            col_logo, col_form = st.columns([1, 1.6])

            with col_logo:
                st.write("") # Padding atas logo
                if os.path.exists("logo_sipandai.png"):
                    st.image(Image.open("logo_sipandai.png"), use_container_width=True)
                else:
                    st.write("SI-PANDAI")

            with col_form:
                st.markdown("<h4 style='margin:0;'>LOGIN USER</h4>", unsafe_allow_html=True)
                st.markdown("<p style='margin:0 0 15px 0; font-size:12px; opacity:0.8;'>Sistem Pemetaan ATS Disabilitas</p>", unsafe_allow_html=True)
                
                # Ikon orang dan kunci diletakkan di dalam placeholder
                username = st.text_input("Username", placeholder="👤 Username", key="user_input")
                password = st.text_input("Password", type="password", placeholder="🔑 Password", key="pass_input")
                
                st.write("") # Spasi sebelum tombol
                
                if st.button("MASUK SISTEM"):
                    # Dummy Check (Ganti dengan logika Excel Anda)
                    if username == "admin" and password == "admin":
                        st.session_state.login = True
                        st.session_state.role = "admin"
                        st.rerun()
                    else:
                        st.error("Akses Ditolak", icon="🚫")

        st.markdown('<p style="text-align:center; font-size:10px; color:#888; margin-top:10px;">© 2024 Dinas Pendidikan Provinsi Sumatera Utara</p>', unsafe_allow_html=True)

    st.stop()

# ==================================
# Bagian 4: DASHBOARD (SETELAH LOGIN)
# ==================================
st.success(f"Berhasil Masuk sebagai {st.session_state.role}")
if st.button("Keluar"):
    st.session_state.login = False
    st.rerun()
