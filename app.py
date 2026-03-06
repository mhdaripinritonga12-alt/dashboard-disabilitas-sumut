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
# Bagian 1: CSS CUSTOM (GRADASI BIRU & LAYOUT KARTU)
# ==================================
st.markdown("""
<style>
    /* Latar belakang halaman */
    [data-testid="stAppViewContainer"] {
        background-color: #f4f7f9 !important;
    }

    /* Menghilangkan header default agar bersih */
    header {visibility: hidden;}

    /* Logo Sumut di tengah atas */
    .logo-top-container {
        display: flex;
        justify-content: center;
        padding-top: 20px;
        margin-bottom: -10px;
    }

    /* KARTU LOGIN UTAMA (BIRU GRADASI) */
    .stColumn > div > div > div[data-testid="stVerticalBlock"] {
        /* Container kartu */
    }

    [data-testid="stVerticalBlockBorderWrapper"] > div {
        background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%) !important; /* Gradasi Biru Deep */
        border-radius: 12px !important;
        border: none !important;
        padding: 15px !important;
        box-shadow: 0px 10px 25px rgba(0,0,0,0.2) !important;
    }

    /* Teks di dalam kartu */
    .stMarkdown h4 {
        color: #ffffff !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-weight: 700 !important;
        margin-bottom: 0px !important;
    }
    .stMarkdown p {
        color: #a0d2eb !important;
        font-size: 11px !important;
        margin-bottom: 20px !important;
    }

    /* Gaya Input Field agar Ikon terlihat bagus */
    div[data-testid="stTextInput"] input {
        border-radius: 8px !important;
        background-color: rgba(255, 255, 255, 0.95) !important;
        border: 1px solid #ddd !important;
        color: #333 !important;
    }

    /* Tombol Login */
    div.stButton > button {
        background: linear-gradient(90deg, #00d2ff 0%, #3a7bd5 100%) !important;
        color: white !important;
        border-radius: 8px !important;
        font-weight: bold !important;
        border: none !important;
        width: 100%;
        height: 40px;
        margin-top: 10px;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0px 5px 15px rgba(0,210,255,0.4);
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

    # 1. Logo Sumut (DITENGAH & TIDAK TERPOTONG)
    st.markdown('<div class="logo-top-container">', unsafe_allow_html=True)
    col_t1, col_t2, col_t3 = st.columns([2, 0.4, 2])
    with col_t2:
        if os.path.exists("logo_sumut.png"):
            st.image(Image.open("logo_sumut.png"), width=50) # Ukuran diperkecil agar pas
    st.markdown('</div>', unsafe_allow_html=True)

    st.write("") # Jarak

    # 2. KARTU LOGIN (COMPACT / SEPARUH LEBAR)
    _, col_card, _ = st.columns([1.6, 2.2, 1.6]) 

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
# DASHBOARD (Hanya tampil setelah login)
# ==================================
st.title("Dashboard SI-PANDAI SUMUT")
st.write(f"Selamat datang, **{st.session_state.role}**")
if st.button("Logout"):
    st.session_state.login = False
    st.rerun()
    
