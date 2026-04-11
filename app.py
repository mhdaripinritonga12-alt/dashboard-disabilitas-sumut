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

def proses_logout():
    st.session_state.selected_kab = "Semua"
    st.session_state.login = False
    st.session_state.page_view = "dashboard"
    st.rerun()

def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

# ==================================
# Bagian 1: CSS CUSTOM (ROYAL PREMIUM DESIGN)
# ==================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
    html, body, [data-testid="stWidgetLabel"] { font-family: 'Inter', sans-serif !important; }

    /* --- 1. SETTING AREA KONTEN (MENTOK PINGGIR) --- */
    .block-container {
        padding-top: 0rem !important;
        padding-left: 0rem !important;
        padding-right: 0rem !important;
        max-width: 100% !important;
    }
    [data-testid="stHeader"] { display: none !important; }

    /* --- 2. BAR PELANGI TIPIS --- */
    .top-gradient-bar {
        position: fixed;
        top: 0; left: 0; width: 100%; height: 6px;
        background: linear-gradient(90deg, #ff8a00, #e52e71, #9c27b0, #1e88e5, #4caf50, #ffeb3b);
        z-index: 999999;
    }

    /* --- 3. HEADER "ISTIMEWA" (ROYAL BLUE SLIM CARD) --- */
    .header-special-card {
        background: linear-gradient(90deg, #0d47a1 0%, #1a237e 50%, #0d47a1 100%) !important;
        padding: 10px 0px;
        text-align: center;
        margin-top: 6px; /* Di bawah bar pelangi */
        width: 100% !important;
        border-bottom: 3px solid #00d2ff; /* Aksen Biru Muda Menyala */
        box-shadow: 0 10px 20px rgba(0,0,0,0.2);
    }

    .header-special-card h1 {
        color: white !important;
        font-weight: 800 !important;
        font-size: 1.8rem !important;
        margin: 0 !important;
        letter-spacing: 2px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }

    .header-special-card p {
        color: rgba(255, 255, 255, 0.8) !important;
        font-size: 12px !important;
        font-weight: 600 !important;
        margin: 5px 0 0 0 !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* --- 4. SIDEBAR BIRU TUA SOLID --- */
    [data-testid="stSidebar"] {
        background-color: #0d47a1 !important;
    }
    [data-testid="stSidebar"] * { color: white !important; }

    /* TOMBOL SIDEBAR POLOS */
    section[data-testid="stSidebar"] .stButton button {
        background-color: transparent !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 8px !important;
        width: 100% !important;
        text-align: left !important;
        transition: 0.3s;
    }
    section[data-testid="stSidebar"] .stButton button:hover {
        background-color: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid white !important;
    }

    /* --- 5. DASHBOARD TILES --- */
    .metric-tile { padding: 20px; border-radius: 12px; color: white; margin-bottom: 15px; display: flex; align-items: center; gap: 15px; }
    .tile-orange { background: linear-gradient(135deg, #ff9800, #f57c00); }
    .tile-blue { background: linear-gradient(135deg, #03a9f4, #0288d1); }
    .tile-navy { background: linear-gradient(135deg, #3f51b5, #1a237e); }
    .tile-green { background: linear-gradient(135deg, #4caf50, #2e7d32); }

    /* Memberi jarak isi dashboard dari header agar tidak terlalu mepet */
    .main-content-wrapper {
        padding: 20px 40px;
    }
</style>
""", unsafe_allow_html=True)

def draw_tile_svg(label, value, svg_icon, style_class):
    st.markdown(f'<div class="metric-tile {style_class}"><div style="width:40px;height:40px;">{svg_icon}</div><div><div style="font-size:12px;font-weight:800;opacity:0.9;">{label}</div><div style="font-size:22px;font-weight:800;">{value}</div></div></div>', unsafe_allow_html=True)

# SVG Icons
svg_people = '<svg viewBox="0 0 16 16" fill="white"><path d="M7 14s-1 0-1-1 1-4 5-4 5 3 5 4-1 1-1 1H7zm4-6a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm-5.784 6A2.238 2.238 0 0 1 5 13c0-1.355.68-2.75 1.936-3.72A6.325 6.325 0 0 0 5 9c-4 0-5 3-5 4s1 1 1 1h4.216zM4.5 8a2.5 2.5 0 1 0 0-5 2.5 2.5 0 0 0 0 5z"/></svg>'
svg_cap = '<svg viewBox="0 0 16 16" fill="white"><path d="M8.211 2.047a.5.5 0 0 0-.422 0l-7.5 3.5a.5.5 0 0 0 .025.917l7.5 3 7.5-3a.5.5 0 0 0 .025-.917l-7.5-3.5Z"/><path d="M4.176 9.032a.5.5 0 0 0-.656.327l-.5 1.7a.5.5 0 0 0 .254.539l1.5.75A.5.5 0 0 0 5.25 12h5.5a.5.5 0 0 0 .476-.346l.5-1.7a.5.5 0 0 0-.656-.327L10 10.25l-.117-.043-4 .876L4.176 9.032Z"/></svg>'
svg_warning = '<svg viewBox="0 0 16 16" fill="white"><path d="M8.982 1.566a1.13 1.13 0 0 0-1.96 0L.165 13.233c-.457.778.091 1.767.98 1.767h13.713c.889 0 1.438-.99.98-1.767L8.982 1.566zM8 5c.535 0 .954.462.9.995l-.35 3.507a.552.552 0 0 1-1.1 0L7.1 5.995A.905.905 0 0 1 8 5zm.002 6a1 1 0 1 1 0 2 1 1 0 0 1 0-2z"/></svg>'
svg_chart = '<svg viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M18 20V10M12 20V4M6 20v-6"/></svg>'

# ==================================
# Bagian 2: DATA LOAD
# ==================================
@st.cache_data
def load_all_data():
    try:
        df_ats = pd.read_csv("master_data_si_pandai.csv")
        for df in [df_ats]: df.columns = df.columns.str.strip().str.lower()
        return df_ats
    except: return pd.DataFrame()

data_wilayah = load_all_data()

# =========================
# Bagian 3: LOGIN
# =========================
if not st.session_state.login:
    _, col_card, _ = st.columns([1.5, 2, 1.5])
    with col_card:
        with st.container(border=True):
            st.markdown("<h3 style='text-align:center;'>LOGIN SI-PANDAI</h3>", unsafe_allow_html=True)
            u = st.text_input("Username")
            p = st.text_input("Password", type="password")
            if st.button("MASUK", use_container_width=True):
                if u == "admin" and p == "admin": st.session_state.login = True; st.rerun()
                else: st.error("Gagal")
    st.stop()

# ==================================
# Bagian 4: SIDEBAR (FIXED)
# ==================================
with st.sidebar:
    logo_b64 = get_base64_image("logo_sumut.png")
    if logo_b64:
        st.markdown(f'''
            <div style="display:flex;align-items:center;gap:12px;padding-bottom:15px;">
                <img src="data:image/png;base64,{logo_b64}" width="40">
                <span style="font-size:16px;font-weight:800;color:white;">SI-PANDAI SUMUT</span>
            </div>
        ''', unsafe_allow_html=True)
    
    if st.button("👤 Role: ADMIN", key="role_admin_btn"):
        st.session_state.page_view = "admin_profile"
        st.rerun()
    
    st.divider()

    st.header("📌 Menu Utama")
    nav = st.radio("Navigasi:", ["🚀 Dashboard Utama", "🎓 Pendidikan Khusus", "ℹ️ Tentang Dashboard"], key="nav_radio")
    
    # Update Page View Based on Radio
    if "Dashboard" in nav: st.session_state.page_view = "dashboard"
    elif "Pendidikan" in nav: st.session_state.page_view = "tentang_pk"
    elif "Tentang" in nav: st.session_state.page_view = "tentang_dashboard"

    st.divider()
    st.header("🔎 Filter Wilayah")
    col_kab = "kab_kota" if "kab_kota" in data_wilayah.columns else "kabupaten"
    opsi = ["Semua"] + sorted(data_wilayah[col_kab].unique().tolist()) if not data_wilayah.empty else ["Semua"]
    kab_pilih = st.sidebar.selectbox("Kabupaten / Kota", opsi, key="selected_kab")

    st.divider()
    st.button("Logout 🚪", key="logout_btn", on_click=proses_logout, use_container_width=True)

# ==================================
# Bagian 5: HEADER CARD (ISTIMEWA)
# ==================================
st.markdown('<div class="top-gradient-bar"></div>', unsafe_allow_html=True)

st.markdown("""
    <div class="header-special-card">
        <h1>DASHBOARD UTAMA SI-PANDAI SUMUT</h1>
        <p>Sistem Informasi Anak Tidak Sekolah Disabilitas Sumatera Utara</p>
    </div>
""", unsafe_allow_html=True)

# Bungkus Konten Dashboard agar rapi
st.markdown('<div class="main-content-wrapper">', unsafe_allow_html=True)

# --- LOGIKA HALAMAN ---
if st.session_state.page_view == "dashboard":
    # Matriks Tiles
    m1, m2, m3, m4 = st.columns(4)
    with m1: draw_tile_svg("Penduduk Disabilitas", "110,876", svg_people, "tile-orange")
    with m2: draw_tile_svg("Siswa Belajar", "14,561", svg_cap, "tile-blue")
    with m3: draw_tile_svg("ATS", "67,231", svg_warning, "tile-navy")
    with m4: draw_tile_svg("Angka Partisipasi", "65.71%", svg_chart, "tile-green")

    st.divider()
    c1, c2 = st.columns([1.5, 1])
    with c1:
        st.subheader("🗺️ Peta Lokasi ATS")
        st.info("Visualisasi Peta Sebaran Wilayah")
    with c2:
        st.subheader("📊 Statistik ATS Wilayah")
        st.write("Grafik perbandingan data")

elif st.session_state.page_view == "admin_profile":
    st.markdown("### 👤 Profil Administrator")
    if st.button("⬅️ Kembali"):
        st.session_state.page_view = "dashboard"
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)
