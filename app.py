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
if "selected_school_data" not in st.session_state: st.session_state.selected_school_data = None

def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

# ==================================
# Bagian 1: CSS CUSTOM (SIDEBAR PERMANEN & GRID RAPI)
# ==================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
    html, body, [data-testid="stWidgetLabel"] { font-family: 'Inter', sans-serif !important; }

    /* --- SIDEBAR PERMANEN (TIDAK BISA DITUTUP) --- */
    [data-testid="sidebar-close-button"] { display: none !important; }
    [data-testid="collapsedControl"] { display: none !important; }
    
    /* Mengunci Lebar Sidebar */
    section[data-testid="stSidebar"] {
        min-width: 320px !important;
        max-width: 320px !important;
        background: linear-gradient(180deg, #1e88e5 0%, #0d47a1 100%) !important;
    }
    section[data-testid="stSidebar"] * { color: white !important; }

    .block-container {
        padding-top: 1rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
    }
    [data-testid="stHeader"] { display: none !important; }

    /* HEADER STYLING */
    .header-card {
        background: linear-gradient(90deg, #f0f7ff 0%, #ffffff 100%) !important;
        border-radius: 15px;
        padding: 25px;
        border-bottom: 4px solid #0d47a1;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        text-align: center;
        margin-bottom: 30px;
    }

    /* GRID METRIK PROPORSIONAL */
    .metric-grid-container {
        display: flex;
        justify-content: space-between;
        gap: 20px;
        margin-bottom: 30px;
    }
    .metric-tile {
        flex: 1;
        padding: 25px;
        border-radius: 15px;
        color: white;
        display: flex;
        align-items: center;
        gap: 15px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
    }
    .metric-tile:hover { transform: translateY(-5px); }
    
    .tile-blue { background: linear-gradient(135deg, #0288d1 0%, #03a9f4 100%); }
    .tile-red { background: linear-gradient(135deg, #d32f2f 0%, #f44336 100%); }
    .tile-green { background: linear-gradient(135deg, #2e7d32 0%, #4caf50 100%); }
    
    .tile-icon { font-size: 40px; opacity: 0.9; }
    .tile-label { font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; }
    .tile-value { font-size: 28px; font-weight: 800; line-height: 1; }

    /* Buttons Style */
    div.stButton > button {
        border-radius: 10px !important;
        font-weight: 700 !important;
        height: 45px;
    }
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
# Bagian 3: SIDEBAR (LOGIKA NAVIGASI)
# ==================================
with st.sidebar:
    logo_b64 = get_base64_image("logo_sumut.png")
    if logo_b64:
        st.markdown(f'<div style="text-align:center;"><img src="data:image/png;base64,{logo_b64}" width="100"></div>', unsafe_allow_html=True)
    
    st.markdown("<h2 style='text-align:center;'>SI-PANDAI SUMUT</h2>", unsafe_allow_html=True)
    st.divider()
    
    nav = st.radio("🧭 Navigasi Sistem", ["🚀 Dashboard Utama", "ℹ️ Tentang Dashboard"])
    st.session_state.page_view = "dashboard" if "Dashboard" in nav else "tentang_dashboard"
    
    st.divider()
    st.subheader("🔎 Filter Wilayah")
    col_kab = "kab_kota" if not data_wilayah.empty and "kab_kota" in data_wilayah.columns else data_wilayah.columns[0]
    opsi = ["Semua"] + sorted(data_wilayah[col_kab].unique().tolist()) if not data_wilayah.empty else ["Semua"]
    kab_pilih = st.sidebar.selectbox("Kabupaten / Kota", opsi, key="selected_kab")
    
    st.divider()
    st.markdown(f"**Inovator:**\nIma Safitri Sianipar, S.Kom")

# ==================================
# Bagian 4: HEADER & MAIN CONTENT
# ==================================
st.markdown(f"""
    <div class="header-card">
        <h1 style='color: #0d47a1; margin: 0; font-size: 2.5rem;'>DASHBOARD SI-PANDAI SUMUT</h1>
        <p style='color: #1565c0; font-size: 1.1rem; font-weight: 600; margin-top: 10px;'>
            Sistem Informasi Pemetaan Anak Tidak Sekolah (ATS) Disabilitas
        </p>
    </div>
""", unsafe_allow_html=True)

if st.session_state.page_view == "dashboard":
    df_f = data_wilayah.copy()
    if kab_pilih != "Semua": df_f = df_f[df_f[col_kab] == kab_pilih]

    # --- GRID 3 METRIK PROPORSIONAL ---
    v_belajar = int(df_f.iloc[:,2].sum()) if not df_f.empty else 0
    v_ats = int(df_f.iloc[:,3].sum()) if not df_f.empty else 0
    v_total = int(df_f.iloc[:,1].sum()) if not df_f.empty else 0
    v_perc = f"{(v_belajar / v_total * 100):.2f}%" if v_total > 0 else "0.00%"

    st.markdown(f"""
    <div class="metric-grid-container">
        <div class="metric-tile tile-blue">
            <div class="tile-icon">🎓</div>
            <div>
                <div class="tile-label">Siswa Belajar</div>
                <div class="tile-value">{v_belajar:,}</div>
            </div>
        </div>
        <div class="metric-tile tile-red">
            <div class="tile-icon">⚠️</div>
            <div>
                <div class="tile-label">Anak Tidak Sekolah</div>
                <div class="tile-value">{v_ats:,}</div>
            </div>
        </div>
        <div class="metric-tile tile-green">
            <div class="tile-icon">📊</div>
            <div>
                <div class="tile-label">Persentase Partisipasi</div>
                <div class="tile-value">{v_perc}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- PETA & GRAFIK ---
    st.divider()
    c1, c2 = st.columns([1.6, 1.1])
    with c1:
        st.subheader("🗺️ Peta Sebaran Spasial")
        if not df_f.empty:
            fig_map = px.scatter_mapbox(df_f, lat="lat", lon="lon", size=df_f.columns[3], color=df_f.columns[3],
                                       color_continuous_scale="RdYlGn_r", zoom=7, height=450)
            fig_map.update_layout(mapbox_style="carto-positron", margin={"r":0,"t":0,"l":0,"b":0})
            st.plotly_chart(fig_map, use_container_width=True)

    with c2:
        st.subheader("📊 5 Tertinggi ATS")
        if not df_f.empty:
            df_top = df_f.sort_values(by=df_f.columns[3], ascending=False).head(5)
            fig_bar = px.bar(df_top, x=df_f.columns[3], y=col_kab, orientation='h', color=df_f.columns[3], 
                             color_continuous_scale="Blues", text_auto=True)
            fig_bar.update_layout(height=350, showlegend=False, margin=dict(l=0, r=0, t=10, b=0))
            st.plotly_chart(fig_bar, use_container_width=True)

    # --- DETAIL SEKOLAH ---
    if kab_pilih != "Semua":
        st.divider()
        st.subheader(f"🏫 Satuan Pendidikan di {kab_pilih}")
        sch_wil = data_sekolah[data_sekolah[col_kab] == kab_pilih] if not data_sekolah.empty else pd.DataFrame()
        if not sch_wil.empty:
            cols = st.columns(3)
            for i, row in enumerate(sch_wil.itertuples()):
                with cols[i % 3]:
                    with st.container(border=True):
                        if st.button(getattr(row, 'nama_sekolah', 'SEKOLAH').upper(), key=f"sch_{i}", use_container_width=True):
                            st.session_state.selected_school_data = row._asdict()
                            st.session_state.page_view = "detail"
                            st.rerun()

elif st.session_state.page_view == "tentang_dashboard":
    st.header("ℹ️ Tentang SI-PANDAI")
    st.video("https://youtu.be/Wa4C8Ci3Iys?si=vbJRAa-G2dr2kYw8")

# ==================================
# Bagian 5: FOOTER
# ==================================
st.markdown("<br><hr>", unsafe_allow_html=True)
st.markdown("""
    <div style="text-align: center; color: #888; font-size: 11px; padding-bottom: 20px;">
        © 2026 DINAS PENDIDIKAN PROVINSI SUMATERA UTARA | Digitalisasi Pemetaan ATS Disabilitas
    </div>
""", unsafe_allow_html=True)
