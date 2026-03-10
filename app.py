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
    initial_sidebar_state="expanded"
)

# Inisialisasi State Navigasi & Memori Filter
if "page_view" not in st.session_state:
    st.session_state.page_view = "dashboard"
if "selected_school_data" not in st.session_state:
    st.session_state.selected_school_data = None
# State untuk mengunci pilihan kabupaten
if "selected_kab" not in st.session_state:
    st.session_state.selected_kab = "Semua"

def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

# ==================================
# Bagian 1: CSS CUSTOM (LOCKED)
# ==================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&display=swap');
    html, body, [data-testid="stWidgetLabel"] { font-family: 'Inter', sans-serif !important; }
    [data-testid="stAppViewContainer"] { background-color: #f4f7f9 !important; }
    header {visibility: hidden;}

    /* SIDEBAR GRADASI ASLI */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d47a1 0%, #1565c0 100%) !important;
    }
    [data-testid="stSidebar"] * { color: white !important; }
    div[data-testid="stSelectbox"] div div { color: #333 !important; }

    /* TOMBOL LOGIN (GRADASI BIRU) */
    div.stButton > button:not([key^="btn_"]) {
        background: linear-gradient(90deg, #1565c0 0%, #1e88e5 100%) !important;
        color: white !important; border-radius: 10px !important; 
        font-weight: 700 !important; height: 48px; border: none !important;
        width: 100%;
    }

    /* KOTAK BALON SEKOLAH (SHADOW) */
    [data-testid="stVerticalBlockBorderWrapper"] > div {
        background: white !important;
        border-radius: 15px !important;
        padding: 20px !important;
        border: 1px solid #e2e8f0 !important;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1) !important;
    }

    /* NAMA SEKOLAH (BIRU TEBAL) */
    div.stButton > button[key^="btn_"] {
        background: transparent !important;
        border: none !important;
        color: #0d47a1 !important;
        font-size: 18px !important;
        font-weight: 800 !important;
        padding: 0px !important;
        text-align: left !important;
        box-shadow: none !important;
        margin-bottom: -10px !important;
    }
    div.stButton > button[key^="btn_"]:hover {
        color: #1e88e5 !important;
        text-decoration: underline !important;
    }

    /* BALON REKOMENDASI */
    .rec-box { padding: 8px 12px; border-radius: 8px; font-size: 11px; font-weight: 700; margin-bottom: 12px; }
    .mendesak { background-color: #fee2e2; color: #b91c1c; border-left: 5px solid #ef4444; }
    .rehab { background-color: #fef3c7; color: #b45309; border-left: 5px solid #f59e0b; }
    .aman { background-color: #dcfce7; color: #15803d; border-left: 5px solid #22c55e; }

    /* INFO BOX DETAIL */
    .detail-info-box {
        background-color: #e3f2fd; padding: 15px; border-radius: 10px; 
        border-left: 5px solid #1565c0; margin-top: 20px;
    }

    /* LOGOUT & BACK BUTTON */
    section[data-testid="stSidebar"] div.stButton > button {
        background: linear-gradient(90deg, #ff9966 0%, #ff5e62 100%) !important;
        height: 40px !important;
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
# Bagian 3: HALAMAN LOGIN (LOCKED)
# =========================
if "login" not in st.session_state: st.session_state.login = False

if not st.session_state.login:
    _, col_logo, _ = st.columns([2, 0.6, 2])
    with col_logo:
        if os.path.exists("logo_sumut.png"):
            st.image("logo_sumut.png", width=100)
    
    _, col_card, _ = st.columns([1.5, 2, 1.5])
    with col_card:
        with st.container(border=True):
            col_l, col_r = st.columns([1, 1.5])
            with col_l:
                if os.path.exists("logo_sipandai.png"):
                    st.image("logo_sipandai.png", use_container_width=True)
            with col_r:
                st.markdown("<h3 style='color:#0d47a1; margin-bottom:0;'>LOGIN USER</h3>", unsafe_allow_html=True)
                st.caption("Dashboard SI-PANDAI SUMUT")
                u = st.text_input("Username", placeholder="Username", label_visibility="collapsed")
                p = st.text_input("Password", type="password", placeholder="Password", label_visibility="collapsed")
                if st.button("MASUK KE DASHBOARD"):
                    if u == "admin" and p == "admin":
                        st.session_state.login = True
                        st.rerun()
                    else:
                        st.error("Login Gagal")
    st.stop()

# ==================================
# Bagian 4: DASHBOARD UTAMA & DETAIL
# ==================================

# --- SIDEBAR (SESUAI GAMBAR 87b987) ---
logo_b64 = get_base64_image("logo_sumut.png")
if logo_b64:
    st.sidebar.markdown(f"""
        <div style="display: flex; align-items: center; gap: 12px; padding-bottom: 20px;">
            <img src="data:image/png;base64,{logo_b64}" width="45">
            <span style="font-size: 18px; font-weight: 800; color: white; line-height: 1.1;">SI-PANDAI<br>SUMUT</span>
        </div>
    """, unsafe_allow_html=True)

st.sidebar.write(f"👤 Role: **ADMIN**")
st.sidebar.divider()

# FILTER DIKELUARKAN AGAR TERKUNCI (MEMORY FILTER AKTIF)
st.sidebar.header("🔎 Filter")
opsi_kab = ["Semua"] + sorted(data_wilayah["kab_kota"].unique().tolist())
kab_pilih = st.sidebar.selectbox(
    "Pilih Kabupaten / Kota", 
    opsi_kab, 
    key="selected_kab" # KUNCI PILIHAN DI SINI
)

st.sidebar.divider()
if st.sidebar.button("Logout 🚪", use_container_width=True):
    st.session_state.selected_kab = "Semua"
    st.session_state.login = False
    st.rerun()

# --- KONTEN HALAMAN ---
if st.session_state.page_view == "dashboard":
    st.markdown('<p style="font-size:26px; font-weight:800; color:#0d47a1;">🚀 Dashboard Utama</p>', unsafe_allow_html=True)
    st.markdown('<p style="color: #546e7a; font-size: 14px; margin-top: -5px;">Sistem Informasi Pemetaan ATS Disabilitas Sumatera Utara</p>', unsafe_allow_html=True)
    st.divider()

    df_filter = data_wilayah.copy()
    if kab_pilih != "Semua":
        df_filter = df_filter[df_filter["kab_kota"] == kab_pilih]

    # Matriks
    st.subheader("📌 Matriks Capaian Sektoral")
    m1, m2, m3 = st.columns(3)
    if kab_pilih == "Semua":
        m1.metric("Total Penduduk Disabilitas", "6.732", help="Sumber: LPPD PK 2025")
        m2.metric("Total Siswa Disabilitas", "4.573", help="Sumber: TIKP Provsu 2025")
        m3.metric("Angka Partisipasi Sekolah", "67.93%", delta="Target Sektoral")
    else:
        m1.metric("Penduduk Disabilitas", int(df_filter['jumlah_penduduk'].sum()))
        m2.metric("Siswa Belajar", int(df_filter['jumlah_siswa'].sum()))
        m3.metric("Anak Tidak Sekolah (ATS)", int(df_filter['ats_disabilitas'].sum()), delta_color="inverse")

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

                        if st.button(row.nama_sekolah, key=f"btn_{row.npsn}"):
                            st.session_state.selected_school_data = row._asdict()
                            st.session_state.page_view = "detail"
                            st.rerun()
                        st.markdown(f"<p style='color:#64748b; font-size:13px; margin-top:-10px;'>🆔 NPSN: {row.npsn}</p>", unsafe_allow_html=True)

    st.divider()
    # Peta
    st.subheader("🗺️ Peta Pemetaan ATS Disabilitas")
    df_filter['map_size'] = df_filter['ats_disabilitas'] * 30
    st.map(df_filter, latitude="lat", longitude="lon", size="map_size")

    # TABEL DETAIL DATA PER WILAYAH
    st.divider()
    st.subheader("📋 Detail Data per Wilayah")
    st.dataframe(
        df_filter[['kab_kota', 'jumlah_penduduk', 'jumlah_siswa', 'ats_disabilitas']],
        use_container_width=True,
        column_config={
            "kab_kota": "Kabupaten / Kota",
            "jumlah_penduduk": "Populasi Disabilitas",
            "jumlah_siswa": "Siswa Belajar",
            "ats_disabilitas": "ATS (Gap)"
        }
    )

else:
    # HALAMAN DETAIL
    sch = st.session_state.selected_school_data
    if st.button("⬅️ Kembali ke Dashboard"):
        st.session_state.page_view = "dashboard"
        st.rerun()
    
    st.markdown(f"<h1 style='color:#0d47a1; margin-bottom:0;'>🏫 {sch['nama_sekolah']}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='color:#546e7a; font-size:16px;'>Wilayah: <b>{sch['kab_kota']}</b> | NPSN: <b>{sch['npsn']}</b></p>", unsafe_allow_html=True)
    st.divider()
    
    col1, col2 = st.columns(2)
    with col1:
        with st.container(border=True):
            st.subheader("📌 Profil Umum")
            st.write(f"**Status Sekolah:** {sch['status']}")
            st.write(f"**Alamat:** {sch['alamat']}")
            st.write(f"**Jumlah Siswa:** {sch['jumlah_siswa']} Orang")
            
    with col2:
        with st.container(border=True):
            st.subheader("🏗️ Sarana Prasarana")
            st.write(f"**Jumlah Rombel:** {sch['jumlah_rombel']}")
            st.write(f"**Jumlah Ruang Kelas:** {sch['jumlah_ruang_kelas']}")
            st.write(f"**Rusak Sedang:** {sch['rusak_sedang']} Ruang")
            st.write(f"**Rusak Berat:** {sch['rusak_berat']} Ruang")

    st.markdown(f"""
        <div class="detail-info-box">
            <p style="font-size: 14px; color: #0d47a1; margin: 0;">
                <b>Rekomendasi Kebijakan:</b><br>
                Sekolah ini memerlukan perhatian pada aspek sarana prasarana sesuai dengan rekapitulasi data Bidang PK.
            </p>
        </div>
        <p style='font-size:10px; color:gray; margin-top:10px;'>Sumber: Data Kerusakan & Sarpras Bidang PK</p>
    """, unsafe_allow_html=True)
