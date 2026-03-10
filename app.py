import streamlit as st
import pandas as pd
from PIL import Image
import os
from io import BytesIO
import plotly.express as px
import base64

# ==================================
# Bagian 0: KONFIGURASI HALAMAN
# ==================================
st.set_page_config(
    page_title="Login SI-PANDAI SUMUT",
    layout="wide",
    page_icon="🔒",
    initial_sidebar_state="expanded"
)

# Inisialisasi State untuk Navigasi Halaman
if "page" not in st.session_state:
    st.session_state.page = "dashboard"
if "selected_school" not in st.session_state:
    st.session_state.selected_school = None

# Fungsi Base64 untuk Logo Sidebar
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

# ==================================
# Bagian 1: CSS CUSTOM (SHADOW & COLOR SCHEME)
# ==================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&display=swap');
    html, body, [data-testid="stWidgetLabel"] { font-family: 'Inter', sans-serif !important; }
    [data-testid="stAppViewContainer"] { background-color: #f4f7f9 !important; }
    header {visibility: hidden;}

    /* Style Kotak Balon Sekolah dengan Shadow */
    .school-card-shadow {
        background: white !important;
        border-radius: 15px !important;
        padding: 20px !important;
        border: 1px solid #e2e8f0 !important;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05) !important;
        margin-bottom: 20px;
    }

    /* Styling Tombol Nama Sekolah (Biru & Tebal, Tanpa Panah) */
    div.stButton > button[key^="btn_"] {
        background: transparent !important;
        border: none !important;
        color: #0d47a1 !important;
        font-size: 18px !important;
        font-weight: 800 !important;
        padding: 0px !important;
        text-align: left !important;
        box-shadow: none !important;
        display: block !important;
    }
    div.stButton > button[key^="btn_"]:hover {
        color: #1e88e5 !important;
        text-decoration: underline !important;
    }

    /* Balon Rekomendasi Warna */
    .rec-box-mendesak {
        background-color: #fee2e2; color: #b91c1c; border-left: 5px solid #ef4444;
        padding: 8px 12px; border-radius: 8px; font-size: 12px; font-weight: 700; margin-bottom: 12px;
    }
    .rec-box-rehab {
        background-color: #fef3c7; color: #b45309; border-left: 5px solid #f59e0b;
        padding: 8px 12px; border-radius: 8px; font-size: 12px; font-weight: 700; margin-bottom: 12px;
    }
    .rec-box-aman {
        background-color: #dcfce7; color: #15803d; border-left: 5px solid #22c55e;
        padding: 8px 12px; border-radius: 8px; font-size: 12px; font-weight: 700; margin-bottom: 12px;
    }

    /* Default UI Elements */
    [data-testid="stVerticalBlockBorderWrapper"] > div {
        background: linear-gradient(180deg, #e3f2fd 0%, #ffffff 100%) !important;
        border-radius: 20px !important;
        border: 1px solid #cde4f7 !important;
        padding: 35px !important;
        box-shadow: 0px 10px 30px rgba(0,0,0,0.08) !important;
    }
    [data-testid="stSidebar"] { background: linear-gradient(180deg, #0d47a1 0%, #1565c0 100%) !important; }
    [data-testid="stSidebar"] * { color: white !important; }
    div[data-testid="stSelectbox"] div div { color: #333 !important; }
    section[data-testid="stSidebar"] div.stButton > button {
        background: linear-gradient(90deg, #ff9966 0%, #ff5e62 100%) !important;
        color: white !important; border-radius: 8px !important; font-weight: 700 !important; height: 40px; border: none !important;
    }
</style>
""", unsafe_allow_html=True)

# =========================
# Bagian 2: LOAD DATA MASTER
# =========================
@st.cache_data
def load_master_data():
    try:
        df_ats = pd.read_csv("master_data_si_pandai.csv")
        df_sekolah = pd.read_csv("master_data_sekolah.csv") if os.path.exists("master_data_sekolah.csv") else pd.DataFrame()
        return df_ats, df_sekolah
    except Exception as e:
        st.error(f"Gagal memuat data: {e}")
        return pd.DataFrame(), pd.DataFrame()

data, data_sekolah = load_master_data()

def check_login(u, p):
    return u == "admin" and p == "admin"

if "login" not in st.session_state:
    st.session_state.login = False
    st.session_state.role = "Admin"

# =========================
# Bagian 3: HALAMAN LOGIN
# =========================
if not st.session_state.login:
    st.markdown('<div style="display: flex; justify-content: center; padding-top: 30px; margin-bottom: 10px;">', unsafe_allow_html=True)
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
                u_in = st.text_input("Username", placeholder="👤 Masukkan Username", key="user_input", label_visibility="collapsed")
                p_in = st.text_input("Password", type="password", placeholder="🔑 Masukkan Password", key="pass_input", label_visibility="collapsed")
                if st.button("MASUK KE DASHBOARD", use_container_width=True):
                    if check_login(u_in, p_in):
                        st.session_state.login = True
                        st.rerun()
                    else:
                        st.error("Username atau Password Salah")
    st.stop()

# ==================================
# Bagian 4: DASHBOARD UTAMA (LOGIKA HALAMAN)
# ==================================

# --- SIDEBAR (Tetap Muncul di Semua Halaman) ---
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

if st.session_state.page == "dashboard":
    # --- FILTER (Hanya di Dashboard) ---
    st.sidebar.header("🔎 Filter")
    kab_pilih = st.sidebar.selectbox("Pilih Kabupaten / Kota", ["Semua"] + sorted(data["kab_kota"].unique().tolist()))
    df_filter = data.copy()
    if kab_pilih != "Semua":
        df_filter = df_filter[df_filter["kab_kota"] == kab_pilih]
else:
    # --- INFO DI SIDEBAR SAAT HALAMAN DETAIL ---
    st.sidebar.info("Sedang melihat detail sekolah. Klik tombol kembali di area utama untuk ke dashboard.")

st.sidebar.divider()
if st.sidebar.button("Logout 🚪", use_container_width=True):
    st.session_state.login = False
    st.rerun()

# ==================================
# Bagian 5: KONTEN UTAMA
# ==================================

if st.session_state.page == "dashboard":
    # --- TAMPILAN DASHBOARD ---
    st.markdown('<p style="font-size: 24px; font-weight: 800; color: #0d47a1; margin-bottom: 0px;">🚀 Dashboard Utama</p>', unsafe_allow_html=True)
    st.markdown('<p style="color: #546e7a; font-size: 14px; margin-top: -5px;">Sistem Informasi Pemetaan ATS Disabilitas Sumatera Utara</p>', unsafe_allow_html=True)
    st.divider()

    # MATRIKS
    m1, m2, m3 = st.columns(3)
    if kab_pilih == "Semua":
        m1.metric("Total Penduduk Disabilitas", "6.732", help="Sumber: LPPD PK 2025")
        m2.metric("Total Siswa Disabilitas", "4.573", help="Sumber: TIKP Provsu 2025")
        m3.metric("Angka Partisipasi Sekolah", "67.93%", delta="Target Sektoral")
    else:
        m1.metric("Penduduk Disabilitas", f"{int(df_filter['jumlah_penduduk'].sum()):,}")
        m2.metric("Siswa Belajar", f"{int(df_filter['jumlah_siswa'].sum()):,}")
        m3.metric("Anak Tidak Sekolah (ATS)", f"{int(df_filter['ats_disabilitas'].sum()):,}", delta_color="inverse")

    st.divider()

    # --- KOTAK BALON SEKOLAH ---
    if kab_pilih != "Semua":
        st.subheader(f"🏫 Daftar SLB di {kab_pilih}")
        sekolah_wilayah = data_sekolah[data_sekolah['kab_kota'] == kab_pilih]
        
        if not sekolah_wilayah.empty:
            cols = st.columns(3)
            for i, row in enumerate(sekolah_wilayah.itertuples()):
                with cols[i % 3]:
                    # Container Balon Kotak
                    st.markdown('<div class="school-card-shadow">', unsafe_allow_html=True)
                    
                    # 1. Rekomendasi
                    if row.jumlah_rombel > row.jumlah_ruang_kelas:
                        st.markdown(f"<div class='rec-box-mendesak'>⚠️ MENDESAK: Butuh {row.jumlah_rombel - row.jumlah_ruang_kelas} RKB</div>", unsafe_allow_html=True)
                    elif row.rusak_berat > 0:
                        st.markdown(f"<div class='rec-box-rehab'>🛠️ PRIORITAS: Rehab {row.rusak_berat} Ruang</div>", unsafe_allow_html=True)
                    else:
                        st.markdown("<div class='rec-box-aman'>✅ KONDISI STABIL</div>", unsafe_allow_html=True)

                    # 2. Nama Sekolah sebagai Tombol Pindah Halaman
                    if st.button(row.nama_sekolah, key=f"btn_{row.npsn}"):
                        st.session_state.page = "detail"
                        st.session_state.selected_school = row._asdict()
                        st.rerun()
                    
                    st.write(f"🆔 **NPSN:** {row.npsn}")
                    st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info(f"Belum ada data detail sekolah untuk {kab_pilih}")
        st.divider()

    # PETA & TABEL
    st.subheader("🗺️ Peta Pemetaan ATS Disabilitas")
    df_filter['map_size'] = df_filter['ats_disabilitas'].apply(lambda x: (x + 1) * 20) 
    st.map(df_filter, latitude="lat", longitude="lon", size="map_size")
    st.divider()
    st.subheader("📋 Detail Data per Wilayah")
    st.dataframe(df_filter[['kab_kota', 'jumlah_penduduk', 'jumlah_siswa', 'ats_disabilitas']], use_container_width=True)

else:
    # --- TAMPILAN HALAMAN DETAIL SEKOLAH ---
    sch = st.session_state.selected_school
    
    if st.button("⬅️ Kembali ke Dashboard"):
        st.session_state.page = "dashboard"
        st.rerun()
        
    st.markdown(f"<h1 style='color: #0d47a1; margin-bottom: 0px;'>🏫 {sch['nama_sekolah']}</h1>", unsafe_allow_html=True)
    st.write(f"Wilayah: **{sch['kab_kota']}** | NPSN: **{sch['npsn']}**")
    st.divider()
    
    col_d1, col_d2 = st.columns(2)
    with col_d1:
        with st.container(border=True):
            st.subheader("📌 Profil Umum")
            st.write(f"**Status Sekolah:** {sch['status']}")
            st.write(f"**Alamat:** {sch['alamat']}")
            st.write(f"**Jumlah Siswa:** {sch['jumlah_siswa']} Orang")
            
    with col_d2:
        with st.container(border=True):
            st.subheader("🏗️ Sarana Prasarana")
            st.write(f"**Jumlah Rombel:** {sch['jumlah_rombel']}")
            st.write(f"**Jumlah Ruang Kelas:** {sch['jumlah_ruang_kelas']}")
            st.write(f"**Rusak Sedang:** {sch['rusak_sedang']} Ruang")
            st.write(f"**Rusak Berat:** {sch['rusak_berat']} Ruang")

    st.markdown(f"""
        <div style="background-color: #e3f2fd; padding: 15px; border-radius: 10px; border-left: 5px solid #1565c0; margin-top: 20px;">
            <p style="font-size: 14px; color: #0d47a1; margin: 0;">
                <b>Rekomendasi Kebijakan:</b><br>
                Sekolah ini memerlukan perhatian pada aspek sarana prasarana sesuai dengan rekapitulasi data Bidang PK.
            </p>
        </div>
    """, unsafe_allow_html=True)

# Tombol Download (Hanya muncul di dashboard)
if st.session_state.page == "dashboard":
    csv_data = df_filter.to_csv(index=False).encode('utf-8')
    st.sidebar.download_button(
        label="Download Data (CSV) ⬇️",
        data=csv_data,
        file_name='data_si_pandai_filtered.csv',
        mime='text/csv',
        use_container_width=True
    )

