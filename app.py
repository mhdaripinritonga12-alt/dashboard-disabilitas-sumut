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
# Bagian 1: CSS CUSTOM (DESAIN BALON KOTAK & BAYANGAN)
# ==================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&display=swap');
    html, body, [data-testid="stWidgetLabel"] { font-family: 'Inter', sans-serif !important; }
    [data-testid="stAppViewContainer"] { background-color: #f8fafc !important; }
    
    /* STYLE KARTU SEKOLAH DENGAN BAYANGAN & GARIS */
    [data-testid="stVerticalBlockBorderWrapper"] > div {
        background: white !important;
        border-radius: 12px !important;
        padding: 15px !important;
        border: 1px solid #e2e8f0 !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06) !important;
        transition: transform 0.2s ease-in-out;
    }

    /* GAYA EXPANDER (NAMA SEKOLAH) */
    .stExpander {
        border: none !important;
        background: transparent !important;
    }
    .stExpander [data-testid="stExpanderHeader"] p {
        font-size: 16px !important;
        font-weight: 800 !important;
        color: #0f172a !important;
    }

    /* BALON REKOMENDASI WARNA */
    .rec-mendesak {
        background-color: #fee2e2; color: #b91c1c; border-left: 5px solid #ef4444;
        padding: 10px; border-radius: 6px; font-size: 12px; font-weight: 700; margin-bottom: 8px;
    }
    .rec-rehab {
        background-color: #fef3c7; color: #b45309; border-left: 5px solid #f59e0b;
        padding: 10px; border-radius: 6px; font-size: 12px; font-weight: 700; margin-bottom: 8px;
    }
    .rec-aman {
        background-color: #dcfce7; color: #15803d; border-left: 5px solid #22c55e;
        padding: 10px; border-radius: 6px; font-size: 12px; font-weight: 700; margin-bottom: 8px;
    }
</style>
""", unsafe_allow_html=True)

# =========================
# Bagian 2: LOAD DATA
# =========================
@st.cache_data
def load_all_data():
    df_ats = pd.read_csv("master_data_si_pandai.csv")
    df_sch = pd.read_csv("master_data_sekolah.csv") if os.path.exists("master_data_sekolah.csv") else pd.DataFrame()
    return df_ats, df_sch

data_wilayah, data_sekolah = load_all_data()

# ==================================
# Bagian 3: DASHBOARD UTAMA
# ==================================

# Sidebar Filter
st.sidebar.header("🔎 Filter Wilayah")
kab_pilih = st.sidebar.selectbox("Pilih Kabupaten / Kota", ["Semua"] + sorted(data_wilayah["kab_kota"].unique().tolist()))

df_filter = data_wilayah.copy()
if kab_pilih != "Semua":
    df_filter = df_filter[df_filter["kab_kota"] == kab_pilih]

# Header
st.markdown('<p style="font-size:26px; font-weight:800; color:#1e293b; margin-bottom:0;">🚀 SI-PANDAI SUMUT</p>', unsafe_allow_html=True)
st.divider()

# Matriks Utama
m1, m2, m3 = st.columns(3)
if kab_pilih == "Semua":
    m1.metric("Total Penduduk Disabilitas", "6.732", help="LPPD PK 2025")
    m2.metric("Total Siswa Disabilitas", "4.573", help="TIKP Provsu 2025")
    m3.metric("Angka Partisipasi Sekolah", "67.93%")
else:
    pop = int(df_filter['jumlah_penduduk'].sum())
    siswa = int(df_filter['jumlah_siswa'].sum())
    ats = int(df_filter['ats_disabilitas'].sum())
    m1.metric("Penduduk Disabilitas", f"{pop}")
    m2.metric("Siswa Belajar", f"{siswa}")
    m3.metric("ATS Disabilitas", f"{ats}", delta_color="inverse")

# --- DETAIL SEKOLAH (GRID BALON KOTAK) ---
if kab_pilih != "Semua":
    st.divider()
    st.subheader(f"🏫 Daftar Satuan Pendidikan di {kab_pilih}")
    
    sekolah_wilayah = data_sekolah[data_sekolah['kab_kota'] == kab_pilih]
    ats_wilayah = int(df_filter['ats_disabilitas'].sum())
    
    if not sekolah_wilayah.empty:
        cols = st.columns(3)
        for i, row in enumerate(sekolah_wilayah.itertuples()):
            with cols[i % 3]:
                # Mulai Balon Kotak Sekolah
                with st.container(border=True):
                    
                    # LOGIKA REKOMENDASI & WARNA
                    if row.jumlah_rombel > row.jumlah_ruang_kelas:
                        selisih = row.jumlah_rombel - row.jumlah_ruang_kelas
                        st.markdown(f"<div class='rec-mendesak'>⚠️ MENDESAK: Butuh {selisih} Ruang Kelas Baru (RKB)</div>", unsafe_allow_html=True)
                    elif row.rusak_berat > 0:
                        st.markdown(f"<div class='rec-rehab'>🛠️ PRIORITAS REHAB: {row.rusak_berat} Ruang Rusak Berat</div>", unsafe_allow_html=True)
                    else:
                        st.markdown("<div class='rec-aman'>✅ KONDISI STABIL</div>", unsafe_allow_html=True)

                    # NAMA SEKOLAH SEBAGAI CLICKABLE HEADER
                    with st.expander(f"{row.nama_sekolah}"):
                        st.markdown(f"""
                            **Informasi Sekolah:**
                            - 🆔 NPSN: `{row.npsn}`
                            - 🏢 Status: {row.status}
                            
                            **Detail Sarpras:**
                            - 👥 Jumlah Siswa: {row.jumlah_siswa} Orang
                            - 📚 Jumlah Rombel: {row.jumlah_rombel}
                            - 🏫 Ruang Kelas: {row.jumlah_ruang_kelas}
                            - ❌ Rusak (S/B): {row.rusak_sedang} / {row.rusak_berat}
                            
                            **Lokasi:**
                            - 📍 {row.alamat}
                            
                            <hr style='margin:10px 0;'>
                            <p style='font-size:10px; color:gray;'>Sumber: Spreadsheet Bidang Pembinaan PK</p>
                        """, unsafe_allow_html=True)
    else:
        st.info(f"Belum ada data detail sekolah untuk {kab_pilih}")

st.divider()
# Peta & Tabel (Opsional di bawah)
st.map(df_filter, latitude="lat", longitude="lon", size=df_filter['ats_disabilitas']*30)
