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
# Bagian 1: CSS CUSTOM (LOCKED & ENHANCED)
# ==================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&display=swap');
    html, body, [data-testid="stWidgetLabel"] { font-family: 'Inter', sans-serif !important; }
    [data-testid="stAppViewContainer"] { background-color: #f4f7f9 !important; }
    header {visibility: hidden;}

    /* SIDEBAR GRADASI */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d47a1 0%, #1565c0 100%) !important;
    }
    [data-testid="stSidebar"] * { color: white !important; }
    div[data-testid="stSelectbox"] div[data-baseweb="select"] * { color: #31333f !important; }

    /* MENU TABS */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; background-color: white; padding: 10px 20px; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
    .stTabs [data-baseweb="tab"] { height: 45px; background-color: #f8fafc; border-radius: 10px; color: #64748b; font-weight: 700; padding: 0 20px; }
    .stTabs [aria-selected="true"] { background-color: #0d47a1 !important; color: white !important; }

    /* CUSTOM METRIC CARD (KOTAK SEPERTI GAMBAR) */
    .metric-container {
        background: white;
        padding: 20px;
        border-radius: 12px;
        border-top: 5px solid #0d47a1;
        box-shadow: 0 4px 10px rgba(0,0,0,0.08);
        text-align: center;
        margin-bottom: 10px;
    }
    .metric-label { font-size: 14px; color: #64748b; font-weight: 600; margin-bottom: 5px; }
    .metric-value { font-size: 28px; color: #0d47a1; font-weight: 800; }
    .metric-delta { font-size: 12px; color: #15803d; font-weight: 700; margin-top: 5px; }

    /* KARTU SEKOLAH & BALON */
    [data-testid="stVerticalBlockBorderWrapper"] > div { background: white !important; border-radius: 15px !important; padding: 20px !important; border: 1px solid #e2e8f0 !important; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1) !important; }
    .rec-box { padding: 8px 12px; border-radius: 8px; font-size: 11px; font-weight: 700; margin-bottom: 12px; }
    .mendesak { background-color: #fee2e2 !important; color: #b91c1c !important; border-left: 5px solid #ef4444 !important; }
    .rehab { background-color: #fef3c7 !important; color: #b45309 !important; border-left: 5px solid #f59e0b !important; }
    .aman { background-color: #dcfce7 !important; color: #15803d !important; border-left: 5px solid #22c55e !important; }

    /* NAMA SEKOLAH */
    div.stButton > button[key^="btn_"] { background: transparent !important; color: #0d47a1 !important; font-size: 16px !important; font-weight: 800 !important; text-align: left !important; box-shadow: none !important; margin-bottom: -5px !important; }

    /* DOWNLOAD BUTTON */
    .stDownloadButton > button { background: linear-gradient(90deg, #2e7d32 0%, #4caf50 100%) !important; color: white !important; border-radius: 10px !important; font-weight: 700 !important; width: 100% !important; height: 48px !important; }
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

# --- FUNGSI TAMPILKAN KOTAK METRIC ---
def metric_card(label, value, delta=""):
    st.markdown(f"""
        <div class="metric-container">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-delta">{delta}</div>
        </div>
    """, unsafe_allow_html=True)

# =========================
# Bagian 3: HALAMAN LOGIN
# =========================
if "login" not in st.session_state: st.session_state.login = False

if not st.session_state.login:
    _, col_card, _ = st.columns([1, 1.5, 1])
    with col_card:
        with st.container(border=True):
            st.markdown("<h2 style='text-align:center; color:#0d47a1;'>LOGIN SI-PANDAI</h2>", unsafe_allow_html=True)
            u = st.text_input("Username", placeholder="Username")
            p = st.text_input("Password", type="password", placeholder="Password")
            if st.button("MASUK"):
                if u == "admin" and p == "admin":
                    st.session_state.login = True
                    st.rerun()
                else: st.error("Login Gagal")
    st.stop()

# ==================================
# Bagian 4: DASHBOARD & DETAIL
# ==================================

# SIDEBAR
st.sidebar.markdown(f"### 🏛️ PANEL KONTROL")
st.sidebar.write(f"👤 Role: **ADMIN**")
st.sidebar.divider()
opsi_kab = ["Semua"] + sorted(data_wilayah["kab_kota"].unique().tolist())
kab_pilih = st.sidebar.selectbox("Pilih Kabupaten / Kota", opsi_kab, key="selected_kab")
st.sidebar.divider()
df_dl = data_wilayah.copy() if kab_pilih == "Semua" else data_wilayah[data_wilayah["kab_kota"] == kab_pilih]
st.sidebar.download_button("Download Data (CSV) ⬇️", df_dl.to_csv(index=False).encode('utf-8'), f"data_sipandai_{kab_pilih}.csv", "text/csv")
st.sidebar.divider()
st.sidebar.button("Logout 🚪", use_container_width=True, on_click=proses_logout)

# MENU UTAMA
if st.session_state.page_view == "dashboard":
    tab_utama, tab_biodata, tab_bidang = st.tabs(["🚀 Dashboard Utama", "👤 Profil & Biodata", "🏛️ Informasi Bidang PK"])

    with tab_utama:
        st.markdown('<p style="font-size:24px; font-weight:800; color:#0d47a1;">📊 Monitoring ATS Disabilitas</p>', unsafe_allow_html=True)
        
        df_filter = data_wilayah.copy()
        if kab_pilih != "Semua":
            df_filter = df_filter[df_filter["kab_kota"] == kab_pilih]

        # --- MATRIX KOTAK (TILE STYLE) ---
        m1, m2, m3 = st.columns(3)
        if kab_pilih == "Semua":
            with m1: metric_card("Total Penduduk Disabilitas", "6.732")
            with m2: metric_card("Total Siswa Disabilitas", "4.573")
            with m3: metric_card("Angka Partisipasi Sekolah", "67.93%", "Target Sektoral")
        else:
            with m1: metric_card("Penduduk Disabilitas", f"{int(df_filter['jumlah_penduduk'].sum()):,}")
            with m2: metric_card("Siswa Belajar", f"{int(df_filter['jumlah_siswa'].sum()):,}")
            with m3: metric_card("Anak Tidak Sekolah (ATS)", f"{int(df_filter['ats_disabilitas'].sum()):,}", "Data Wilayah")

        # Daftar Sekolah
        if kab_pilih != "Semua":
            st.divider()
            st.subheader(f"🏫 Satuan Pendidikan di {kab_pilih}")
            sekolah_wilayah = data_sekolah[data_sekolah['kab_kota'] == kab_pilih]
            if not sekolah_wilayah.empty:
                cols_sch = st.columns(3)
                for i, row in enumerate(sekolah_wilayah.itertuples()):
                    with cols_sch[i % 3]:
                        with st.container(border=True):
                            if row.rusak_berat > 0: st.markdown(f"<div class='rec-box rehab'>🛠️ PRIORITAS REHAB: {row.rusak_berat} Ruang</div>", unsafe_allow_html=True)
                            elif row.jumlah_rombel > row.jumlah_ruang_kelas: st.markdown(f"<div class='rec-box mendesak'>⚠️ MENDESAK: Butuh RKB</div>", unsafe_allow_html=True)
                            else: st.markdown("<div class='rec-box aman'>✅ KONDISI STABIL</div>", unsafe_allow_html=True)
                            
                            if st.button(row.nama_sekolah.upper(), key=f"btn_{row.npsn}"):
                                st.session_state.selected_school_data = row._asdict()
                                st.session_state.page_view = "detail"
                                st.rerun()
                            st.caption(f"NPSN: {row.npsn}")

        # Visualisasi
        st.divider()
        cv1, cv2 = st.columns([1.5, 1])
        with cv1:
            st.subheader("🗺️ Peta Sebaran")
            df_filter['map_size'] = df_filter['ats_disabilitas'] * 30
            st.map(df_filter, latitude="lat", longitude="lon", size="map_size", use_container_width=True)
        with cv2:
            st.subheader("📊 Grafik ATS")
            df_chart = df_filter.sort_values("ats_disabilitas", ascending=False).head(10)
            fig = px.bar(df_chart, x='ats_disabilitas', y='kab_kota', orientation='h', color='ats_disabilitas', color_continuous_scale='Blues')
            fig.update_layout(height=350, margin=dict(l=0, r=0, t=0, b=0))
            st.plotly_chart(fig, use_container_width=True)

        # --- TABEL BERWARNA (THEMED) ---
        st.divider()
        with st.expander("📋 Lihat Detail Tabel Wilayah"):
            # Styling Tabel agar berwarna
            df_styled = df_filter[['kab_kota', 'jumlah_penduduk', 'jumlah_siswa', 'ats_disabilitas']].copy()
            df_styled.columns = ['Kabupaten/Kota', 'Penduduk Disabilitas', 'Siswa Aktif', 'ATS']
            
            st.dataframe(
                df_styled.style.set_properties(**{'background-color': '#f8fafc', 'color': '#334155', 'border-color': '#e2e8f0'})
                .set_table_styles([
                    {'selector': 'th', 'props': [('background-color', '#0d47a1'), ('color', 'white'), ('font-weight', 'bold')]}
                ]),
                use_container_width=True
            )

    with tab_biodata:
        st.markdown('<p style="font-size:24px; font-weight:800; color:#0d47a1;">👤 Profil Pengembang</p>', unsafe_allow_html=True)
        b1, b2 = st.columns([1, 2])
        with b1:
            with st.container(border=True):
                st.subheader("Biodata")
                st.write("**Nama:** Frayogi Aditiya")
                st.write("**Unit Kerja:** Dinas Pendidikan Prov. Sumut")
                st.write("**Mentor:** Faisyal Hartawan Isma, SE.")
        with b2:
            with st.container(border=True):
                st.subheader("🚀 Proyek Si-Cerdas")
                st.info("Sistem Cepat Lapor Data Pendidikan Sumut")
                st.write("Inovasi digital untuk optimalisasi pelaporan data sarpras dan ATS Disabilitas se-Sumatera Utara.")

    with tab_bidang:
        st.subheader("🏛️ Struktur Bidang PK")
        st.info("Bidang Pembinaan Pendidikan Khusus - Dinas Pendidikan Provsu")
        st.write("- **Fokus:** Koordinasi SLB se-Sumut & Pemetaan Data Sarpras.")

else:
    # HALAMAN DETAIL
    sch = st.session_state.selected_school_data
    if st.button("⬅️ Kembali ke Dashboard"):
        st.session_state.page_view = "dashboard"
        st.rerun()
    st.markdown(f"<h1 style='color:#0d47a1;'>🏫 {sch['nama_sekolah'].upper()}</h1>", unsafe_allow_html=True)
    st.divider()
    c1, c2 = st.columns(2)
    with c1:
        with st.container(border=True):
            st.subheader("📌 Profil Umum")
            st.write(f"**Jumlah Siswa:** {sch.get('jumlah_siswa', '0')} Orang")
            st.write(f"**Akses Internet:** {sch.get('akses_internet', '-')}")
    with c2:
        with st.container(border=True):
            st.subheader("🏗️ Sarana Prasarana")
            st.write(f"**Rusak Berat:** {sch['rusak_berat']} Ruang")
            st.write(f"**Daya Listrik:** {sch.get('daya_listrik', '-')}")
    st.markdown("<p style='font-size:10px; color:gray;'>Sumber: Bidang PK Provsu</p>", unsafe_allow_html=True)
