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
# Bagian 1: CSS CUSTOM (MODERN DESIGN)
# ==================================
st.markdown("""
<style>
    /* Menggunakan Font yang lebih modern */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&display=swap');
    
    html, body, [data-testid="stWidgetLabel"] {
        font-family: 'Inter', sans-serif !important;
    }

    /* Background Halaman */
    [data-testid="stAppViewContainer"] {
        background-color: #f0f4f8 !important;
    }

    /* KOTAK LOGIN: BIRU LEMBUT GRADASI PUTIH */
    [data-testid="stVerticalBlockBorderWrapper"] > div {
        background: linear-gradient(180deg, #e3f2fd 0%, #ffffff 100%) !important;
        border-radius: 24px !important;
        border: 1px solid rgba(255, 255, 255, 0.8) !important;
        padding: 35px !important;
        box-shadow: 0px 20px 40px rgba(0,0,0,0.05) !important;
    }

    /* Teks Judul LOGIN USER */
    .login-title {
        color: #0d47a1 !important;
        font-size: 24px !important;
        font-weight: 800 !important;
        margin-bottom: 2px !important;
        letter-spacing: -0.5px;
    }
    
    .login-subtitle {
        color: #546e7a !important;
        font-size: 13px !important;
        margin-bottom: 25px !important;
    }

    /* STYLE INPUT FIELD */
    div[data-testid="stTextInput"] input {
        border-radius: 12px !important;
        border: 1.5px solid #d1d9e0 !important;
        padding: 12px !important;
        background-color: white !important;
        transition: 0.3s;
    }

    /* TOMBOL LOGIN (Vibrant Blue) */
    div.stButton > button {
        background: linear-gradient(90deg, #1565c0 0%, #1e88e5 100%) !important;
        color: white !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        height: 48px;
        border: none !important;
        width: 100%;
        margin-top: 20px;
        box-shadow: 0px 4px 15px rgba(21, 101, 192, 0.3);
    }
    
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0px 6px 20px rgba(21, 101, 192, 0.4);
    }

    /* Logo Sumut di atas */
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

# Memuat data
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

# --- TAMPILAN LOGIN ---
if not st.session_state.login:
    # 1. LOGO SUMUT
    st.markdown('<div class="logo-header">', unsafe_allow_html=True)
    col_l1, col_l2, col_l3 = st.columns([2, 0.5, 2])
    with col_l2:
        if os.path.exists("logo_sumut.png"):
            st.image(Image.open("logo_sumut.png"), width=100)
    st.markdown('</div>', unsafe_allow_html=True)

    # 2. KARTU LOGIN
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
                    # Validasi Login ke Excel
                    user_match = users[
                        (users["username"] == username) & 
                        (users["password"] == password)
                    ]
                    
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

# HEADER DASHBOARD
st.title("📊 Dashboard Sebaran Penyandang Disabilitas")
st.subheader("Provinsi Sumatera Utara")

col_header_1, col_header_2 = st.columns([5,1])
with col_header_1:
    st.write(f"👤 Role: **{st.session_state.role}**")
with col_header_2:
    if st.button("Logout", use_container_width=True):
        st.session_state.login = False
        st.session_state.role = ""
        st.rerun()

st.divider()

# =========================
# FILTER WILAYAH (SIDEBAR)
# =========================
st.sidebar.header("🔎 Filter Wilayah")

kabkota = st.sidebar.selectbox(
    "Pilih Kabupaten / Kota",
    ["Semua"] + sorted(data["kab_kota"].unique())
)

df = data.copy()
if kabkota != "Semua":
    df = df[df["kab_kota"] == kabkota]

kecamatan = st.sidebar.selectbox(
    "Pilih Kecamatan",
    ["Semua"] + sorted(df["kecamatan"].unique())
)

if kecamatan != "Semua":
    df = df[df["kecamatan"] == kecamatan]

desa = st.sidebar.selectbox(
    "Pilih Desa / Kelurahan",
    ["Semua"] + sorted(df["desa_kelurahan"].unique())
)

if desa != "Semua":
    df = df[df["desa_kelurahan"] == desa]

# =========================
# REKAP CEPAT
# =========================
col1, col2, col3 = st.columns(3)
col1.metric("Jumlah Data", len(df))
col2.metric("Jumlah Kecamatan", df["kecamatan"].nunique())
col3.metric("Jumlah Kelurahan", df["desa_kelurahan"].nunique())

st.divider()

# =========================
# A. REKAP & GRAFIK
# =========================
st.subheader("📌 Rekap Penyandang per Jenis Disabilitas")

rekap = df.groupby("jenis_disabilitas").size().reset_index(name="Jumlah")
st.dataframe(rekap, use_container_width=True)

st.divider()
st.subheader("📈 Grafik Penyandang Disabilitas")

rekap_jenis = df.groupby("jenis_disabilitas").size().reset_index(name="Jumlah")

fig_bar = px.bar(
    rekap_jenis,
    x="jenis_disabilitas",
    y="Jumlah",
    title="Jumlah Penyandang Disabilitas per Jenis",
    color="jenis_disabilitas",
    labels={"jenis_disabilitas": "Jenis Disabilitas", "Jumlah": "Jumlah"}
)
st.plotly_chart(fig_bar, use_container_width=True)

fig_pie = px.pie(
    rekap_jenis,
    values="Jumlah",
    names="jenis_disabilitas",
    title="Distribusi Jenis Disabilitas"
)
st.plotly_chart(fig_pie, use_container_width=True)

# =========================
# B. PETA SEBARAN
# =========================
st.divider()
st.subheader("🗺️ Peta Sebaran Penyandang Disabilitas (Kab/Kota)")

map_data_full = data.groupby("kab_kota").size().reset_index(name="Jumlah")

peta_kab = {
    "Kota Medan": [3.5952, 98.6722],
    "Kab. Deli Serdang": [3.4200, 98.9800],
    "Kab. Langkat": [3.7000, 98.2000],
}

map_rows = []
for k, v in peta_kab.items():
    jumlah = map_data_full.loc[map_data_full["kab_kota"] == k, "Jumlah"]
    if not jumlah.empty:
        map_rows.append({
            "lat": v[0],
            "lon": v[1],
            "jumlah": int(jumlah.values[0]) * 100 # perkecil multiplier jika terlalu besar
        })

if map_rows:
    map_df = pd.DataFrame(map_rows)
    st.map(map_df, size="jumlah")
else:
    st.info("Data peta belum tersedia untuk wilayah yang dipilih")

# =========================
# C. DETAIL DATA
# =========================
st.divider()
st.subheader("📋 Detail Nama Berdasarkan Jenis")

jenis_pilih = st.selectbox(
    "Pilih Jenis Disabilitas untuk Detail",
    ["Semua"] + sorted(df["jenis_disabilitas"].unique())
)

if jenis_pilih != "Semua":
    df_detail = df[df["jenis_disabilitas"] == jenis_pilih]
else:
    df_detail = df

st.dataframe(
    df_detail[["nama", "jenis_disabilitas", "desa_kelurahan", "kecamatan"]],
    use_container_width=True
)

# =========================
# D. DOWNLOAD EXCEL (Berdasarkan Role)
# =========================
st.divider()
st.subheader("⬇️ Download Data")

if st.session_state.role in ["admin", "operator"]:
    output = BytesIO()
    df.to_excel(output, index=False, engine="openpyxl")
    output.seek(0)

    st.download_button(
        label="Download Excel",
        data=output,
        file_name="rekap_disabilitas_filtered.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
else:
    st.info("Role viewer tidak memiliki hak akses untuk mengunduh data.")

# =========================
# E. ROLE INFO
# =========================
st.divider()
st.caption("""
Role:
- Admin    : Semua akses
- Operator : Lihat & Download
- Viewer   : Lihat saja
""")
