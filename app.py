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
    initial_sidebar_state="expanded" # Kunci agar terbuka otomatis
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
# Bagian 1: CSS CUSTOM (FIXED SIDEBAR)
# ==================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&display=swap');
    html, body, [data-testid="stWidgetLabel"] { font-family: 'Inter', sans-serif !important; }
    [data-testid="stAppViewContainer"] { background-color: #f4f7f9 !important; }
    
    /* FIX: Jangan sembunyikan header total agar tombol sidebar muncul */
    header { background-color: rgba(0,0,0,0) !important; }
    [data-testid="stHeader"] { background: none !important; }

    /* SIDEBAR NAVY */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d47a1 0%, #1565c0 100%) !important;
    }
    [data-testid="stSidebar"] * { color: white !important; }

    /* TEKS FILTER TETAP HITAM */
    div[data-testid="stSelectbox"] div[data-baseweb="select"] * {
        color: #31333f !important;
    }

    /* MATRIKS KOTAK (BOX) */
    .metric-card {
        background: white; padding: 20px; border-radius: 12px;
        border-top: 6px solid #0d47a1; box-shadow: 0 4px 10px rgba(0,0,0,0.08);
        text-align: center; margin-bottom: 10px;
    }
    .m-label { font-size: 13px; color: #64748b; font-weight: 700; text-transform: uppercase; }
    .m-value { font-size: 30px; color: #0d47a1; font-weight: 800; }

    /* TOMBOL DOWNLOAD */
    .stDownloadButton > button {
        background: linear-gradient(90deg, #16a34a 0%, #22c55e 100%) !important;
        color: white !important; border-radius: 10px !important; 
        font-weight: 700 !important; width: 100% !important; height: 48px !important;
    }
</style>
""", unsafe_allow_html=True)

# --- FUNGSI DRAW BOX ---
def draw_box(label, value):
    st.markdown(f'<div class="metric-card"><div class="m-label">{label}</div><div class="m-value">{value}</div></div>', unsafe_allow_html=True)

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
# Bagian 4: SIDEBAR
# ==================================
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
kab_pilih = st.sidebar.selectbox("Pilih Kabupaten / Kota", opsi_kab, key="selected_kab")

st.sidebar.divider()
df_dl = data_wilayah.copy() if kab_pilih == "Semua" else data_wilayah[data_wilayah["kab_kota"] == kab_pilih]
st.sidebar.download_button("Download Data (CSV) ⬇️", df_dl.to_csv(index=False).encode('utf-8'), f"data_{kab_pilih}.csv", "text/csv")

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

    # Matrix Capaian
    m1, m2, m3 = st.columns(3)
    if kab_pilih == "Semua":
        with m1: draw_box("TOTAL PENDUDUK DISABILITAS", "6.732")
        with m2: draw_box("TOTAL SISWA BELAJAR", "4.573")
        with m3: draw_box("APS SUMUT", "67.93%")
    else:
        with m1: draw_box("PENDUDUK DISABILITAS", f"{int(df_filter['jumlah_penduduk'].sum()):,}")
        with m2: draw_box("SISWA AKTIF", f"{int(df_filter['jumlah_siswa'].sum()):,}")
        with m3: draw_box("ATS WILAYAH", f"{int(df_filter['ats_disabilitas'].sum()):,}")

    # Peta Vivid Satelit
    st.divider()
    st.subheader("🗺️ Peta Lokasi Riil")
    fig_map = px.scatter_mapbox(
        df_filter, lat="lat", lon="lon", size="ats_disabilitas",
        color="ats_disabilitas", color_continuous_scale="Reds",
        size_max=20, zoom=7, mapbox_style="open-street-map"
    )
    fig_map.update_layout(
        mapbox_layers=[{
            "below": 'traces', "sourcetype": "raster",
            "source": ["https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"]
        }],
        margin={"r":0,"t":0,"l":0,"b":0}, height=500
    )
    st.plotly_chart(fig_map, use_container_width=True)

else:
    # --- HALAMAN DETAIL ---
    sch = st.session_state.selected_school_data
    if st.button("⬅️ Kembali ke Dashboard"):
        st.session_state.page_view = "dashboard"
        st.rerun()
    st.header(f"🏫 {sch['nama_sekolah'].upper()}")
