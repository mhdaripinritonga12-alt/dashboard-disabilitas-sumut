import streamlit as st
import pandas as pd
from PIL import Image
import os
import base64

# ==================================
# Bagian 0: KONFIGURASI HALAMAN
# ==================================
st.set_page_config(page_title="Dashboard SI-PANDAI SUMUT", layout="wide", page_icon="🔒")

def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

# ==================================
# Bagian 1: CSS CUSTOM (KARTU SEKOLAH TANPA PANAH)
# ==================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&display=swap');
    html, body, [data-testid="stWidgetLabel"] { font-family: 'Inter', sans-serif !important; }
    [data-testid="stAppViewContainer"] { background-color: #f8fafc !important; }
    header {visibility: hidden;}

    /* 1. CONTAINER BALON KOTAK (SHADOW & BORDER) */
    [data-testid="stVerticalBlockBorderWrapper"] > div {
        background: white !important;
        border-radius: 15px !important;
        padding: 20px !important;
        border: 1px solid #e2e8f0 !important;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05) !important;
        margin-bottom: 10px;
    }

    /* 2. MENGHILANGKAN GARIS BAWAAN & PANAH EXPANDER */
    .stExpander {
        border: none !important;
        background: transparent !important;
    }
    [data-testid="stExpanderIcon"] {
        display: none !important;
    }

    /* 3. STYLE NAMA SEKOLAH (TEBAL & BIRU) */
    .stExpander [data-testid="stExpanderHeader"] p {
        font-size: 18px !important;
        font-weight: 800 !important;
        color: #0d47a1 !important; /* Warna Biru */
        text-align: left;
    }

    /* 4. BALON REKOMENDASI WARNA */
    .rec-mendesak {
        background-color: #fee2e2; color: #b91c1c; border-left: 5px solid #ef4444;
        padding: 8px 12px; border-radius: 8px; font-size: 12px; font-weight: 700; margin-bottom: 12px;
    }
    .rec-rehab {
        background-color: #fef3c7; color: #b45309; border-left: 5px solid #f59e0b;
        padding: 8px 12px; border-radius: 8px; font-size: 12px; font-weight: 700; margin-bottom: 12px;
    }
    .rec-aman {
        background-color: #dcfce7; color: #15803d; border-left: 5px solid #22c55e;
        padding: 8px 12px; border-radius: 8px; font-size: 12px; font-weight: 700; margin-bottom: 12px;
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
# Bagian LOGIN (TIDAK BERUBAH)
# =========================
if "login" not in st.session_state:
    st.session_state.login = False

if not st.session_state.login:
    # (Kode login Anda tetap di sini)
    st.session_state.login = True # Simulasi
    st.rerun()

# ==================================
# Bagian 4: DASHBOARD UTAMA
# ==================================

# Sidebar (TIDAK BERUBAH)
st.sidebar.header("🔎 Filter Wilayah")
kab_pilih = st.sidebar.selectbox("Pilih Kabupaten / Kota", ["Semua"] + sorted(data_wilayah["kab_kota"].unique().tolist()))

df_filter = data_wilayah.copy()
if kab_pilih != "Semua":
    df_filter = df_filter[df_filter["kab_kota"] == kab_pilih]

# Header Dashboard
st.markdown('<p style="font-size:26px; font-weight:800; color:#1e293b;">🚀 Dashboard Utama</p>', unsafe_allow_html=True)

# Matriks Capaian (TIDAK BERUBAH)
m1, m2, m3 = st.columns(3)
if kab_pilih == "Semua":
    m1.metric("Total Penduduk Disabilitas", "6.732")
    m2.metric("Total Siswa Disabilitas", "4.573")
    m3.metric("Angka Partisipasi Sekolah", "67.93%")
else:
    pop = int(df_filter['jumlah_penduduk'].sum())
    siswa = int(df_filter['jumlah_siswa'].sum())
    ats = int(df_filter['ats_disabilitas'].sum())
    m1.metric("Penduduk Disabilitas", f"{pop}")
    m2.metric("Siswa Belajar", f"{siswa}")
    m3.metric("ATS Disabilitas", f"{ats}", delta_color="inverse")

# --- DETAIL SEKOLAH (FITUR BARU DENGAN SHADOW & TANPA PANAH) ---
if kab_pilih != "Semua":
    st.divider()
    st.subheader(f"🏫 Daftar Satuan Pendidikan di {kab_pilih}")
    
    sekolah_wilayah = data_sekolah[data_sekolah['kab_kota'] == kab_pilih]
    
    if not sekolah_wilayah.empty:
        cols = st.columns(3)
        for i, row in enumerate(sekolah_wilayah.itertuples()):
            with cols[i % 3]:
                # SELURUH ELEMEN MASUK DALAM SATU CONTAINER (BALON KOTAK)
                with st.container(border=True):
                    
                    # 1. Keterangan Rekomendasi (Di dalam balon, di atas nama sekolah)
                    if row.jumlah_rombel > row.jumlah_ruang_kelas:
                        selisih = row.jumlah_rombel - row.jumlah_ruang_kelas
                        st.markdown(f"<div class='rec-mendesak'>⚠️ MENDESAK: Butuh {selisih} RKB</div>", unsafe_allow_html=True)
                    elif row.rusak_berat > 0:
                        st.markdown(f"<div class='rec-rehab'>🛠️ PRIORITAS REHAB: {row.rusak_berat} Ruang</div>", unsafe_allow_html=True)
                    else:
                        st.markdown("<div class='rec-aman'>✅ KONDISI STABIL</div>", unsafe_allow_html=True)

                    # 2. Nama Sekolah (Clickable, Biru, Tebal, Tanpa Panah)
                    with st.expander(f"{row.nama_sekolah}"):
                        st.markdown(f"""
                            <div style="color: #475569; font-size: 13px; margin-top: 10px;">
                                <p>🆔 <b>NPSN:</b> {row.npsn}</p>
                                <p>🏢 <b>Status:</b> {row.status}</p>
                                <p>👥 <b>Siswa:</b> {row.jumlah_siswa} Orang</p>
                                <p>📚 <b>Rombel:</b> {row.jumlah_rombel}</p>
                                <p>🏫 <b>Ruang Kelas:</b> {row.jumlah_ruang_kelas}</p>
                                <p>📍 <b>Alamat:</b> {row.alamat}</p>
                                <hr>
                                <p style="font-size: 10px; color: gray;">Sumber: Spreadsheet Bidang Pembinaan PK</p>
                            </div>
                        """, unsafe_allow_html=True)
    else:
        st.info(f"Belum ada data sekolah untuk {kab_pilih}")

st.divider()
# Peta Sebaran (Sudah Fix Tanpa Error)
st.subheader("🗺️ Peta Pemetaan ATS Disabilitas")
df_filter['map_size'] = df_filter['ats_disabilitas'] * 30
st.map(df_filter, latitude="lat", longitude="lon", size="map_size")
