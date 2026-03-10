import streamlit as st
import pandas as pd
from PIL import Image
import os
import base64

# ==================================
# Bagian 0: KONFIGURASI HALAMAN
# ==================================
st.set_page_config(page_title="SI-PANDAI SUMUT", layout="wide", page_icon="🔒")

def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

# ==================================
# Bagian 1: CSS CUSTOM (KEMBALI KE GRADASI ASLI)
# ==================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&display=swap');
    html, body, [data-testid="stWidgetLabel"] { font-family: 'Inter', sans-serif !important; }
    
    /* 1. SIDEBAR GRADASI BIRU (SESUAI GAMBAR KEDUA ANDA) */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d47a1 0%, #1565c0 100%) !important;
    }
    [data-testid="stSidebar"] * { color: white !important; }
    div[data-testid="stSelectbox"] div div { color: #333 !important; }

    /* 2. BACKGROUND & CONTAINER DASHBOARD */
    [data-testid="stAppViewContainer"] { background-color: #f4f7f9 !important; }
    header {visibility: hidden;}

    /* 3. BALON KOTAK SEKOLAH (SHADOW & BORDER) */
    [data-testid="stVerticalBlockBorderWrapper"] > div {
        background: white !important;
        border-radius: 20px !important;
        padding: 25px !important;
        border: 1px solid #e2e8f0 !important;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1) !important;
        margin-bottom: 15px;
    }

    /* 4. TOMBOL NAMA SEKOLAH (BIRU, TEBAL, TANPA GARIS TOMBOL) */
    div.stButton > button[key^="btn_"] {
        background: transparent !important;
        border: none !important;
        color: #0d47a1 !important;
        font-size: 18px !important;
        font-weight: 800 !important;
        padding: 0px !important;
        text-align: left !important;
        box-shadow: none !important;
    }
    div.stButton > button[key^="btn_"]:hover {
        color: #1e88e5 !important;
        text-decoration: underline !important;
    }

    /* 5. BALON REKOMENDASI WARNA */
    .rec-box { padding: 8px 12px; border-radius: 8px; font-size: 12px; font-weight: 700; margin-bottom: 12px; }
    .mendesak { background-color: #fee2e2; color: #b91c1c; border-left: 5px solid #ef4444; }
    .rehab { background-color: #fef3c7; color: #b45309; border-left: 5px solid #f59e0b; }
    .aman { background-color: #dcfce7; color: #15803d; border-left: 5px solid #22c55e; }

    /* TOMBOL LOGOUT ORANGE */
    section[data-testid="stSidebar"] div.stButton > button {
        background: linear-gradient(90deg, #ff9966 0%, #ff5e62 100%) !important;
        color: white !important; border-radius: 8px !important; font-weight: 700 !important;
    }
</style>
""", unsafe_allow_html=True)

# =========================
# Bagian 2: LOAD DATA
# =========================
@st.cache_data
def load_all_data():
    try:
        df_ats = pd.read_csv("master_data_si_pandai.csv")
        df_sch = pd.read_csv("master_data_sekolah.csv")
        return df_ats, df_sch
    except:
        return pd.DataFrame(), pd.DataFrame()

data_wilayah, data_sekolah = load_all_data()

# =========================
# Bagian 3: FUNGSI POP-UP
# =========================
@st.dialog("Detail Satuan Pendidikan")
def show_details(row):
    st.markdown(f"### {row.nama_sekolah}")
    st.divider()
    c1, c2 = st.columns(2)
    with c1:
        st.write(f"🆔 **NPSN:** `{row.npsn}`")
        st.write(f"🏢 **Status:** {row.status}")
        st.write(f"📍 **Alamat:** {row.alamat}")
    with c2:
        st.write(f"👥 **Siswa:** {row.jumlah_siswa} Orang")
        st.write(f"📚 **Rombel:** {row.jumlah_rombel}")
        st.write(f"🏫 **Ruang Kelas:** {row.jumlah_ruang_kelas}")
    
    st.divider()
    if row.rusak_berat > 0:
        st.error(f"⚠️ Perhatian: Terdapat {row.rusak_berat} Ruang Rusak Berat")
    st.caption("Sumber: Spreadsheet Bidang Pembinaan Pendidikan Khusus")

# =========================
# Bagian 4: DASHBOARD
# =========================
if "login" not in st.session_state:
    st.session_state.login = False

# (Fungsi Login Anda tetap di sini)
if not st.session_state.login:
    st.session_state.login = True
    st.rerun()

# --- SIDEBAR ---
logo_b64 = get_base64_image("logo_sumut.png")
if logo_b64:
    st.sidebar.markdown(f"""
        <div style="display: flex; align-items: center; gap: 12px; padding-bottom: 20px;">
            <img src="data:image/png;base64,{logo_b64}" width="45">
            <span style="font-size: 18px; font-weight: 800; color: white;">SI-PANDAI SUMUT</span>
        </div>
    """, unsafe_allow_html=True)

kab_pilih = st.sidebar.selectbox("Pilih Kabupaten / Kota", ["Semua"] + sorted(data_wilayah["kab_kota"].unique().tolist()))
if st.sidebar.button("Logout 🚪", use_container_width=True):
    st.session_state.login = False
    st.rerun()

# --- MAIN ---
st.markdown('<p style="font-size:26px; font-weight:800; color:#0d47a1;">🚀 Dashboard Utama</p>', unsafe_allow_html=True)
st.divider()

# Matriks
df_filter = data_wilayah.copy()
if kab_pilih != "Semua":
    df_filter = df_filter[df_filter["kab_kota"] == kab_pilih]

m1, m2, m3 = st.columns(3)
if kab_pilih == "Semua":
    m1.metric("Total Penduduk Disabilitas", "6.732")
    m2.metric("Total Siswa Disabilitas", "4.573")
    m3.metric("Angka Partisipasi Sekolah", "67.93%")
else:
    m1.metric("Penduduk Disabilitas", int(df_filter['jumlah_penduduk'].sum()))
    m2.metric("Siswa Belajar", int(df_filter['jumlah_siswa'].sum()))
    m3.metric("ATS Disabilitas", int(df_filter['ats_disabilitas'].sum()), delta_color="inverse")

# --- DETAIL SEKOLAH (BALON KOTAK SHADOW) ---
if kab_pilih != "Semua":
    st.divider()
    st.subheader(f"🏫 Satuan Pendidikan di {kab_pilih}")
    sekolah_wilayah = data_sekolah[data_sekolah['kab_kota'] == kab_pilih]
    
    if not sekolah_wilayah.empty:
        cols = st.columns(3)
        for i, row in enumerate(sekolah_wilayah.itertuples()):
            with cols[i % 3]:
                with st.container(border=True):
                    # 1. Rekomendasi
                    if row.jumlah_rombel > row.jumlah_ruang_kelas:
                        st.markdown(f"<div class='rec-box mendesak'>⚠️ MENDESAK: Butuh {row.jumlah_rombel - row.jumlah_ruang_kelas} RKB</div>", unsafe_allow_html=True)
                    elif row.rusak_berat > 0:
                        st.markdown(f"<div class='rec-box rehab'>🛠️ PRIORITAS REHAB: {row.rusak_berat} Ruang</div>", unsafe_allow_html=True)
                    else:
                        st.markdown("<div class='rec-box aman'>✅ KONDISI STABIL</div>", unsafe_allow_html=True)

                    # 2. Nama Sekolah (Tombol Pop-up)
                    if st.button(row.nama_sekolah, key=f"btn_{row.npsn}"):
                        show_details(row)

# --- PETA ---
st.divider()
st.subheader("🗺️ Peta Pemetaan ATS Disabilitas")
df_filter['map_size'] = df_filter['ats_disabilitas'] * 30
st.map(df_filter, latitude="lat", longitude="lon", size="map_size")
