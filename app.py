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
    st.rerun()

def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

# ==================================
# Bagian 1: CSS CUSTOM (MODERN DEEP BLUE)
# ==================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
    html, body, [data-testid="stWidgetLabel"] { font-family: 'Inter', sans-serif !important; }

    /* --- SIDEBAR DEEP BLUE GRADIENT --- */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d47a1 0%, #1565c0 45%, #1976d2 100%) !important;
        background-attachment: fixed !important;
    }
    [data-testid="stSidebar"] * { color: white !important; }
    div[data-testid="stSelectbox"] div[data-baseweb="select"] * { color: #31333f !important; }

   /* --- KUNCI KODING: HAPUS KOTAK PUTIH ADMIN --- */
    .admin-role-container .stButton button {
        background-color: transparent !important;
        background: transparent !important;
        color: white !important;
        border-radius: 10px !important;
        border: 1px solid rgba(255, 255, 255, 0.4) !important;
        width: auto !important;
        font-size: 13px !important;
        box-shadow: none !important;
        transition: 0.3s;
        padding: 5px 10px !important;
    }

    .admin-role-container .stButton button:hover {
        background-color: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid white !important;
    }

    /* --- MENU NAVIGASI (SIDEBAR CARDS) --- */
    div[data-testid="stSidebar"] div.stRadio > div { gap: 8px !important; }
    div[data-testid="stSidebar"] div.stRadio label {
        background: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 12px !important;
        padding: 10px 15px !important;
        transition: 0.3s;
    }
    div[data-testid="stSidebar"] div.stRadio label[data-selected="true"] {
        background: rgba(255, 255, 255, 0.25) !important;
        border: 1px solid white !important;
    }

    /* --- TOMBOL LOGOUT (ORANGE) --- */
    div[data-testid="stSidebar"] .stButton button[key="logout_btn"] {
        background: linear-gradient(90deg, #ff7043 0%, #ff5722 100%) !important;
        border: none !important;
        font-weight: 700 !important;
        height: 45px !important;
    }

    /* --- DASHBOARD TILES --- */
    .metric-tile { padding: 20px; border-radius: 12px; color: white; margin-bottom: 15px; display: flex; align-items: center; gap: 15px; }
    .tile-orange { background: linear-gradient(135deg, #ff9800 0%, #f57c00 100%); }
    .tile-blue-light { background: linear-gradient(135deg, #03a9f4 0%, #0288d1 100%); }
    .tile-red-dark { background: linear-gradient(135deg, #ff4b2b 0%, #ff416c 100%); }
    .tile-green { background: linear-gradient(135deg, #4caf50 0%, #2e7d32 100%); }
    .tile-label { font-size: 14px; font-weight: 800; text-transform: uppercase; }
    .tile-value { font-size: 24px; font-weight: 800; }

    /* BALON NAMA SEKOLAH */
    div.stButton > button[key^="btn_"] {
        background: linear-gradient(90deg, #0d47a1 0%, #1976d2 100%) !important;
        color: white !important; border-radius: 20px !important; font-size: 13px !important; font-weight: 700 !important; width: 100% !important;
    }
</style>
""", unsafe_allow_html=True)

def draw_tile_svg(label, value, svg_icon, style_class):
    st.markdown(f'<div class="metric-tile {style_class}"><div style="width:42px;height:42px;">{svg_icon}</div><div><div class="tile-label">{label}</div><div class="tile-value">{value}</div></div></div>', unsafe_allow_html=True)

# Icons SVG
svg_people = '<svg viewBox="0 0 16 16" fill="white"><path d="M7 14s-1 0-1-1 1-4 5-4 5 3 5 4-1 1-1 1H7zm4-6a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm-5.784 6A2.238 2.238 0 0 1 5 13c0-1.355.68-2.75 1.936-3.72A6.325 6.325 0 0 0 5 9c-4 0-5 3-5 4s1 1 1 1h4.216zM4.5 8a2.5 2.5 0 1 0 0-5 2.5 2.5 0 0 0 0 5z"/></svg>'
svg_cap = '<svg viewBox="0 0 16 16" fill="white"><path d="M8.211 2.047a.5.5 0 0 0-.422 0l-7.5 3.5a.5.5 0 0 0 .025.917l7.5 3 7.5-3a.5.5 0 0 0 .025-.917l-7.5-3.5Z"/><path d="M4.176 9.032a.5.5 0 0 0-.656.327l-.5 1.7a.5.5 0 0 0 .254.539l1.5.75A.5.5 0 0 0 5.25 12h5.5a.5.5 0 0 0 .476-.346l.5-1.7a.5.5 0 0 0-.656-.327L10 10.25l-.117-.043-4 .876L4.176 9.032Z"/></svg>'
svg_warning = '<svg viewBox="0 0 16 16" fill="white"><path d="M8.982 1.566a1.13 1.13 0 0 0-1.96 0L.165 13.233c-.457.778.091 1.767.98 1.767h13.713c.889 0 1.438-.99.98-1.767L8.982 1.566zM8 5c.535 0 .954.462.9.995l-.35 3.507a.552.552 0 0 1-1.1 0L7.1 5.995A.905.905 0 0 1 8 5zm.002 6a1 1 0 1 1 0 2 1 1 0 0 1 0-2z"/></svg>'
svg_chart = '<svg viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M18 20V10M12 20V4M6 20v-6"/></svg>'

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
    _, col_card, _ = st.columns([1.5, 2, 1.5])
    with col_card:
        with st.container(border=True):
            if os.path.exists("logo_sipandai.png"): st.image("logo_sipandai.png", use_container_width=True)
            st.markdown("<h3 style='text-align:center; color:#0d47a1;'>LOGIN</h3>", unsafe_allow_html=True)
            u = st.text_input("Username")
            p = st.text_input("Password", type="password")
            if st.button("MASUK", use_container_width=True):
                if u == "admin" and p == "admin": st.session_state.login = True; st.rerun()
                else: st.error("Login Gagal")
    st.stop()

# ==================================
# Bagian 4: SIDEBAR
# ==================================
with st.sidebar:
    logo_b64 = get_base64_image("logo_sumut.png")
    if logo_b64:
        st.markdown(f'<div style="display:flex;align-items:center;gap:12px;padding-bottom:15px;"><img src="data:image/png;base64,{logo_b64}" width="45"><span style="font-size:18px;font-weight:800;color:white;">SI-PANDAI SUMUT</span></div>', unsafe_allow_html=True)
    
    # TOMBOL ROLE ADMIN KLIKABEL (TANPA KOTAK PUTIH)
   # Bungkus tombol dalam div khusus untuk menghilangkan kotak putih
    st.markdown('<div class="admin-role-container">', unsafe_allow_html=True)
    if st.button("👤 Role: ADMIN"):
        st.session_state.page_view = "admin_profile"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.divider()
    def nav_change():
        p = st.session_state.nav_radio
        if "Dashboard" in p: st.session_state.page_view = "dashboard"
        elif "Pendidikan" in p: st.session_state.page_view = "tentang_pk"
        else: st.session_state.page_view = "tentang_dashboard"

    st.sidebar.header("📌 Menu Utama")
    st.sidebar.radio("Navigasi:", ["🚀 Dashboard Utama", "🎓 Pendidikan Khusus", "ℹ️ Tentang Dashboard"], key="nav_radio", on_change=nav_change)

    st.divider()
    st.sidebar.header("🔎 Filter")
    col_kab = "kab_kota" if "kab_kota" in data_wilayah.columns else data_wilayah.columns[0]
    opsi = ["Semua"] + sorted(data_wilayah[col_kab].unique().tolist()) if not data_wilayah.empty else ["Semua"]
    kab_pilih = st.sidebar.selectbox("Pilih Wilayah", opsi, key="selected_kab")

    st.divider()
    st.button("Logout 🚪", key="logout_btn", on_click=proses_logout, use_container_width=True)

# ==================================
# Bagian 5: MAIN CONTENT
# ==================================
st.markdown("<h2 style='text-align:right; color:#0d47a1; font-weight:800; margin-top:5px;'>OVERVIEW SI-PANDAI SUMUT</h2>", unsafe_allow_html=True)
st.divider()

# 1. DASHBOARD
if st.session_state.page_view == "dashboard":
    df_f = data_wilayah.copy()
    if kab_pilih != "Semua": df_f = df_f[df_f[col_kab] == kab_pilih]

    # Matriks
    m1, m2, m3, m4 = st.columns(4)
    val_p = f"{int(df_f.iloc[:,1].sum()):,}" if not df_f.empty else "0"
    val_s = f"{int(df_f.iloc[:,2].sum()):,}" if not df_f.empty else "0"
    val_a = f"{int(df_f.iloc[:,3].sum()):,}" if not df_f.empty else "0"
    val_APS = f"{(int(df_f.iloc[:,2].sum()) / int(df_f.iloc[:,1].sum()) * 100):.2f}%" if not df_f.empty and int(df_f.iloc[:,1].sum()) > 0 else "0%"

    with m1: draw_tile_svg("Penduduk Disabilitas", val_p, svg_people, "tile-orange")
    with m2: draw_tile_svg("Siswa Belajar", val_s, svg_cap, "tile-blue-light")
    with m3: draw_tile_svg("Anak Tidak Sekolah", val_a, svg_warning, "tile-red-dark")
    with m4: draw_tile_svg("Angka Partisipasi", val_APS, svg_chart, "tile-green")

    # Tabel Download
    st.divider()
    with st.expander("📋 Lihat & Download Data Wilayah"):
        st.dataframe(df_f, use_container_width=True)
        csv = df_f.to_csv(index=False).encode('utf-8')
        st.download_button(label="Download CSV 📥", data=csv, file_name=f'data_{kab_pilih}.csv', mime='text/csv')

    if kab_pilih != "Semua":
        st.divider()
        st.subheader(f"🏫 Sekolah di {kab_pilih}")
        sch_wil = data_sekolah[data_sekolah[col_kab] == kab_pilih] if not data_sekolah.empty else pd.DataFrame()
        if not sch_wil.empty:
            cols = st.columns(3)
            for i, row in enumerate(sch_wil.itertuples()):
                with cols[i % 3]:
                    with st.container(border=True):
                        if st.button(row.nama_sekolah.upper(), key=f"btn_{i}"):
                            st.session_state.selected_school_data = row._asdict()
                            st.session_state.page_view = "detail"
                            st.rerun()
                        st.caption(f"NPSN: {row.npsn}")

# 2. PROFIL ADMIN (HALAMAN BARU)
elif st.session_state.page_view == "admin_profile":
    st.markdown("### 👤 Profil Administrator")
    with st.container(border=True):
        st.write("### Super Admin SI-PANDAI")
        st.write("**Username:** admin")
        st.write("**Instansi:** Dinas Pendidikan Provinsi Sumatera Utara")
        st.write("**Bidang:** Pendidikan Khusus (PK)")
        st.write("**Status:** Aktif")
        st.caption("Data ini hanya dapat diakses oleh user dengan role Admin.")
    
    if st.button("⬅️ Kembali ke Dashboard"):
        st.session_state.page_view = "dashboard"
        st.rerun()

# 3. LAINNYA
elif st.session_state.page_view == "detail":
    sch = st.session_state.selected_school_data
    st.markdown(f"### 🏫 {sch['nama_sekolah'].upper()}")
    if st.button("⬅️ Kembali"):
        st.session_state.page_view = "dashboard"
        st.rerun()

elif st.session_state.page_view == "tentang_pk":
    st.title("🎓 Pendidikan Khusus")
    st.write("Konten mengenai Pendidikan Khusus.")

elif st.session_state.page_view == "tentang_dashboard":
    st.title("ℹ️ Tentang SI-PANDAI")
    st.write("Sistem Informasi Analitik Pendidikan Khusus.")
