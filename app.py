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
# Bagian 1: CSS (GRADASI BIRU & ESTETIKA)
# ==================================
st.markdown("""
<style>
    /* Mengatur background halaman utama */
    [data-testid="stAppViewContainer"] {
        background-color: #f0f2f6 !important;
    }

    /* KOTAK LOGIN BIRU GRADASI */
    /* Menargetkan container border agar memiliki gradasi biru */
    [data-testid="stVerticalBlockBorderWrapper"] > div {
        background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%) !important;
        border-radius: 15px !important;
        border: none !important;
        padding: 20px !important;
        box-shadow: 0px 10px 25px rgba(0,0,0,0.2) !important;
    }

    /* Teks di dalam kartu agar putih */
    .stMarkdown h4, .stMarkdown p {
        color: white !important;
        margin-bottom: 0px !important;
    }

    /* Tombol Login (Biru Langit agar kontras) */
    div.stButton > button {
        background: linear-gradient(90deg, #00d2ff 0%, #3a7bd5 100%) !important;
        color: white !important;
        border-radius: 8px !important;
        font-weight: bold !important;
        border: none !important;
        height: 42px;
        width: 100%;
        margin-top: 15px;
    }
    
    div.stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0px 5px 15px rgba(0,210,255,0.3);
    }

    /* Logo Sumut di atas agar tidak terpotong */
    .logo-container {
        display: flex;
        justify-content: center;
        padding-top: 25px; /* Memberi ruang di atas logo */
        margin-bottom: -10px;
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
# Bagian 3: TAMPILAN LOGIN
# ==================================
if not st.session_state.login:
    
    # 1. LOGO SUMUT DI TENGAH (Kecil & Aman)
    st.markdown('<div class="logo-container">', unsafe_allow_html=True)
    col_s1, col_s2, col_s3 = st.columns([2, 0.3, 2]) # Rasio kecil di tengah
    with col_s2:
        if os.path.exists("logo_sumut.png"):
            st.image(Image.open("logo_sumut.png"), width=50)
        else:
            st.write("LOGO")
    st.markdown('</div>', unsafe_allow_html=True)

    # 2. KARTU LOGIN (Compact/Separuh)
    _, col_card, _ = st.columns([1.6, 2.2, 1.6]) 

    with col_card:
        # Container dengan gradasi biru (via CSS)
        with st.container(border=True):
            # Layout Horizontal: Logo Kiri, Form Kanan
            col_l, col_r = st.columns([0.8, 1.5])

            with col_l:
                st.write("") # Padding atas
                if os.path.exists("logo_sipandai.png"):
                    st.image(Image.open("logo_sipandai.png"), use_container_width=True)
                else:
                    st.write("SI-PANDAI")

            with col_r:
                st.markdown("<h4>LOGIN USER</h4>", unsafe_allow_html=True)
                st.markdown("<p style='font-size:11px; opacity:0.8;'>Sistem Pemetaan ATS Disabilitas</p>", unsafe_allow_html=True)
                
                # Input dengan Ikon di dalam placeholder
                user = st.text_input("Username", placeholder="👤  Masukkan Username", label_visibility="collapsed")
                pwd = st.text_input("Password", type="password", placeholder="🔑  Masukkan Password", label_visibility="collapsed")
                
                if st.button("MASUK KE SISTEM"):
                    # Logika dummy (Silakan hubungkan ke Excel Anda)
                    if user == "admin" and pwd == "admin":
                        st.session_state.login = True
                        st.session_state.role = "Admin"
                        st.rerun()
                    else:
                        st.error("Login Gagal", icon="⚠️")

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
