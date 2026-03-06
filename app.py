import streamlit as st
import pandas as pd
from PIL import Image
import os
from io import BytesIO
import plotly.express as px

# ==================================
# Bagian 0: KONFIGURASI HALAMAN
# ==================================
st.set_page_config(
    page_title="Dashboard Disabilitas Sumut",
    layout="wide",
    page_icon="🔒"
)

# ==================================
# Bagian 1: STYLE LOGIN (CSS Khusus)
# ==================================
st.markdown("""
<style>
    /* Reset & Background */
    .block-container {
        padding-top: 2rem;
    }
    [data-testid="stAppViewContainer"] {
        background-color: #f4f7f6;
    }

    /* CONTAINER UTAMA */
    .login-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }

    /* LOGO SUMUT (DI LUAR KARTU) */
    .logo-sumut-top {
        margin-bottom: 20px;
        text-align: center;
    }

    /* KARTU LOGIN */
    .login-card {
        width: 380px;
        background-color: white;
        border-radius: 15px;
        box-shadow: 0px 10px 30px rgba(0,0,0,0.1);
        overflow: hidden; /* Agar header gradasi mengikuti radius kartu */
        border: 1px solid #eaeaea;
    }

    /* HEADER GRADASI (Sesuai Gambar) */
    .login-header-gradient {
        background: linear-gradient(135deg, #1D976C 0%, #073642 100%);
        padding: 25px;
        color: white;
        text-align: center;
    }
    .login-header-gradient h2 {
        margin: 0;
        font-size: 22px;
        font-weight: 800;
        letter-spacing: 1px;
    }
    .login-header-gradient p {
        margin: 5px 0 0 0;
        font-size: 14px;
        opacity: 0.9;
    }

    /* FORM CONTENT (AREA PUTIH) */
    .login-form-content {
        padding: 30px;
        text-align: center;
    }

    /* LOGO SI-PANDAI (DI DALAM KARTU) */
    .logo-app-inside {
        margin-bottom: 20px;
    }

    /* BUTTON LOGIN */
    div.stButton > button {
        background-color: #1D976C;
        color: white;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 700;
        border: none;
        width: 100%;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        background-color: #147a57;
        color: white;
    }

    /* INPUT STYLE */
    div[data-testid="stTextInput"] > div > div > input {
        border-radius: 8px;
    }

    /* FOOTER TEKS */
    .info-footer {
        text-align: center;
        margin-top: 20px;
        color: #666;
        font-size: 13px;
        line-height: 1.4;
    }
</style>
""", unsafe_allow_html=True)

# =========================
# LOAD DATA (Tetap Sama)
# =========================
@st.cache_data
def load_data():
    return pd.read_excel(
        "KOTA_MEDAN_LENGKAP_KELURAHAN_DISABILITAS.xlsx",
        sheet_name="data_disabilitas"
    )

@st.cache_data
def load_users():
    return pd.read_excel(
        "KOTA_MEDAN_LENGKAP_KELURAHAN_DISABILITAS.xlsx",
        sheet_name="users"
    )

data = load_data()
users = load_users()

# =========================
# SESSION LOGIN
# =========================
if "login" not in st.session_state:
    st.session_state.login = False
    st.session_state.role = ""

# ==================================
# Bagian 4: HALAMAN LOGIN (KARTU)
# ==================================
if not st.session_state.login:

    # Gunakan Kolom untuk menengahkan
    _, col_main, _ = st.columns([1, 2, 1])

    with col_main:
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        
        # 1. LOGO SUMUT (Di luar kartu)
        st.markdown('<div class="logo-sumut-top">', unsafe_allow_html=True)
        if os.path.exists("logo_sumut.png"):
            st.image(Image.open("logo_sumut.png"), width=70)
        st.markdown('</div>', unsafe_allow_html=True)

        # 2. MULAI KARTU LOGIN
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        
        # A. Header Gradasi
        st.markdown("""
            <div class="login-header-gradient">
                <h2>LOGIN USER</h2>
                <p>SI-PANDAI SUMUT</p>
            </div>
        """, unsafe_allow_html=True)

        # B. Konten Form (Area Putih)
        st.markdown('<div class="login-form-content">', unsafe_allow_html=True)
        
        # Logo SI-PANDAI (Di dalam kartu)
        if os.path.exists("logo_sipandai.png"):
            st.image(Image.open("logo_sipandai.png"), width=80)
        
        # Input Streamlit (akan otomatis masuk ke dalam div karena urutan kode)
        username = st.text_input("👤 Username", placeholder="Username")
        password = st.text_input("🔑 Password", type="password", placeholder="Password")
        
        st.markdown('<div style="margin-top:20px;">', unsafe_allow_html=True)
        if st.button("LOGIN", use_container_width=True):
            user = users[
                (users["username"] == username) & 
                (users["password"] == password)
            ]
            if not user.empty:
                st.session_state.login = True
                st.session_state.role = user.iloc[0]["role"]
                st.rerun()
            else:
                st.error("Username atau password salah")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True) # Tutup form-content
        st.markdown('</div>', unsafe_allow_html=True) # Tutup login-card

        # 3. Teks Info Bawah
        st.markdown("""
            <div class="info-footer">
                Sistema Informasion Pensissiaan SI-Pandai Sumut<br>
                © 2024 Dinas Pendidikan Provinsi Sumatera Utara
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True) # Tutup login-container

    st.stop()

# ==================================
# DASHBOARD (DI BAWAH SINI TIDAK BERUBAH)
# ==================================
st.sidebar.title("📂 Menu")
menu = st.sidebar.radio("Pilih Menu", ["Home"])
st.sidebar.divider()

# ... (Sisa kode Anda diteruskan di sini tanpa ada perubahan)
st.sidebar.header("🔎 Filter Wilayah")
kabkota = st.sidebar.selectbox("Pilih Kabupaten / Kota", ["Semua"] + sorted(data["kab_kota"].unique()))

df = data.copy()
if kabkota != "Semua":
    df = df[df["kab_kota"] == kabkota]

st.title("📊 Dashboard Sebaran Penyandang Disabilitas")
st.subheader("Provinsi Sumatera Utara")
st.write(f"👤 Role: **{st.session_state.role}**")

if st.button("Logout"):
    st.session_state.login = False
    st.session_state.role = ""
    st.rerun()

st.divider()
# ... dst (lanjutkan rekap cepat, grafik, peta, dan detail data seperti kode asli Anda)
