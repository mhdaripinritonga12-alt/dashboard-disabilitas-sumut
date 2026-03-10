import streamlit as st
import pandas as pd
from PIL import Image
import os
import base64

# ==================================
# Bagian 0: KONFIGURASI HALAMAN
# ==================================
st.set_page_config(
    page_title="SI-PANDAI SUMUT",
    layout="wide",
    page_icon="🔒"
)

# Fungsi Base64 untuk Logo Sidebar
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

# ==================================
# Bagian 1: CSS CUSTOM (UI & KARTU SEKOLAH)
# ==================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&display=swap');
    html, body, [data-testid="stWidgetLabel"] { font-family: 'Inter', sans-serif !important; }
    [data-testid="stAppViewContainer"] { background-color: #f8fafc !important; }
    header {visibility: hidden;}

    /* LOGIN CARD STYLE */
    [data-testid="stVerticalBlockBorderWrapper"] > div {
        background: linear-gradient(180deg, #e3f2fd 0%, #ffffff 100%) !important;
        border-radius: 20px !important;
        border: 1px solid #cde4f7 !important;
        padding: 35px !important;
        box-shadow: 0px 10px 30px rgba(0,0,0,0.08) !important;
    }

    /* TOMBOL LOGIN */
    div.stButton > button {
        background: linear-gradient(90deg, #1565c0 0%, #1e88e5 100%) !important;
        color: white !important; border-radius: 10px !important; font-weight: 700 !important; height: 48px;
    }

    /* SIDEBAR STYLE */
    [data-testid="stSidebar"] { background: linear-gradient(180deg, #0d47a1 0%, #1565c0 100%) !important; }
    [data-testid="stSidebar"] * { color: white !important; }
    div[data-testid="stSelectbox"] div div { color: #333 !important; }

    /* BALON KOTAK SEKOLAH DENGAN BAYANGAN */
    .school-container {
        background: white !important;
        border-radius: 12px !important;
        padding: 15px !important;
        border: 1px solid #e2e8f0 !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06) !important;
        margin-bottom: 15px;
    }

    /* WARNA REKOMENDASI */
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

    .main-dashboard-title { font-size: 26px !important; font-weight: 800 !important; color: #0d47a1 !important; margin-bottom: 0px !important; }
    .logo-header-center { display: flex; justify-content: center; padding-top: 30px; margin-bottom: 10px; }
</style>
""", unsafe_allow_html=True)

# =========================
# Bagian 2: LOAD DATA
# =========================
@st.cache_data
def load_all_data():
    try:
        df_ats = pd.read_csv("master_data_si_pandai.csv")
        df_sch = pd.read_csv("master_data_sekolah.csv") if os.path.exists("master_data_sekolah.csv") else pd.DataFrame()
        return df_ats, df_sch
    except Exception as e:
        st.error(f"Gagal memuat data master: {e}")
        return pd.DataFrame(), pd.DataFrame()

data_wilayah, data_sekolah = load_all_data()

# Login Hardcoded
def check_login(u, p):
    return u == "admin" and p == "admin"

if "login" not in st.session_state:
    st.session_state.login = False
    st.session_state.role = "Admin"

# =========================
# Bagian 3: HALAMAN LOGIN
# =========================
if not st.session_state.login:
    st.markdown('<div class="logo-header-center">', unsafe_allow_html=True)
    col_l1, col_l2, col_l3 = st.columns([2, 0.4, 2])
    with col_l2:
        if os.path.exists("logo_sumut.png"):
            st.image(Image.open("logo_sumut.png"), width=95)
    st.markdown('</div>', unsafe_allow_html=True)

    _, col_card, _ = st.columns([1.5, 2.5, 1.5]) 
    with col_card:
        with st.container(border=True):
            col_left, col_right = st.columns([1, 1.4])
            with col_left:
                if os.path.exists("logo_sipandai.png"):
                    st.image(Image.open("logo_sipandai.png"), use_container_width=True)
            with col_right:
                st.markdown('<div style="color: #0d47a1; font-size: 24px; font-weight: 800; margin-bottom: 2px;">LOGIN USER</div>', unsafe_allow_html=True)
                st.markdown('<div style="color: #546e7a; font-size: 13px; margin-bottom: 25px;">Akses Dashboard SI-PANDAI SUMUT</div>', unsafe_allow_html=True)
                u_in = st.text_input("Username", placeholder="👤  Masukkan Username", key="user_input", label_visibility="collapsed")
                p_in = st.text_input("Password", type="password", placeholder="🔑  Masukkan Password", key="pass_input", label_visibility="collapsed")
                if st.button("MASUK KE DASHBOARD", use_container_width=True):
                    if check_login(u_in, p_in):
                        st.session_state.login = True
                        st.rerun()
                    else:
                        st.error("Username atau Password Salah")
    st.stop()

# ==================================
# Bagian 4: DASHBOARD UTAMA
# ==================================

# --- SIDEBAR ---
logo_b64 = get_base64_image("logo_sumut.png")
if logo_b64:
    st.sidebar.markdown(f"""
        <div style="display: flex; align-items: center; gap: 12px; padding-bottom: 20px;">
            <img src="data:image/png;base64,{logo_b64}" width="45">
            <span style="font-size: 18px; font-weight: 800; color: white; line-height: 1.1;">SI-PANDAI<br>SUMUT</span>
        </div>
    """, unsafe_allow_html=True)

st.sidebar.write(f"👤 Role: **{st.session_state.role.upper()}**")
st.sidebar.divider()

st.sidebar.header("🔎 Filter Wilayah")
kab_pilih = st.sidebar.selectbox("Pilih Kabupaten / Kota", ["Semua"] + sorted(data_wilayah["kab_kota"].unique().tolist()))

df_filter = data_wilayah.copy()
if kab_pilih != "Semua":
    df_filter = df_filter[df_filter["kab_kota"] == kab_pilih]

st.sidebar.divider()
if st.sidebar.button("Logout 🚪", use_container_width=True):
    st.session_state.login = False
    st.rerun()

# --- HEADER MAIN ---
st.markdown('<p class="main-dashboard-title">🚀 Dashboard Utama</p>', unsafe_allow_html=True)
st.markdown('<p style="color: #546e7a; font-size: 14px; margin-top: -5px;">Sistem Informasi Pemetaan ATS Disabilitas Sumatera Utara</p>', unsafe_allow_html=True)
st.divider()

# --- MATRIKS UTAMA ---
st.subheader("📌 Matriks Capaian Sektoral")
m1, m2, m3 = st.columns(3)
if kab_pilih == "Semua":
    m1.metric("Total Penduduk Disabilitas", "6.732", help="Sumber: LPPD PK 2025")
    m2.metric("Total Siswa Disabilitas", "4.573", help="Sumber: TIKP Provsu 2025")
    m3.metric("Angka Partisipasi Sekolah", "67.93%")
else:
    pop = int(df_filter['jumlah_penduduk'].sum())
    siswa = int(df_filter['jumlah_siswa'].sum())
    ats = int(df_filter['ats_disabilitas'].sum())
    m1.metric("Penduduk Disabilitas", f"{pop:,}")
    m2.metric("Siswa Belajar", f"{siswa:,}")
    m3.metric("Anak Tidak Sekolah (ATS)", f"{ats:,}", delta_color="inverse")

# Sumber Data Label
st.markdown("""
    <div style="background-color: #e3f2fd; padding: 10px; border-radius: 10px; border-left: 5px solid #1565c0; margin-top: 10px;">
        <p style="font-size: 12px; color: #0d47a1; margin: 0;">
            <b>Sumber Data:</b> Bidang PK - Laporan LPPD 2025 & Rekapitulasi Dapodik/TIKP Provsu 2025
        </p>
    </div>
""", unsafe_allow_html=True)

st.divider()

# --- FITUR KARTU SEKOLAH (GRID BALON KOTAK) ---
if kab_pilih != "Semua":
    st.subheader(f"🏫 Daftar Satuan Pendidikan di {kab_pilih}")
    sekolah_wilayah = data_sekolah[data_sekolah['kab_kota'] == kab_pilih]
    ats_wilayah = int(df_filter['ats_disabilitas'].sum())
    
    if not sekolah_wilayah.empty:
        cols = st.columns(3)
        for i, row in enumerate(sekolah_wilayah.itertuples()):
            with cols[i % 3]:
                # Mulai Container Kartu
                with st.container():
                    st.markdown('<div class="school-container">', unsafe_allow_html=True)
                    
                    # 1. Logika Rekomendasi & Warna Balon
                    if row.jumlah_rombel > row.jumlah_ruang_kelas:
                        selisih = row.jumlah_rombel - row.jumlah_ruang_kelas
                        st.markdown(f"<div class='rec-mendesak'>⚠️ MENDESAK: Butuh {selisih} Ruang Kelas Baru (RKB)</div>", unsafe_allow_html=True)
                    elif row.rusak_berat > 0:
                        st.markdown(f"<div class='rec-rehab'>🛠️ PRIORITAS REHAB: {row.rusak_berat} Ruang Rusak Berat</div>", unsafe_allow_html=True)
                    else:
                        st.markdown("<div class='rec-aman'>✅ KONDISI STABIL</div>", unsafe_allow_html=True)

                    # 2. Nama Sekolah (Clickable Expander)
                    with st.expander(f"{row.nama_sekolah}"):
                        st.markdown(f"""
                            **Informasi Utama:**
                            - 🆔 NPSN: `{row.npsn}`
                            - 🏢 Status: {row.status}
                            
                            **Detail Sarana Prasarana:**
                            - 👥 Jumlah Siswa: {row.jumlah_siswa} Orang
                            - 📚 Jumlah Rombel: {row.jumlah_rombel}
                            - 🏫 Total Ruang Kelas: {row.jumlah_ruang_kelas}
                            - ❌ Kondisi Rusak (S/B): {row.rusak_sedang} / {row.rusak_berat}
                            
                            **Lokasi Sekolah:**
                            - 📍 {row.alamat}
                            
                            <hr style='margin:10px 0;'>
                            <p style='font-size:10px; color:gray;'>Sumber: Spreadsheet Bidang Pembinaan PK</p>
                        """, unsafe_allow_html=True)
                    
                    st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info(f"Data detail sekolah untuk {kab_pilih} belum tersedia.")
    st.divider()

# --- PETA SEBARAN (VERSI FIX TANPA ERROR) ---
st.subheader("🗺️ Peta Pemetaan ATS Disabilitas")
if not df_filter.empty:
    # Buat kolom ukuran titik agar tidak error JSON
    df_filter['map_size'] = df_filter['ats_disabilitas'].apply(lambda x: (x + 1) * 20)
    st.map(
        df_filter, 
        latitude="lat", 
        longitude="lon", 
        size="map_size"
    )
else:
    st.info("Data koordinat tidak tersedia.")

st.divider()

# --- TABEL DETAIL ---
st.subheader("📋 Detail Data Sektoral per Wilayah")
st.dataframe(df_filter[['kab_kota', 'jumlah_penduduk', 'jumlah_siswa', 'ats_disabilitas']], use_container_width=True)

# Tombol Download
csv_data = df_filter.to_csv(index=False).encode('utf-8')
st.download_button(
    label="Download Master Data (CSV) ⬇️",
    data=csv_data,
    file_name='master_data_si_pandai_filtered.csv',
    mime='text/csv',
)
