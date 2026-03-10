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
    page_title="Login SI-PANDAI SUMUT",
    layout="wide",
    page_icon="🔒"
)

# Fungsi Base64 untuk Logo Sidebar (Agar Sejajar)
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

# ==================================
# Bagian 1: CSS CUSTOM
# ==================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&display=swap');
    html, body, [data-testid="stWidgetLabel"] { font-family: 'Inter', sans-serif !important; }
    [data-testid="stAppViewContainer"] { background-color: #f4f7f9 !important; }
    header {visibility: hidden;}
    [data-testid="stVerticalBlockBorderWrapper"] > div {
        background: linear-gradient(180deg, #e3f2fd 0%, #ffffff 100%) !important;
        border-radius: 20px !important;
        border: 1px solid #cde4f7 !important;
        padding: 35px !important;
        box-shadow: 0px 10px 30px rgba(0,0,0,0.08) !important;
    }
    .login-title { color: #0d47a1 !important; font-size: 24px !important; font-weight: 800 !important; margin-bottom: 2px !important; }
    .login-subtitle { color: #546e7a !important; font-size: 13px !important; margin-bottom: 25px !important; }
    div.stButton > button {
        background: linear-gradient(90deg, #1565c0 0%, #1e88e5 100%) !important;
        color: white !important; border-radius: 10px !important; font-weight: 700 !important; height: 48px;
    }
    [data-testid="stSidebar"] { background: linear-gradient(180deg, #0d47a1 0%, #1565c0 100%) !important; }
    [data-testid="stSidebar"] * { color: white !important; }
    div[data-testid="stSelectbox"] div div { color: #333 !important; }
    section[data-testid="stSidebar"] div.stButton > button {
        background: linear-gradient(90deg, #ff9966 0%, #ff5e62 100%) !important;
        color: white !important; border-radius: 8px !important; font-weight: 700 !important; height: 40px; border: none !important;
    }
    .main-dashboard-title { font-size: 24px !important; font-weight: 800 !important; color: #0d47a1 !important; margin-bottom: 0px !important; }
    .logo-header-center { display: flex; justify-content: center; padding-top: 30px; margin-bottom: 10px; }
</style>
""", unsafe_allow_html=True)

# =========================
# Bagian 2: LOAD DATA MASTER
# =========================
@st.cache_data
def load_master_data():
    try:
        # Memuat file master yang telah disepakati (Mengambil lat/lon dari sini)
        df = pd.read_csv("master_data_si_pandai.csv")
        return df
    except Exception as e:
        st.error(f"File master_data_si_pandai.csv tidak ditemukan: {e}")
        return pd.DataFrame(columns=["kab_kota", "jumlah_penduduk", "jumlah_siswa", "ats_disabilitas", "lat", "lon"])

data = load_master_data()

# Login Hardcoded
def check_login(u, p):
    return u == "admin" and p == "admin"

if "login" not in st.session_state:
    st.session_state.login = False
    st.session_state.role = "Admin"

# =========================
# Bagian 3: HALAMAN LOGIN
# =========================
if not st.session_state.login:
    st.markdown('<div class="logo-header-center">', unsafe_allow_html=True)
    col_l1, col_l2, col_l3 = st.columns([2, 0.4, 2])
    with col_l2:
        if os.path.exists("logo_sumut.png"):
            st.image(Image.open("logo_sumut.png"), width=95)
    st.markdown('</div>', unsafe_allow_html=True)

    _, col_card, _ = st.columns([1.5, 2.5, 1.5]) 
    with col_card:
        with st.container(border=True):
            col_left, col_right = st.columns([1, 1.4])
            with col_left:
                if os.path.exists("logo_sipandai.png"):
                    st.image(Image.open("logo_sipandai.png"), use_container_width=True)
            with col_right:
                st.markdown('<div class="login-title">LOGIN USER</div>', unsafe_allow_html=True)
                st.markdown('<div class="login-subtitle">Akses Dashboard SI-PANDAI SUMUT</div>', unsafe_allow_html=True)
                u_in = st.text_input("Username", placeholder="👤  Masukkan Username", label_visibility="collapsed")
                p_in = st.text_input("Password", type="password", placeholder="🔑  Masukkan Password", label_visibility="collapsed")
                if st.button("MASUK KE DASHBOARD", use_container_width=True):
                    if check_login(u_in, p_in):
                        st.session_state.login = True
                        st.rerun()
                    else:
                        st.error("Username atau Password Salah")
    st.stop()

# ==================================
# Bagian 4: DASHBOARD UTAMA
# ==================================

# --- SIDEBAR ---
logo_b64 = get_base64_image("logo_sumut.png")
if logo_b64:
    st.sidebar.markdown(f"""
        <div style="display: flex; align-items: center; gap: 12px; padding-bottom: 20px;">
            <img src="data:image/png;base64,{logo_b64}" width="45">
            <span style="font-size: 18px; font-weight: 800; color: white; line-height: 1.1;">SI-PANDAI<br>SUMUT</span>
        </div>
    """, unsafe_allow_html=True)

st.sidebar.write(f"👤 Role: **{st.session_state.role.upper()}**")
st.sidebar.divider()

# Filter Kabupaten
st.sidebar.header("🔎 Filter")
kab_pilih = st.sidebar.selectbox("Pilih Kabupaten / Kota", ["Semua"] + sorted(data["kab_kota"].unique().tolist()))

df_filter = data.copy()
if kab_pilih != "Semua":
    df_filter = df_filter[df_filter["kab_kota"] == kab_pilih]

st.sidebar.divider()
if st.sidebar.button("Logout 🚪", use_container_width=True):
    st.session_state.login = False
    st.rerun()

# --- MAIN AREA ---
st.markdown('<p class="main-dashboard-title">🚀 Dashboard Utama</p>', unsafe_allow_html=True)
st.markdown('<p style="color: #546e7a; font-size: 14px; margin-top: -5px;">Sistem Informasi Pemetaan ATS Disabilitas Sumatera Utara</p>', unsafe_allow_html=True)
st.divider()

# MATRIKS DASHBOARD
st.subheader("📌 Matriks Capaian Sektoral")
m1, m2, m3 = st.columns(3)

if kab_pilih == "Semua":
    m1.metric("Total Penduduk Disabilitas", "6.732", help="Sumber: LPPD PK 2025")
    m2.metric("Total Siswa Disabilitas", "4.573", help="Sumber: TIKP Provsu 2025")
    m3.metric("Angka Partisipasi Sekolah", "67.93%", delta="Target Sektoral")
else:
    total_pop = int(df_filter['jumlah_penduduk'].sum())
    total_siswa = int(df_filter['jumlah_siswa'].sum())
    ats = int(df_filter['ats_disabilitas'].sum())
    m1.metric("Penduduk Disabilitas", f"{total_pop}")
    m2.metric("Siswa Belajar", f"{total_siswa}")
    m3.metric("Anak Tidak Sekolah (ATS)", f"{ats}", delta_color="inverse")

# Sumber Data
st.markdown("""
    <div style="background-color: #e3f2fd; padding: 10px; border-radius: 10px; border-left: 5px solid #1565c0;">
        <p style="font-size: 12px; color: #0d47a1; margin: 0;">
            <b>Sumber Data:</b><br>
            - Data Popul
