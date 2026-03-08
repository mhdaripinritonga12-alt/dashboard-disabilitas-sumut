import streamlit as st
import pandas as pd
from PIL import Image
import os
from io import BytesIO
import plotly.express as px
import base64

# ==================================
# Bagian 0: KONFIGURASI HALAMAN (Wajib Paling Atas)
# ==================================
st.set_page_config(
    page_title="SI-PANDAI SUMUT",
    layout="wide",
    page_icon="🔒"
)

# Fungsi Base64 untuk Logo Sidebar
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

# ==================================
# Bagian 1: CSS CUSTOM (WHITE CARD & BACKGROUND)
# ==================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&display=swap');
    html, body, [data-testid="stWidgetLabel"] { font-family: 'Inter', sans-serif !important; }

    /* BACKGROUND PEMANDANGAN SUMUT */
    [data-testid="stAppViewContainer"] {
        background-image: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)), 
                          url("https://images.unsplash.com/photo-1571746243149-6012b84299ec?q=80&w=2000&auto=format&fit=crop");
        background-size: cover; background-position: center; background-attachment: fixed;
    }

    header {visibility: hidden;}

    /* KOTAK LOGIN PUTIH SOLID */
    [data-testid="stVerticalBlockBorderWrapper"] > div {
        background-color: white !important;
        border-radius: 20px !important;
        padding: 40px !important;
        box-shadow: 0px 15px 40px rgba(0,0,0,0.4) !important;
    }

    .login-title { color: #0d47a1 !important; font-size: 26px !important; font-weight: 800 !important; }
    .login-subtitle { color: #1D976C !important; font-size: 13px !important; font-weight: 700; }

    /* TOMBOL LOGIN */
    div.stButton > button {
        background: linear-gradient(90deg, #1565c0 0%, #1e88e5 100%) !important;
        color: white !important; border-radius: 10px !important; font-weight: 700 !important; height: 48px;
    }

    /* SIDEBAR */
    [data-testid="stSidebar"] { background: linear-gradient(180deg, #0d47a1 0%, #1565c0 100%) !important; }
    [data-testid="stSidebar"] * { color: white !important; }
    div[data-testid="stSelectbox"] div div { color: #333 !important; }

    /* LOGOUT ORANGE */
    section[data-testid="stSidebar"] div.stButton > button {
        background: linear-gradient(90deg, #ff9966 0%, #ff5e62 100%) !important;
        color: white !important; font-weight: 700 !important; height: 40px;
    }
</style>
""", unsafe_allow_html=True)

# =========================
# Bagian 2: LOAD DATA (DENGAN PROTEKSI ERROR)
# =========================
EXCEL_PATH = "KOTA_MEDAN_LENGKAP_KELURAHAN_DISABILITAS.xlsx"

@st.cache_data
def load_data():
    if not os.path.exists(EXCEL_PATH):
        return pd.DataFrame(columns=["nama", "jenis_disabilitas", "kab_kota", "kecamatan", "desa_kelurahan"])
    return pd.read_excel(EXCEL_PATH, sheet_name="data_disabilitas")

@st.cache_data
def load_users():
    if not os.path.exists(EXCEL_PATH):
        return pd.DataFrame([{"username": "admin", "password": "admin", "role": "admin"}])
    return pd.read_excel(EXCEL_PATH, sheet_name="users")

# Cek keberadaan file Excel
if not os.path.exists(EXCEL_PATH):
    st.warning(f"⚠️ File '{EXCEL_PATH}' tidak ditemukan di folder!")

data = load_data()
users = load_users()

if "login" not in st.session_state:
    st.session_state.login = False
    st.session_state.role = ""

# =========================
# Bagian 3: HALAMAN LOGIN
# =========================
if not st.session_state.login:
    st.markdown('<div style="display: flex; justify-content: center; padding-top: 20px; margin-bottom: 15px;">', unsafe_allow_html=True)
    col_l1, col_l2, col_l3 = st.columns([2, 0.4, 2])
    with col_l2:
        if os.path.exists("logo_sumut.png"):
            st.image(Image.open("logo_sumut.png"), width=100)
    st.markdown('</div>', unsafe_allow_html=True)

    _, col_card, _ = st.columns([1.4, 2.6, 1.4]) 
    with col_card:
        with st.container(border=True):
            col_left, col_right = st.columns([1, 1.4])
            with col_left:
                if os.path.exists("logo_sipandai.png"):
                    st.image(Image.open("logo_sipandai.png"), use_container_width=True)
            with col_right:
                st.markdown('<div class="login-title">LOGIN USER</div>', unsafe_allow_html=True)
                st.markdown('<div class="login-subtitle">SI-PANDAI SUMUT</div>', unsafe_allow_html=True)
                u_in = st.text_input("Username", placeholder="👤  Username", label_visibility="collapsed")
                p_in = st.text_input("Password", type="password", placeholder="🔑  Password", label_visibility="collapsed")
                if st.button("MASUK KE DASHBOARD", use_container_width=True):
                    match = users[(users["username"] == u_in) & (users["password"] == p_in)]
                    if not match.empty:
                        st.session_state.login = True
                        st.session_state.role = match.iloc[0]["role"]
                        st.rerun()
                    else:
                        st.error("Login Gagal! Periksa Username/Password.")
    st.stop()

# ==================================
# Bagian 4: DASHBOARD
# ==================================
# Sidebar Logo
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

# Filter & Logout
st.sidebar.header("🔎 Filter")
kab_pilih = st.sidebar.selectbox("Kabupaten / Kota", ["Semua"] + sorted(data["kab_kota"].unique().tolist()))
df_filter = data.copy()
if kab_pilih != "Semua":
    df_filter = df_filter[df_filter["kab_kota"] == kab_pilih]

st.sidebar.divider()
if st.sidebar.button("Logout 🚪", use_container_width=True):
    st.session_state.login = False
    st.rerun()

# Main Dashboard
st.markdown('<p style="font-size: 24px; font-weight: 800; color: #0d47a1;">🚀 Dashboard</p>', unsafe_allow_html=True)
st.divider()

# Peta
st.subheader("🗺️ Peta Sebaran")
peta_kab = {
    "Kota Medan": [3.5952, 98.6722],
    "Kab. Deli Serdang": [3.5358, 98.8166],
    "Kab. Langkat": [3.9141, 98.2443],
}
map_rows = []
stats_map = df_filter.groupby("kab_kota").size().reset_index(name="Jumlah")
for index, row in stats_map.iterrows():
    kab = row["kab_kota"]
    if kab in peta_kab:
        map_rows.append({"lat": peta_kab[kab][0], "lon": peta_kab[kab][1], "size": int(row["Jumlah"]) * 80})

if map_rows:
    st.map(pd.DataFrame(map_rows), latitude="lat", longitude="lon", size="size")

# Metrics
m1, m2, m3 = st.columns(3)
m1.metric("Total Data", len(df_filter))
m2.metric("Kab/Kota", df_filter["kab_kota"].nunique())
m3.metric("Kategori", df_filter["jenis_disabilitas"].nunique())

# Table
st.divider()
st.subheader("📋 Detail Data")
st.dataframe(df_filter[["nama", "jenis_disabilitas", "kab_kota", "kecamatan"]], use_container_width=True)
