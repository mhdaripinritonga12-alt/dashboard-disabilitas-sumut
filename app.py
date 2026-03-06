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
    page_title="Halaman Login SI-PANDAI SUMUT",
    layout="wide",
    page_icon="🔒"
)

# ==================================
# Bagian 1: STYLE LOGIN (CSS Khusus)
# ==================================
# Bagian ini mengatur estetika kartu login, gradasi, posisi logo, dan tombol teal.
st.markdown("""
<style>
    /* Reset padding default Streamlit agar konten lebih rapi */
    .block-container {
        padding-top: 0rem;
        padding-bottom: 0rem;
        padding-left: 0rem;
        padding-right: 0rem;
    }

    /* Memastikan latar belakang halaman utama berwarna abu-abu sangat muda/bersih */
    [data-testid="stAppViewContainer"] {
        background-color: #F8F9FA;
    }

    /* --- CONTAINER UTAMA LOGIN --- */
    /* Membuat konten login berada di tengah-tengah layar secara vertikal & horizontal */
    .login-main-container {
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 100vh; /* Memenuhi tinggi layar */
        flex-direction: column; /* Menyusun elemen secara vertikal (Logo Sumut, Kartu, Info) */
    }

    /* --- INFO HEADER (DI LUAR KARTU) --- */
    /* Tempat Logo Pemprov Sumut berada */
    .info-header {
        text-align: center;
        margin-bottom: 30px; /* Jarak dari kartu login */
    }

    /* --- KARTU LOGIN UTAMA --- */
    /* Mengatur ukuran dan tampilan kartu login */
    .login-card {
        width: 380px; /* Ukuran kartu yang proporsional */
        background-color: white;
        border-radius: 12px; /* Sudut halus */
        box-shadow: 0px 8px 25px rgba(0,0,0,0.08); /* Bayangan lembut */
        overflow: hidden; /* Memastikan header gradasi mengikuti bentuk border-radius kartu */
        border: 1px solid #EAEAEA; /* Border tipis */
        text-align: center;
    }

    /* --- HEADER KARTU GRADASI (Teal ke Gelap) --- */
    .login-header-gradient {
        background: linear-gradient(135deg, #1D976C 0%, #073642 100%); /* Gradasi sesuai gambar */
        padding: 25px 20px; /* Padding vertikal */
        color: white;
    }

    .login-header-title {
        font-size: 22px; /* Ukuran font disesuaikan */
        font-weight: 800; /* Sangat tebal */
        letter-spacing: 1px; /* Jarak antar huruf */
        margin: 0;
        text-transform: uppercase; /* Huruf besar semua */
    }

    .login-header-subtitle {
        font-size: 14px;
        font-weight: 600;
        margin-top: 4px;
        opacity: 0.9;
    }

    /* --- KONTEN FORM LOGIN (Area Putih) --- */
    /* Area tempat Logo SI-PANDAI dan Input berada */
    .login-form-content {
        padding: 30px 30px 35px 30px; /* Padding yang luas */
    }

    /* --- LOGO SI-PANDAI (DI DALAM KARTU) --- */
    .login-card-logo-container {
        text-align: center;
        margin-bottom: 25px; /* Jarak dari input fields */
    }

    /* --- STYLING INPUT & TOMBOL (Aksen Teal) --- */
    /* Mengubah warna fokus input field menjadi Teal */
    div[data-testid="stTextInput"] > div > div > input:focus {
        border-color: #1D976C;
        box-shadow: 0 0 0 0.15rem rgba(29, 151, 108, 0.20);
    }

    /* Mengubah warna tombol LOGIN menjadi warna tema (Teal) */
    div.stButton > button {
        background-color: #1D976C; /* Warna Teal Solid */
        color: white;
        border-radius: 6px; /* Sudut tombol lebih halus */
        padding: 10px 20px;
        font-weight: 700;
        border: none;
        width: 100%;
        transition: all 0.3s ease; /* Efek transisi halus */
    }
    
    div.stButton > button:hover {
        background-color: #147a57; /* Warna lebih gelap saat hover */
        border: none;
        color: white;
    }

    /* Teks 'Forgot Password' */
    .forgot-password {
        text-align: right;
        font-size: 13px;
        color: #1D976C;
        margin-top: -10px;
        margin-bottom: 18px;
    }

    /* --- INFO TEKS & FOOTER (Luar Kartu) --- */
    .info-text-container {
        text-align: center;
        margin-top: 25px;
        color: #666; /* Warna teks info */
        font-size: 13px;
        line-height: 1.5;
    }

    .page-footer {
        text-align: center;
        color: #888;
        padding: 15px 0;
        font-size: 11px;
        margin-top: 40px;
    }

</style>
""", unsafe_allow_html=True)

# ==================================
# Bagian 2: LOAD DATA & USERS
# ==================================
# GANTI DENGAN PATH FILE EXCEL ANDA YANG SEBENARNYA
FILE_PATH = "KOTA_MEDAN_LENGKAP_KELURAHAN_DISABILITAS.xlsx" 

@st.cache_data
def load_data():
    if not os.path.exists(FILE_PATH):
        st.error(f"File '{FILE_PATH}' tidak ditemukan. Silakan periksa path file Excel Anda.")
        return pd.DataFrame() # Kembalikan dataframe kosong jika file tidak ada
    return pd.read_excel(FILE_PATH, sheet_name="KOTA_MEDAN_LENGKAP_KELURAHAN_DISABILITAS")

@st.cache_data
def load_users():
    if not os.path.exists(FILE_PATH):
        return pd.DataFrame()
    return pd.read_excel(FILE_PATH, sheet_name="users")

data = load_data()
users = load_users()

# ==================================
# Bagian 3: SESSION LOGIN
# ==================================
if "login" not in st.session_state:
    st.session_state.login = False
    st.session_state.role = ""

# ==================================
# Bagian 4: HALAMAN LOGIN (Kartu)
# ==================================
if not st.session_state.login:

    # Menempatkan seluruh konten login di dalam container utama agar berada di tengah halaman
    st.markdown('<div class="login-main-container">', unsafe_allow_html=True)
    
    # --- 1. Info Header (Luar Kartu - Logo Sumut) ---
    st.markdown('<div class="info-header">', unsafe_allow_html=True)
    try:
        # Mencoba memuat Logo Pemprov Sumut
        logo_pemprov = Image.open("logo_sumut.png") 
        st.image(logo_pemprov, width=70) # Ukuran logo disesuaikan
    except FileNotFoundError:
        st.warning("File 'logo_sumut.png' tidak ditemukan. Letakkan file logo di folder yang sama.")
    st.markdown('</div>', unsafe_allow_html=True)

    # --- 2. Kartu Login Utama ---
    st.markdown('<div class="login-card">', unsafe_allow_html=True)

    # A. Header Gradasi (Sesuai Gambar)
    st.markdown("""
        <div class="login-header-gradient">
            <div class="login-header-title">LOGIN USER</div>
            <div class="login-header-subtitle">SI-PANDAI SUMUT</div>
        </div>
    """, unsafe_allow_html=True)

    # B. Konten Form (Area Putih)
    st.markdown('<div class="login-form-content">', unsafe_allow_html=True)
    
    # Mencoba memuat Logo SI-PANDAI (Di dalam kartu)
    st.markdown('<div class="login-card-logo-container">', unsafe_allow_html=True)
    try:
        logo_sipandai = Image.open("logo_sipandai.png") 
        st.image(logo_sipandai, width=65) # Ukuran logo disesuaikan
    except FileNotFoundError:
        st.warning("File 'logo_sipandai.png' tidak ditemukan. Letakkan file logo di folder yang sama.")
    st.markdown('</div>', unsafe_allow_html=True)

    # Input Fields menggunakan Streamlit natif
    username = st.text_input("👤 Username", placeholder="Masukkan Username Anda")
    password = st.text_input("🔑 Password", type="password", placeholder="Masukkan Password Anda")
    
    # Teks 'Forgot Password' (Dummy)
    st.markdown('<div class="forgot-password"><a href="#" style="color: #1D976C; text-decoration: none;">Forgot Password?</a></div>', unsafe_allow_html=True)

    # Tombol LOGIN
    if st.button("LOGIN", use_container_width=True):
        if users.empty:
            st.error("Data pengguna tidak tersedia.")
        else:
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

    st.markdown('</div>', unsafe_allow_html=True) # Menutup login-form-content
    st.markdown('</div>', unsafe_allow_html=True) # Menutup login-card

    # --- 3. Info Teks di Bawah Kartu ---
    st.markdown("""
        <div class="info-text-container">
            <div>Sistema Informasion Pensissiaan SI-Pandai Sumut</div>
            <div>Pengatururaan Dengnan SI-Pandai Sumut</div>
        </div>
    """, unsafe_allow_html=True)

    # --- 4. Footer Halaman ---
    st.markdown("""
        <div class="page-footer">
            © 2024 Dinas Pendidikan Provinsi Sumatera Utara
        </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True) # Menutup login-main-container

    st.stop() # Menghentikan eksekusi kode dashboard di bawahnya jika belum login


# SIDEBAR
# =========================
st.sidebar.title("📂 Menu")

menu = st.sidebar.radio(
    "Pilih Menu",
    ["Home"]
)

st.sidebar.divider()

# =========================
# FILTER WILAYAH
# =========================
st.sidebar.header("🔎 Filter Wilayah")

kabkota = st.sidebar.selectbox(
    "Pilih Kabupaten / Kota",
    ["Semua"] + sorted(data["kab_kota"].unique())
)

df = data.copy()

if kabkota != "Semua":
    df = df[df["kab_kota"] == kabkota]

# =========================
# HEADER
# =========================
st.title("📊 Dashboard Sebaran Penyandang Disabilitas")
st.subheader("Provinsi Sumatera Utara")

st.write(f"👤 Role: **{st.session_state.role}**")

if st.button("Logout"):
    st.session_state.login = False
    st.session_state.role = ""
    st.rerun()

st.divider()

# =========================
# REKAP CEPAT
# =========================
col1, col2, col3 = st.columns(3)

col1.metric("Jumlah Data", len(df))
col2.metric("Jumlah Kabupaten/Kota", df["kab_kota"].nunique())
col3.metric("Jumlah Jenis Disabilitas", df["jenis_disabilitas"].nunique())

st.divider()

# =========================
# REKAP PER JENIS
# =========================
st.subheader("📌 Rekap Penyandang per Jenis Disabilitas")

rekap = df.groupby("jenis_disabilitas").size().reset_index(name="Jumlah")

st.dataframe(rekap, use_container_width=True)

# =========================
# GRAFIK
# =========================
st.subheader("📈 Grafik Penyandang Disabilitas")

fig_bar = px.bar(
    rekap,
    x="jenis_disabilitas",
    y="Jumlah",
    title="Jumlah Penyandang Disabilitas per Jenis"
)

st.plotly_chart(fig_bar, use_container_width=True)

fig_pie = px.pie(
    rekap,
    values="Jumlah",
    names="jenis_disabilitas",
    title="Distribusi Jenis Disabilitas"
)

st.plotly_chart(fig_pie, use_container_width=True)

# =========================
# PETA
# =========================
st.divider()
st.subheader("🗺️ Peta Sebaran Penyandang Disabilitas (Kab/Kota)")

map_data = (
    df.groupby("kab_kota")
    .size()
    .reset_index(name="Jumlah")
)

peta_kab = {
    "Kota Medan": [3.5952, 98.6722],
    "Kab. Deli Serdang": [3.4200, 98.9800],
    "Kab. Langkat": [3.7000, 98.2000],
}

map_rows = []

for k, v in peta_kab.items():

    jumlah = map_data.loc[
        map_data["kab_kota"] == k,
        "Jumlah"
    ]

    if not jumlah.empty:

        map_rows.append({
            "lat": v[0],
            "lon": v[1],
            "jumlah": int(jumlah.values[0])
        })

if map_rows:

    map_df = pd.DataFrame(map_rows)

    st.map(
        map_df,
        latitude="lat",
        longitude="lon",
        size="jumlah"
    )

else:

    st.info("Data peta belum tersedia")

# =========================
# DETAIL DATA
# =========================
st.divider()
st.subheader("📋 Detail Data Penyandang Disabilitas")

jenis_pilih = st.selectbox(
    "Pilih Jenis Disabilitas",
    ["Semua"] + sorted(df["jenis_disabilitas"].unique())
)

if jenis_pilih != "Semua":
    df_detail = df[df["jenis_disabilitas"] == jenis_pilih]
else:
    df_detail = df

st.dataframe(
    df_detail[
        ["nama", "jenis_disabilitas", "kab_kota"]
    ],
    use_container_width=True
)

# =========================
# DOWNLOAD DATA
# =========================
st.divider()
st.subheader("⬇️ Download Data")

if st.session_state.role in ["admin", "operator"]:

    output = BytesIO()

    df.to_excel(
        output,
        index=False,
        engine="openpyxl"
    )

    output.seek(0)

    st.download_button(
        label="Download Excel",
        data=output,
        file_name="rekap_disabilitas_filtered.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

else:
    st.info("Role viewer tidak memiliki hak download")

# =========================
# ROLE INFO
# =========================
st.divider()

st.caption("""
Role:
- Admin    : Semua akses
- Operator : Lihat & Download
- Viewer   : Lihat saja
""")



