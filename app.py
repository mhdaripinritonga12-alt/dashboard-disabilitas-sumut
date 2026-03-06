import streamlit as st
import pandas as pd
from PIL import Image
import os
from io import BytesIO
import plotly.express as px

# ==================================
# Bagian 0: KONFIGURASI HALAMAN
# ==================================
st.set_page_config(
    page_title="SI-PANDAI SUMUT",
    layout="wide",
    page_icon="🔒"
)

# ==================================
# Bagian 1: CSS CUSTOM (LOGIN & SIDEBAR GRADASI)
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

    /* --- STYLE SIDEBAR GRADASI --- */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d47a1 0%, #1565c0 100%) !important;
    }
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    /* Mengubah warna selectbox di sidebar agar terbaca */
    div[data-testid="stSelectbox"] div div {
        color: #333 !important;
    }

    /* KOTAK LOGIN: BIRU LEMBUT GRADASI PUTIH */
    [data-testid="stVerticalBlockBorderWrapper"] > div {
        background: linear-gradient(180deg, #e3f2fd 0%, #ffffff 100%) !important;
        border-radius: 24px !important;
        border: 1px solid rgba(255, 255, 255, 0.8) !important;
        padding: 35px !important;
        box-shadow: 0px 20px 40px rgba(0,0,0,0.05) !important;
    }

    .login-title {
        color: #0d47a1 !important;
        font-size: 24px !important;
        font-weight: 800 !important;
        margin-bottom: 2px !important;
    }
    
    .login-subtitle {
        color: #546e7a !important;
        font-size: 13px !important;
        margin-bottom: 25px !important;
    }

    div.stButton > button {
        background: linear-gradient(90deg, #1565c0 0%, #1e88e5 100%) !important;
        color: white !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        height: 48px;
        border: none !important;
        width: 100%;
        margin-top: 20px;
    }

    .logo-header {
        display: flex;
        justify-content: center;
        padding: 40px 0 20px 0;
    }
</style>
""", unsafe_allow_html=True)

# =========================
# Bagian 2: LOAD DATA
# =========================
@st.cache_data
def load_data():
    return pd.read_excel(
        "KOTA_MEDAN_LENGKAP_KELURAHAN_DISABILITAS.xlsx",
        sheet_name="data_disabilitas"
    )

@st.cache_data
def load_users():
    return pd.read_excel(
        "KOTA_MEDAN_LENGKAP_KELURAHAN_DISABILITAS.xlsx",
        sheet_name="users"
    )

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
    st.markdown('<div class="logo-header">', unsafe_allow_html=True)
    col_l1, col_l2, col_l3 = st.columns([2, 0.5, 2])
    with col_l2:
        if os.path.exists("logo_sumut.png"):
            st.image(Image.open("logo_sumut.png"), width=100)
    st.markdown('</div>', unsafe_allow_html=True)

    _, col_card, _ = st.columns([1.5, 2.5, 1.5]) 

    with col_card:
        with st.container(border=True):
            col_left, col_right = st.columns([1, 1.4])
            with col_left:
                st.write("") 
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

    st.markdown('<p style="text-align:center; color:#adb5bd; font-size:11px; margin-top:30px;">Dinas Pendidikan Provinsi Sumatera Utara © 2026</p>', unsafe_allow_html=True)
    st.stop()

# ==================================
# Bagian 4: DASHBOARD UTAMA (SETELAH LOGIN)
# ==================================

# --- SIDEBAR (FILTER & LOGOUT) ---
st.sidebar.markdown("### SI-PANDAI SUMUT")
st.sidebar.write(f"👤 Role: **{st.session_state.role}**")
st.sidebar.divider()

st.sidebar.header("🔎 Filter Wilayah")
kabkota = st.sidebar.selectbox(
    "Pilih Kabupaten / Kota",
    ["Semua"] + sorted(data["kab_kota"].unique())
)

df = data.copy()
if kabkota != "Semua":
    df = df[df["kab_kota"] == kabkota]

st.sidebar.divider()

# Tombol Logout dipindahkan ke Sidebar
if st.sidebar.button("Logout 🚪", use_container_width=True):
    st.session_state.login = False
    st.session_state.role = ""
    st.rerun()

# --- MAIN DASHBOARD ---
st.title("📊 Dashboard Sebaran Penyandang Disabilitas")
st.subheader("Provinsi Sumatera Utara")
st.divider()

# Metrik Utama
col1, col2, col3 = st.columns(3)
col1.metric("Jumlah Data", len(df))
col2.metric("Jumlah Kabupaten/Kota", df["kab_kota"].nunique())
col3.metric("Kategori Disabilitas", df["jenis_disabilitas"].nunique())

st.divider()

# Grafik
st.subheader("📌 Rekap & Visualisasi")
rekap_jenis = df.groupby("jenis_disabilitas").size().reset_index(name="Jumlah")

col_v1, col_v2 = st.columns(2)
with col_v1:
    fig_bar = px.bar(
        rekap_jenis,
        x="jenis_disabilitas",
        y="Jumlah",
        title="Jumlah ATS per Jenis Disabilitas",
        color="jenis_disabilitas",
        template="plotly_white"
    )
    st.plotly_chart(fig_bar, use_container_width=True)

with col_v2:
    fig_pie = px.pie(
        rekap_jenis,
        values="Jumlah",
        names="jenis_disabilitas",
        title="Distribusi Persentase Disabilitas",
        hole=0.4
    )
    st.plotly_chart(fig_pie, use_container_width=True)

# Peta Sebaran
st.divider()
st.subheader("🗺️ Peta Sebaran (Kab/Kota)")
peta_kab = {
    "Kota Medan": [3.5952, 98.6722],
    "Kab. Deli Serdang": [3.4200, 98.9800],
    "Kab. Langkat": [3.7000, 98.2000],
}
map_rows = []
map_data_full = data.groupby("kab_kota").size().reset_index(name="Jumlah")
for k, v in peta_kab.items():
    jumlah = map_data_full.loc[map_data_full["kab_kota"] == k, "Jumlah"]
    if not jumlah.empty:
        map_rows.append({"lat": v[0], "lon": v[1], "jumlah": int(jumlah.values[0]) * 100})

if map_rows:
    st.map(pd.DataFrame(map_rows), size="jumlah")
else:
    st.info("Data peta lokasi belum tersedia.")

# Detail Data & Download
st.divider()
st.subheader("📋 Detail Data")
st.dataframe(df[["nama", "jenis_disabilitas", "kab_kota", "kecamatan", "desa_kelurahan"]], use_container_width=True)

if st.session_state.role in ["admin", "operator"]:
    output = BytesIO()
    df.to_excel(output, index=False, engine="openpyxl")
    output.seek(0)
    st.download_button(
        label="Download Excel ⬇️",
        data=output,
        file_name="rekap_disabilitas_sumut.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

st.divider()
st.caption("Dinas Pendidikan Provinsi Sumatera Utara © 2026")
