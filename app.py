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
    page_icon="🔒",
    initial_sidebar_state="expanded" # Sidebar otomatis terbuka
)

# Inisialisasi State untuk Navigasi Halaman
if "page_view" not in st.session_state:
    st.session_state.page_view = "dashboard"
if "selected_school_data" not in st.session_state:
    st.session_state.selected_school_data = None

# Fungsi Base64 untuk Logo Sidebar
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

# ==================================
# Bagian 1: CSS CUSTOM (SIDEBAR GRADASI & BALON SHADOW)
# ==================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&display=swap');
    html, body, [data-testid="stWidgetLabel"] { font-family: 'Inter', sans-serif !important; }
    
    /* 1. SIDEBAR GRADASI BIRU ASLI */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d47a1 0%, #1565c0 100%) !important;
    }
    [data-testid="stSidebar"] * { color: white !important; }
    div[data-testid="stSelectbox"] div div { color: #333 !important; }

    /* 2. BACKGROUND HALAMAN */
    [data-testid="stAppViewContainer"] { background-color: #f4f7f9 !important; }
    
    /* 3. KOTAK BALON SEKOLAH (SHADOW & BORDER) */
    .school-card-container {
        background: white !important;
        border-radius: 15px !important;
        padding: 20px !important;
        border: 1px solid #e2e8f0 !important;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1) !important;
        margin-bottom: 20px;
    }

    /* 4. TOMBOL NAMA SEKOLAH (BIRU, TEBAL, TANPA PANAH) */
    div.stButton > button[key^="btn_"] {
        background: transparent !important;
        border: none !important;
        color: #0d47a1 !important;
        font-size: 18px !important;
        font-weight: 800 !important;
        padding: 0px !important;
        text-align: left !important;
        box-shadow: none !important;
        line-height: 1.2 !important;
    }
    div.stButton > button[key^="btn_"]:hover {
        color: #1e88e5 !important;
        text-decoration: underline !important;
    }

    /* 5. BALON REKOMENDASI WARNA */
    .rec-box { padding: 8px 12px; border-radius: 8px; font-size: 11px; font-weight: 700; margin-bottom: 12px; }
    .mendesak { background-color: #fee2e2; color: #b91c1c; border-left: 5px solid #ef4444; }
    .rehab { background-color: #fef3c7; color: #b45309; border-left: 5px solid #f59e0b; }
    .aman { background-color: #dcfce7; color: #15803d; border-left: 5px solid #22c55e; }

    /* TOMBOL LOGOUT & KEMBALI */
    section[data-testid="stSidebar"] div.stButton > button, .back-button button {
        background: linear-gradient(90deg, #ff9966 0%, #ff5e62 100%) !important;
        color: white !important; font-weight: 700 !important; border: none !important;
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
# Bagian 3: LOGIN & SESSION
# =========================
if "login" not in st.session_state: st.session_state.login = False

def check_login(u, p): return u == "admin" and p == "admin"

if not st.session_state.login:
    # --- HALAMAN LOGIN ---
    st.markdown('<div style="text-align:center; padding-top:50px;">', unsafe_allow_html=True)
    if os.path.exists("logo_sumut.png"): st.image("logo_sumut.png", width=100)
    
    _, col_card, _ = st.columns([1.5, 2, 1.5])
    with col_card:
        with st.container(border=True):
            st.markdown("<h2 style='text-align:center; color:#0d47a1;'>LOGIN USER</h2>", unsafe_allow_html=True)
            u = st.text_input("Username", placeholder="Masukkan Username")
            p = st.text_input("Password", type="password", placeholder="Masukkan Password")
            if st.button("MASUK KE DASHBOARD", use_container_width=True):
                if check_login(u, p):
                    st.session_state.login = True
                    st.rerun()
                else:
                    st.error("Login Gagal. Gunakan admin/admin")
    st.stop()

# ==================================
# Bagian 4: SIDEBAR (SELALU MUNCUL)
# ==================================
logo_b64 = get_base64_image("logo_sumut.png")
if logo_b64:
    st.sidebar.markdown(f"""
        <div style="display: flex; align-items: center; gap: 12px; padding-bottom: 20px;">
            <img src="data:image/png;base64,{logo_b64}" width="45">
            <span style="font-size: 18px; font-weight: 800; color: white; line-height: 1.1;">SI-PANDAI<br>SUMUT</span>
        </div>
    """, unsafe_allow_html=True)

# Filter hanya muncul di Dashboard Utama
if st.session_state.page_view == "dashboard":
    kab_pilih = st.sidebar.selectbox("Pilih Kabupaten / Kota", ["Semua"] + sorted(data_wilayah["kab_kota"].unique().tolist()))
else:
    st.sidebar.info("Sedang melihat Detail Sekolah")

st.sidebar.divider()
if st.sidebar.button("Logout 🚪", use_container_width=True):
    st.session_state.login = False
    st.rerun()

# ==================================
# Bagian 5: LOGIKA NAVIGASI HALAMAN
# ==================================

if st.session_state.page_view == "dashboard":
    # --- TAMPILAN A: DASHBOARD UTAMA ---
    st.markdown('<p style="font-size:26px; font-weight:800; color:#0d47a1; margin-bottom:0;">🚀 Dashboard Utama</p>', unsafe_allow_html=True)
    st.divider()

    df_filter = data_wilayah.copy()
    if kab_pilih != "Semua":
        df_filter = df_filter[df_filter["kab_kota"] == kab_pilih]

    # Matriks Capaian
    m1, m2, m3 = st.columns(3)
    if kab_pilih == "Semua":
        m1.metric("Total Penduduk Disabilitas", "6.732")
        m2.metric("Total Siswa Disabilitas", "4.573")
        m3.metric("Angka Partisipasi Sekolah", "67.93%")
    else:
        m1.metric("Penduduk Disabilitas", int(df_filter['jumlah_penduduk'].sum()))
        m2.metric("Siswa Belajar", int(df_filter['jumlah_siswa'].sum()))
        m3.metric("ATS Disabilitas", int(df_filter['ats_disabilitas'].sum()), delta_color="inverse")

    # --- KOTAK BALON SEKOLAH ---
    if kab_pilih != "Semua":
        st.divider()
        st.subheader(f"🏫 Satuan Pendidikan di {kab_pilih}")
        sekolah_wilayah = data_sekolah[data_sekolah['kab_kota'] == kab_pilih]
        
        if not sekolah_wilayah.empty:
            cols = st.columns(3)
            for i, row in enumerate(sekolah_wilayah.itertuples()):
                with cols[i % 3]:
                    # Membungkus sekolah dalam div kustom untuk shadow
                    st.markdown('<div class="school-card-container">', unsafe_allow_html=True)
                    
                    # 1. Label Rekomendasi
                    if row.jumlah_rombel > row.jumlah_ruang_kelas:
                        st.markdown(f"<div class='rec-box mendesak'>⚠️ MENDESAK: Butuh {row.jumlah_rombel - row.jumlah_ruang_kelas} RKB</div>", unsafe_allow_html=True)
                    elif row.rusak_berat > 0:
                        st.markdown(f"<div class='rec-box rehab'>🛠️ PRIORITAS REHAB: {row.rusak_berat} Ruang</div>", unsafe_allow_html=True)
                    else:
                        st.markdown("<div class='rec-box aman'>✅ KONDISI STABIL</div>", unsafe_allow_html=True)

                    # 2. Nama Sekolah sebagai Tombol Navigasi Halaman
                    if st.button(row.nama_sekolah, key=f"btn_{row.npsn}"):
                        st.session_state.selected_school_data = row._asdict()
                        st.session_state.page_view = "detail"
                        st.rerun()
                    
                    st.write(f"🆔 NPSN: {row.npsn}")
                    st.markdown('</div>', unsafe_allow_html=True)

    # --- PETA SEBARAN (VERSI FIX) ---
    st.divider()
    st.subheader("🗺️ Peta Pemetaan ATS Disabilitas")
    df_filter['map_size'] = df_filter['ats_disabilitas'] * 30
    st.map(df_filter, latitude="lat", longitude="lon", size="map_size")

else:
    # --- TAMPILAN B: HALAMAN DETAIL SEKOLAH ---
    sch = st.session_state.selected_school_data
    
    st.markdown('<div class="back-button">', unsafe_allow_html=True)
    if st.button("⬅️ Kembali ke Dashboard"):
        st.session_state.page_view = "dashboard"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown(f"<h1 style='color:#0d47a1; margin-top:20px;'>🏫 {sch['nama_sekolah']}</h1>", unsafe_allow_html=True)
    st.write(f"Wilayah: **{sch['kab_kota']}** | NPSN: **{sch['npsn']}**")
    st.divider()
    
    col_d1, col_d2 = st.columns(2)
    with col_d1:
        with st.container(border=True):
            st.subheader("📋 Profil Sekolah")
            st.write(f"**Status Satuan Pendidikan:** {sch['status']}")
            st.write(f"**Alamat Lengkap:** {sch['alamat']}")
            st.write(f"**Total Siswa Saat Ini:** {sch['jumlah_siswa']} Orang")
    
    with col_d2:
        with st.container(border=True):
            st.subheader("🏗️ Analisis Sarana Prasarana")
            st.write(f"**Kapasitas Rombel:** {sch['jumlah_rombel']}")
            st.write(f"**Ruang Kelas Tersedia:** {sch['jumlah_ruang_kelas']}")
            st.write(f"**Kondisi Bangunan:** {sch['rusak_berat']} Ruang Rusak Berat")
            
            # Analisis Singkat
            if sch['jumlah_rombel'] > sch['jumlah_ruang_kelas']:
                st.warning(f"Kekurangan: {sch['jumlah_rombel'] - sch['jumlah_ruang_kelas']} Ruang Kelas.")

    st.info("**Keterangan:** Data ini bersumber dari Spreadsheet Bidang Pembinaan PK Dinas Pendidikan Provinsi Sumatera Utara.")
