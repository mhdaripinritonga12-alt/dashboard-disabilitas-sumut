import streamlit as st
import pandas as pd
from io import BytesIO
import plotly.express as px
from PIL import Image
import os

st.set_page_config(
    page_title="Dashboard Disabilitas Sumut",
    layout="wide"
)

# =========================
# STYLE LOGIN (Diperbarui)
# =========================
st.markdown("""
<style>

/* Mengatur background halaman login menjadi abu-abu muda agar kartu menonjol */
[data-testid="stAppViewContainer"] {
    background-color: #f4f7f6;
}

/* KARTU LOGIN */
.login-card {
    width: 400px;
    margin: auto;
    padding: 30px;
    border-radius: 15px;
    border: none;
    box-shadow: 0px 10px 30px rgba(0,0,0,0.1);
    text-align: center;
    background: white;
    /* Membuat jarak vertikal agar berada di tengah layar */
    position: relative;
    top: 50px; 
}

/* AREA LOGO */
.logo-container {
    margin-bottom: 20px;
}

/* AREA INPUT */
/* Memberikan sedikit style pada text input agar selaras */
div[data-testid="stTextInput"] > div > div > input {
    border-radius: 8px;
    border: 1px solid #ddd;
}

/* AREA TOMBOL LOGIN */
/* Mengubah tombol login menjadi warna tema (teal/hijau) */
div.stButton > button {
    background-color: #1ca65a;
    color: white;
    border-radius: 8px;
    border: none;
    padding: 10px 20px;
    font-weight: 700;
    transition: all 0.3s ease;
}

div.stButton > button:hover {
    background-color: #147a42;
    border: none;
    color: white;
}

/* Area Footer Kartu */
.card-footer {
    margin-top: 15px;
    font-size: 14px;
    color: #888;
}

</style>
""", unsafe_allow_html=True)

# =========================
# LOAD DATA (Tidak Berubah)
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
# SESSION LOGIN (Tidak Berubah)
# =========================
if "login" not in st.session_state:
    st.session_state.login = False
    st.session_state.role = ""

# =========================
# LOGIN PAGE (Diperbarui)
# =========================
if not st.session_state.login:

    # Membuat layout kolom untuk menengahkan kartu
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        # Pembuka Kartu Login
        st.markdown('<div class="login-card">', unsafe_allow_html=True)

        # 1. Menampilkan Logo Aplikasi
        st.markdown('<div class="logo-container">', unsafe_allow_html=True)
        # Pastikan file "logo_sipandai.png" ada di folder yang sama
        if os.path.exists("logo_sipandai.png"):
            logo = Image.open("logo_sipandai.png")
            st.image(logo, width=150) # Ukuran logo disesuaikan
        else:
            st.warning("File 'logo_sipandai.png' tidak ditemukan. Letakkan file logo di folder yang sama.")
        st.markdown('</div>', unsafe_allow_html=True)

        # 2. Judul Login
        st.markdown('<h2 style="color: #0b7d3e; margin-bottom: 5px;">LOGIN USER</h2>', unsafe_allow_html=True)
        st.markdown('<h4 style="color: #1ca65a; margin-top: 0; margin-bottom: 25px;">SI-PANDAI SUMUT</h4>', unsafe_allow_html=True)

        # 3. Input Fields (Menggunakan Streamlit natif)
        # Placeholder ditambahkan agar lebih bersih
        username = st.text_input("👤 Username", placeholder="Masukkan Username Anda")
        password = st.text_input("🔑 Password", type="password", placeholder="Masukkan Password Anda")

        st.markdown('<br>', unsafe_allow_html=True)

        # 4. Tombol LOGIN
        if st.button("LOGIN", use_container_width=True):

            if users.empty:
                st.error("Data pengguna tidak tersedia (cek file Excel).")
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

        # 5. Footer Kartu (Opsional)
        st.markdown('<div class="card-footer">© 2024 Dinas Pendidikan Sumut</div>', unsafe_allow_html=True)

        # Penutup Kartu Login
        st.markdown('</div>', unsafe_allow_html=True)

    st.stop() # Menghentikan eksekusi kode dashboard di bawahnya jika belum login

# =========================
# SIDEBAR (Tidak Berubah)
# =========================
# (Sisa kode Anda dimasukkan kembali di sini tanpa perubahan)
st.sidebar.title("📂 Menu")

menu = st.sidebar.radio(
    "Pilih Menu",
    ["Home"]
)

st.sidebar.divider()

# =========================
# FILTER WILAYAH (Tidak Berubah)
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
# HEADER (Tidak Berubah)
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
# REKAP CEPAT (Tidak Berubah)
# =========================
col1, col2, col3 = st.columns(3)

col1.metric("Jumlah Data", len(df))
col2.metric("Jumlah Kabupaten/Kota", df["kab_kota"].nunique())
col3.metric("Jumlah Jenis Disabilitas", df["jenis_disabilitas"].nunique())

st.divider()

# =========================
# REKAP PER JENIS (Tidak Berubah)
# =========================
st.subheader("📌 Rekap Penyandang per Jenis Disabilitas")

rekap = df.groupby("jenis_disabilitas").size().reset_index(name="Jumlah")

st.dataframe(rekap, use_container_width=True)

# =========================
# GRAFIK (Tidak Berubah)
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
# PETA (Tidak Berubah)
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
# DETAIL DATA (Tidak Berubah)
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
# DOWNLOAD DATA (Tidak Berubah)
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
# ROLE INFO (Tidak Berubah)
# =========================
st.divider()

st.caption("""
Role:
- Admin    : Semua akses
- Operator : Lihat & Download
- Viewer   : Lihat saja
""")
