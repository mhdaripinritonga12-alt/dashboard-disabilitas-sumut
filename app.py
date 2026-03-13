import streamlit as st
import pandas as pd
import plotly.express as px
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

# --- FUNGSI RESET LOGOUT (FIX ERROR) ---
def proses_logout():
    st.session_state.selected_kab = "Semua"
    st.session_state.login = False
    st.session_state.page_view = "dashboard"

# Inisialisasi State
if "page_view" not in st.session_state:
    st.session_state.page_view = "dashboard"
if "selected_school_data" not in st.session_state:
    st.session_state.selected_school_data = None
if "selected_kab" not in st.session_state:
    st.session_state.selected_kab = "Semua"

def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

# ==================================
# Bagian 1: CSS CUSTOM (LOCKED & FIXED)
# ==================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&display=swap');
    html, body, [data-testid="stWidgetLabel"] { font-family: 'Inter', sans-serif !important; }
    [data-testid="stAppViewContainer"] { background-color: #f4f7f9 !important; }
    header {visibility: hidden;}
/* FIX: Jangan sembunyikan header total agar tombol sidebar muncul */
    header { background-color: rgba(0,0,0,0) !important; }
    [data-testid="stHeader"] { background: none !important; }
    /* SIDEBAR GRADASI */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d47a1 0%, #1565c0 100%) !important;
    }
    [data-testid="stSidebar"] * { color: white !important; }

    /* FIX: TULISAN DI FILTER (SELECTBOX) TETAP HITAM */
    div[data-testid="stSelectbox"] div[data-baseweb="select"] * {
        color: #31333f !important;
    }

    /* TOMBOL UTAMA & LOGIN */
    div.stButton > button:not([key^="btn_"]) {
        background: linear-gradient(90deg, #1565c0 0%, #1e88e5 100%) !important;
        color: white !important; border-radius: 10px !important; 
        font-weight: 700 !important; height: 48px; border: none !important;
        width: 100%;
    }

    /* KARTU SEKOLAH */
    [data-testid="stVerticalBlockBorderWrapper"] > div {
        background: white !important;
        border-radius: 15px !important;
        padding: 20px !important;
        border: 1px solid #e2e8f0 !important;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1) !important;
    }

    /* BALON STATUS WARNA */
    .rec-box { padding: 8px 12px; border-radius: 8px; font-size: 11px; font-weight: 700; margin-bottom: 12px; }
    .mendesak { background-color: #fee2e2 !important; color: #b91c1c !important; border-left: 5px solid #ef4444 !important; }
    .rehab { background-color: #fef3c7 !important; color: #b45309 !important; border-left: 5px solid #f59e0b !important; }
    .aman { background-color: #dcfce7 !important; color: #15803d !important; border-left: 5px solid #22c55e !important; }

    /* NAMA SEKOLAH (BIRU TEBAL) */
    div.stButton > button[key^="btn_"] {
        background: transparent !important; color: #0d47a1 !important;
        font-size: 16px !important; font-weight: 800 !important;
        padding: 0px !important; text-align: left !important;
        box-shadow: none !important; margin-bottom: -5px !important;
    }

    /* KOTAK SUMBER DATA */
    .source-box-ui {
        background-color: #e3f2fd !important; padding: 15px !important; 
        border-radius: 10px !important; border-left: 6px solid #0d47a1 !important; 
        margin-bottom: 25px !important;
    }

    /* TARGET SEKTORAL (HIJAU KECIL) */
    [data-testid="stMetricDelta"] > div {
        color: #15803d !important; font-size: 13px !important; font-weight: 700 !important;
    }
    [data-testid="stMetricDelta"] svg { display: none !important; }

    /* DOWNLOAD BUTTON (HIJAU) */
    .stDownloadButton > button {
        background: linear-gradient(90deg, #2e7d32 0%, #4caf50 100%) !important;
        color: white !important; border-radius: 10px !important; 
        font-weight: 700 !important; width: 100% !important; height: 48px !important;
    }

    /* LOGOUT */
    section[data-testid="stSidebar"] div.stButton > button {
        background: linear-gradient(90deg, #ff9966 0%, #ff5e62 100%) !important;
        height: 40px !important;
    }
</style>
""", unsafe_allow_html=True)

# ==================================
# Bagian 2: LOAD DATA
# ==================================
@st.cache_data
def load_all_data():
    try:
        df_ats = pd.read_csv("master_data_si_pandai.csv")
        df_sch = pd.read_csv("master_data_sekolah1.csv")
        return df_ats, df_sch
    except:
        return pd.DataFrame(), pd.DataFrame()

data_wilayah, data_sekolah = load_all_data()

# =========================
# Bagian 3: HALAMAN LOGIN
# =========================
if "login" not in st.session_state: st.session_state.login = False

if not st.session_state.login:
    _, col_logo, _ = st.columns([2, 0.6, 2])
    with col_logo:
        if os.path.exists("logo_sumut.png"): st.image("logo_sumut.png", width=100)
    
    _, col_card, _ = st.columns([1.5, 2, 1.5])
    with col_card:
        with st.container(border=True):
            col_l, col_r = st.columns([1, 1.5])
            with col_l:
                if os.path.exists("logo_sipandai.png"): st.image("logo_sipandai.png", use_container_width=True)
            with col_r:
                st.markdown("<h3 style='color:#0d47a1; margin-bottom:0;'>LOGIN USER</h3>", unsafe_allow_html=True)
                st.caption("Dashboard SI-PANDAI SUMUT")
                u = st.text_input("Username", placeholder="Username", label_visibility="collapsed")
                p = st.text_input("Password", type="password", placeholder="Password", label_visibility="collapsed")
                if st.button("MASUK KE DASHBOARD"):
                    if u == "admin" and p == "admin":
                        st.session_state.login = True
                        st.rerun()
                    else: st.error("Login Gagal")
    st.stop()

# ==================================
# Bagian 4: DASHBOARD & DETAIL
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

st.sidebar.write(f"👤 Role: **ADMIN**")
st.sidebar.divider()

st.sidebar.header("🔎 Filter")
opsi_kab = ["Semua"] + sorted(data_wilayah["kab_kota"].unique().tolist())
# Filter Kabupaten/Kota
kab_pilih = st.sidebar.selectbox("Pilih Kabupaten / Kota", opsi_kab, key="selected_kab")

st.sidebar.divider()
df_dl = data_wilayah.copy() if kab_pilih == "Semua" else data_wilayah[data_wilayah["kab_kota"] == kab_pilih]
csv_data = df_dl.to_csv(index=False).encode('utf-8')
st.sidebar.download_button("Download Data (CSV) ⬇️", csv_data, f"data_sipandai_{kab_pilih}.csv", "text/csv")

st.sidebar.divider()
st.sidebar.button("Logout 🚪", use_container_width=True, on_click=proses_logout)

# --- KONTEN DASHBOARD ---
if st.session_state.page_view == "dashboard":
    st.markdown('<p style="font-size:26px; font-weight:800; color:#0d47a1;">🚀 Dashboard Utama</p>', unsafe_allow_html=True)
    st.markdown('<p style="color: #546e7a; font-size: 14px; margin-top: -5px;">Sistem Informasi Pemetaan ATS Disabilitas Sumatera Utara</p>', unsafe_allow_html=True)
    st.divider()

    df_filter = data_wilayah.copy()
    if kab_pilih != "Semua":
        df_filter = df_filter[df_filter["kab_kota"] == kab_pilih]

    # 1. Matriks Capaian
    st.subheader("📌 Matriks Capaian Sektoral")
    st.markdown("""<div class="source-box-ui"><p style="font-size: 13px; color: #0d47a1; margin: 0;"><b>ℹ️ Sumber Data:</b> Bidang PK - LPPD & TIKP Provsu 2025</p></div>""", unsafe_allow_html=True)

    m1, m2, m3 = st.columns(3)
    if kab_pilih == "Semua":
        m1.metric("Total Penduduk Disabilitas", "6.732")
        m2.metric("Total Siswa Disabilitas", "4.573")
        m3.metric("Angka Partisipasi Sekolah", "67.93%", delta="Target Sektoral")
    else:
        m1.metric("Penduduk Disabilitas", int(df_filter['jumlah_penduduk'].sum()))
        m2.metric("Siswa Belajar", int(df_filter['jumlah_siswa'].sum()))
        m3.metric("Anak Tidak Sekolah (ATS)", int(df_filter['ats_disabilitas'].sum()), delta_color="inverse")

    # 2. Daftar Sekolah (POSISI DI BAWAH MATRIKS)
    if kab_pilih != "Semua":
        st.divider()
        st.subheader(f"🏫 Satuan Pendidikan di {kab_pilih}")
        sekolah_wilayah = data_sekolah[data_sekolah['kab_kota'] == kab_pilih]
        
        if not sekolah_wilayah.empty:
            cols_sch = st.columns(3)
            for i, row in enumerate(sekolah_wilayah.itertuples()):
                with cols_sch[i % 3]:
                    with st.container(border=True):
                        # BALON STATUS WARNA
                        if row.rusak_berat > 0:
                            st.markdown(f"<div class='rec-box rehab'>🛠️ PRIORITAS REHAB: {row.rusak_berat} Ruang</div>", unsafe_allow_html=True)
                        elif row.jumlah_rombel > row.jumlah_ruang_kelas:
                            st.markdown(f"<div class='rec-box mendesak'>⚠️ MENDESAK: Butuh RKB</div>", unsafe_allow_html=True)
                        else:
                            st.markdown("<div class='rec-box aman'>✅ KONDISI STABIL</div>", unsafe_allow_html=True)
                        
                        # NAMA SEKOLAH (HURUF BESAR)
                        if st.button(row.nama_sekolah.upper(), key=f"btn_{row.npsn}"):
                            st.session_state.selected_school_data = row._asdict()
                            st.session_state.page_view = "detail"
                            st.rerun()
                        st.caption(f"NPSN: {row.npsn}")

    # 3. Visualisasi
    st.divider()
    cv1, cv2 = st.columns([1.5, 1])
    with cv1:
        st.subheader("🗺️ Peta Sebaran ATS")
        df_filter['map_size'] = df_filter['ats_disabilitas'] * 30
        st.map(df_filter, latitude="lat", longitude="lon", size="map_size", use_container_width=True)
    with cv2:
        st.subheader("📊 Grafik ATS Wilayah")
        df_chart = df_filter.sort_values("ats_disabilitas", ascending=False).head(10)
        fig = px.bar(df_chart, x='ats_disabilitas', y='kab_kota', orientation='h', color='ats_disabilitas', color_continuous_scale='Blues')
        fig.update_layout(height=350, margin=dict(l=0, r=0, t=0, b=0))
        st.plotly_chart(fig, use_container_width=True)

    st.divider()
    with st.expander("📋 Lihat Detail Tabel"):
        st.dataframe(df_filter[['kab_kota', 'jumlah_penduduk', 'jumlah_siswa', 'ats_disabilitas']], use_container_width=True)

else:
    # --- HALAMAN DETAIL ---
    sch = st.session_state.selected_school_data
    if st.button("⬅️ Kembali ke Dashboard"):
        st.session_state.page_view = "dashboard"
        st.rerun()
    
    # NAMA SEKOLAH DETAIL (HURUF BESAR)
    st.markdown(f"<h1 style='color:#0d47a1; margin-bottom:0;'>🏫 {sch['nama_sekolah'].upper()}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='color:#546e7a; font-size:16px;'>Wilayah: <b>{sch['kab_kota']}</b> | NPSN: <b>{sch['npsn']}</b></p>", unsafe_allow_html=True)
    st.divider()
    
    c1, c2 = st.columns(2)
    with c1:
        with st.container(border=True):
            st.subheader("📌 Profil Umum")
            st.write(f"**Status:** {sch['status']}")
            st.write(f"**Alamat:** {sch['alamat']}")
            st.write(f"**Jumlah Siswa:** {sch.get('jumlah_siswa', '0')} Orang")
            st.write(f"**Akses Internet:** {sch.get('akses_internet', '-')}")
    with c2:
        with st.container(border=True):
            st.subheader("🏗️ Sarana Prasarana")
            st.write(f"**Rombel:** {sch['jumlah_rombel']}")
            st.write(f"**Ruang Kelas:** {sch['jumlah_ruang_kelas']}")
            st.write(f"**Rusak Berat:** {sch['rusak_berat']} Ruang")
            st.write(f"**Daya Listrik:** {sch.get('daya_listrik', '-')}")

    st.markdown("""<div class="source-box-ui"><p style="font-size: 14px; color: #0d47a1; margin: 0;"><b>Rekomendasi:</b> Sekolah ini memerlukan perhatian pada digitalisasi & sarpras sesuai data Bidang PK.</p></div><p style='font-size:10px; color:gray;'>Sumber: Data Kerusakan & Sarpras Bidang PK</p>""", unsafe_allow_html=True)

