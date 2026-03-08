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
# Bagian 1: CSS CUSTOM (KARTU BIRU LEMBUT & SIDEBAR)
# ==================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&display=swap');
    
    html, body, [data-testid="stWidgetLabel"] {
        font-family: 'Inter', sans-serif !important;
    }

    /* Background Halaman Utama */
    [data-testid="stAppViewContainer"] {
        background-color: #f4f7f9 !important;
    }

    header {visibility: hidden;}

    /* KOTAK LOGIN: BIRU LEMBUT GRADASI PUTIH (KEMBALI KE ASLI) */
    [data-testid="stVerticalBlockBorderWrapper"] > div {
        background: linear-gradient(180deg, #e3f2fd 0%, #ffffff 100%) !important;
        border-radius: 20px !important;
        border: 1px solid #cde4f7 !important;
        padding: 35px !important;
        box-shadow: 0px 10px 30px rgba(0,0,0,0.08) !important;
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

    /* TOMBOL LOGIN BIRU */
    div.stButton > button {
        background: linear-gradient(90deg, #1565c0 0%, #1e88e5 100%) !important;
        color: white !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        height: 48px;
    }

    /* --- STYLE SIDEBAR GRADASI --- */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d47a1 0%, #1565c0 100%) !important;
    }
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    div[data-testid="stSelectbox"] div div {
        color: #333 !important;
    }

    /* TOMBOL LOGOUT ORANGE GRADASI */
    section[data-testid="stSidebar"] div.stButton > button {
        background: linear-gradient(90deg, #ff9966 0%, #ff5e62 100%) !important;
        color: white !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
        height: 40px;
        border: none !important;
    }

    /* Judul Dashboard (Ringkas) */
    .main-dashboard-title {
        font-size: 24px !important;
        font-weight: 800 !important;
        color: #0d47a1 !important;
        margin-bottom: 0px !important;
    }

    .logo-header-center {
        display: flex;
        justify-content: center;
        padding-top: 30px;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# =========================
# Bagian 2: LOAD DATA
# =========================
@st.cache_data
def load_data():
    try:
        return pd.read_excel("KOTA_MEDAN_LENGKAP_KELURAHAN_DISABILITAS.xlsx", sheet_name="data_disabilitas")
    except:
        return pd.DataFrame(columns=["nama", "jenis_disabilitas", "kab_kota", "kecamatan", "desa_kelurahan"])

@st.cache_data
def load_users():
    try:
        return pd.read_excel("KOTA_MEDAN_LENGKAP_KELURAHAN_DISABILITAS.xlsx", sheet_name="users")
    except:
        return pd.DataFrame([{"username": "admin", "password": "admin", "role": "admin"}])

data = load_data()
users = load_users()

if "login" not in st.session_state:
    st.session_state.login = False
    st.session_state.role = ""

# =========================
# Bagian 3: HALAMAN LOGIN
# =========================
if not st.session_state.login:
    # Logo Sumut Tengah
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
                    match = users[(users["username"] == u_in) & (users["password"] == p_in)]
                    if not match.empty:
                        st.session_state.login = True
                        st.session_state.role = match.iloc[0]["role"]
                        st.rerun()
                    else:
                        st.error("Gagal Login")
    st.stop()

# ==================================
# Bagian 4: DASHBOARD (SETELAH LOGIN)
# ==================================

# --- SIDEBAR: LOGO & JUDUL SEJAJAR ---
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

# Filter HANYA Kabupaten
st.sidebar.header("🔎 Filter")
kab_pilih = st.sidebar.selectbox("Pilih Kabupaten / Kota", ["Semua"] + sorted(data["kab_kota"].unique().tolist()))

df_filter = data.copy()
if kab_pilih != "Semua":
    df_filter = df_filter[df_filter["kab_kota"] == kab_pilih]

st.sidebar.divider()

# Tombol Logout Orange di Sidebar
if st.sidebar.button("Logout 🚪", use_container_width=True):
    st.session_state.login = False
    st.rerun()

# --- MAIN AREA ---
st.markdown('<p class="main-dashboard-title">🚀 Dashboard</p>', unsafe_allow_html=True)
st.markdown('<p style="color: #546e7a; font-size: 14px; margin-top: -5px;">Sistem Informasi Pemetaan ATS Disabilitas Sumatera Utara</p>', unsafe_allow_html=True)
st.divider()

# Rekap Cepat
m1, m2, m3 = st.columns(3)
m1.metric("Jumlah ATS Disabilitas", len(df_filter))
m2.metric("Wilayah Terdata", df_filter["kab_kota"].nunique())
m3.metric("Kategori Disabilitas", df_filter["jenis_disabilitas"].nunique())

st.divider()

# --- BAGIAN PETA (FIXED) ---
st.subheader("🗺️ Peta Sebaran Disabilitas (Kab/Kota)")

# Koordinat Kabupaten/Kota Sumatera Utara
peta_kab = {
    "Kota Medan": [3.5952, 98.6722],
    "Kab. Deli Serdang": [3.5358, 98.8166],
    "Kab. Langkat": [3.9141, 98.2443],
    "Kab. Karo": [3.1167, 98.5000],
    "Kab. Simalungun": [2.9157, 99.0717],
    "Kab. Asahan": [2.9904, 99.6339],
    "Kab. Serdang Bedagai": [3.3833, 99.1833],
    "Kota Binjai": [3.6000, 98.4833],
    "Kota Pematangsiantar": [2.9603, 99.0620],
}

map_rows = []
# Kita hitung jumlah ATS per Kabupaten dari data yang sudah difilter
stats_map = df_filter.groupby("kab_kota").size().reset_index(name="Jumlah")

for index, row in stats_map.items():
    kab_name = row if isinstance(row, str) else "" # Guard
    # Ambil koordinat jika ada di dictionary
    for kab, coord in peta_kab.items():
        # Cek apakah nama kabupaten di data ada di kamus koordinat kita
        if kab in stats_map["kab_kota"].values:
            jml = stats_map[stats_map["kab_kota"] == kab]["Jumlah"].values[0]
            map_rows.append({
                "lat": coord[0],
                "lon": coord[1],
                "kab": kab,
                "size": int(jml) * 50 # Multiplier agar bulatan terlihat
            })
            break

if map_rows:
    map_df = pd.DataFrame(map_rows).drop_duplicates()
    # Menampilkan Peta
    st.map(map_df, latitude="lat", longitude="lon", size="size")
else:
    st.info("Koordinat lokasi untuk wilayah ini belum terdaftar di sistem peta.")

st.divider()

# Grafik
c_bar, c_pie = st.columns(2)
rekap_stat = df_filter.groupby("jenis_disabilitas").size().reset_index(name="Total")

with c_bar:
    fig_bar = px.bar(rekap_stat, x="jenis_disabilitas", y="Total", title="Statistik per Jenis", color="jenis_disabilitas", template="plotly_white")
    st.plotly_chart(fig_bar, use_container_width=True)

with c_pie:
    fig_pie = px.pie(rekap_stat, values="Total", names="jenis_disabilitas", title="Proporsi Disabilitas", hole=0.4)
    st.plotly_chart(fig_pie, use_container_width=True)

st.divider()
st.subheader("📋 Detail Data")
st.dataframe(df_filter[["nama", "jenis_disabilitas", "kab_kota", "kecamatan", "desa_kelurahan"]], use_container_width=True)

if st.session_state.role in ["admin", "operator"]:
    out = BytesIO()
    df_filter.to_excel(out, index=False, engine="openpyxl")
    out.seek(0)
    st.download_button("Download Excel ⬇️", data=out, file_name="data_si_pandai.xlsx")
