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

# Fungsi bantuan untuk metrik (agar kode tidak error saat running)
def draw_metric_card(label, value, color):
    st.markdown(f"""
        <div style="background-color: white; padding: 20px; border-radius: 15px; border-left: 5px solid {color}; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
            <p style="margin:0; color: #64748b; font-size: 12px; font-weight: 700; text-transform: uppercase;">{label}</p>
            <h2 style="margin:0; color: #0f172a; font-weight: 800;">{value}</h2>
        </div>
    """, unsafe_allow_html=True)

# ==================================
# Bagian 1: CSS CUSTOM (DIPERBAIKI UNTUK MUNCULKAN SIDEBAR)
# ==================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
    html, body, [data-testid="stWidgetLabel"] { font-family: 'Inter', sans-serif !important; }

    .block-container {
        padding-top: 0.5rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
    }
    
    /* Tombol sidebar dimunculkan kembali */
    [data-testid="collapsedControl"] {
        display: flex !important;
    }

    .top-gradient-bar {
        position: fixed;
        top: 0; left: 0; width: 100%; height: 5px;
        background: #1e88e5;
        z-index: 999999;
    }

    /* Memastikan konten sidebar terlihat (Warna Biru Gradien) */
    [data-testid="stSidebar"] { 
        background: linear-gradient(180deg, #1e88e5 0%, #0d47a1 100%) !important; 
    }
    
    /* Memaksa teks di dalam sidebar berwarna putih agar kontras */
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] label, [data-testid="stSidebar"] span {
        color: white !important;
    }
    
    /* Fix untuk warna dropdown/selectbox di sidebar agar tidak putih-diatas-putih */
    div[data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] div {
        color: #1e293b !important;
    }

    .header-balloon-card {
        background: linear-gradient(90deg, #f0f7ff 0%, #d1e9ff 100%) !important;
        border-radius: 0px 0px 15px 15px;
        padding: 5px 0px;
        border-bottom: 2px solid rgba(13, 71, 161, 0.1);
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        text-align: center;
        margin-top: 2px;
        margin-bottom: 20px;
        width: 100% !important;
        display: block;
    }
</style>
""", unsafe_allow_html=True)

# ==================================
# Bagian 2: LOAD DATA
# ==================================
@st.cache_data
def load_all_data():
    try:
        # Gunakan nama file yang sama dengan kode Anda
        df_ats = pd.read_csv("master_data_si_pandai.csv") if os.path.exists("master_data_si_pandai.csv") else pd.DataFrame()
        df_sch = pd.read_csv("master_data_sekolah1.csv") if os.path.exists("master_data_sekolah1.csv") else pd.DataFrame()
        
        if not df_ats.empty:
            df_ats.columns = df_ats.columns.str.strip().str.lower()
        if not df_sch.empty:
            df_sch.columns = df_sch.columns.str.strip().str.lower()
        return df_ats, df_sch
    except:
        return pd.DataFrame(), pd.DataFrame()

data_wilayah, data_sekolah = load_all_data()

# ==================================
# Bagian 4: SIDEBAR & NAVIGASI
# ==================================
with st.sidebar:
    st.markdown('<div style="padding: 20px 0px 40px 0px;">', unsafe_allow_html=True)
    logo_b64 = get_base64_image("logo_sumut.png")
    if logo_b64:
        st.markdown(f'''
            <div style="display:flex;flex-direction:column;gap:15px;">
                <img src="data:image/png;base64,{logo_b64}" width="60">
                <div>
                   <span style="font-size:22px;font-weight:800;letter-spacing:-0.02em;">SI-PANDAI</span>
                   <p style="font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:0.1em;margin-top:2px;">Provinsi Sumatera Utara</p>
                </div>
            </div>
        ''', unsafe_allow_html=True)
    else:
        # Fallback jika file gambar tidak ada
        st.markdown('### SI-PANDAI SUMUT')
    st.markdown('</div>', unsafe_allow_html=True)

    def ubah_halaman():
        if "nav_radio" in st.session_state:
            pilihan = st.session_state.nav_radio
            if "Beranda Utama" in pilihan: st.session_state.page_view = "dashboard"
            elif "Informasi Sistem" in pilihan: st.session_state.page_view = "tentang_dashboard"

    st.markdown('<p style="font-size:10px; font-weight:800; text-transform:uppercase; letter-spacing:0.15em; margin-bottom:15px;">Navigasi Utama</p>', unsafe_allow_html=True)
    st.sidebar.radio(
        "Menu", 
        ["🏠 Beranda Utama", "ℹ️ Informasi Sistem"],
        key="nav_radio",
        on_change=ubah_halaman,
        label_visibility="collapsed"
    )

    st.markdown('<div style="height:40px;"></div>', unsafe_allow_html=True)
    st.markdown('<p style="font-size:10px; font-weight:800; text-transform:uppercase; letter-spacing:0.15em; margin-bottom:15px;">Wilayah Kerja</p>', unsafe_allow_html=True)

    col_kab = "kab_kota"
    if not data_wilayah.empty and col_kab in data_wilayah.columns:
        raw_opsi = data_wilayah[col_kab].dropna().unique().tolist()
        opsi = ["Semua"] + sorted([str(x) for x in raw_opsi])
    else:
        opsi = ["Semua"]

    st.selectbox("Pilih Kabupaten/Kota", opsi, key="selected_kab", label_visibility="collapsed")

# ==================================
# Bagian 5: HEADER & DASHBOARD
# ==================================
st.markdown('<div class="top-gradient-bar"></div>', unsafe_allow_html=True)
st.markdown("""
    <div class="header-balloon-card">
        <h2 style='color: #0f172a; font-weight:800; margin: 0; font-size: 1.85rem;'>
            SI-PANDAI Sistem Informasi Pemetaan Anak Tidak Sekolah Disabilitas
        </h2>
        <p style='color: #64748b; font-size: 12px; font-weight: 700; margin-top: 8px; text-transform: uppercase; letter-spacing: 0.15em;'>
            Dinas Pendidikan Provinsi Sumatera Utara
        </p>
    </div>
""", unsafe_allow_html=True)

# Render Dashboard sederhana agar data muncul
if st.session_state.page_view == "dashboard":
    df_f = data_wilayah.copy()
    if st.session_state.selected_kab != "Semua":
        df_f = df_f[df_f["kab_kota"] == st.session_state.selected_kab]
    
    st.write("### Data Overview")
    st.dataframe(df_f, use_container_width=True)
