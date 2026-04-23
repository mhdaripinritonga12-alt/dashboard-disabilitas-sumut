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

# Fungsi tambahan untuk metric card agar tidak error
def draw_metric_card(label, value, color):
    st.markdown(f"""
        <div style="background-color: white; padding: 20px; border-radius: 15px; border-left: 5px solid {color}; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
            <p style="margin:0; color: #64748b; font-size: 12px; font-weight: 700; text-transform: uppercase;">{label}</p>
            <h2 style="margin:0; color: #0f172a; font-weight: 800;">{value}</h2>
        </div>
    """, unsafe_allow_html=True)

# ==================================
# Bagian 1: CSS CUSTOM (OFF-WHITE PROFESSIONAL SIDEBAR)
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
    [data-testid="stHeader"] { display: none !important; }
    
    /* SIDEBAR STYLING */
    [data-testid="stSidebar"] {
        background-color: #f8fafc !important; /* Off-white color */
        border-right: 1px solid #e2e8f0;
    }
    
    /* Memastikan teks sidebar terlihat (Hitam/Abu Gelap) */
    [data-testid="stSidebar"] .stMarkdown p, 
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] .stRadio span {
        color: #1e293b !important;
    }

    .top-gradient-bar {
        position: fixed;
        top: 0; left: 0; width: 100%; height: 5px;
        background: #1e88e5;
        z-index: 999999;
    }

    .header-balloon-card {
        background: linear-gradient(90deg, #f0f7ff 0%, #d1e9ff 100%) !important;
        border-radius: 0px 0px 15px 15px;
        padding: 20px 0px;
        border-bottom: 2px solid rgba(13, 71, 161, 0.1);
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        text-align: center;
        margin-top: 2px;
        margin-bottom: 20px;
        width: 100% !important;
        display: block;
    }

    .insight-box { 
        background-color: #e3f2fd !important; 
        border-radius: 8px; 
        border-left: 4px solid #0d47a1; 
        padding: 15px; 
        margin-top: 10px; 
    }
    
    /* Styling Radio Button Sidebar agar lebih pro */
    div[data-testid="stSidebar"] div.stRadio div[role="radiogroup"] {
        gap: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ==================================
# Bagian 2: LOAD DATA
# ==================================
@st.cache_data
def load_all_data():
    try:
        # Load data dummy jika file tidak ada, atau sesuaikan dengan file Anda
        if os.path.exists("master_data_si_pandai.csv"):
            df_ats = pd.read_csv("master_data_si_pandai.csv")
        else:
            df_ats = pd.DataFrame({'kab_kota': ['Medan', 'Deli Serdang'], 'belajar': [100, 200], 'ats': [10, 20], 'lat': [3.59, 3.55], 'lon': [98.67, 98.85]})
            
        if os.path.exists("master_data_sekolah1.csv"):
            df_sch = pd.read_csv("master_data_sekolah1.csv")
        else:
            df_sch = pd.DataFrame()

        df_ats.columns = df_ats.columns.str.strip().str.lower()
        df_sch.columns = df_sch.columns.str.strip().str.lower()
        return df_ats, df_sch
    except Exception as e:
        st.error(f"Gagal memuat data: {e}")
        return pd.DataFrame(), pd.DataFrame()

data_wilayah, data_sekolah = load_all_data()

# ==================================
# Bagian 4: SIDEBAR & NAVIGASI
# ==================================
with st.sidebar:
    st.markdown('<div style="padding: 10px 0px 30px 0px;">', unsafe_allow_html=True)
    logo_b64 = get_base64_image("logo_sumut.png")
    if logo_b64:
        st.markdown(f'''
            <div style="display:flex;flex-direction:column;gap:10px;align-items:center;text-align:center;">
                <img src="data:image/png;base64,{logo_b64}" width="70">
                <div>
                   <span style="font-size:20px;font-weight:800;color:#0f172a;">SI-PANDAI</span>
                   <p style="font-size:10px;font-weight:700;color:#1e88e5;text-transform:uppercase;margin:0;">Provinsi Sumatera Utara</p>
                </div>
            </div>
        ''', unsafe_allow_html=True)
    else:
        st.markdown('<h2 style="color:#0f172a; text-align:center;">SI-PANDAI</h2>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    def ubah_halaman():
        if "nav_radio" in st.session_state:
            pilihan = st.session_state.nav_radio
            if "Beranda Utama" in pilihan: 
                st.session_state.page_view = "dashboard"
            elif "Informasi Sistem" in pilihan: 
                st.session_state.page_view = "tentang_dashboard"

    st.markdown('<p style="font-size:10px; font-weight:800; color:#94a3b8; text-transform:uppercase; letter-spacing:0.15em;">Navigasi Utama</p>', unsafe_allow_html=True)
    st.radio(
        "Menu", 
        ["🏠 Beranda Utama", "ℹ️ Informasi Sistem"],
        key="nav_radio",
        on_change=ubah_halaman,
        label_visibility="collapsed"
    )

    st.markdown('<div style="height:30px;"></div>', unsafe_allow_html=True)
    st.markdown('<p style="font-size:10px; font-weight:800; color:#94a3b8; text-transform:uppercase; letter-spacing:0.15em;">Wilayah Kerja</p>', unsafe_allow_html=True)

    col_kab = "kab_kota"
    if not data_wilayah.empty:
        raw_opsi = data_wilayah[col_kab].dropna().unique().tolist()
        opsi = ["Semua"] + sorted([str(x) for x in raw_opsi])
    else:
        opsi = ["Semua"]

    kab_pilih = st.selectbox("Pilih Kabupaten/Kota", opsi, key="selected_kab", label_visibility="collapsed")

# ==================================
# Bagian 5: HEADER & ISI HALAMAN
# ==================================
st.markdown('<div class="top-gradient-bar"></div>', unsafe_allow_html=True)
st.markdown("""
    <div class="header-balloon-card">
        <h2 style='color: #0f172a; font-weight:800; margin: 0; font-size: 1.85rem;'>
            SI-PANDAI Sistem Informasi Pemetaan Anak Tidak Sekolah Disabilitas
        </h2>
        <p style='color: #64748b; font-size: 12px; font-weight: 700; margin-top: 8px; text-transform: uppercase;'>
            Dinas Pendidikan Provinsi Sumatera Utara
        </p>
    </div>
""", unsafe_allow_html=True)

if st.session_state.page_view == "dashboard":
    df_f = data_wilayah.copy()
    if st.session_state.selected_kab != "Semua": 
        df_f = df_f[df_f[col_kab] == st.session_state.selected_kab]

    ats_col = "ats"
    belajar_col = "belajar"
    
    total_ats = int(df_f[ats_col].sum()) if not df_f.empty and ats_col in df_f.columns else 0
    total_belajar = int(df_f[belajar_col].sum()) if not df_f.empty and belajar_col in df_f.columns else 0
    rasio = (total_belajar / (total_belajar + total_ats) * 100) if (total_belajar + total_ats) > 0 else 0

    m1, m2, m3 = st.columns(3)
    with m1: draw_metric_card("Siswa Belajar", f"{total_belajar:,}", "#3b82f6")
    with m2: draw_metric_card("Anak Tidak Sekolah", f"{total_ats:,}", "#f59e0b")
    with m3: draw_metric_card("Rasio Partisipasi", f"{rasio:.2f}%", "#10b981")

    # ... Sisa kode dashboard (Map & Chart) tetap sama ...
    st.write("### Data Overview")
    st.dataframe(df_f, use_container_width=True)

elif st.session_state.page_view == "tentang_dashboard":
    st.markdown('<div class="insight-box">', unsafe_allow_html=True)
    st.markdown('### Mengenal SI-PANDAI')
    st.write("Sistem monitoring berbasis data untuk memetakan Anak Tidak Sekolah (ATS) disabilitas.")
    st.markdown('</div>', unsafe_allow_html=True)
    if st.button("⬅️ Kembali ke Beranda"):
        st.session_state.page_view = "dashboard"
        st.rerun()

# FOOTER
st.markdown('<div style="height:100px;"></div>', unsafe_allow_html=True)
st.divider()
st.markdown('<p style="text-align:center; color:#94a3b8; font-size:11px;">© 2026 Dinas Pendidikan Provinsi Sumatera Utara</p>', unsafe_allow_html=True)
