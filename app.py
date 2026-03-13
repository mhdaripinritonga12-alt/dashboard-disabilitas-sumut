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
    initial_sidebar_state="expanded" # Sidebar dipaksa terbuka sejak awal
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
# Bagian 1: CSS CUSTOM (LOCKED & FIXED)
# ==================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&display=swap');
    html, body, [data-testid="stWidgetLabel"] { font-family: 'Inter', sans-serif !important; }
    [data-testid="stAppViewContainer"] { background-color: #f4f7f9 !important; }
    header {visibility: hidden;}

    /* SIDEBAR GRADASI (NAVY BLUE) */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d47a1 0%, #1e3a8a 100%) !important;
        border-right: 1px solid #e2e8f0;
    }
    [data-testid="stSidebar"] * { color: white !important; }
    
    /* FIX: TEKS SELECTBOX DI SIDEBAR AGAR TETAP HITAM (UNTUK KETERBACAAN) */
    div[data-testid="stSelectbox"] div[data-baseweb="select"] * {
        color: #1e293b !important;
    }

    /* KOTAK METRIK (BOX MODEL) */
    .metric-card {
        background: white; padding: 25px; border-radius: 12px;
        border-top: 6px solid #0d47a1; box-shadow: 0 4px 10px rgba(0,0,0,0.08);
        text-align: center; margin-bottom: 20px;
    }
    .m-label { font-size: 13px; color: #64748b; font-weight: 700; text-transform: uppercase; margin-bottom: 5px; }
    .m-value { font-size: 32px; color: #0d47a1; font-weight: 800; }

    /* BALON STATUS (VIVID COLOR) */
    .rec-box { padding: 10px; border-radius: 8px; font-size: 12px; font-weight: 800; margin-bottom: 12px; text-align: center; }
    .mendesak { background-color: #ff3333 !important; color: white !important; border: 1px solid #990000; }
    .rehab { background-color: #ffcc00 !important; color: #663300 !important; border: 2px solid #cc9900; }
    .aman { background-color: #22c55e !important; color: white !important; border: 1px solid #166534; }

    /* TOMBOL DOWNLOAD */
    .stDownloadButton > button {
        background: linear-gradient(90deg, #16a34a 0%, #22c55e 100%) !important;
        color: white !important; border-radius: 10px !important; 
        font-weight: 700 !important; width: 100% !important; height: 48px !important;
        border: none !important;
    }

    /* TOMBOL LOGOUT */
    section[data-testid="stSidebar"] div.stButton > button {
        background: linear-gradient(90deg, #ff9966 0%, #ff5e62 100%) !important;
        height: 40px !important; border-radius: 8px !important;
    }
</style>
""", unsafe_allow_html=True)

# --- FUNGSI RENDER KOTAK ---
def draw_box(label, value):
    st.markdown(f"""
        <div class="metric-card">
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
            st.markdown("<h3 style='color:#0d47a1; text-align:center;'>LOGIN USER</h3>", unsafe_allow_html=True)
            u = st.text_input("Username", placeholder="Username")
            p = st.text_input("Password", type="password", placeholder="Password")
            if st.button("MASUK KE DASHBOARD"):
                if u == "admin" and p == "admin":
                    st.session_state.login = True
                    st.rerun()
                else: st.error("Login Gagal")
    st.stop()

# ==================================
# Bagian 4: SIDEBAR (SETELAH LOGIN)
# ==================================
# Bagian ini akan muncul di samping setiap halaman setelah login berhasil

logo_b64 = get_base64_image("logo_sumut.png")
if logo_b64:
    st.sidebar.markdown(f"""
        <div style="display: flex; align-items: center; gap: 12px; padding-bottom: 20px;">
            <img src="data:image/png;base64,{logo_b64}" width="45">
            <span style="font-size: 18px; font-weight: 800; color: white; line-height: 1.1;">SI-PANDAI<br>SUMUT</span>
        </div>
    """, unsafe_allow_html=True)

st.sidebar.write(f"👤 Role: **ADMINISTRATOR**")
st.sidebar.write(f"📂 Unit: **Subbagian Keuangan**")
st.sidebar.divider()

st.sidebar.header("🔎 Navigasi Wilayah")
opsi_kab = ["Semua"] + sorted(data_wilayah["kab_kota"].unique().tolist())
kab_pilih = st.sidebar.selectbox("Pilih Kabupaten / Kota", opsi_kab, key="selected_kab")

st.sidebar.divider()
st.sidebar.subheader("📄 Ekspor Data")
df_dl = data_wilayah.copy() if kab_pilih == "Semua" else data_wilayah[data_wilayah["kab_kota"] == kab_pilih]
csv_data = df_dl.to_csv(index=False).encode('utf-8')
st.sidebar.download_button("Unduh Master Data (CSV) ⬇️", csv_data, f"data_{kab_pilih}.csv", "text/csv")

st.sidebar.divider()
st.sidebar.button("Logout 🚪", use_container_width=True, on_click=proses_logout)

# ==================================
# Bagian 5: KONTEN DASHBOARD
# ==================================
if st.session_state.page_view == "dashboard":
    st.markdown('<p style="font-size:26px; font-weight:800; color:#0d47a1;">🚀 Dashboard Utama Monitoring</p>', unsafe_allow_html=True)
    st.divider()

    df_filter = data_wilayah.copy()
    if kab_pilih != "Semua":
        df_filter = df_filter[df_filter["kab_kota"] == kab_pilih]

    # 1. Matriks Kotak (Box Style)
    m1, m2, m3 = st.columns(3)
    if kab_pilih == "Semua":
        with m1: draw_box("TOTAL PENDUDUK DISABILITAS", "6.732")
        with m2: draw_box("TOTAL SISWA BELAJAR", "4.573")
        with m3: draw_box("ANGKA PARTISIPASI (APS)", "67.93%")
    else:
        with m1: draw_box("PENDUDUK DISABILITAS", f"{int(df_filter['jumlah_penduduk'].sum()):,}")
        with m2: draw_box("SISWA AKTIF", f"{int(df_filter['jumlah_siswa'].sum()):,}")
        with m3: draw_box("ATS WILAYAH", f"{int(df_filter['ats_disabilitas'].sum()):,}")

    # 2. Peta GIS (Vivid Satellite Style)
    st.divider()
    col_map, col_bar = st.columns([1.6, 1])
    
    with col_map:
        st.subheader("🗺️ Peta Pemetaan Lokasi Riil")
        fig_map = px.scatter_mapbox(
            df_filter, lat="lat", lon="lon", size="ats_disabilitas",
            color="ats_disabilitas", color_continuous_scale="Reds",
            size_max=20, zoom=7, mapbox_style="open-street-map"
        )
        # Menambahkan layer satelit yang lebih hidup dan detail
        fig_map.update_layout(
            mapbox_layers=[{
                "below": 'traces', "sourcetype": "raster",
                "source": ["https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"]
            }],
            margin={"r":0,"t":0,"l":0,"b":0}, height=500
        )
        st.plotly_chart(fig_map, use_container_width=True)

    with col_bar:
        st.subheader("📊 Statistik ATS Per Wilayah")
        df_chart = df_filter.sort_values("ats_disabilitas", ascending=False).head(10)
        fig_bar = px.bar(df_chart, x='ats_disabilitas', y='kab_kota', orientation='h', color_discrete_sequence=['#0d47a1'])
        fig_bar.update_layout(height=400, margin=dict(l=0, r=0, t=0, b=0))
        st.plotly_chart(fig_bar, use_container_width=True)

    # 3. Daftar Sekolah (Balon Warna Tajam)
    if kab_pilih != "Semua":
        st.divider()
        st.subheader(f"🏫 Daftar Satuan Pendidikan: {kab_pilih}")
        sch_wil = data_sekolah[data_sekolah['kab_kota'] == kab_pilih]
        cols = st.columns(3)
        for i, row in enumerate(sch_wil.itertuples()):
            with cols[i % 3]:
                with st.container(border=True):
                    # BALON STATUS
                    if row.rusak_berat > 0: 
                        st.markdown(f"<div class='rec-box mendesak'>⚠️ RUSAK BERAT: {row.rusak_berat} RUANG</div>", unsafe_allow_html=True)
                    elif row.jumlah_rombel > row.jumlah_ruang_kelas:
                        st.markdown(f"<div class='rec-box rehab'>🛠️ BUTUH RKB</div>", unsafe_allow_html=True)
                    else: 
                        st.markdown("<div class='rec-box aman'>✅ KONDISI STABIL</div>", unsafe_allow_html=True)
                    
                    if st.button(row.nama_sekolah.upper(), key=f"btn_{row.npsn}"):
                        st.session_state.selected_school_data = row._asdict()
                        st.session_state.page_view = "detail"
                        st.rerun()
                    st.caption(f"NPSN: {row.npsn}")

else:
    # --- HALAMAN DETAIL ---
    sch = st.session_state.selected_school_data
    if st.button("⬅️ Kembali ke Dashboard Utama"):
        st.session_state.page_view = "dashboard"
        st.rerun()
    st.markdown(f"<h1 style='color:#0d47a1;'>🏫 {sch['nama_sekolah'].upper()}</h1>", unsafe_allow_html=True)
    st.divider()
    
    col_a, col_b = st.columns(2)
    with col_a:
        with st.container(border=True):
            st.subheader("📌 Profil Sekolah")
            st.write(f"**Jumlah Siswa:** {sch.get('jumlah_siswa', '0')} Orang")
            st.write(f"**Alamat:** {sch.get('alamat', '-')}")
            st.write(f"**Akses Internet:** {sch.get('akses_internet', '-')}")
    with col_b:
        with st.container(border=True):
            st.subheader("🏗️ Data Sarpras")
            st.write(f"**Rusak Berat:** {sch['rusak_berat']} Ruang")
            st.write(f"**Daya Listrik:** {sch.get('daya_listrik', '-')}")
