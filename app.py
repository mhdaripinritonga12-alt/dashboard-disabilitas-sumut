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

   /* --- PERBAIKAN TOMBOL ADMIN (TRANSPARAN TOTAL) --- */
    div[data-testid="stSidebar"] div.stButton > button[key="admin_sidebar_btn"] {
        background-color: rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        padding: 10px 15px !important;
        font-weight: 700 !important;
        border: 1px solid rgba(255, 255, 255, 0.4) !important; /* Hanya border tipis */
        width: 100% !important;
        text-align: left !important;
        
    }

    /* --- MENU NAVIGASI (SIDEBAR CARDS) --- */
    div[data-testid="stSidebar"] div.stRadio > div { gap: 10px !important; }
    div[data-testid="stSidebar"] div.stRadio label {
        background: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 12px !important;
        padding: 12px 15px !important;
        transition: 0.3s;
    }
    div[data-testid="stSidebar"] div.stRadio label[data-selected="true"] {
        background: rgba(255, 255, 255, 0.25) !important;
        border: 1px solid white !important;
        font-weight: 700 !important;
    }

    /* --- TOMBOL LOGOUT (ORANGE GRADIENT) --- */
    div[data-testid="stSidebar"] .stButton button[key="logout_btn"] {
                border-radius: 12px !important;
        font-weight: 700 !important;
        height: 50px !important;
        border: none !important;
    }

    /* --- DASHBOARD CONTENT STYLE --- */
    .metric-tile { padding: 20px; border-radius: 12px; color: white; margin-bottom: 15px; display: flex; align-items: center; gap: 15px; }
    .tile-orange { background: linear-gradient(135deg, #ff9800 0%, #f57c00 100%); }
    .tile-blue-light { background: linear-gradient(135deg, #03a9f4 0%, #0288d1 100%); }
    .tile-navy { background: linear-gradient(135deg, #3f51b5 0%, #1a237e 100%); }
    .tile-green { background: linear-gradient(135deg, #4caf50 0%, #2e7d32 100%); }
    .tile-icon-svg { width: 42px; height: 42px; fill: white !important; }
    .tile-label { font-size: 14px; font-weight: 800; text-transform: uppercase; }
    .tile-value { font-size: 24px; font-weight: 800; }

    /* TOMBOL BALON SEKOLAH */
    div.stButton > button[key^="btn_"] {
        background: linear-gradient(90deg, #0d47a1 0%, #1976d2 100%) !important;
        color: white !important; border-radius: 20px !important; font-size: 13px !important; width: 100% !important;
    }
</style>
""", unsafe_allow_html=True)

def draw_tile_svg(label, value, svg_icon, style_class):
    st.markdown(f'<div class="metric-tile {style_class}"><div class="tile-icon-svg">{svg_icon}</div><div><div class="tile-label">{label}</div><div class="tile-value">{value}</div></div></div>', unsafe_allow_html=True)

# SVG Icons
svg_people = '<svg viewBox="0 0 16 16"><path d="M7 14s-1 0-1-1 1-4 5-4 5 3 5 4-1 1-1 1H7zm4-6a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm-5.784 6A2.238 2.238 0 0 1 5 13c0-1.355.68-2.75 1.936-3.72A6.325 6.325 0 0 0 5 9c-4 0-5 3-5 4s1 1 1 1h4.216zM4.5 8a2.5 2.5 0 1 0 0-5 2.5 2.5 0 0 0 0 5z"/></svg>'
svg_cap = '<svg viewBox="0 0 16 16"><path d="M8.211 2.047a.5.5 0 0 0-.422 0l-7.5 3.5a.5.5 0 0 0 .025.917l7.5 3 7.5-3a.5.5 0 0 0 .025-.917l-7.5-3.5Z"/><path d="M4.176 9.032a.5.5 0 0 0-.656.327l-.5 1.7a.5.5 0 0 0 .254.539l1.5.75A.5.5 0 0 0 5.25 12h5.5a.5.5 0 0 0 .476-.346l.5-1.7a.5.5 0 0 0-.656-.327L10 10.25l-.117-.043-4 .876L4.176 9.032Z"/></svg>'
svg_warning = '<svg viewBox="0 0 16 16"><path d="M8.982 1.566a1.13 1.13 0 0 0-1.96 0L.165 13.233c-.457.778.091 1.767.98 1.767h13.713c.889 0 1.438-.99.98-1.767L8.982 1.566zM8 5c.535 0 .954.462.9.995l-.35 3.507a.552.552 0 0 1-1.1 0L7.1 5.995A.905.905 0 0 1 8 5zm.002 6a1 1 0 1 1 0 2 1 1 0 0 1 0-2z"/></svg>'
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
    except:
        return pd.DataFrame(), pd.DataFrame()

data_wilayah, data_sekolah = load_all_data()

# =========================
# Bagian 3: LOGIN
# =========================
if not st.session_state.login:
    _, col_card, _ = st.columns([1.5, 2, 1.5])
    with col_card:
        with st.container(border=True):
            if os.path.exists("logo_sipandai.png"): st.image("logo_sipandai.png", use_container_width=True)
            st.markdown("<h3 style='text-align:center; color:#0d47a1;'>LOGIN USER</h3>", unsafe_allow_html=True)
            u = st.text_input("Username", placeholder="Username", label_visibility="collapsed")
            p = st.text_input("Password", type="password", placeholder="Password", label_visibility="collapsed")
            if st.button("MASUK KE DASHBOARD", use_container_width=True):
                if u == "admin" and p == "admin":
                    st.session_state.login = True
                    st.rerun()
                else:
                    st.error("Login Gagal")
    st.stop()

# ==================================
# Bagian 4: SIDEBAR
# ==================================
with st.sidebar:
    logo_b64 = get_base64_image("logo_sumut.png")
    if logo_b64:
        st.markdown(f'<div style="display:flex;align-items:center;gap:12px;padding-bottom:15px;"><img src="data:image/png;base64,{logo_b64}" width="45"><span style="font-size:18px;font-weight:800;color:white;">SI-PANDAI SUMUT</span></div>', unsafe_allow_html=True)
    
    st.write("👤Role: **Administrator**")
  
    # Tombol Admin Tanpa Kotak Putih
    if st.button("👤Role: **Administrator**", key="admin_sidebar_btn", use_container_width=True):
        st.session_state.page_view = "admin_profile"
        st.rerun()
    
    st.divider()
    # ... navigasi menu lainnya ...

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
    # Fixed Logout Button (Tanpa IF di depan)
    st.button("Logout 🚪", key="logout_btn", on_click=proses_logout, use_container_width=True)

# ==================================
# Bagian 5: HEADER & ISI KONTEN
# ==================================

st.markdown("<h2 style='text-align:right; color:#0d47a1; font-weight:800; margin-top:5px;'>OVERVIEW SI-PANDAI SUMUT</h2>", unsafe_allow_html=True)
st.divider()

# --- LOGIKA HALAMAN ---

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
    with m3: draw_tile_svg("Anak Tidak Sekolah", val_a, svg_warning, "tile-navy")
    with m4: draw_tile_svg("Angka Partisipasi", val_APS, svg_chart, "tile-green")

    if kab_pilih != "Semua":
        st.divider()
        st.subheader(f"🏫 Sekolah di {kab_pilih}")
        sch_wil = data_sekolah[data_sekolah[col_kab] == kab_pilih] if not data_sekolah.empty else pd.DataFrame()
        if not sch_wil.empty:
            cols = st.columns(3)
            for i, row in enumerate(sch_wil.itertuples()):
                with cols[i % 3]:
                    with st.container(border=True):
                        st.button(row.nama_sekolah.upper(), key=f"btn_{i}")
                        st.caption(f"NPSN: {row.npsn}")

    st.divider()
    c1, c2 = st.columns([1.5, 1])
    with c1:
        st.subheader("🗺️ Peta Wilayah")
        if not df_f.empty: st.map(df_f)
    with c2:
        st.subheader("📊 Statistik")
        if not df_f.empty: st.plotly_chart(px.bar(df_f.head(10), x=df_f.columns[3], y=col_kab, orientation='h'), use_container_width=True)

# 2. PROFIL ADMIN
elif st.session_state.page_view == "admin_profile":
    st.markdown("### 👤 Data Administrator")
    with st.container(border=True):
        col_admin_l, col_admin_r = st.columns([1, 4])
        with col_admin_l:
            st.markdown("<h1 style='text-align:center; font-size:100px; color:#0d47a1;'>👤</h1>", unsafe_allow_html=True)
        with col_admin_r:
            st.markdown("### Super Admin SI-PANDAI")
            st.write("**NIP:** 198807012010121001")
            st.write("**Instansi:** Bidang Pendidikan Khusus Provsu")
            st.write("**Email:** admin.pk@sumutprov.go.id")
            st.caption("Akses Level: Full Access")
    
    if st.button("⬅️ Kembali ke Dashboard"):
        st.session_state.page_view = "dashboard"
        st.rerun()

# 3. HALAMAN LAINNYA
elif st.session_state.page_view == "tentang_pk":
    st.title("🎓 Pendidikan Khusus")
    st.write("Informasi mengenai Pendidikan Khusus Sumatera Utara.")

elif st.session_state.page_view == "tentang_dashboard":
    st.title("ℹ️ Tentang SI-PANDAI")
    st.write("Sistem Informasi Analitik Pendidikan Khusus.")
