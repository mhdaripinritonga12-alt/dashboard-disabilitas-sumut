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
    page_icon="🎓",
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
# Bagian 1: CSS CUSTOM (HARD-LOCK SIDEBAR)
# ==================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
    html, body, [data-testid="stWidgetLabel"] { font-family: 'Inter', sans-serif !important; }

    /* --- FORMULA PENGUNCI SIDEBAR (ANTI-HIDE) --- */
    /* 1. Hilangkan tombol navigasi header (garis tiga / X) */
    [data-testid="stHeader"] { display: none !important; }
    
    /* 2. Hilangkan tombol collapse di dalam sidebar */
    button[kind="headerNoPadding"] { display: none !important; }
    [data-testid="sidebar-close-button"] { display: none !important; }
    
    /* 3. Hilangkan kontrol expander jika sidebar tersembunyi */
    [data-testid="collapsedControl"] { display: none !important; }

    /* 4. Paksa Sidebar Lebar & Permanen */
    section[data-testid="stSidebar"] {
        min-width: 320px !important;
        max-width: 320px !important;
        background-color: #ffffff !important;
        border-right: 1px solid #ececec !important;
    }
    
    /* Styling Konten Sidebar agar kontras */
    section[data-testid="stSidebar"] .stMarkdown p, 
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h5 {
        color: #0d47a1 !important;
    }

    .block-container {
        padding-top: 1.5rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
    }

    /* HEADER CARD */
    .header-card {
        background: linear-gradient(135deg, #f0f7ff 0%, #ffffff 100%);
        padding: 30px;
        border-radius: 20px;
        border-bottom: 5px solid #0d47a1;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        margin-bottom: 35px;
    }

    /* GRID METRIK PROPORSIONAL */
    .metric-grid {
        display: flex;
        justify-content: space-between;
        gap: 20px;
        margin-bottom: 25px;
    }
    .metric-item {
        flex: 1;
        padding: 25px;
        border-radius: 15px;
        color: white;
        display: flex;
        align-items: center;
        gap: 20px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.1);
        min-height: 120px;
    }
    .m-blue { background: linear-gradient(135deg, #0288d1 0%, #03a9f4 100%); }
    .m-red { background: linear-gradient(135deg, #d32f2f 0%, #f44336 100%); }
    .m-green { background: linear-gradient(135deg, #2e7d32 0%, #4caf50 100%); }
    
    .m-icon { font-size: 40px; opacity: 0.9; }
    .m-label { font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; opacity: 0.9; }
    .m-value { font-size: 30px; font-weight: 800; line-height: 1; }
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
    except:
        # Data dummy untuk preview jika file tidak ada
        df_dummy = pd.DataFrame({'kab_kota': ['Medan'], 'total': [1000], 'belajar': [800], 'ats': [200], 'lat': [3.59], 'lon': [98.67]})
        return df_dummy, pd.DataFrame()

data_wilayah, data_sekolah = load_all_data()

# ==================================
# Bagian 3: SIDEBAR (ANTI-HIDE & PROFESIONAL)
# ==================================
with st.sidebar:
    logo_b64 = get_base64_image("logo_sumut.png")
    if logo_b64:
        st.markdown(f'<div style="text-align:center;"><img src="data:image/png;base64,{logo_b64}" width="100"></div>', unsafe_allow_html=True)
    
    st.markdown("""
        <div style="text-align:center; margin-top:15px; margin-bottom:20px;">
            <h2 style="margin-bottom:0;">SI-PANDAI</h2>
            <p style="font-size:13px; font-weight:600; opacity:0.8;">DINAS PENDIDIKAN SUMUT</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("##### 🧭 Navigasi")
    nav = st.radio("Halaman", ["🚀 Dashboard Utama", "ℹ️ Tentang Dashboard"], label_visibility="collapsed")
    st.session_state.page_view = "dashboard" if "Dashboard" in nav else "tentang_dashboard"
    
    st.markdown("---")
    st.markdown("##### 🔎 Filter")
    col_kab = "kab_kota" if not data_wilayah.empty and "kab_kota" in data_wilayah.columns else data_wilayah.columns[0]
    opsi = ["Semua"] + sorted(data_wilayah[col_kab].unique().tolist())
    kab_pilih = st.selectbox("Wilayah", opsi, key="selected_kab", label_visibility="collapsed")
    
    st.markdown("<br><br>" * 3, unsafe_allow_html=True)
    st.divider()
    st.markdown("👤 **Inovator:**\nIma Safitri Sianipar, S.Kom")

# ==================================
# Bagian 4: KONTEN UTAMA
# ==================================
st.markdown(f"""
    <div class="header-card">
        <h1 style='color: #0d47a1; margin: 0; font-size: 2.5rem; font-weight: 800;'>DASHBOARD SI-PANDAI SUMUT</h1>
        <p style='color: #1565c0; font-size: 1.1rem; font-weight: 600; margin-top: 10px;'>
            Sistem Informasi Pemetaan Anak Tidak Sekolah (ATS) Disabilitas
        </p>
    </div>
""", unsafe_allow_html=True)

if st.session_state.page_view == "dashboard":
    df_f = data_wilayah.copy()
    if kab_pilih != "Semua": df_f = df_f[df_f[col_kab] == kab_pilih]

    # --- GRID 3 METRIK PROPORSIONAL ---
    st.markdown('<h4 style="color:#333; font-weight:700; margin-bottom:20px;">Matriks Capaian Sektoral</h4>', unsafe_allow_html=True)
    
    v_belajar = int(df_f.iloc[:,2].sum()) if not df_f.empty else 0
    v_ats = int(df_f.iloc[:,3].sum()) if not df_f.empty else 0
    v_total = int(df_f.iloc[:,1].sum()) if not df_f.empty else 0
    v_perc = f"{(v_belajar / v_total * 100):.2f}%" if v_total > 0 else "0.00%"

    st.markdown(f"""
    <div class="metric-grid">
        <div class="metric-item m-blue">
            <div class="m-icon">🎓</div>
            <div><div class="m-label">Siswa Belajar</div><div class="m-value">{v_belajar:,}</div></div>
        </div>
        <div class="metric-item m-red">
            <div class="m-icon">⚠️</div>
            <div><div class="m-label">Anak Tidak Sekolah</div><div class="m-value">{v_ats:,}</div></div>
        </div>
        <div class="metric-item m-green">
            <div class="m-icon">📈</div>
            <div><div class="m-label">Persentase</div><div class="m-value">{v_perc}</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()
    
    # --- VISUALISASI ---
    c1, c2 = st.columns([1.6, 1.1])
    with c1:
        st.subheader("🗺️ Peta Sebaran Spasial")
        if not df_f.empty and "lat" in df_f.columns:
            fig_map = px.scatter_mapbox(df_f, lat="lat", lon="lon", size=df_f.columns[3], color=df_f.columns[3],
                                       color_continuous_scale="RdYlGn_r", zoom=7, height=450)
            fig_map.update_layout(mapbox_style="carto-positron", margin={"r":0,"t":0,"l":0,"b":0})
            st.plotly_chart(fig_map, use_container_width=True)

    with c2:
        st.subheader("📊 5 Tertinggi ATS")
        if not df_f.empty:
            df_top = df_f.sort_values(by=df_f.columns[3], ascending=False).head(5)
            fig_bar = px.bar(df_top, x=df_f.columns[3], y=col_kab, orientation='h', 
                             color_continuous_scale="Blues", text_auto=True)
            fig_bar.update_layout(height=400, showlegend=False, margin=dict(l=0, r=0, t=10, b=0))
            st.plotly_chart(fig_bar, use_container_width=True)

elif st.session_state.page_view == "tentang_dashboard":
    st.header("ℹ️ Tentang SI-PANDAI")
    st.video("https://youtu.be/Wa4C8Ci3Iys?si=vbJRAa-G2dr2kYw8")

st.markdown("<br><hr>", unsafe_allow_html=True)
st.markdown("""
    <div style="text-align: center; color: #888; font-size: 11px;">
        © 2026 Dinas Pendidikan Sumatera Utara | Digitalisasi Pendidikan Khusus
    </div>
""", unsafe_allow_html=True)
