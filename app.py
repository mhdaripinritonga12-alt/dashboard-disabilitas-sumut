import streamlit as st
import pandas as pd
from PIL import Image
import os
from io import BytesIO
import plotly.express as px
import base64

# ==================================
# Bagian 0: KONFIGURASI HALAMAN
# ==================================
st.set_page_config(
    page_title="SI-PANDAI SUMUT",
    layout="wide",
    page_icon="🔒"
)

# Fungsi untuk konversi gambar ke Base64 (Agar bisa sejajar dengan teks di HTML)
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

# ==================================
# Bagian 1: CSS CUSTOM (MODERN DESIGN)
# ==================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&display=swap');
    
    html, body, [data-testid="stWidgetLabel"] {
        font-family: 'Inter', sans-serif !important;
    }

    /* Background Halaman Utama */
    [data-testid="stAppViewContainer"] {
        background-color: #f0f4f8 !important;
    }

    /* --- STYLE SIDEBAR GRADASI BIRU --- */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d47a1 0%, #1565c0 100%) !important;
    }
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    div[data-testid="stSelectbox"] div div {
        color: #333 !important;
    }

    /* --- STYLE TOMBOL LOGOUT ORANGE GRADASI --- */
    section[data-testid="stSidebar"] div.stButton > button {
        background: linear-gradient(90deg, #ff9966 0%, #ff5e62 100%) !important;
        color: white !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
        border: none !important;
        width: 100%;
        height: 40px;
        transition: 0.3s;
    }
    section[data-testid="stSidebar"] div.stButton > button:hover {
        opacity: 0.9;
        transform: scale(1.02);
    }

    /* --- STYLE LOGIN --- */
    [data-testid="stVerticalBlockBorderWrapper"] > div {
        background: linear-gradient(180deg, #e3f2fd 0%, #ffffff 100%) !important;
        border-radius: 24px !important;
        border: 1px solid rgba(255, 255, 255, 0.8) !important;
        padding: 35px !important;
        box-shadow: 0px 20px 40px rgba(0,0,0,0.05) !important;
    }

    .login-title { color: #0d47a1 !important; font-size: 24px !important; font-weight: 800 !important; }
    .login-subtitle { color: #546e7a !important; font-size: 13px !important; }

    /* Judul Dashboard Utama (Dikecilkan) */
    .main-title {
        font-size: 26px !important;
        font-weight: 800 !important;
        color: #0d47a1 !important;
        margin-bottom: 0px !important;
        padding-bottom: 0px !important;
    }
</style>
""", unsafe_allow_html=True)

# =========================
# Bagian 2: LOAD DATA
# =========================
@st.cache_data
def load_data():
    return pd.read_excel("KOTA_MEDAN_LENGKAP_KELURAHAN_DISABILITAS.xlsx", sheet_name="data_disabilitas")

@st.cache_data
def load_users():
    return pd.read_excel("KOTA_MEDAN_LENGKAP_KELURAHAN_DISABILITAS.xlsx", sheet_name="users")

try:
    data = load_data()
    users = load_users()
except Exception as e:
    st.error(f"Gagal memuat file Excel
