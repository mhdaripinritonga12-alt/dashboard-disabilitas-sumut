import streamlit as st
import pandas as pd
import plotly.express as px
import os
import base64
import streamlit.components.v1 as components

# ==================================
# 0. KONFIGURASI HALAMAN
# ==================================
st.set_page_config(
    page_title="SI-PANDAI SUMUT",
    layout="wide",
    page_icon="🎓",
    initial_sidebar_state="expanded"
)

# Inisialisasi State
if "page_view" not in st.session_state: st.session_state.page_view = "dashboard"
if "selected_kab" not in st.session_state: st.session_state.selected_kab = "Semua"
if "selected_school_data" not in st.session_state: st.session_state.selected_school_data = None

# ==================================
# 1. CSS CORPORATE (PROFESIONAL & BERSIH)
# ==================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
    
    /* Global Styles */
    html, body, [data-testid="stWidgetLabel"] { font-family: 'Inter', sans-serif !important; }
    .stApp { background-color: #f8fafc; }

    /* Clean Sidebar */
    [data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #e2e8f0;
    }
    [data-testid="stSidebar"] * { color: #1e293b !important; }
    
    /* Header Section */
    .app-header {
        background-color: white;
        padding: 30px 40px;
        border-bottom: 3px solid #2563eb;
        border-radius: 0 0 20px 20px;
        margin-bottom: 40px;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.05);
    }
    .header-title {
        color: #1e3a8a;
        font-weight: 800;
        font-size: 24px;
        margin: 0;
        line-height: 1.2;
    }

    /* Metric Tiles */
    .metric-box {
        background: white;
        padding: 30px;
        border-radius: 20px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1);
        text-align: center;
    }
    .m-label { font-size: 11px; font-weight: 700; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.1em; }
    .m-value { font-size: 32px; font-weight: 800; color: #1e293b; margin-top: 5px; }

    /* Button Styling */
    div.stButton > button {
        background: #2563eb !important;
        color: white !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        border: none !important;
        width: 100%;
        padding: 10px;
    }
    div.stButton > button:hover { background: #1d4ed8 !important; }
</style>
""", unsafe_allow_html=True)

def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

# ==================================
# 2. LOAD DATA
# ==================================
@st.cache_data
def load_data():
    try:
        df_ats = pd.read_csv("master_data_si_pandai.csv")
        df_sch = pd.read_csv("master_data_sekolah1.csv")
        for df in [df_ats, df_sch]:
            df.columns = df.columns.str.strip().str.lower()
        return df_ats, df_sch
    except: return pd.DataFrame(), pd.DataFrame()

df_ats, df_sch = load_data()

# ==================================
# 3. SIDEBAR (RAPID & CLEAN)
# ==================================
with st.sidebar:
    logo_b64 = get_base64_image("logo_sumut.png")
    if logo_b64:
        st.markdown(f'<div style="text-align:center; padding-bottom:20px;"><img src="data:image/png;base64,{logo_b64}" width="80"></div>', unsafe_allow_html=True)
    
    st.markdown("<h3 style='text-align:center; font-weight:800;'>SI-PANDAI</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-size:10px; color:#94a3b8; font-weight:700;'>DINAS PENDIDIKAN SUMUT</p>", unsafe_allow_html=True)
    st.divider()

    if st.button("🚀 BERANDA"):
        st.session_state.page_view = "dashboard"
        st.session_state.selected_kab = "Semua"
        st.rerun()

    if st.button("ℹ️ INFORMASI"):
        st.session_state.page_view = "about"
        st.rerun()

    st.divider()
    st.markdown("##### 🔎 FILTER WILAYAH")
    col_kab = "kab_kota" if "kab_kota" in df_ats.columns else df_ats.columns[0]
    opsi = ["Semua"] + sorted(df_ats[col_kab].unique().tolist()) if not df_ats.empty else ["Semua"]
    kab_pilih = st.selectbox("Pilih Kabupaten/Kota", opsi, key="selected_kab")

# ==================================
# 4. HEADER (SESUAI REQUEST)
# ==================================
st.markdown(f"""
    <div class="app-header">
        <h1 class="header-title">SI-PANDAI Sistem Informasi Pemetaan Anak Tidak Sekolah Disabilitas</h1>
        <p style="color:#94a3b8; font-size:13px; font-weight:700; margin-top:5px; text-transform:uppercase; letter-spacing:0.1em;">
            Provinsi Sumatera Utara
        </p>
    </div>
""", unsafe_allow_html=True)

# ==================================
# 5. DASHBOARD MAIN
# ==================================
if st.session_state.page_view == "dashboard":
    df_f = df_ats.copy()
    if kab_pilih != "Semua": df_f = df_f[df_f[col_kab] == kab_pilih]

    # Metrics
    m1, m2, m3 = st.columns(3)
    v_belajar = int(df_f.iloc[:,2].sum()) if not df_f.empty else 0
    # AMBIL LANGSUNG DARI KOLOM ATS TANPA RUMUS
    v_ats = int(df_f.iloc[:,3].sum()) if not df_f.empty else 0
    v_rasio = f"{(v_belajar / (v_belajar + v_ats) * 100):.2f}%" if (v_belajar + v_ats) > 0 else "0.00%"

    with m1: st.markdown(f'<div class="metric-box"><div class="m-label">Siswa Belajar</div><div class="m-value">{v_belajar:,}</div></div>', unsafe_allow_html=True)
    with m2: st.markdown(f'<div class="metric-box"><div class="m-label">Anak Tidak Sekolah</div><div class="m-value" style="color:#f97316;">{v_ats:,}</div></div>', unsafe_allow_html=True)
    with m3: st.markdown(f'<div class="metric-box"><div class="m-label">Partisipasi</div><div class="m-value" style="color:#10b981;">{v_rasio}</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Graphs
    c1, c2 = st.columns([1.6, 1])
    with c1:
        st.markdown("##### 🗺️ Sebaran Spasial ATS")
        if not df_f.empty:
            ats_col_name = df_f.columns[3]
            fig_map = px.scatter_mapbox(
                df_f, lat="lat", lon="lon", size=ats_col_name, color=ats_col_name,
                color_continuous_scale="Viridis", zoom=8, height=450
            )
            fig_map.update_layout(mapbox_style="open-street-map", margin={"r":0,"t":0,"l":0,"b":0}, coloraxis_showscale=False)
            st.plotly_chart(fig_map, use_container_width=True)

    with c2:
        st.markdown("##### 📊 Wilayah Prioritas (Top 5)")
        if not df_f.empty:
            df_top = df_f.sort_values(by=df_f.columns[3], ascending=False).head(5)
            fig_bar = px.bar(df_top, x=df_f.columns[3], y=col_kab, orientation='h', color=df_f.columns[3], color_continuous_scale="Blues")
            fig_bar.update_layout(height=400, showlegend=False, coloraxis_showscale=False)
            st.plotly_chart(fig_bar, use_container_width=True)

    # Database Table
    st.markdown("##### 📋 Database Wilayah")
    st.dataframe(df_f, use_container_width=True)

# ----------------- PAGE: ABOUT -----------------
elif st.session_state.page_view == "about":
    st.markdown("### Mengenal SI-PANDAI")
    st.write("Sistem digitalisasi pemetaan Anak Tidak Sekolah Disabilitas di Provinsi Sumatera Utara.")
    with st.container(border=True):
        st.info("**Inovator**: Ima Safitri Sianipar, S.Kom - Dinas Pendidikan Provinsi Sumatera Utara")
    
    st.markdown("##### 🎬 Video Tutorial")
    st.video("https://youtu.be/Wa4C8Ci3Iys?si=vbJRAa-G2dr2kYw8")

# ==================================
# 6. FOOTER
# ==================================
st.divider()
st.markdown("""
    <div style="text-align:center; color:#94a3b8; font-size:11px; padding-bottom:40px;">
        <p><b>DINAS PENDIDIKAN PROVINSI SUMATERA UTARA</b></p>
        <p>Bidang Pembinaan Pendidikan Khusus | © 2026 SI-PANDAI SUMUT</p>
    </div>
""", unsafe_allow_html=True)
