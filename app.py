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
    [data-testid="stAppViewContainer"] { background-color: #f8fafc !important; }
    header {visibility: hidden;}

    /* SIDEBAR NAVY */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d47a1 0%, #1565c0 100%) !important;
    }
    [data-testid="stSidebar"] * { color: white !important; }
    div[data-testid="stSelectbox"] div[data-baseweb="select"] * { color: #31333f !important; }

    /* CUSTOM METRIC TILES (BALON WARNA) */
    .metric-tile {
        padding: 25px;
        border-radius: 15px;
        color: white;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        display: flex;
        align-items: center;
        gap: 20px;
    }
    .tile-orange { background: linear-gradient(135deg, #ff9800 0%, #f57c00 100%); }
    .tile-blue-light { background: linear-gradient(135deg, #03a9f4 0%, #0288d1 100%); }
    .tile-blue-dark { background: linear-gradient(135deg, #3f51b5 0%, #303f9f 100%); }
    
    .tile-icon { font-size: 40px; opacity: 0.8; }
    .tile-label { font-size: 14px; font-weight: 600; opacity: 0.9; text-transform: uppercase; }
    .tile-value { font-size: 32px; font-weight: 800; line-height: 1; }

    /* KARTU SEKOLAH */
    [data-testid="stVerticalBlockBorderWrapper"] > div {
        background: white !important; border-radius: 15px !important;
        padding: 20px !important; border: 1px solid #e2e8f0 !important;
    }

    /* BALON STATUS */
    .rec-box { padding: 8px 12px; border-radius: 8px; font-size: 11px; font-weight: 700; margin-bottom: 12px; }
    .mendesak { background-color: #fee2e2 !important; color: #b91c1c !important; border-left: 5px solid #ef4444 !important; }
    .rehab { background-color: #fef3c7 !important; color: #b45309 !important; border-left: 5px solid #f59e0b !important; }
    .aman { background-color: #dcfce7 !important; color: #15803d !important; border-left: 5px solid #22c55e !important; }

    /* DOWNLOAD BUTTON */
    .stDownloadButton > button {
        background: linear-gradient(90deg, #2e7d32 0%, #4caf50 100%) !important;
        color: white !important; border-radius: 10px !important; 
        font-weight: 700 !important; width: 100% !important; height: 48px !important;
    }
</style>
""", unsafe_allow_html=True)

# --- FUNGSI DRAW TILE ---
def draw_tile(label, value, icon, style_class):
    st.markdown(f"""
        <div class="metric-tile {style_class}">
            <div class="tile-icon">{icon}</div>
            <div>
                <div class="tile-label">{label}</div>
                <div class="tile-value">{value}</div>
            </div>
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
    _, col_card, _ = st.columns([1, 1.2, 1])
    with col_card:
        with st.container(border=True):
            st.markdown("<h3 style='text-align:center; color:#0d47a1;'>LOGIN SI-PANDAI</h3>", unsafe_allow_html=True)
            u = st.text_input("Username", placeholder="Username")
            p = st.text_input("Password", type="password", placeholder="Password")
            if st.button("MASUK KE DASHBOARD"):
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

# --- KONTEN DASHBOARD ---
if st.session_state.page_view == "dashboard":
    st.markdown('<p style="font-size:26px; font-weight:800; color:#0d47a1;">🚀 Dashboard Utama Monitoring</p>', unsafe_allow_html=True)
    st.divider()

    # Logika Data: Jika 'Semua', ambil total satu provinsi
    df_f = data_wilayah.copy()
    if kab_pilih != "Semua":
        df_f = df_f[df_f["kab_kota"] == kab_pilih]

    # 1. Matriks Capaian (KOTAK BALON SESUAI GAMBAR)
    m1, m2, m3 = st.columns(3)
    with m1:
        draw_tile("Penduduk Disabilitas", f"{int(df_f['jumlah_penduduk'].sum()):,}", "👥", "tile-orange")
    with m2:
        draw_tile("Siswa Belajar", f"{int(df_f['jumlah_siswa'].sum()):,}", "🎓", "tile-blue-light")
    with m3:
        # Menampilkan total ATS seluruhnya jika filter = Semua
        draw_tile("Anak Tidak Sekolah (ATS)", f"{int(df_f['ats_disabilitas'].sum()):,}", "⚠️", "tile-blue-dark")

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
                        st.caption(f"NPSN: {row.npsn}")

    # 3. Visualisasi
    st.divider()
    cv1, cv2 = st.columns([1.5, 1])
    with cv1:
        st.subheader("🗺️ Peta Sebaran ATS")
        df_f['map_size'] = df_f['ats_disabilitas'] * 30
        st.map(df_f, latitude="lat", longitude="lon", size="map_size", use_container_width=True)
    with cv2:
        st.subheader("📊 Grafik ATS Wilayah")
        df_chart = df_f.sort_values("ats_disabilitas", ascending=False).head(10)
        fig = px.bar(df_chart, x='ats_disabilitas', y='kab_kota', orientation='h', color='ats_disabilitas', color_continuous_scale='Blues')
        fig.update_layout(height=350, margin=dict(l=0, r=0, t=0, b=0))
        st.plotly_chart(fig, use_container_width=True)

else:
    # --- HALAMAN DETAIL ---
    sch = st.session_state.selected_school_data
    if st.button("⬅️ Kembali ke Dashboard"):
        st.session_state.page_view = "dashboard"
        st.rerun()
    st.markdown(f"<h1 style='color:#0d47a1;'>🏫 {sch['nama_sekolah'].upper()}</h1>")
