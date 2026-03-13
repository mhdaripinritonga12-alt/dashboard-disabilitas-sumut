import streamlit as st
import pandas as pd
import plotly.express as px
import os
import base64

# ==================================
# Bagian 0: KONFIGURASI & STATE (FIXED)
# ==================================
st.set_page_config(page_title="SI-PANDAI SUMUT", layout="wide", initial_sidebar_state="expanded")

if "login" not in st.session_state: st.session_state.login = False
if "page_view" not in st.session_state: st.session_state.page_view = "dashboard"

def proses_logout():
    st.session_state.login = False
    st.session_state.page_view = "dashboard"

# ==================================
# Bagian 1: CSS TILES (PERSIS GAMBAR)
# ==================================
st.markdown("""
<style>
    [data-testid="stAppViewContainer"] { background-color: #f4f7f9 !important; }
    header { background-color: rgba(0,0,0,0) !important; visibility: visible !important; }
    
    .metric-tile {
        padding: 20px; border-radius: 15px; color: white; margin-bottom: 15px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1); display: flex; align-items: center; gap: 15px;
    }
    .tile-orange { background: linear-gradient(135deg, #ff9800 0%, #f57c00 100%); }
    .tile-blue-light { background: linear-gradient(135deg, #03a9f4 0%, #0288d1 100%); }
    .tile-blue-dark { background: linear-gradient(135deg, #3f51b5 0%, #303f9f 100%); }
    
    .tile-icon-svg { width: 40px; height: 40px; fill: white; opacity: 0.9; }
    .tile-label { font-size: 11px; font-weight: 700; opacity: 0.8; text-transform: uppercase; }
    .tile-value { font-size: 22px; font-weight: 800; }
</style>
""", unsafe_allow_html=True)

def draw_tile_svg(label, value, svg_icon, style_class):
    st.markdown(f"""
        <div class="metric-tile {style_class}">
            <div class="tile-icon-svg">{svg_icon}</div>
            <div><div class="tile-label">{label}</div><div class="tile-value">{value}</div></div>
        </div>
    """, unsafe_allow_html=True)

# SVG Icons
svg_people = '<svg viewBox="0 0 16 16"><path d="M7 14s-1 0-1-1 1-4 5-4 5 3 5 4-1 1-1 1H7zm4-6a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm-5.784 6A2.238 2.238 0 0 1 5 13c0-1.355.68-2.75 1.936-3.72A6.325 6.325 0 0 0 5 9c-4 0-5 3-5 4s1 1 1 1h4.216zM4.5 8a2.5 2.5 0 1 0 0-5 2.5 2.5 0 0 0 0 5z"/></svg>'
svg_cap = '<svg viewBox="0 0 16 16"><path d="M8.211 2.047a.5.5 0 0 0-.422 0l-7.5 3.5a.5.5 0 0 0 .025.917l7.5 3 7.5-3a.5.5 0 0 0 .025-.917l-7.5-3.5Z"/><path d="M4.176 9.032a.5.5 0 0 0-.656.327l-.5 1.7a.5.5 0 0 0 .254.539l1.5.75A.5.5 0 0 0 5.25 12h5.5a.5.5 0 0 0 .476-.346l.5-1.7a.5.5 0 0 0-.656-.327L10 10.25l-.117-.043-4 .876L4.176 9.032Z"/></svg>'
svg_warning = '<svg viewBox="0 0 16 16"><path d="M8.982 1.566a1.13 1.13 0 0 0-1.96 0L.165 13.233c-.457.778.091 1.767.98 1.767h13.713c.889 0 1.438-.99.98-1.767L8.982 1.566zM8 5c.535 0 .954.462.9.995l-.35 3.507a.552.552 0 0 1-1.1 0L7.1 5.995A.905.905 0 0 1 8 5z"/></svg>'

# ==================================
# Bagian 2: DATA & LOGIN
# ==================================
@st.cache_data
def load_all_data():
    try:
        df_ats = pd.read_csv("master_data_si_pandai.csv")
        df_sch = pd.read_csv("master_data_sekolah1.csv")
        return df_ats, df_sch
    except: return pd.DataFrame(), pd.DataFrame()

data_wilayah, data_sekolah = load_all_data()

if not st.session_state.login:
    _, col_card, _ = st.columns([1, 1.2, 1])
    with col_card:
        with st.container(border=True):
            st.subheader("🔑 Login SI-PANDAI")
            u = st.text_input("User")
            p = st.text_input("Pass", type="password")
            if st.button("MASUK"):
                if u == "admin" and p == "admin":
                    st.session_state.login = True
                    st.rerun()
    st.stop()

# ==================================
# Bagian 3: DASHBOARD
# ==================================
st.sidebar.header("🔎 Navigasi")
kab_pilih = st.sidebar.selectbox("Wilayah", ["Semua"] + sorted(data_wilayah["kab_kota"].unique().tolist()))
st.sidebar.button("Logout 🚪", on_click=proses_logout)

if st.session_state.page_view == "dashboard":
    st.title("🚀 Dashboard Utama")
    
    df_f = data_wilayah.copy()
    if kab_pilih != "Semua":
        df_f = df_f[df_f["kab_kota"] == kab_pilih]

    # Matriks 4 Kolom (FIXED)
    m1, m2, m3, m4 = st.columns(4)
    val_p = f"{int(df_f['jumlah_penduduk'].sum()):,}"
    val_s = f"{int(df_f['jumlah_siswa'].sum()):,}"
    val_a = f"{int(df_f['ats_disabilitas'].sum()):,}"
    val_aps = "67.93%" # Contoh statis

    with m1: draw_tile_svg("Penduduk", val_p, svg_people, "tile-orange")
    with m2: draw_tile_svg("Siswa", val_s, svg_cap, "tile-blue-light")
    with m3: draw_tile_svg("ATS", val_a, svg_warning, "tile-blue-dark")
    with m4: draw_tile_svg("Partisipasi", val_aps, svg_cap, "tile-blue-light")

    st.divider()
    st.subheader("🗺️ Sebaran Wilayah")
    st.map(df_f, latitude="lat", longitude="lon")
