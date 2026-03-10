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

# --- FUNGSI RESET LOGOUT ---
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
# Bagian 1: CSS CUSTOM (LOCKED & PRO UI)
# ==================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&display=swap');
    html, body, [data-testid="stWidgetLabel"] { font-family: 'Inter', sans-serif !important; }
    [data-testid="stAppViewContainer"] { background-color: #f8fafc !important; }
    header {visibility: hidden;}

    /* SIDEBAR */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d47a1 0%, #1565c0 100%) !important;
    }
    [data-testid="stSidebar"] * { color: white !important; }

    /* TOMBOL UTAMA */
    div.stButton > button:not([key^="btn_"]) {
        background: linear-gradient(90deg, #1565c0 0%, #1e88e5 100%) !important;
        color: white !important; border-radius: 10px !important; 
        font-weight: 700 !important; height: 45px; border: none !important;
        width: 100%;
    }

    /* KARTU VISUALISASI */
    .viz-card {
        background: white;
        border-radius: 15px;
        padding: 20px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }

    /* KOTAK BALON SEKOLAH */
    [data-testid="stVerticalBlockBorderWrapper"] > div {
        background: white !important;
        border-radius: 15px !important;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1) !important;
    }

    /* NAMA SEKOLAH */
    div.stButton > button[key^="btn_"] {
        background: transparent !important; color: #0d47a1 !important;
        font-size: 16px !important; font-weight: 800 !important;
        text-align: left !important; border: none !important;
    }

    /* SOURCE BOX */
    .source-box-ui {
        background-color: #e3f2fd !important; padding: 15px !important; 
        border-radius: 10px !important; border-left: 6px solid #0d47a1 !important; 
        margin-bottom: 20px !important;
    }

    /* METRIC DELTA */
    [data-testid="stMetricDelta"] > div { color: #15803d !important; font-size: 13px !important; }
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
# Bagian 3: LOGIN (LOCKED)
# =========================
if "login" not in st.session_state: st.session_state.login = False
if not st.session_state.login:
    _, col_card, _ = st.columns([1, 1.5, 1])
    with col_card:
        with st.container(border=True):
            st.markdown("<h3 style='text-align:center; color:#0d47a1;'>SI-PANDAI SUMUT</h3>", unsafe_allow_html=True)
            u = st.text_input("Username")
            p = st.text_input("Password", type="password")
            if st.button("LOGIN"):
                if u == "admin" and p == "admin":
                    st.session_state.login = True
                    st.rerun()
                else: st.error("Akses Ditolak")
    st.stop()

# ==================================
# Bagian 4: SIDEBAR
# ==================================
st.sidebar.markdown(f"### 🏛️ DASHBOARD PANEL")
st.sidebar.write(f"👤 User: **Frayogi Aditiya**")
opsi_kab = ["Semua"] + sorted(data_wilayah["kab_kota"].unique().tolist())
kab_pilih = st.sidebar.selectbox("Pilih Wilayah", opsi_kab, key="selected_kab")

# Ekspor Data
csv_data = data_wilayah.to_csv(index=False).encode('utf-8')
st.sidebar.download_button("Download Data (CSV) ⬇️", csv_data, f"data_{kab_pilih}.csv", "text/csv")
st.sidebar.divider()
st.sidebar.button("Logout 🚪", use_container_width=True, on_click=proses_logout)

# ==================================
# Bagian 5: KONTEN DASHBOARD
# ==================================
if st.session_state.page_view == "dashboard":
    st.markdown('<h2 style="color:#0d47a1;">🚀 Pemetaan Sektoral & ATS Disabilitas</h2>', unsafe_allow_html=True)
    
    # --- ROW 1: METRICS ---
    df_f = data_wilayah.copy() if kab_pilih == "Semua" else data_wilayah[data_wilayah["kab_kota"] == kab_pilih]
    m1, m2, m3 = st.columns(3)
    with m1: st.metric("Populasi Disabilitas", f"{int(df_f['jumlah_penduduk'].sum()):,}")
    with m2: st.metric("Siswa Aktif", f"{int(df_f['jumlah_siswa'].sum()):,}")
    with m3: st.metric("ATS Disabilitas", f"{int(df_f['ats_disabilitas'].sum()):,}", delta="Target Penurunan", delta_color="inverse")

    st.markdown('<div class="source-box-ui"><b>ℹ️ Sumber:</b> Bidang PK - LPPD & Dapodik TIKP Provsu 2025</div>', unsafe_allow_html=True)

    # --- ROW 2: GIS MAP & BAR CHART (PROFESIONAL) ---
    col_map, col_chart = st.columns([1.2, 1])
    
    with col_map:
        st.markdown('<p style="font-weight:700; margin-bottom:5px;">📍 Sebaran Geografis ATS</p>', unsafe_allow_html=True)
        # Map lebih kecil & profesional
        st.map(df_f, latitude="lat", longitude="lon", size=df_f["ats_disabilitas"]*20, use_container_width=True)

    with col_chart:
        st.markdown('<p style="font-weight:700; margin-bottom:5px;">📊 Statistik ATS per Wilayah</p>', unsafe_allow_html=True)
        fig_ats = px.bar(
            df_f.sort_values("ats_disabilitas", ascending=False).head(10),
            x="ats_disabilitas", y="kab_kota", orientation='h',
            color="ats_disabilitas", color_continuous_scale="Blues",
            labels={"ats_disabilitas": "Jumlah ATS", "kab_kota": ""},
            template="plotly_white", height=300
        )
        fig_ats.update_layout(margin=dict(l=0, r=0, t=0, b=0), showlegend=False)
        st.plotly_chart(fig_ats, use_container_width=True)

    # --- ROW 3: SEKOLAH (JIKA FILTER TERPILIH) ---
    if kab_pilih != "Semua":
        st.divider()
        st.subheader(f"🏫 Satuan Pendidikan: {kab_pilih}")
        df_sch_f = data_sekolah[data_sekolah['kab_kota'] == kab_pilih]
        
        if not df_sch_f.empty:
            cols = st.columns(3)
            for i, row in enumerate(df_sch_f.itertuples()):
                with cols[i % 3]:
                    with st.container(border=True):
                        if row.rusak_berat > 0: st.markdown("<span style='color:red; font-size:12px;'>⚠️ Rusak Berat</span>", unsafe_allow_html=True)
                        else: st.markdown("<span style='color:green; font-size:12px;'>✅ Kondisi Aman</span>", unsafe_allow_html=True)
                        
                        if st.button(row.nama_sekolah, key=f"btn_{row.npsn}"):
                            st.session_state.selected_school_data = row._asdict()
                            st.session_state.page_view = "detail"
                            st.rerun()
                        st.caption(f"NPSN: {row.npsn}")

    # --- ROW 4: TABEL DATA ---
    st.divider()
    with st.expander("📋 Lihat Detail Tabel Wilayah"):
        st.dataframe(df_f[['kab_kota', 'jumlah_penduduk', 'jumlah_siswa', 'ats_disabilitas']], use_container_width=True)

else:
    # --- HALAMAN DETAIL (LOCKED) ---
    sch = st.session_state.selected_school_data
    if st.button("⬅️ Kembali ke Dashboard"):
        st.session_state.page_view = "dashboard"
        st.rerun()
    
    st.header(f"🏫 {sch['nama_sekolah']}")
    st.write(f"📍 {sch['alamat']} | NPSN: **{sch['npsn']}**")
    
    c1, c2 = st.columns(2)
    with c1:
        with st.container(border=True):
            st.subheader("📌 Fasilitas & Siswa")
            st.write(f"Siswa: **{sch['jumlah_siswa']}**")
            st.write(f"Internet: **{sch.get('akses_internet', '-')}**")
            st.write(f"Listrik: **{sch.get('daya_listrik', '-')}**")
    with c2:
        with st.container(border=True):
            st.subheader("🏗️ Prasarana")
            st.write(f"Ruang Kelas: **{sch['jumlah_ruang_kelas']}**")
            st.write(f"Rusak Berat: **{sch['rusak_berat']}**")
            st.write(f"Rombel: **{sch['jumlah_rombel']}**")

    st.markdown('<p style="font-size:10px; color:gray;">Sumber: Data Kerusakan & Sarpras Bidang PK</p>', unsafe_allow_html=True)
