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
    st.session_state.selected_kab = "Semua"
    st.session_state.login = False
    st.session_state.page_view = "dashboard"

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
    html, body, [data-testid="stWidgetLabel"] { font-family: 'Inter', sans-serif !important; }

    /* SIDEBAR GRADIENT SESUAI GAMBAR */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1565c0 0%, #0d47a1 100%) !important;
        padding-top: 20px;
    }
    [data-testid="stSidebar"] * { color: white !important; }

    /* MENU UTAMA - NAVIGASI STYLE */
    div[data-testid="stSidebarNav"] { display: none; } /* Sembunyikan default */
    
    /* Styling Radio Button agar seperti Button List di gambar */
    div[data-testid="stSidebar"] div.stRadio > div {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 5px;
    }
    div[data-testid="stSidebar"] div.stRadio label {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        margin-bottom: 5px;
        padding: 12px 15px !important;
        transition: 0.3s;
        border: 1px solid rgba(255,255,255,0.1);
        width: 100%;
    }
    div[data-testid="stSidebar"] div.stRadio label:hover {
        background: rgba(255, 255, 255, 0.2);
    }
    div[data-testid="stSidebar"] div.stRadio label[data-selected="true"] {
        background: #1e88e5 !important;
        border: 1px solid white;
    }

    /* FILTER BOX (BIRU MUDA CARD) */
    .filter-card {
        background: #bbdefb !important;
        padding: 20px;
        border-radius: 15px;
        margin: 10px 0;
    }
    .filter-card label, .filter-card p { color: #0d47a1 !important; font-weight: 700 !important; }
    div[data-testid="stSidebar"] div[data-baseweb="select"] * { color: #31333f !important; }

    /* TOMBOL LOGOUT ORANGE SESUAI GAMBAR */
    .stButton > button[key="logout_btn"] {
        background: linear-gradient(90deg, #ff8a65 0%, #f4511e 100%) !important;
        color: white !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        height: 50px !important;
        border: none !important;
        margin-top: 20px;
    }

    /* DASHBOARD MATRIKS */
    .metric-tile { padding: 20px; border-radius: 15px; color: white; margin-bottom: 15px; display: flex; align-items: center; gap: 15px; }
    .tile-orange { background: #ff9800; }
    .tile-blue-light { background: #03a9f4; }
    .tile-red-dark { background: #3f51b5; } /* Di gambar ATS pakai Biru Tua */
    .tile-green-light { background: #4caf50; }
    
    div.stButton > button[key^="btn_"] {
        background: #1e88e5 !important;
        color: white !important; border-radius: 10px !important; font-size: 14px !important; width: 100% !important;
    }
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
        st.image("logo_sipandai.png", width=250) if os.path.exists("logo_sipandai.png") else None
        st.markdown("<h2 style='text-align: center; color:#0d47a1;'>LOGIN USER</h2>", unsafe_allow_html=True)
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")
        if st.button("MASUK KE DASHBOARD", use_container_width=True):
            if u == "admin" and p == "admin": st.session_state.login = True; st.rerun()
            else: st.error("Login Gagal")
    st.stop()

# ==================================
# Bagian 4: SIDEBAR CUSTOM (FIXED UI)
# ==================================
with st.sidebar:
    # Header Logo & Title
    col1, col2 = st.columns([0.3, 0.7])
    with col1:
        if os.path.exists("logo_sumut.png"): st.image("logo_sumut.png", width=50)
    with col2:
        st.markdown("### SI-PANDAI SUMUT")
        st.caption("Role: **ADMIN**")
    
    st.divider()

    # Navigasi Menu Utama
    st.markdown("#### 🏠 Menu Utama")
    
    def on_nav_change():
        pilihan = st.session_state.nav_radio
        if "Dashboard" in pilihan: st.session_state.page_view = "dashboard"
        elif "Pendidikan" in pilihan: st.session_state.page_view = "tentang_pk"
        else: st.session_state.page_view = "tentang_dashboard"

    st.radio(
        "Navigasi:",
        ["🏠 Dashboard Utama", "🎓 Pendidikan Khusus", "ℹ️ Tentang Dashboard"],
        key="nav_radio",
        label_visibility="collapsed",
        on_change=on_nav_change
    )

    st.divider()

    # Filter Wilayah Card
    st.markdown("#### 🔍 Filter Wilayah")
    with st.container():
        st.markdown('<div class="filter-card">', unsafe_allow_html=True)
        col_kab = "kab_kota" if "kab_kota" in data_wilayah.columns else data_wilayah.columns[0]
        opsi = ["Semua"] + sorted(data_wilayah[col_kab].unique().tolist()) if not data_wilayah.empty else ["Semua"]
        kab_pilih = st.selectbox("Pilih Kabupaten / Kota", opsi, key="selected_kab")
        if st.button("🔄 Reset Filter", use_container_width=True):
            st.session_state.selected_kab = "Semua"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # Logout Button at Bottom
    st.button("🚪 Logout", key="logout_btn", on_click=proses_logout, use_container_width=True)

# ==================================
# Bagian 5: LOGIKA HALAMAN
# ==================================

# --- DASHBOARD ---
if st.session_state.page_view == "dashboard":
    st.markdown(f'<h2 style="color:#0d47a1;">🚀 Dashboard Utama: {kab_pilih}</h2>', unsafe_allow_html=True)
    st.divider()

    df_f = data_wilayah.copy()
    if kab_pilih != "Semua": df_f = df_f[df_f[col_kab] == kab_pilih]

    # Matriks Sesuai Warna Gambar
    m1, m2, m3, m4 = st.columns(4)
    val_p = f"{int(df_f.iloc[:,1].sum()):,}" if not df_f.empty else "0"
    val_s = f"{int(df_f.iloc[:,2].sum()):,}" if not df_f.empty else "0"
    val_a = f"{int(df_f.iloc[:,3].sum()):,}" if not df_f.empty else "0"
    val_APS = f"{(int(df_f.iloc[:,2].sum()) / int(df_f.iloc[:,1].sum()) * 100):.2f}%" if not df_f.empty and int(df_f.iloc[:,1].sum()) > 0 else "0%"

    with m1: st.markdown(f'<div class="metric-tile tile-orange"><div><div class="tile-label">PENDUDUK DISABILITAS</div><div class="tile-value">{val_p}</div></div></div>', unsafe_allow_html=True)
    with m2: st.markdown(f'<div class="metric-tile tile-blue-light"><div><div class="tile-label">SISWA BELAJAR</div><div class="tile-value">{val_s}</div></div></div>', unsafe_allow_html=True)
    with m3: st.markdown(f'<div class="metric-tile tile-red-dark"><div><div class="tile-label">ANAK TIDAK SEKOLAH</div><div class="tile-value">{val_a}</div></div></div>', unsafe_allow_html=True)
    with m4: st.markdown(f'<div class="metric-tile tile-green-light"><div><div class="tile-label">ANGKA PARTISIPASI</div><div class="tile-value">{val_APS}</div></div></div>', unsafe_allow_html=True)

    if kab_pilih != "Semua":
        st.divider()
        st.subheader(f"🏫 Satuan Pendidikan di {kab_pilih}")
        sch_wil = data_sekolah[data_sekolah[col_kab] == kab_pilih] if not data_sekolah.empty else pd.DataFrame()
        if not sch_wil.empty:
            cols = st.columns(3)
            for i, row in enumerate(sch_wil.itertuples()):
                with cols[i % 3]:
                    with st.container(border=True):
                        st.button(getattr(row, 'nama_sekolah', 'SEKOLAH').upper(), key=f"btn_{i}")
                        st.caption(f"NPSN: {getattr(row, 'npsn', '-')}")

    st.divider()
    c_map, c_chart = st.columns([1.5, 1])
    with c_map:
        st.subheader("🗺️ Lokasi ATS")
        if not df_f.empty: st.map(df_f, latitude="lat", longitude="lon")
    with c_chart:
        st.subheader("📊 Statistik")
        if not df_f.empty: st.plotly_chart(px.bar(df_f.head(10), x=df_f.columns[3], y=col_kab, orientation='h'), use_container_width=True)

# --- LAINNYA ---
elif st.session_state.page_view == "tentang_pk":
    st.title("🎓 Pendidikan Khusus Sumatera Utara")
elif st.session_state.page_view == "tentang_dashboard":
    st.title("ℹ️ Tentang Dashboard SI-PANDAI")
