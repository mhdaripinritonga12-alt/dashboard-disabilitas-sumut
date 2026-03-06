import streamlit as st
import pandas as pd
from io import BytesIO
import plotly.express as px
from PIL import Image
import os

# Konfigurasi Halaman (Sudah benar di kode Anda, tetap sertakan)
st.set_page_config(
    page_title="Dashboard Disabilitas Sumut",
    layout="wide",
    page_icon="📊" # Menambahkan favicon
)

# ==================================
# Bagian 1: STYLE LOGIN (PERBAIKAN UTAMA)
# ==================================
# Bagian CSS ini berfokus untuk membuat header kartu login berwarna gradasi gelap
# dan elemen lainnya berwarna teal, sesuai gambar contoh.
st.markdown("""
<style>
    /* 1. Reset & Layout Dasar */
    /* Menghilangkan padding default Streamlit bagian atas agar konten lebih naik */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 0rem;
    }

    /* Memastikan latar belakang halaman utama berwarna putih bersih/abu sangat muda */
    [data-testid="stAppViewContainer"] {
        background-color: #F8F9FA;
    }

    /* --- KARTU LOGIN --- */
    /* Container utama untuk memposisikan kartu login di tengah halaman secara vertikal & horizontal */
    .login-card-container {
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 80vh; /* Mengisi 80% tinggi layar untuk menengahkan */
    }

    /* Desain Kartu Login Utama */
    .login-card {
        width: 450px; /* Sedikit lebih lebar dari kode lama agar tidak sesak */
        background-color: white;
        border-radius: 15px; /* Sudut lebih halus/membulat */
        box-shadow: 0px 10px 30px rgba(0,0,0,0.1); /* Bayangan lebih lembut dan elegan */
        overflow: hidden; /* Penting! Agar header gradasi mengikuti bentuk border-radius kartu */
        border: 1px solid #EAEAEA; /* Border tipis abu-abu */
        text-align: center; /* Perataan teks tengah default untuk konten di dalamnya */
    }

    /* --- HEADER KARTU LOGIN (PERBAIKAN SESUAI GAMBAR) --- */
    /* Bagian ini menciptakan area berwarna gradasi gelap di bagian atas kartu */
    .login-header-gradient {
        background: linear-gradient(135deg, #1D976C 0%, #073642 100%); /* Gradasi Teal ke Biru Tua/Gelap */
        padding: 30px 20px; /* Padding vertikal yang cukup */
        color: white; /* Semua teks di dalam header ini berwarna putih */
    }

    /* Teks 'LOGIN USER' di dalam header gradasi */
    .login-header-title {
        font-size: 24px;
        font-weight: 800; /* Sangat tebal */
        letter-spacing: 1px; /* Jarak antar huruf */
        margin: 0;
        text-transform: uppercase; /* Huruf besar semua */
    }

    /* Teks 'SI-PANDAI SUMUT' di dalam header gradasi */
    .login-header-subtitle {
        font-size: 16px;
        font-weight: 600;
        margin-top: 5px; /* Jarak dari judul atas */
        opacity: 0.9; /* Sedikit transparan agar tidak terlalu mencolok dibanding judul */
    }

    /* --- KONTEN FORM LOGIN --- */
    /* Area form di dalam kartu, di bawah header gradasi, berwarna latar putih */
    .login-form-content {
        padding: 40px 35px; /* Padding yang luas agar form tidak berdesakan */
    }

    /* --- STYLING INPUT & TOMBOL (Aksen Teal) --- */
    /* Mengubah warna border input field (Username/Password) saat fokus/aktif menjadi Teal */
    div[data-testid="stTextInput"] > div > div > input:focus {
        border-color: #1D976C;
        box-shadow: 0 0 0 0.2rem rgba(29, 151, 108, 0.25);
    }

    /* Mengubah warna tombol LOGIN menjadi warna tema (Teal) */
    div.stButton > button {
        background-color: #1D976C; /* Warna Teal Solid */
        color: white;
        border-radius: 8px;
        padding: 12px 20px;
        font-weight: 700;
        border: none;
        width: 100%;
        transition: all 0.3s ease; /* Efek transisi halus saat hover */
    }
    
    /* Efek hover tombol LOGIN (Teal lebih gelap) */
    div.stButton > button:hover {
        background-color: #147a57; 
        border: none;
        color: white;
    }

    /* Teks 'Forgot Password' (Dummy) */
    .forgot-password {
        text-align: right;
        font-size: 14px;
        color: #1D976C; /* Warna Teal */
        margin-top: -10px; /* Menaikkan sedikit agar dekat dengan input password */
        margin-bottom: 20px;
    }

    /* --- INFO HEADER & FOOTER (Luar Kartu) --- */
    /* Area logo di luar kartu login */
    .info-header {
        text-align: center;
        margin-bottom: 30px;
    }

    /* Info teks di bawah login form */
    .info-text-container {
        text-align: center;
        margin-top: 30px;
        color: #555;
        font-size: 14px;
        line-height: 1.6;
    }

</style>
""", unsafe_allow_html=True)

# =========================
# Bagian 2: Load Data & Users (Sama seperti kode Anda)
# =========================
# GANTI DENGAN PATH FILE ANDA YANG SEBENARNYA
FILE_PATH = "KOTA_MEDAN_LENGKAP_KELURAHAN_DISABILITAS.xlsx" 

@st.cache_data
def load_data():
    if not os.path.exists(FILE_PATH):
        st.error(f"File '{FILE_PATH}' tidak ditemukan. Periksa path file Anda.")
        return pd.DataFrame()
    return pd.read_excel(FILE_PATH, sheet_name="data_disabilitas")

@st.cache_data
def load_users():
    if not os.path.exists(FILE_PATH):
        return pd.DataFrame()
    return pd.read_excel(FILE_PATH, sheet_name="users")

data = load_data()
users = load_users()

# =========================
# Bagian 3: Session Login (Sama seperti kode Anda)
# =========================
if "login" not in st.session_state:
    st.session_state.login = False
    st.session_state.role = ""

# ==================================
# Bagian 4: HALAMAN LOGIN (PERBAIKAN STRUKTUR HTML)
# ==================================
if not st.session_state.login:

    # Menempatkan seluruh konten login di dalam container agar berada di tengah
    st.markdown('<div class="login-card-container">', unsafe_allow_html=True)
    
    # Membuat kolom untuk memposisikan kartu di tengah secara horizontal
    col_left, col_main, col_right = st.columns([1, 2.5, 1])

    with col_main:
        # 1. Info Header (Logo Pemprov Sumut - Di luar kartu)
        st.markdown('<div class="info-header">', unsafe_allow_html=True)
        # GANTI DENGAN NAMA FILE LOGO PEMPROV ANDA
        try:
            logo_pemprov = Image.open("logo_pemprov_sumut.png") 
            st.image(logo_pemprov, width=80)
        except FileNotFoundError:
            st.warning("File 'logo_pemprov_sumut.png' tidak ditemukan. Letakkan file logo di folder yang sama.")
        st.markdown('</div>', unsafe_allow_html=True)

        # 2. Kartu Login Utama
        st.markdown('<div class="login-card">', unsafe_allow_html=True)

        # --- Bagian A: Header Gradasi (Sesuai Gambar) ---
        # Ini adalah area berwarna gelap dengan teks putih
        st.markdown("""
            <div class="login-header-gradient">
                <div class="login-header-title">LOGIN USER</div>
                <div class="login-header-subtitle">SI-PANDAI SUMUT</div>
            </div>
        """, unsafe_allow_html=True)

        # --- Bagian B: Konten Form (Area Putih) ---
        st.markdown('<div class="login-form-content">', unsafe_allow_html=True)
        
        # Input Fields menggunakan Streamlit natif
        # Placeholder ditambahkan agar lebih informatif
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

        # 3. Info Teks di Bawah Kartu
        st.markdown("""
            <div class="info-text-container">
                <div>Sistema Informasion Pensissiaan SI-Pandai Sumut</div>
                <div>Pengatururaan Dengnan SI-Pandai Sumut</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True) # Menutup login-card-container

    # Footer Halaman (Opsional, menambahkan kesan profesional)
    st.markdown("""
        <div style="text-align: center; color: #888; padding: 20px 0; font-size: 12px; margin-top: 50px;">
            © 2024 Dinas Pendidikan Provinsi Sumatera Utara
        </div>
    """, unsafe_allow_html=True)

    st.stop() # Menghentikan eksekusi kode dashboard di bawahnya jika belum login
# =========================
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

