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
    st.error(f"Gagal memuat file Excel: {e}")
    st.stop()

# =========================
# Bagian 3: LOGIN SYSTEM
# =========================
if "login" not in st.session_state:
    st.session_state.login = False
    st.session_state.role = ""

if not st.session_state.login:
    col_l1, col_l2, col_l3 = st.columns([2, 0.5, 2])
    with col_l2:
        if os.path.exists("logo_sumut.png"):
            st.image(Image.open("logo_sumut.png"), width=100)

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
                username = st.text_input("Username", placeholder="👤 Username", label_visibility="collapsed")
                password = st.text_input("Password", type="password", placeholder="🔑 Password", label_visibility="collapsed")
                if st.button("MASUK KE DASHBOARD"):
                    user_match = users[(users["username"] == username) & (users["password"] == password)]
                    if not user_match.empty:
                        st.session_state.login = True
                        st.session_state.role = user_match.iloc[0]["role"]
                        st.rerun()
                    else:
                        st.error("Username atau Password Salah")
    st.stop()

# ==================================
# Bagian 4: DASHBOARD UTAMA
# ==================================

# --- SIDEBAR ---
# Tampilan Logo dan Judul Menyamping
logo_base64 = get_base64_image("logo_sumut.png")
if logo_base64:
    st.sidebar.markdown(f"""
        <div style="display: flex; align-items: center; gap: 12px; padding: 10px 0px;">
            <img src="data:image/png;base64,{logo_base64}" width="45">
            <span style="font-size: 18px; font-weight: 800; color: white; line-height: 1.2;">SI-PANDAI<br>SUMUT</span>
        </div>
    """, unsafe_allow_html=True)
else:
    st.sidebar.title("SI-PANDAI SUMUT")

st.sidebar.write(f"👤 Role: **{st.session_state.role}**")
st.sidebar.divider()

st.sidebar.header("🔎 Filter Wilayah")
kabkota = st.sidebar.selectbox("Pilih Kabupaten / Kota", ["Semua"] + sorted(data["kab_kota"].unique()))

df = data.copy()
if kabkota != "Semua":
    df = df[df["kab_kota"] == kabkota]

st.sidebar.divider()

if st.sidebar.button("Logout 🚪", use_container_width=True):
    st.session_state.login = False
    st.rerun()

# --- MAIN DASHBOARD ---
# Mengganti Title menjadi lebih pendek dan keren dengan Ikon Dashboard Modern
st.markdown('<p class="main-title">🚀 Dashboard</p>', unsafe_allow_html=True)
st.markdown('<p style="color: #546e7a; font-size: 14px; margin-top: -5px;">Sistem Informasi Pemetaan ATS Disabilitas Sumatera Utara</p>', unsafe_allow_html=True)
st.divider()

# Metrik Utama
col1, col2, col3 = st.columns(3)
col1.metric("Jumlah Data", len(df))
col2.metric("Jumlah Kabupaten/Kota", df["kab_kota"].nunique())
col3.metric("Kategori Disabilitas", df["jenis_disabilitas"].nunique())

st.divider()

# Grafik & Visualisasi
rekap_jenis = df.groupby("jenis_disabilitas").size().reset_index(name="Jumlah")
col_v1, col_v2 = st.columns(2)
with col_v1:
    fig_bar = px.bar(rekap_jenis, x="jenis_disabilitas", y="Jumlah", title="Jumlah ATS per Jenis", color="jenis_disabilitas", template="plotly_white")
    st.plotly_chart(fig_bar, use_container_width=True)
with col_v2:
    fig_pie = px.pie(rekap_jenis, values="Jumlah", names="jenis_disabilitas", title="Distribusi Disabilitas", hole=0.4)
    st.plotly_chart(fig_pie, use_container_width=True)

# Peta & Detail Data Tetap Sama
st.divider()
st.subheader("📋 Detail Data")
st.dataframe(df[["nama", "jenis_disabilitas", "kab_kota", "kecamatan", "desa_kelurahan"]], use_container_width=True)

if st.session_state.role in ["admin", "operator"]:
    output = BytesIO()
    df.to_excel(output, index=False, engine="openpyxl")
    output.seek(0)
    st.download_button(label="Download Excel ⬇️", data=output, file_name="rekap_disabilitas_sumut.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
