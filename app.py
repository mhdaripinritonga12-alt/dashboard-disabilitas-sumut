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

# ==================================
# Bagian 1: CSS CUSTOM (FIX HEADER POSITION)
# ==================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
    html, body, [data-testid="stWidgetLabel"] { font-family: 'Inter', sans-serif !important; }
    
    /* MENAIKKAN HEADER: Mengurangi padding atas pada container utama */
    .block-container {
        padding-top: 0rem !important; 
        padding-bottom: 0rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
    }
    
    [data-testid="stHeader"] { display: none !important; }

    /* HEADER BALLOON CARD: Dibuat lebih ramping dan naik */
    .header-balloon-card {
        background: linear-gradient(90deg, #f0f7ff 0%, #d1e9ff 100%) !important;
        border-radius: 0px 0px 20px 20px;
        padding: 10px 0px; /* Padding dikurangi agar tidak terlalu turun */
        border-bottom: 2px solid rgba(13, 71, 161, 0.1);
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        text-align: center;
        margin-top: -5px; /* Margin negatif ditarik ke atas */
        margin-bottom: 25px;
        width: 100% !important;
        display: block;
    }

    .top-gradient-bar {
        position: fixed;
        top: 0; left: 0; width: 100%; height: 5px;
        background: #1e88e5;
        z-index: 999999;
    }

    /* CSS Metrik & Sidebar tetap */
    .metric-tile { padding: 20px; border-radius: 12px; color: white; margin-bottom: 15px; display: flex; align-items: center; gap: 15px; }
    .tile-orange { background: linear-gradient(135deg, #ff9800 0%, #f57c00 100%); }
    .tile-blue-light { background: linear-gradient(135deg, #03a9f4 0%, #0288d1 100%); }
    .tile-red-dark { background: linear-gradient(135deg, #ff4b2b 0%, #ff416c 100%); }
    .tile-green-light { background: linear-gradient(135deg, #4caf50 0%, #2e7d32 100%); }
    .tile-value { font-size: 22px; font-weight: 800; }
    .tile-label { font-size: 14px; font-weight: 800; text-transform: uppercase; }

    [data-testid="stSidebar"] { background: linear-gradient(180deg, #1e88e5 0%, #0d47a1 100%) !important; }
    [data-testid="stSidebar"] * { color: white !important; }
    div[data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] div { color: black !important; }
    
    .insight-box { background-color: #e3f2fd !important; border-radius: 8px; border-left: 4px solid #0d47a1; padding: 10px 12px; margin-top: 10px; }
</style>
""", unsafe_allow_html=True)

def draw_tile_svg(label, value, svg_icon, style_class):
    st.markdown(f'<div class="metric-tile {style_class}"><div class="tile-icon-svg" style="width:42px; height:42px; fill:white;">{svg_icon}</div><div><div class="tile-label">{label}</div><div class="tile-value">{value}</div></div></div>', unsafe_allow_html=True)

# SVG Icons
svg_people = '<svg viewBox="0 0 16 16"><path d="M7 14s-1 0-1-1 1-4 5-4 5 3 5 4-1 1-1 1H7zm4-6a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm-5.784 6A2.238 2.238 0 0 1 5 13c0-1.355.68-2.75 1.936-3.72A6.325 6.325 0 0 0 5 9c-4 0-5 3-5 4s1 1 1 1h4.216zM4.5 8a2.5 2.5 0 1 0 0-5 2.5 2.5 0 0 0 0 5z"/></svg>'
svg_cap = '<svg viewBox="0 0 16 16"><path d="M8.211 2.047a.5.5 0 0 0-.422 0l-7.5 3.5a.5.5 0 0 0 .025.917l7.5 3 7.5-3a.5.5 0 0 0 .025-.917l-7.5-3.5Z"/><path d="M4.176 9.032a.5.5 0 0 0-.656.327l-.5 1.7a.5.5 0 0 0 .254.539l1.5.75A.5.5 0 0 0 5.25 12h5.5a.5.5 0 0 0 .476-.346l.5-1.7a.5.5 0 0 0-.656-.327L10 10.25l-.117-.043-4 .876L4.176 9.032Z"/></svg>'
svg_warning = '<svg viewBox="0 0 16 16"><path d="M8.982 1.566a1.13 1.13 0 0 0-1.96 0L.165 13.233c-.457.778.091 1.767.98 1.767h13.713c.889 0 1.438-.99.98-1.767L8.982 1.566zM8 5c.535 0 .954.462.9.995l-.35 3.507a.552.552 0 0 1-1.1 0L7.1 5.995A.905.905 0 0 1 8 5zm.002 6a1 1 0 1 1 0 2 1 1 0 0 1 0-2z"/></svg>'
svg_chart = '<svg viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M18 20V10M12 20V4M6 20v-6"/></svg>'

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
# Bagian 4: SIDEBAR & HEADER RENDER
# ==================================
with st.sidebar:
    st.markdown('<p style="font-size:10px; font-weight:800; color:#94a3b8; text-transform:uppercase; letter-spacing:0.15em; margin-bottom:15px;">Navigasi Sistem</p>', unsafe_allow_html=True)
    st.sidebar.radio("Klik :", ["🚀 Dashboard Utama", "ℹ️ Tentang Dashboard"], key="nav_radio")
    
    st.sidebar.divider()
    col_kab = "kab_kota" if "kab_kota" in data_wilayah.columns else data_wilayah.columns[0]
    opsi = ["Semua"] + sorted(data_wilayah[col_kab].unique().tolist()) if not data_wilayah.empty else ["Semua"]
    kab_pilih = st.sidebar.selectbox("Filter Wilayah", opsi, key="selected_kab")

st.markdown('<div class="top-gradient-bar"></div>', unsafe_allow_html=True)
st.markdown("""
    <div class="header-balloon-card">
        <h2 style='color: #0d47a1; font-weight:800; margin: 0; font-size: 1.8rem;'>DASHBOARD SI-PANDAI SUMUT</h2>
        <p style='color: #1565c0; font-size: 14px; font-weight: 700; margin: 0;'>Sistem Informasi Pemetaan Anak Tidak Sekolah (ATS) Disabilitas</p>
    </div>
""", unsafe_allow_html=True)

# --- A. HALAMAN DASHBOARD ---
if st.session_state.page_view == "dashboard":
    df_f = data_wilayah.copy()
    if kab_pilih != "Semua": df_f = df_f[df_f[col_kab] == kab_pilih]

    # Matriks Capaian
    m1, m2, m3, m4 = st.columns(4)
    populasi = int(df_f.iloc[:,1].sum()) if not df_f.empty else 0
    belajar = int(df_f.iloc[:,2].sum()) if not df_f.empty else 0
    ats = int(df_f.iloc[:,3].sum()) if not df_f.empty else 0
    persen = f"{(belajar/populasi*100):.2f}%" if populasi > 0 else "0.00%"

    with m1: draw_tile_svg("Estimasi Sasaran", f"{populasi:,}", svg_people, "tile-orange")
    with m2: draw_tile_svg("Siswa Belajar", f"{belajar:,}", svg_cap, "tile-blue-light")
    with m3: draw_tile_svg("Anak Tidak Sekolah", f"{ats:,}", svg_warning, "tile-red-dark")
    with m4: draw_tile_svg("Persentase", persen, svg_chart, "tile-green-light")

    st.divider()
    cv1, cv2 = st.columns([1.6, 1.1])
    
    with cv1:
        st.subheader("🗺️ Peta Sebaran ATS")
        if not df_f.empty:
            fig_map = px.scatter_mapbox(df_f, lat="lat", lon="lon", size=df_f.columns[3], color=df_f.columns[3],
                                      color_continuous_scale="RdYlGn_r", zoom=7, height=450)
            fig_map.update_layout(mapbox_style="open-street-map", margin={"r":0,"t":0,"l":0,"b":0})
            st.plotly_chart(fig_map, use_container_width=True)

    with cv2:
        st.subheader("📊 5 Peringkat ATS Tertinggi")
        if not df_f.empty:
            ats_col = df_f.columns[3]
            df_top5 = df_f.sort_values(by=ats_col, ascending=False).head(5)
            
            # PERBAIKAN: Warna Balon Biru Gradasi (Cerah ke Royal)
            fig = px.bar(df_top5, x=ats_col, y=col_kab, orientation='h',
                         color=ats_col,
                         color_continuous_scale=[[0, '#00d2ff'], [1, '#3a7bd5']], # Gradasi Biru
                         text=ats_col)
            
            fig.update_traces(textposition='outside', marker_line_width=0, width=0.8)
            fig.update_layout(height=350, margin=dict(l=10, r=100, t=20, b=10),
                              showlegend=False, coloraxis_showscale=False,
                              plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)

    with st.expander("📋 Lihat Data Tabel"):
        st.dataframe(df_f, use_container_width=True)
