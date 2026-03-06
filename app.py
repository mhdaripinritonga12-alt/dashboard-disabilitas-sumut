import streamlit as st
import pandas as pd
from PIL import Image
import os
from io import BytesIO
import plotly.express as px

# ==================================
# 0. KONFIGURASI HALAMAN
# ==================================
st.set_page_config(
    page_title="SI-PANDAI SUMUT - Login",
    layout="wide",
    page_icon="🔒"
)

# ==================================
# 1. STYLE CSS (GLASSMORPHISM & BACKGROUND)
# ==================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&display=swap');
    
    html, body, [data-testid="stWidgetLabel"] {
        font-family: 'Inter', sans-serif !important;
    }

    /* BACKGROUND PEMANDANGAN DANAU TOBA DENGAN OVERLAY */
    [data-testid="stAppViewContainer"] {
        background-image: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)), 
                          url("https://images.unsplash.com/photo-1571746243149-6012b84299ec?q=80&w=2000&auto=format&fit=crop");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    /* Menghilangkan Header Default Streamlit */
    header {visibility: hidden;}

    /* KARTU LOGIN: GLASSMORPHISM (PUTIH SEMI-TRANSPARAN) */
    [data-testid="stVerticalBlockBorderWrapper"] > div {
        background: rgba(255, 255, 255, 0.15) !important;
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        border-radius: 25px !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        padding: 40px !important;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.5) !important;
    }

    /* WADAH LOGO APLIKASI DI DALAM KARTU (SEMI-TRANSPARAN) */
    .logo-app-box {
        background: rgba(255, 255, 255, 0.1);
        padding: 20px;
        border-radius: 20px;
        display: flex;
        justify-content: center;
        align-items: center;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 10px;
    }

    /* TIPOGRAFI LOGIN */
    .login-header-text {
        color: #ffffff !important;
        font-size: 28px !important;
        font-weight: 800 !important;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.5);
        margin-bottom: 0px;
    }
    
    .login-subheader-text {
        color: #00e5ff !important;
        font-size: 14px !important;
        font-weight: 700;
        margin-bottom: 30px !important;
        letter-spacing: 1px;
    }

    /* INPUT FIELD DENGAN BACKGROUND BERSIH */
    div[data-testid="stTextInput"] input {
        background-color: rgba(255, 255, 255, 0.95) !important;
        border-radius: 12px !important;
        border: none !important;
        height: 48px !important;
        color: #222 !important;
    }

    /* TOMBOL LOGIN BIRU GRADASI */
    div.stButton > button {
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%) !important;
        color: white !important;
        border-radius: 12px !important;
        font-weight: 800 !important;
        height: 50px;
        border: none !important;
        width: 100%;
        margin-top: 15px;
        text-transform: uppercase;
        box-shadow: 0px 5px 15px rgba(30, 60, 114, 0.4);
    }
    
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0px 8px 25px rgba(30, 60, 114, 0.6);
    }

    /* LOGO SUMUT CONTAINER */
    .logo-sumut-center {
        display: flex;
        justify-content: center;
        padding-top: 40px;
        padding-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# ==================================
# 2. LOGIKA DATA & SESSION
# ==================================
EXCEL_FILE = "KOTA_MEDAN_LENGKAP_KELURAHAN_DISABILITAS.xlsx"

@st.cache_data
def load_data():
    try:
        return pd.read_excel(EXCEL_FILE, sheet_name="data_disabilitas")
    except Exception:
        return pd.DataFrame()

@st.cache_data
def load_users():
    try:
        return pd.read_excel(EXCEL_FILE, sheet_name="users")
    except Exception:
        # Fallback admin jika file tidak ditemukan
        return pd.DataFrame([{"username": "admin", "password": "admin", "role": "admin"}])

df_raw = load_data()
df_users = load_users()

if "login" not in st.session_state:
    st.session_state.login = False
    st.session_state.role = ""

# ==================================
# 3. HALAMAN LOGIN
# ==================================
if not st.session_state.login:
    
    # Logo Sumut di Tengah Atas (Besar)
    st.markdown('<div class="logo-sumut-center">', unsafe_allow_html=True)
    col_t1, col_t2, col_t3 = st.columns([2, 0.4, 2])
    with col_t2:
        if os.path.exists("logo_sumut.png"):
            st.image(Image.open("logo_sumut.png"), width=110)
    st.markdown('</div>', unsafe_allow_html=True)

    # Kotak Login Glassmorphism
    _, col_card, _ = st.columns([1.2, 2.8, 1.2]) 
    with col_card:
        with st.container(border=True):
            col_l, col_r = st.columns([1, 1.4])

            with col_l:
                # Logo SI-PANDAI di dalam kotak transparan kiri
                st.markdown('<div class="logo-app-box">', unsafe_allow_html=True)
                if os.path.exists("logo_sipandai.png"):
                    st.image(Image.open("logo_sipandai.png"), use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)

            with col_r:
                st.markdown('<div class="login-header-text">LOGIN USER</div>', unsafe_allow_html=True)
                st.markdown('<div class="login-subheader-text">SI-PANDAI SUMUT</div>', unsafe_allow_html=True)
                
                # Input Username & Password dengan Ikon Placeholder
                user_input = st.text_input("Username", placeholder="👤  Masukkan Username", label_visibility="collapsed")
                pass_input = st.text_input("Password", type="password", placeholder="🔑  Masukkan Password", label_visibility="collapsed")
                
                if st.button("MASUK SISTEM"):
                    match = df_users[(df_users["username"] == user_input) & (df_users["password"] == pass_input)]
                    if not match.empty:
                        st.session_state.login = True
                        st.session_state.role = match.iloc[0]["role"]
                        st.rerun()
                    else:
                        st.error("Username atau Password Salah")

    st.markdown('<p style="text-align:center; color:rgba(255,255,255,0.6); font-size:12px; margin-top:30px; font-weight:700;">DINAS PENDIDIKAN PROVINSI SUMATERA UTARA © 2026</p>', unsafe_allow_html=True)
    st.stop()

# ==================================
# 4. HALAMAN DASHBOARD (SETELAH LOGIN)
# ==================================

# --- SIDEBAR ---
st.sidebar.title("SI-PANDAI SUMUT")
st.sidebar.write(f"Login sebagai: **{st.session_state.role.upper()}**")
st.sidebar.divider()

if not df_raw.empty:
    kab_list = ["Semua"] + sorted(df_raw["kab_kota"].unique().tolist())
    kab_select = st.sidebar.selectbox("Filter Wilayah", kab_list)
    
    df_filtered = df_raw.copy()
    if kab_select != "Semua":
        df_filtered = df_filtered[df_filtered["kab_kota"] == kab_select]
else:
    df_filtered = pd.DataFrame()

if st.sidebar.button("Keluar / Logout"):
    st.session_state.login = False
    st.rerun()

# --- MAIN DASHBOARD ---
st.title("📊 Dashboard SI-PANDAI SUMUT")
st.subheader("Sistem Informasi Pemetaan Anak Tidak Sekolah Disabilitas")
st.divider()

if not df_filtered.empty:
    # Metrik Utama
    m1, m2, m3 = st.columns(3)
    m1.metric("Total ATS Disabilitas", len(df_filtered))
    m2.metric("Wilayah (Kab/Kota)", df_filtered["kab_kota"].nunique())
    m3.metric("Kategori Disabilitas", df_filtered["jenis_disabilitas"].nunique())

    st.divider()

    # Visualisasi
    col_v1, col_v2 = st.columns(2)
    with col_v1:
        st.write("### Distribusi Jenis Disabilitas")
        rekap_jenis = df_filtered.groupby("jenis_disabilitas").size().reset_index(name="Jumlah")
        fig_pie = px.pie(rekap_jenis, values="Jumlah", names="jenis_disabilitas", hole=0.4)
        st.plotly_chart(fig_pie, use_container_width=True)

    with col_v2:
        st.write("### Angka ATS per Wilayah")
        rekap_wilayah = df_filtered.groupby("kab_kota").size().reset_index(name="Jumlah")
        fig_bar = px.bar(rekap_wilayah, x="kab_kota", y="Jumlah", color="Jumlah", color_continuous_scale="Viridis")
        st.plotly_chart(fig_bar, use_container_width=True)

    # Tabel Detail
    st.divider()
    st.write("### Detail Data")
    st.dataframe(df_filtered, use_container_width=True)
else:
    st.info("Data belum tersedia atau filter tidak menemukan hasil.")
