import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(
    page_title="Dashboard Disabilitas Sumut",
    layout="wide"
)

# =========================
# LOAD DATA
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
# LOGIN SYSTEM
# =========================
if "login" not in st.session_state:
    st.session_state.login = False
    st.session_state.role = ""

if not st.session_state.login:
    st.title("🔐 Login Dashboard Disabilitas")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = users[
            (users["username"] == username) &
            (users["password"] == password)
        ]

        if not user.empty:
            st.session_state.login = True
            st.session_state.role = user.iloc[0]["role"]
            st.success("Login berhasil")
            st.rerun()
        else:
            st.error("Username atau password salah")

    st.stop()

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

kecamatan = st.sidebar.selectbox(
    "Pilih Kecamatan",
    ["Semua"] + sorted(df["kecamatan"].unique())
)

if kecamatan != "Semua":
    df = df[df["kecamatan"] == kecamatan]

desa = st.sidebar.selectbox(
    "Pilih Desa / Kelurahan",
    ["Semua"] + sorted(df["desa_kelurahan"].unique())
)

if desa != "Semua":
    df = df[df["desa_kelurahan"] == desa]


# =========================
# REKAP CEPAT
# =========================
col1, col2, col3 = st.columns(3)
col1.metric("Jumlah Data", len(df))
col2.metric("Jumlah Kecamatan", df["kecamatan"].nunique())
col3.metric("Jumlah Kelurahan", df["desa_kelurahan"].nunique())

st.divider()

# =========================
# A. REKAP PER JENIS DISABILITAS
# =========================
st.subheader("📌 Rekap Penyandang per Jenis Disabilitas")

rekap = df.groupby("jenis_disabilitas").size().reset_index(name="Jumlah")
st.dataframe(rekap, use_container_width=True)
st.divider()
st.subheader("📈 Grafik Penyandang Disabilitas")

rekap_chart = (
    df.groupby("jenis_disabilitas")
    .size()
    .reset_index(name="Jumlah")
)

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Grafik Batang")
    st.bar_chart(
        rekap_chart.set_index("jenis_disabilitas")
    )

with col2:
    st.markdown("#### Grafik Pie")
    st.pyplot(
        rekap_chart.set_index("jenis_disabilitas")
        import plotly.express as px

fig = px.pie(
    df,
    values="Jumlah",
    names="Jenis Disabilitas",
    title="Distribusi Jenis Disabilitas"
)

st.plotly_chart(fig, use_container_width=True)

st.divider()
st.subheader("🗺️ Peta Sebaran Penyandang Disabilitas (Kab/Kota)")

map_data = (
    data.groupby("kab_kota")
    .size()
    .reset_index(name="Jumlah")
)

# Titik perkiraan pusat kab/kota (contoh Sumut)
peta_kab = {
    "Kota Medan": [3.5952, 98.6722],
    "Kab. Deli Serdang": [3.4200, 98.9800],
    "Kab. Langkat": [3.7000, 98.2000],
}

map_rows = []
for k, v in peta_kab.items():
    jumlah = map_data.loc[
        map_data["kab_kota"] == k, "Jumlah"
    ]
    if not jumlah.empty:
        map_rows.append({
            "lat": v[0],
            "lon": v[1],
            "jumlah": int(jumlah.values[0])
        })

if map_rows:
    map_df = pd.DataFrame(map_rows)
    st.map(map_df, size="jumlah")
else:
    st.info("Data peta belum tersedia")

# =========================
# B. KLIK REKAP → MUNCUL NAMA
# =========================
st.subheader("📋 Detail Nama Berdasarkan Jenis")

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
        ["nama", "jenis_disabilitas", "desa_kelurahan", "kecamatan"]
    ],
    use_container_width=True
)

# =========================
# C. DOWNLOAD EXCEL (FIX)
# =========================
st.divider()
st.subheader("⬇️ Download Data")

if st.session_state.role in ["admin", "operator"]:
    output = BytesIO()
    df.to_excel(output, index=False, engine="openpyxl")
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
# D. ROLE INFO
# =========================
st.divider()
st.caption("""
Role:
- Admin    : Semua akses
- Operator : Lihat & Download
- Viewer   : Lihat saja
""")

