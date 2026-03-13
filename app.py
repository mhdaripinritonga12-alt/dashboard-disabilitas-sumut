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
# Bagian 1: CSS CUSTOM (LOCKED & FIXED)
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

    /* CUSTOM METRIC BOX */
    .metric-card {
        background: white; padding: 20px; border-radius: 12px;
        border-top: 5px solid #0d47a1; box-shadow: 0 4px 10px rgba(0,0,0,0.08);
        text-align: center; margin-bottom: 10px;
    }
    .m-label { font-size: 13px; color: #64748b; font-weight: 600; text-transform: uppercase; }
    .m-value { font-size: 26px; color: #0d47a1; font-weight: 800; }

    /* KARTU SEKOLAH & BALON */
    [data-testid="stVerticalBlockBorderWrapper"] > div { background: white !important; border-radius: 15px !important; padding: 20px !important; border: 1px solid #e2e8f0 !important; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1) !important; }
    .rec-box { padding: 8px 12px; border-radius: 8px; font-size: 11px; font-weight: 700; margin-bottom: 12px; text-align: center; }
    .mendesak { background-color: #fee2e2 !important; color: #b91c1c !important; border-left: 5px solid #ef4444 !important; }
    .rehab { background-color: #fef3c7 !important; color: #b45309 !important; border-left: 5px solid #f59e0b !important; }
    .aman { background-color: #dcfce7 !important; color: #15803d !important; border-left: 5px solid #22c55e !important; }

    /* NAMA SEKOLAH BUTTON */
    div.stButton > button[key^="btn_"] { background: transparent !important; color: #0d47a1 !important; font-size: 16px !important; font-weight: 800 !important; text-align: left !important; box-shadow: none !important; }

    /* TOMBOL DOWNLOAD (HIJAU) */
    .stDownloadButton > button { background: linear-gradient(90deg, #2e7d32 0%, #4caf50 100%) !important; color: white !important; border-radius: 10px !important; font-weight: 700 !important; width: 100% !important; height: 48px !important; }

    /* TOMBOL GOOGLE MAPS */
    .gmap-btn {
        display: inline-block; padding: 8px 15px; background-color: #4285F4; color: white !important;
        text-decoration: none; border-radius: 6px; font-size: 12px; font-weight: bold; margin-top: 5px;
    }
</style>
""", unsafe_allow_html=True)

# --- FUNGSI RENDER KOTAK MATRIX ---
def draw_metric(label, value):
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
    st.sidebar.markdown(f"""<div style="display:flex; align-items:center; gap:12px; padding-bottom:20px;"><img src="data:image/png;base64,{logo_b64}" width="45"><span style="font-size:18px; font-weight:800; color:white; line-height:1.1;">SI-PANDAI<br>SUMUT</span></div>""", unsafe_allow_html=True)

st.sidebar.write(f"👤 Role: **ADMIN**")
st.sidebar.divider()
st.sidebar.header("🔎 Filter")
opsi_kab = ["Semua"] + sorted(data_wilayah["kab_kota"].unique().tolist())
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
    st.divider()

    df_filter = data_wilayah.copy()
    if kab_pilih != "Semua":
        df_filter = df_filter[df_filter["kab_kota"] == kab_pilih]

    # 1. Matriks Capaian (KOTAK BOX)
    st.subheader("📌 Matriks Capaian Sektoral")
    m1, m2, m3 = st.columns(3)
    if kab_pilih == "Semua":
        with m1: draw_metric("Total Penduduk Disabilitas", "6.732")
        with m2: draw_metric("Total Siswa Disabilitas", "4.573")
        with m3: draw_metric("Angka Partisipasi Sekolah", "67.93%")
    else:
        with m1: draw_metric("Penduduk Disabilitas", f"{int(df_filter['jumlah_penduduk'].sum()):,}")
        with m2: draw_metric("Siswa Belajar", f"{int(df_filter['jumlah_siswa'].sum()):,}")
        with m3: draw_metric("Anak Tidak Sekolah", f"{int(df_filter['ats_disabilitas'].sum()):,}")

    # 2. Daftar Sekolah
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
                        else: st.markdown("<div class='rec-box aman'>✅ KONDISI STABIL</div>", unsafe_allow_html=True)
                        
                        if st.button(row.nama_sekolah.upper(), key=f"btn_{row.npsn}"):
                            st.session_state.selected_school_data = row._asdict()
                            st.session_state.page_view = "detail"
                            st.rerun()
                        
                        # TOMBOL GOOGLE MAPS (Street View)
                        gmap_link = f"https://www.google.com/maps/search/?api=1&query={row.nama_sekolah}+{row.kab_kota}".replace(" ", "+")
                        st.markdown(f'<a href="{gmap_link}" target="_blank" class="gmap-btn">📍 Buka Lokasi Riil</a>', unsafe_allow_html=True)
                        st.caption(f"NPSN: {row.npsn}")

    # 3. Visualisasi (PETA SATELIT / HIDUP)
    st.divider()
    cv1, cv2 = st.columns([1.5, 1])
    with cv1:
        st.subheader("🗺️ Peta Citra Satelit")
        # Menggunakan Mapbox Satellite agar peta "Hidup"
        fig_map = px.scatter_mapbox(
            df_filter, lat="lat", lon="lon", size="ats_disabilitas",
            color="ats_disabilitas", color_continuous_scale="Reds",
            size_max=20, zoom=7, mapbox_style="white-bg"
        )
        # Menambahkan layer Satelit dari Esri (Gratis & Berwarna)
        fig_map.update_layout(
            mapbox_layers=[{
                "below": 'traces',
                "sourcetype": "raster",
                "source": ["https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"]
            }],
            margin={"r":0,"t":0,"l":0,"b":0}
        )
        st.plotly_chart(fig_map, use_container_width=True)

    with cv2:
        st.subheader("📊 Grafik ATS Wilayah")
        df_chart = df_filter.sort_values("ats_disabilitas", ascending=False).head(10)
        fig_bar = px.bar(df_chart, x='ats_disabilitas', y='kab_kota', orientation='h', color='ats_disabilitas', color_continuous_scale='Blues')
        fig_bar.update_layout(height=400, margin=dict(l=0, r=0, t=0, b=0))
        st.plotly_chart(fig_bar, use_container_width=True)

    st.divider()
    with st.expander("📋 Lihat Detail Tabel"):
        st.dataframe(df_filter[['kab_kota', 'jumlah_penduduk', 'jumlah_siswa', 'ats_disabilitas']], use_container_width=True)

else:
    # --- HALAMAN DETAIL ---
    sch = st.session_state.selected_school_data
    if st.button("⬅️ Kembali ke Dashboard"):
        st.session_state.page_view = "dashboard"
        st.rerun()
    
    st.markdown(f"<h1 style='color:#0d47a1; margin-bottom:0;'>🏫 {sch['nama_sekolah'].upper()}</h1>", unsafe_allow_html=True)
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
