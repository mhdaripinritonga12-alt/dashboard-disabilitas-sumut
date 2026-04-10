import streamlit as st
import pandas as pd
import plotly.express as px
import os
import base64
import streamlit.components.v1 as components

# ==================================
# Bagian 0: KONFIGURASI HALAMAN
# ==================================
st.set_page_config(
    page_title="SI-PANDAI SUMUT",
    layout="wide",
    page_icon="🔒",
    initial_sidebar_state="expanded"
)

# Inisialisasi State
if "login" not in st.session_state: st.session_state.login = False
if "page_view" not in st.session_state: st.session_state.page_view = "dashboard"
if "selected_kab" not in st.session_state: st.session_state.selected_kab = "Semua"
if "selected_school_data" not in st.session_state: st.session_state.selected_school_data = None

def proses_logout():
    st.session_state.login = False
    st.session_state.page_view = "dashboard"
    st.rerun()

def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

# ==================================
# Bagian 1: CSS CUSTOM (MODERN SIDEBAR UI)
# ==================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
    
    /* Global Font */
    html, body, [data-testid="stWidgetLabel"], * { font-family: 'Inter', sans-serif !important; }

    /* --- SIDEBAR BACKGROUND GRADIENT --- */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e88e5 0%, #0d47a1 100%) !important;
        background-attachment: fixed !important;
    }
    
    /* Menghilangkan border default sidebar */
    [data-testid="stSidebar"] > div:first-child {
        background: transparent !important;
    }

    /* Warna Teks Putih di Sidebar */
    [data-testid="stSidebar"] .stMarkdown, [data-testid="stSidebar"] label, [data-testid="stSidebar"] p {
        color: white !important;
    }

    /* --- MENU UTAMA (RADIO BUTTON STYLE) --- */
    /* Kotak menu agar transparan seperti di gambar */
    div[data-testid="stSidebar"] div.stRadio > div {
        gap: 8px !important;
    }
    
    div[data-testid="stSidebar"] div.stRadio label {
        background: rgba(255, 255, 255, 0.15) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 12px !important;
        padding: 12px 15px !important;
        color: white !important;
        transition: 0.3s !important;
        cursor: pointer !important;
    }

    /* Saat menu dipilih */
    div[data-testid="stSidebar"] div.stRadio label[data-selected="true"] {
        background: rgba(255, 255, 255, 0.3) !important;
        border: 1px solid white !important;
        font-weight: 700 !important;
    }

    /* Sembunyikan lingkaran radio default */
    div[data-testid="stSidebar"] div.stRadio div[data-testid="stMarkdownContainer"] p {
        font-size: 14px !important;
    }

    /* --- FILTER WILAYAH CARD (BOX BIRU MUDA) --- */
    .filter-container {
        background: rgba(187, 222, 251, 0.9) !important; /* Warna biru muda transparan */
        padding: 20px !important;
        border-radius: 15px !important;
        margin-top: 20px !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1) !important;
    }
    
    /* Warna teks di dalam box filter */
    .filter-container label, .filter-container p {
        color: #0d47a1 !important;
        font-weight: 700 !important;
    }

    /* Dropdown/Selectbox di dalam sidebar agar bersih */
    div[data-testid="stSidebar"] div[data-baseweb="select"] > div {
        background-color: white !important;
        border-radius: 10px !important;
        color: #333 !important;
    }

    /* --- BUTTONS --- */
    /* Tombol Reset Filter (Biru) */
    div[data-testid="stSidebar"] .stButton button {
        border-radius: 10px !important;
    }

    /* Tombol Logout (ORANGE) */
    div[data-testid="stSidebar"] .stButton button[key="logout_btn"] {
        background: linear-gradient(90deg, #ff8a65 0%, #f4511e 100%) !important;
        color: white !important;
        font-weight: 700 !important;
        height: 50px !important;
        border: none !important;
        margin-top: 15px !important;
        box-shadow: 0 4px 10px rgba(244, 81, 30, 0.3) !important;
    }

    /* Dashboard Metrics UI */
    .metric-tile { padding: 20px; border-radius: 15px; color: white; margin-bottom: 15px; display: flex; align-items: center; gap: 15px; }
    .tile-orange { background: #ff9800; }
    .tile-blue-light { background: #03a9f4; }
    .tile-navy { background: #3f51b5; }
    .tile-green { background: #4caf50; }
    .tile-label { font-size: 12px; font-weight: 600; text-transform: uppercase; opacity: 0.9; }
    .tile-value { font-size: 24px; font-weight: 800; }

</style>
""", unsafe_allow_html=True)

# ==================================
# Bagian 2: LOAD DATA
# ==================================
@st.cache_data
def load_all_data():
    try:
        df_ats = pd.read_csv("master_data_si_pandai.csv")
        df_sch = pd.read_csv("master_data_sekolah1.csv")
        for df in [df_ats, df_sch]:
            df.columns = df.columns.str.strip().str.lower()
        return df_ats, df_sch
    except: return pd.DataFrame(), pd.DataFrame()

data_wilayah, data_sekolah = load_all_data()

# =========================
# Bagian 3: LOGIN
# =========================
if not st.session_state.login:
    _, col_card, _ = st.columns([1, 2, 1])
    with col_card:
        if os.path.exists("logo_sipandai.png"): st.image("logo_sipandai.png", width=300)
        st.markdown("<h3 style='text-align: center; color:#0d47a1;'>LOGIN USER</h3>", unsafe_allow_html=True)
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")
        if st.button("MASUK KE DASHBOARD", use_container_width=True):
            if u == "admin" and p == "admin": 
                st.session_state.login = True
                st.rerun()
            else: st.error("Login Gagal")
    st.stop()

# ==================================
# Bagian 4: SIDEBAR CUSTOM (FIXED UI)
# ==================================
with st.sidebar:
    # Header Area
    col_l, col_r = st.columns([0.3, 0.7])
    with col_l:
        if os.path.exists("logo_sumut.png"): st.image("logo_sumut.png", width=60)
    with col_r:
        st.markdown("### SI-PANDAI SUMUT")
        st.caption("Role: **ADMIN**")
    
    st.markdown("---")

    # Menu Utama
    st.markdown("#### 🏠 Menu Utama")
    
    def handle_nav():
        pilih = st.session_state.nav_radio
        if "Dashboard Utama" in pilih: st.session_state.page_view = "dashboard"
        elif "Pendidikan Khusus" in pilih: st.session_state.page_view = "tentang_pk"
        else: st.session_state.page_view = "tentang_dashboard"

    st.radio(
        "Navigasi:",
        ["🏠 Dashboard Utama", "🎓 Pendidikan Khusus", "ℹ️ Tentang Dashboard"],
        key="nav_radio",
        label_visibility="collapsed",
        on_change=handle_nav
    )

    # Filter Wilayah Area (Dengan Container Biru Muda)
    st.markdown('<div class="filter-container">', unsafe_allow_html=True)
    st.markdown("#### 🔍 Filter Wilayah")
    col_kab = "kab_kota" if "kab_kota" in data_wilayah.columns else data_wilayah.columns[0]
    opsi = ["Semua"] + sorted(data_wilayah[col_kab].unique().tolist()) if not data_wilayah.empty else ["Semua"]
    kab_pilih = st.selectbox("Pilih Kabupaten / Kota", opsi, key="selected_kab")
    
    if st.button("🔄 Reset Filter", use_container_width=True):
        st.session_state.selected_kab = "Semua"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # Logout Button (Orange)
    st.button("🚪 Logout", key="logout_btn", on_click=proses_logout, use_container_width=True)

# ==================================
# Bagian 5: LOGIKA HALAMAN
# ==================================

if st.session_state.page_view == "dashboard":
    st.markdown(f'<h2 style="color:#0d47a1;">🚀 Dashboard Utama: {kab_pilih}</h2>', unsafe_allow_html=True)
    st.divider()

    df_f = data_wilayah.copy()
    if kab_pilih != "Semua": df_f = df_f[df_f[col_kab] == kab_pilih]

    # Matriks Capaian
    m1, m2, m3, m4 = st.columns(4)
    val_p = f"{int(df_f.iloc[:,1].sum()):,}" if not df_f.empty else "0"
    val_s = f"{int(df_f.iloc[:,2].sum()):,}" if not df_f.empty else "0"
    val_a = f"{int(df_f.iloc[:,3].sum()):,}" if not df_f.empty else "0"
    val_APS = f"{(int(df_f.iloc[:,2].sum()) / int(df_f.iloc[:,1].sum()) * 100):.2f}%" if not df_f.empty and int(df_f.iloc[:,1].sum()) > 0 else "0%"

    with m1: st.markdown(f'<div class="metric-tile tile-orange"><div><div class="tile-label">Penduduk Disabilitas</div><div class="tile-value">{val_p}</div></div></div>', unsafe_allow_html=True)
    with m2: st.markdown(f'<div class="metric-tile tile-blue-light"><div><div class="tile-label">Siswa Belajar</div><div class="tile-value">{val_s}</div></div></div>', unsafe_allow_html=True)
    with m3: st.markdown(f'<div class="metric-tile tile-navy"><div><div class="tile-label">Anak Tidak Sekolah</div><div class="tile-value">{val_a}</div></div></div>', unsafe_allow_html=True)
    with m4: st.markdown(f'<div class="metric-tile tile-green"><div><div class="tile-label">Angka Partisipasi</div><div class="tile-value">{val_APS}</div></div></div>', unsafe_allow_html=True)

    # Tambahkan visualisasi atau tabel sesuai kebutuhan Anda di sini...
    st.subheader("📊 Detail Data Wilayah")
    st.dataframe(df_f, use_container_width=True)

elif st.session_state.page_view == "tentang_pk":
    st.title("🎓 Pendidikan Khusus Sumatera Utara")
    st.info("Halaman informasi Pendidikan Khusus.")

elif st.session_state.page_view == "tentang_dashboard":
    st.title("ℹ️ Tentang Dashboard SI-PANDAI")
    st.write("Sistem Informasi Analitik Pendidikan Khusus Sumatera Utara.")
