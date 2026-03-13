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
# Bagian 1: CSS CUSTOM (LOCKED & VIVID)
# ==================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&display=swap');
    html, body, [data-testid="stWidgetLabel"] { font-family: 'Inter', sans-serif !important; }
    [data-testid="stAppViewContainer"] { background-color: #f4f7f9 !important; }
    header {visibility: hidden;}

    /* SIDEBAR NAVY GRADASI */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d47a1 0%, #1565c0 100%) !important;
    }
    [data-testid="stSidebar"] * { color: white !important; }
    div[data-testid="stSelectbox"] div[data-baseweb="select"] * { color: #31333f !important; }

    /* MENU TABS */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; background-color: white; padding: 10px 20px; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
    .stTabs [aria-selected="true"] { background-color: #0d47a1 !important; color: white !important; border-radius: 10px; }

    /* MATRIX KOTAK (TILE STYLE) */
    .metric-box {
        background: white; padding: 25px; border-radius: 15px;
        border-top: 6px solid #0d47a1; box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        text-align: center; margin-bottom: 20px;
    }
    .m-label { font-size: 14px; color: #64748b; font-weight: 700; text-transform: uppercase; margin-bottom: 10px; }
    .m-value { font-size: 32px; color: #0d47a1; font-weight: 800; }

    /* KARTU SEKOLAH & BALON WARNA TAJAM */
    [data-testid="stVerticalBlockBorderWrapper"] > div { background: white !important; border-radius: 15px !important; padding: 20px !important; border: 1px solid #e2e8f0 !important; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1) !important; }
    .rec-box { padding: 10px 15px; border-radius: 8px; font-size: 12px; font-weight: 800; margin-bottom: 15px; text-align: center; }
    .mendesak { background-color: #ff3333 !important; color: white !important; border-left: 6px solid #990000 !important; }
    .rehab { background-color: #ffcc00 !important; color: #663300 !important; border-left: 6px solid #cc9900 !important; }
    .aman { background-color: #22c55e !important; color: white !important; border-left: 6px solid #166534 !important; }

    /* TOMBOL DOWNLOAD (HIJAU) */
    .stDownloadButton > button { background: linear-gradient(90deg, #2e7d32 0%, #4caf50 100%) !important; color: white !important; border-radius: 10px !important; font-weight: 700 !important; width: 100% !important; height: 48px !important; }
    
    /* NAMA SEKOLAH BUTTON */
    div.stButton > button[key^="btn_"] { background: transparent !important; color: #0d47a1 !important; font-size: 17px !important; font-weight: 800 !important; text-align: left !important; box-shadow: none !important; }
</style>
""", unsafe_allow_html=True)

# --- FUNGSI DRAW MATRIX ---
def draw_matrix(label, value):
    st.markdown(f"""
        <div class="metric-box">
            <div class="m-label">{label}</div>
            <div class="m-value">{value}</div>
        </div>
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
# Bagian 3: LOGIN
# =========================
if "login" not in st.session_state: st.session_state.login = False
if not st.session_state.login:
    _, col_card, _ = st.columns([1, 1.2, 1])
    with col_card:
        with st.container(border=True):
            st.markdown("<h2 style='text-align:center; color:#0d47a1;'>LOGIN SI-PANDAI</h2>", unsafe_allow_html=True)
            u = st.text_input("Username", placeholder="Username")
            p = st.text_input("Password", type="password", placeholder="Password")
            if st.button("MASUK KE DASHBOARD"):
                if u == "admin" and p == "admin":
                    st.session_state.login = True
                    st.rerun()
                else: st.error("Login Gagal")
    st.stop()

# ==================================
# Bagian 4: DASHBOARD & NAVIGASI
# ==================================

# --- SIDEBAR ---
st.sidebar.markdown(f"### 🏛️ PANEL KONTROL")
st.sidebar.write(f"👤 User: **FRAYOGI ADITIYA**")
st.sidebar.divider()
opsi_kab = ["Semua"] + sorted(data_wilayah["kab_kota"].unique().tolist())
kab_pilih = st.sidebar.selectbox("Pilih Kabupaten / Kota", opsi_kab, key="selected_kab")
st.sidebar.divider()
df_dl = data_wilayah.copy() if kab_pilih == "Semua" else data_wilayah[data_wilayah["kab_kota"] == kab_pilih]
st.sidebar.download_button("Download Data (CSV) ⬇️", df_dl.to_csv(index=False).encode('utf-8'), f"data_sipandai_{kab_pilih}.csv", "text/csv")
st.sidebar.divider()
st.sidebar.button("Logout 🚪", use_container_width=True, on_click=proses_logout)

# --- MENU TABS ---
if st.session_state.page_view == "dashboard":
    tab_utama, tab_biodata, tab_bidang = st.tabs(["🚀 DASHBOARD UTAMA", "👤 BIODATA PENGEMBANG", "🏛️ INFORMASI BIDANG PK"])

    with tab_utama:
        st.markdown('<p style="font-size:24px; font-weight:800; color:#0d47a1;">📊 Monitoring ATS Disabilitas Sumatera Utara</p>', unsafe_allow_html=True)
        
        df_f = data_wilayah.copy() if kab_pilih == "Semua" else data_wilayah[data_wilayah["kab_kota"] == kab_pilih]

        # 1. MATRIX KOTAK (TILE)
        st.subheader("📌 Matriks Capaian Sektoral")
        m1, m2, m3 = st.columns(3)
        if kab_pilih == "Semua":
            with m1: draw_matrix("Penduduk Disabilitas", "6.732")
            with m2: draw_matrix("Siswa Belajar", "4.573")
            with m3: draw_matrix("APS (Angka Partisipasi)", "67.93%")
        else:
            with m1: draw_matrix("Penduduk Disabilitas", f"{int(df_f['jumlah_penduduk'].sum()):,}")
            with m2: draw_matrix("Siswa Belajar", f"{int(df_f['jumlah_siswa'].sum()):,}")
            with m3: draw_matrix("ATS Disabilitas", f"{int(df_f['ats_disabilitas'].sum()):,}")

        # 2. PETA LOKASI RIIL (SATELIT HIDUP)
        st.divider()
        st.subheader("🗺️ Visualisasi Lokasi Riil (Citra Satelit)")
        st.info("💡 Gunakan Mouse Wheel untuk Zoom In. Anda bisa melihat bangunan sekolah dan kondisi wilayah secara nyata.")
        
        fig_map = px.scatter_mapbox(
            df_f, lat="lat", lon="lon", size="ats_disabilitas",
            color="ats_disabilitas", color_continuous_scale="Reds",
            size_max=20, zoom=7, mapbox_style="open-street-map"
        )
        # Menambahkan Citra Satelit Berwarna (Vivid)
        fig_map.update_layout(
            mapbox_layers=[{
                "below": 'traces', "sourcetype": "raster",
                "source": ["https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"]
            }],
            margin={"r":0,"t":0,"l":0,"b":0}, height=500
        )
        st.plotly_chart(fig_map, use_container_width=True)

        # 3. DAFTAR SEKOLAH (BALON WARNA TAJAM)
        if kab_pilih != "Semua":
            st.divider()
            st.subheader(f"🏫 Satuan Pendidikan di {kab_pilih}")
            sch_wil = data_sekolah[data_sekolah['kab_kota'] == kab_pilih]
            cols = st.columns(3)
            for i, row in enumerate(sch_wil.itertuples()):
                with cols[i % 3]:
                    with st.container(border=True):
                        if row.rusak_berat > 0: st.markdown(f"<div class='rec-box mendesak'>⚠️ PRIORITAS REHAB: {row.rusak_berat} RUANG</div>", unsafe_allow_html=True)
                        else: st.markdown("<div class='rec-box aman'>✅ KONDISI STABIL</div>", unsafe_allow_html=True)
                        
                        if st.button(row.nama_sekolah.upper(), key=f"btn_{row.npsn}"):
                            st.session_state.selected_school_data = row._asdict()
                            st.session_state.page_view = "detail"
                            st.rerun()
                        st.caption(f"🆔 NPSN: {row.npsn}")

        # 4. TABEL BERWARNA
        st.divider()
        with st.expander("📋 Tabel Detail Data Wilayah"):
            st.dataframe(
                df_f[['kab_kota', 'jumlah_penduduk', 'jumlah_siswa', 'ats_disabilitas']]
                .style.set_table_styles([{'selector': 'th', 'props': [('background-color', '#0d47a1'), ('color', 'white'), ('font-weight', 'bold')]}])
                .set_properties(**{'background-color': '#f8fafc', 'color': '#334155'}),
                use_container_width=True
            )

    with tab_biodata:
        st.header("👤 Profil Pengembang")
        st.write("**Nama:** Frayogi Aditiya")
        st.write("**Proyek:** Si-Cerdas (Sistem Cepat Lapor Data Pendidikan Sumut)")
        st.info("Dikembangkan untuk optimalisasi pelaporan data Bidang Pendidikan Khusus.")

    with tab_bidang:
        st.header("🏛️ Bidang Pembinaan PK")
        st.write("Dinas Pendidikan Provinsi Sumatera Utara")

else:
    # --- HALAMAN DETAIL ---
    sch = st.session_state.selected_school_data
    if st.button("⬅️ Kembali ke Dashboard"):
        st.session_state.page_view = "dashboard"
        st.rerun()
    st.markdown(f"<h1 style='color:#0d47a1;'>🏫 {sch['nama_sekolah'].upper()}</h1>", unsafe_allow_html=True)
    st.divider()
    c1, c2 = st.columns(2)
    with c1:
        with st.container(border=True):
            st.subheader("📌 Profil")
            st.write(f"**Jumlah Siswa:** {sch.get('jumlah_siswa', '0')} Orang")
            st.write(f"**Alamat:** {sch.get('alamat', '-')}")
    with c2:
        with st.container(border=True):
            st.subheader("🏗️ Sarana Prasarana")
            st.write(f"**Rusak Berat:** {sch['rusak_berat']} Ruang")
            st.write(f"**Akses Internet:** {sch.get('akses_internet', '-')}")
