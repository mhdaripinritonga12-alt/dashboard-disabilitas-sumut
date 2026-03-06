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
# Bagian 1: STYLE LOGIN (Sangat Ringkas & Horizontal)
# ==================================
st.markdown("""
<style>
    /* Mengatur latar belakang */
    [data-testid="stAppViewContainer"] {
        background-color: #f0f2f6 !important;
    }

    /* Menghilangkan header streamlit */
    header {visibility: hidden;}
    
    /* Container Utama */
    .main-login-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        margin-top: 80px;
    }

    /* LOGO SUMUT DI TENAH ATAS */
    .logo-sumut-center {
        margin-bottom: 20px;
        display: flex;
        justify-content: center;
    }

    /* KARTU LOGIN HORIZONTAL (Lebih Kecil/Compact) */
    .login-card-horizontal {
        display: flex;
        flex-direction: row; /* Horizontal */
        width: 550px; /* Ukuran total disusutkan */
        background-color: white;
        border-radius: 12px;
        box-shadow: 0px 8px 20px rgba(0,0,0,0.1);
        overflow: hidden;
        border: 1px solid #ddd;
    }

    /* Sisi Kiri (Tempat Logo SI-PANDAI) */
    .card-left-logo {
        background-color: #f8f9fa;
        flex: 1;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 20px;
        border-right: 1px solid #eee;
    }

    /* Sisi Kanan (Tempat Form Login) */
    .card-right-form {
        flex: 1.5;
        padding: 25px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }

    /* Header Form */
    .form-header {
        margin-bottom: 15px;
    }
    .form-header h2 {
        color: #073642 !important;
        font-size: 18px !important;
        font-weight: 800 !important;
        margin: 0 !important;
        letter-spacing: 0.5px;
    }
    .form-header p {
        color: #1D976C !important;
        font-size: 12px !important;
        margin: 0 !important;
        font-weight: 600;
    }

    /* Button Kecil & Padat */
    div.stButton > button {
        background-color: #1D976C !important;
        color: white !important;
        border-radius: 6px !important;
        font-weight: bold !important;
        height: 38px !important;
        border: none !important;
        width: 100%;
        margin-top: 10px;
    }

    /* Footer Info */
    .footer-note {
        margin-top: 15px;
        color: #888;
        font-size: 10px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# ==================================
# Bagian 2: LOAD DATA (Fungsi Inti)
# ==================================
FILE_PATH = "KOTA_MEDAN_LENGKAP_KELURAHAN_DISABILITAS.xlsx"

@st.cache_data
def load_users():
    if os.path.exists(FILE_PATH):
        return pd.read_excel(FILE_PATH, sheet_name="users")
    return pd.DataFrame(columns=["username", "password", "role"])

users = load_users()

if "login" not in st.session_state:
    st.session_state.login = False
    st.session_state.role = ""

# ==================================
# Bagian 3: HALAMAN LOGIN
# ==================================
if not st.session_state.login:
    
    # Bungkus dalam satu container besar
    st.markdown('<div class="main-login-container">', unsafe_allow_html=True)
    
    # 1. Logo Sumut (DITENGAH ATAS)
    st.markdown('<div class="logo-sumut-center">', unsafe_allow_html=True)
    if os.path.exists("logo_sumut.png"):
        st.image(Image.open("logo_sumut.png"), width=60)
    st.markdown('</div>', unsafe_allow_html=True)

    # 2. Kotak Login Horizontal
    # Menggunakan kolom agar layout card berada di tengah layar
    _, col_card, _ = st.columns([1, 2.5, 1])
    
    with col_card:
        # Kita mulai struktur HTML Card
        st.markdown('''
            <div class="login-card-horizontal">
                <div class="card-left-logo">
        ''', unsafe_allow_html=True)
        
        # Isian Sisi Kiri: Logo SI-PANDAI
        if os.path.exists("logo_sipandai.png"):
            st.image(Image.open("logo_sipandai.png"), width=100)
        else:
            st.write("Logo SI-PANDAI")

        # Pindah ke Sisi Kanan: Form
        st.markdown('''
                </div>
                <div class="card-right-form">
                    <div class="form-header">
                        <h2>LOGIN USER</h2>
                        <p>SI-PANDAI SUMUT</p>
                    </div>
        ''', unsafe_allow_html=True)
        
        # Input Streamlit (Native)
        username = st.text_input("Username", placeholder="Username", label_visibility="collapsed")
        password = st.text_input("Password", type="password", placeholder="Password", label_visibility="collapsed")
        
        if st.button("MASUK"):
            user = users[(users["username"] == username) & (users["password"] == password)]
            if not user.empty:
                st.session_state.login = True
                st.session_state.role = user.iloc[0]["role"]
                st.rerun()
            else:
                st.error("Gagal Login")

        # Tutup elemen HTML
        st.markdown('''
                    <div class="footer-note">© 2024 Dinas Pendidikan Provsu</div>
                </div>
            </div>
        ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# ==================================
# AREA DASHBOARD (HANYA SETELAH LOGIN)
# ==================================
st.title("Selamat Datang di Dashboard")
st.write(f"Anda masuk sebagai: **{st.session_state.role}**")
if st.button("Logout"):
    st.session_state.login = False
    st.rerun()
