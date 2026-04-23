import streamlit as st
import pandas as pd
import plotly.express as px
import os
import base64
import streamlit.components.v1 as components

# ==================================
# Bagian 0: KONFIGURASI HALAMAN
# ==================================
st.set_page_config(
    page_title="SI-PANDAI SUMUT",
    layout="wide",
    page_icon="🔒",
    initial_sidebar_state="expanded"
)

# Inisialisasi State
if "page_view" not in st.session_state: st.session_state.page_view = "dashboard"
if "selected_kab" not in st.session_state: st.session_state.selected_kab = "Semua"

def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

# PERBAIKAN: Definisi fungsi draw_tile_svg agar matriks muncul
def draw_tile_svg(label, value, svg_icon, style_class):
    st.markdown(f"""
        <div class="metric-tile {style_class}">
            <div class="tile-icon-svg">{svg_icon}</div>
            <div>
                <div class="tile-label">{label}</div>
                <div class="tile-value">{value}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

# SVG Icons
svg_people = '<svg viewBox="0 0 16 16" width="30" height="30" fill="white"><path d="M7 14s-1 0-1-1 1-4 5-4 5 3 5 4-1 1-1 1H7zm4-6a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm-5.784 6A2.238 2.238 0 0 1 5 13c0-1.355.68-2.75 1.936-3.72A6.325 6.325 0 0 0 5 9c-4 0-5 3-5 4s1 1 1 1h4.216zM4.5 8a2.5 2.5 0 1 0 0-5 2.5 2.5 0 0 0 0 5z"/></svg>'
svg_cap = '<svg viewBox="0 0 16 16" width="30" height="30" fill="white"><path d="M8.211 2.047a.5.5 0 0 0-.422 0l-7.5 3.5a.5.5 0 0 0 .025.917l7.5 3 7.5-3a.5.5 0 0 0 .025-.917l-7.5-3.5Z"/><path d="M4.176 9.032a.5.5 0 0 0-.656.327l-.5 1.7a.5.5 0 0 0 .254.539l1.5.75A.5.5 0 0 0 5.25 12h5.5a.5.5 0 0 0 .476-.346l.5-1.7a.5.5 0 0 0-.656-.327L10 10.25l-.117-.043-4 .876L4.176 9.032Z"/></svg>'
svg_warning = '<svg viewBox="0 0 16 16" width="30" height="30" fill="white"><path d="M8.982 1.566a1.13 1.13 0 0 0-1.96 0L.165 13.233c-.457.778.091 1.767.98 1.767h13.713c.889 0 1.438-.99.98-1.767L8.982 1.566zM8 5c.535 0 .954.462.9.995l-.35 3.507a.552.552 0 0 1-1.1 0L7.1 5.995A.905.905 0 0 1 8 5zm.002 6a1 1 0 1 1 0 2 1 1 0 0 1 0-2z"/></svg>'
svg_chart = '<svg viewBox="0 0 24 24" width="30" height="30" fill="none" stroke="white" stroke-width="3"><path d="M18 20V10M12 20V4M6 20v-6"/></svg>'

# ==================================
# Bagian 1: CSS CUSTOM
# ==================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
    html, body, [data-testid="stWidgetLabel"] { font-family: 'Inter', sans-serif !important; }
    
    /* CSS Metrik Balon */
    .metric-tile { padding: 20px; border-radius: 15px; color: white; display: flex; align-items: center; gap: 15px; margin-bottom: 10px; }
    .tile-orange { background: linear-gradient(135deg, #ff9800 0%, #f57c00 100%); }
    .tile-blue-light { background: linear-gradient(135deg, #03a9f4 0%, #0288d1 100%); }
    .tile-red-dark { background: linear-gradient(135deg, #ff4b2b 0%, #ff416c 100%); }
    .tile-green-light { background: linear-gradient(135deg, #4caf50 0%, #2e7d32 100%); }
    .tile-label { font-size: 12px; font-weight: 700; text-transform: uppercase; opacity: 0.9; }
    .tile-value { font-size: 24px; font-weight: 800; }
    
    [data-testid="stSidebar"] { background: linear-gradient(180deg, #1e88e5 0%, #0d47a1 100%) !important; }
    [data-testid="stSidebar"] * { color: white !important; }
    div[data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] div { color: #1e293b !important; }
    
    .header-balloon-card {
        background: linear-gradient(90deg, #f0f7ff 0%, #d1e9ff 100%) !important;
        border-radius: 0px 0px 15px 15px; padding: 20px; text-align: center;
        border-bottom: 2px solid rgba(13, 71, 161, 0.1); margin-bottom: 20px;
    }
    .insight-box { background-color: #f8f9fa; border-radius: 10px; padding: 15px; margin-top: 10px; }
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
        for df in [df_ats, df_sch]:
            df.columns = df.columns.str.strip().str.lower()
        return df_ats, df_sch
    except: return pd.DataFrame(), pd.DataFrame()

data_wilayah, data_sekolah = load_all_data()

# ==================================
# Bagian 4: SIDEBAR
# ==================================
with st.sidebar:
    logo_b64 = get_base64_image("logo_sumut.png")
    if logo_b64:
        st.markdown(f'<div style="text-align:center;"><img src="data:image/png;base64,{logo_b64}" width="80"></div>', unsafe_allow_html=True)
    st.markdown("<h2 style='text-align:center;'>SI-PANDAI SUMUT</h2>", unsafe_allow_html=True)

    def ubah_halaman():
        if "nav_radio" in st.session_state:
            pilihan = st.session_state.nav_radio
            if "Dashboard Utama" in pilihan: st.session_state.page_view = "dashboard"
            elif "Tentang Dashboard" in pilihan: st.session_state.page_view = "tentang_dashboard"

    st.radio("🧭 Navigasi", ["🚀 Dashboard Utama", "ℹ️ Tentang Dashboard"], key="nav_radio", on_change=ubah_halaman)
    st.divider()
    
    col_kab = "kab_kota" if "kab_kota" in data_wilayah.columns else data_wilayah.columns[0]
    opsi = ["Semua"] + sorted(data_wilayah[col_kab].unique().tolist()) if not data_wilayah.empty else ["Semua"]
    kab_pilih = st.selectbox("🔎 Filter Wilayah", opsi, key="selected_kab")

# ==================================
# Bagian 5: HEADER
# ==================================
st.markdown("""<div class="header-balloon-card">
    <h2 style='color: #0d47a1; font-weight:800; margin: 0;'>DASHBOARD SI-PANDAI SUMUT</h2>
    <p style='color: #1565c0; font-weight: 700;'>Sistem Informasi Pemetaan Anak Tidak Sekolah (ATS) Disabilitas</p>
</div>""", unsafe_allow_html=True)

# --- HALAMAN DASHBOARD ---
if st.session_state.page_view == "dashboard":
    df_f = data_wilayah.copy()
    if kab_pilih != "Semua": 
        df_f = df_f[df_f[col_kab] == kab_pilih]

    # PERBAIKAN: Logika pengambilan kolom berdasarkan urutan kolom di CSV Anda
    # Index 1: Populasi Sasaran, Index 2: Siswa Belajar, Index 3: ATS
    populasi = int(df_f.iloc[:, 1].sum()) if not df_f.empty else 0
    belajar = int(df_f.iloc[:, 2].sum()) if not df_f.empty else 0
    ats = int(df_f.iloc[:, 3].sum()) if not df_f.empty else 0
    
    # Hitung Persentase Partisipasi (Siswa Belajar / Total Sasaran)
    persentase = (belajar / populasi * 100) if populasi > 0 else 0
    
    st.markdown('<p style="font-size:22px; font-weight:800; color:#0d47a1;">Matriks Capaian Sektoral</p>', unsafe_allow_html=True)
    
    m1, m2, m3, m4 = st.columns(4)
    with m1: draw_tile_svg("Populasi Sasaran", f"{populasi:,}", svg_people, "tile-orange")
    with m2: draw_tile_svg("Siswa Belajar", f"{belajar:,}", svg_cap, "tile-blue-light")
    with m3: draw_tile_svg("Anak Tidak Sekolah", f"{ats:,}", svg_warning, "tile-red-dark")
    with m4: draw_tile_svg("Persentase Capaian", f"{persentase:.2f}%", svg_chart, "tile-green-light")

    st.divider()
    
    # Visualisasi Peta & Bar Chart
    cv1, cv2 = st.columns([1.6, 1.1])
    with cv1:
        st.subheader("🗺️ Peta Sebaran ATS")
        if not df_f.empty:
            fig_map = px.scatter_mapbox(
                df_f, lat="lat", lon="lon", size=df_f.columns[3], color=df_f.columns[3],
                color_continuous_scale="RdYlGn_r", hover_name=col_kab, zoom=7, height=450
            )
            fig_map.update_layout(mapbox_style="open-street-map", margin={"r":0,"t":0,"l":0,"b":0})
            st.plotly_chart(fig_map, use_container_width=True)

    with cv2:
        st.subheader("📊 5 Wilayah ATS Tertinggi")
        if not df_f.empty:
            df_top5 = df_f.sort_values(by=df_f.columns[3], ascending=False).head(5)
            fig = px.bar(df_top5, x=df_f.columns[3], y=col_kab, orientation='h', color=df_f.columns[3],
                         color_continuous_scale="Blues", text_auto=True)
            fig.update_layout(height=350, showlegend=False, coloraxis_showscale=False, yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig, use_container_width=True)

    st.expander("📋 Detail Data Tabel").dataframe(df_f, use_container_width=True)

elif st.session_state.page_view == "tentang_dashboard":
    st.title("ℹ️ Tentang SI-PANDAI")
    st.info("Sistem ini dirancang untuk memetakan Anak Tidak Sekolah (ATS) Disabilitas di Sumatera Utara guna optimalisasi kebijakan pendidikan khusus.")
    if st.button("⬅️ Kembali"):
        st.session_state.page_view = "dashboard"
        st.rerun()

# FOOTER
st.divider()
st.markdown("<p style='text-align:center; color:gray; font-size:12px;'>© 2026 SI-PANDAI SUMUT | Dinas Pendidikan Provinsi Sumatera Utara</p>", unsafe_allow_html=True)
