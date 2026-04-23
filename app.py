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
if "login" not in st.session_state: st.session_state.login = False
if "page_view" not in st.session_state: st.session_state.page_view = "dashboard"
if "selected_kab" not in st.session_state: st.session_state.selected_kab = "Semua"
if "selected_school_data" not in st.session_state: st.session_state.selected_school_data = None

def proses_logout():
    st.session_state.selected_kab = "Semua"
    st.session_state.login = False
    st.session_state.page_view = "dashboard"

def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

# ==================================
# Bagian 1: CSS CUSTOM (OFF-WHITE PROFESSIONAL SIDEBAR)
# ==================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
    html, body, [data-testid="stWidgetLabel"] { font-family: 'Inter', sans-serif !important; }

    .block-container {
        padding-top: 0.5rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
    }
    [data-testid="stHeader"] { display: none !important; }
    
    /* SEMBUNYIKAN TOMBOL SIDEBAR (SIDEBAR PERMANEN) */
    [data-testid="collapsedControl"] {
        display: none;
    }

    .top-gradient-bar {
        position: fixed;
        top: 0; left: 0; width: 100%; height: 5px;
        background: #1e88e5;
        z-index: 999999;
    }

    /* SIDEBAR STYLING - OFF WHITE PROFESSIONAL */
    [data-testid="stSidebar"] { 
        background-color: #fcfcfd !important; 
        border-right: 1px solid #f1f5f9 !important;
    }
    [data-testid="stSidebar"] * { color: #334155 !important; }
    
    /* Style for Sidebar Radio */
    div[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {
        background-color: transparent !important;
        border-radius: 8px !important;
        padding: 8px 12px !important;
        transition: all 0.2s;
    }
    div[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:hover {
        background-color: #f1f5f9 !important;
    }
    div[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label[data-selected="true"] {
        background-color: #e2e8f0 !important;
        border-left: 4px solid #1e88e5 !important;
    }

    div[data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] div { color: #1e293b !important; font-weight: 600 !important; }
    div[data-baseweb="popover"] li, div[data-baseweb="popover"] span { color: black !important; }

    /* Buttons */
    div.stButton > button:not([key^="btn_"]) {
        background: #1e88e5 !important;
        color: white !important; border-radius: 8px !important; 
        font-weight: 700 !important; height: 44px; border: none !important; width: 100%;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
    }

    .header-balloon-card {
        background: #ffffff !important;
        border-radius: 0px 0px 0px 0px;
        padding: 40px 0px;
        border-bottom: 1px solid #f1f5f9;
        text-align: left;
        margin-top: 0px;
        margin-bottom: 40px;
        width: 100% !important;
        display: block;
    }

    .metric-tile { padding: 30px; border-radius: 24px; color: #1e293b; border: 1px solid #f1f5f9; background: white; box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1); }
    .tile-label { font-size: 12px; font-weight: 800; text-transform: uppercase; color: #64748b; letter-spacing: 0.1em; margin-bottom: 8px; }
    .tile-value { font-size: 28px; font-weight: 700; color: #0f172a; }
    
    .insight-box { background-color: #f8fafc !important; border-radius: 16px; border: 1px solid #f1f5f9; padding: 20px; margin-top: 20px; }
    .insight-title { color: #1e293b; font-weight: 800; font-size: 13px; text-transform: uppercase; margin-bottom: 10px; letter-spacing: 0.05em; }
    .insight-text { color: #475569 !important; font-size: 14px; line-height: 1.6; }
</style>
""", unsafe_allow_html=True)

def draw_metric_card(label, value, icon_color="#1e88e5"):
    st.markdown(f'''
        <div class="metric-tile">
            <div class="tile-label">{label}</div>
            <div class="tile-value">{value}</div>
            <div style="height: 4px; width: 40px; background: {icon_color}; margin-top: 15px; border-radius: 2px;"></div>
        </div>
    ''', unsafe_allow_html=True)

# ==================================
# Bagian 2: LOAD DATA
# ==================================
@st.cache_data
def load_all_data():
    try:
        # Load data dari CSV sesuai instruksi
        df_ats = pd.read_csv("master_data_si_pandai.csv")
        df_sch = pd.read_csv("master_data_sekolah1.csv")
        
        # Bersihkan nama kolom
        df_ats.columns = df_ats.columns.str.strip().str.lower()
        df_sch.columns = df_sch.columns.str.strip().str.lower()
        
        return df_ats, df_sch
    except Exception as e:
        st.error(f"Gagal memuat data: {e}")
        return pd.DataFrame(), pd.DataFrame()

data_wilayah, data_sekolah = load_all_data()

# ==================================
# Bagian 4: SIDEBAR & NAVIGASI (OFF-WHITE STYLE)
# ==================================
with st.sidebar:
    st.markdown('<div style="padding: 20px 0px 40px 0px;">', unsafe_allow_html=True)
    logo_b64 = get_base64_image("logo_sumut.png")
    if logo_b64:
        st.markdown(f'''
            <div style="display:flex;flex-direction:column;gap:15px;">
                <img src="data:image/png;base64,{logo_b64}" width="60">
                <div>
                   <span style="font-size:22px;font-weight:800;color:#0f172a;letter-spacing:-0.02em;">SI-PANDAI</span>
                   <p style="font-size:10px;font-weight:700;color:#1e88e5;text-transform:uppercase;letter-spacing:0.1em;margin-top:2px;">Provinsi Sumatera Utara</p>
                </div>
            </div>
        ''', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def ubah_halaman():
    if "nav_radio" in st.session_state:
        pilihan = st.session_state.nav_radio
        if "Beranda Utama" in pilihan: 
            st.session_state.page_view = "dashboard"
            st.session_state.selected_kab = "Semua" 
        elif "Informasi Sistem" in pilihan: 
            st.session_state.page_view = "tentang_dashboard"

st.sidebar.markdown('<p style="font-size:10px; font-weight:800; color:#94a3b8; text-transform:uppercase; letter-spacing:0.15em; margin-bottom:15px;">Navigasi Utama</p>', unsafe_allow_html=True)
st.sidebar.radio(
    "Menu", 
    ["🏠 Beranda Utama", "ℹ️ Informasi Sistem"],
    key="nav_radio",
    on_change=ubah_halaman,
    label_visibility="collapsed"
)

st.sidebar.markdown('<div style="height:40px;"></div>', unsafe_allow_html=True)
st.sidebar.markdown('<p style="font-size:10px; font-weight:800; color:#94a3b8; text-transform:uppercase; letter-spacing:0.15em; margin-bottom:15px;">Wilayah Kerja</p>', unsafe_allow_html=True)

# Handle sidebar options safely to prevent TypeError when data is empty or contains NaN
col_kab = "kab_kota" # Default fallback
if not data_wilayah.empty:
    if "kab_kota" not in data_wilayah.columns and len(data_wilayah.columns) > 0:
        col_kab = data_wilayah.columns[0]
    
    # Filter out NaN values and ensure they are strings before sorting
    raw_opsi = data_wilayah[col_kab].dropna().unique().tolist()
    opsi = ["Semua"] + sorted([str(x) for x in raw_opsi])
else:
    opsi = ["Semua"]

kab_pilih = st.sidebar.selectbox("Pilih Kabupaten/Kota", opsi, key="selected_kab", label_visibility="collapsed")

st.sidebar.markdown('<div style="flex-grow:1;"></div>', unsafe_allow_html=True)
st.sidebar.markdown('''
    <div style="padding: 20px; border-top: 1px solid #f1f5f9;">
        <div style="display:flex; align-items:center; gap:8px;">
            <div style="width:8px; height:8px; background:#10b981; border-radius:50%;"></div>
            <span style="font-size:10px; font-weight:700; color:#64748b; text-transform:uppercase; letter-spacing:0.1em;">Sistem Online</span>
        </div>
    </div>
''', unsafe_allow_html=True)

# ==================================
# Bagian 5: HEADER (EXACT REDACTION)
# ==================================
st.markdown('<div class="top-gradient-bar"></div>', unsafe_allow_html=True)
st.markdown("""
    <div class="header-balloon-card">
        <h2 style='color: #0f172a; font-weight:800; margin: 0; font-size: 1.85rem; tracking-tight: -0.025em;'>
            SI-PANDAI Sistem Informasi Pemetaan Anak Tidak Sekolah Disabilitas
        </h2>
        <p style='color: #64748b; font-size: 12px; font-weight: 700; margin-top: 8px; text-transform: uppercase; letter-spacing: 0.15em;'>
            Dinas Pendidikan Provinsi Sumatera Utara
        </p>
    </div>
""", unsafe_allow_html=True)

# --- A. HALAMAN DASHBOARD ---
if st.session_state.page_view == "dashboard":
    df_f = data_wilayah.copy()
    if kab_pilih != "Semua": df_f = df_f[df_f[col_kab] == kab_pilih]

    # LOGIKA ATS: Ambil langsung dari kolom 'ats' sesuai instruksi
    ats_col = "ats"
    belajar_col = "belajar"
    if not df_f.empty:
        if "ats" not in df_f.columns and len(df_f.columns) > 3:
            ats_col = df_f.columns[3]
        if "belajar" not in df_f.columns and len(df_f.columns) > 2:
            belajar_col = df_f.columns[2]
    
    total_ats = int(df_f[ats_col].sum()) if not df_f.empty and ats_col in df_f.columns else 0
    total_belajar = int(df_f[belajar_col].sum()) if not df_f.empty and belajar_col in df_f.columns else 0
    
    rasio = (total_belajar / (total_belajar + total_ats) * 100) if (total_belajar + total_ats) > 0 else 0

    m1, m2, m3 = st.columns(3)
    with m1: draw_metric_card("Siswa Belajar", f"{total_belajar:,}", "#3b82f6")
    with m2: draw_metric_card("Anak Tidak Sekolah", f"{total_ats:,}", "#f59e0b")
    with m3: draw_metric_card("Rasio Partisipasi", f"{rasio:.2f}%", "#10b981")

    st.markdown('<div style="height:40px;"></div>', unsafe_allow_html=True)

    cv1, cv2 = st.columns([1.5, 1])
    with cv1:
        st.markdown('<p style="font-size:12px; font-weight:800; color:#64748b; text-transform:uppercase; letter-spacing:0.1em; margin-bottom:20px;">Sebaran Spasial Wilayah</p>', unsafe_allow_html=True)
        if not df_f.empty:
            fig_map = px.scatter_mapbox(
                df_f, lat="lat", lon="lon", size=ats_col, color=ats_col,
                color_continuous_scale="RdYlGn_r", hover_name=col_kab, 
                hover_data={ats_col: True, "lat": False, "lon": False},
                zoom=7.5, height=500
            )
            fig_map.update_layout(mapbox_style="carto-positron", margin={"r":0,"t":0,"l":0,"b":0}, coloraxis_showscale=False)
            st.plotly_chart(fig_map, use_container_width=True)

    with cv2:
        st.markdown('<p style="font-size:12px; font-weight:800; color:#64748b; text-transform:uppercase; letter-spacing:0.1em; margin-bottom:20px;">Ranking ATS Tertinggi</p>', unsafe_allow_html=True)
        if not df_f.empty:
            df_top5 = df_f.sort_values(by=ats_col, ascending=False).head(5)
            fig = px.bar(
                df_top5, x=ats_col, y=col_kab, orientation='h',
                color_discrete_sequence=['#3b82f6'], text=ats_col
            )
            fig.update_traces(textposition='outside', marker_color='#1e88e5', marker_line_width=0, opacity=0.8)
            fig.update_layout(
                height=400, margin=dict(l=0, r=0, t=0, b=0),
                showlegend=False, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)'
            )
            fig.update_xaxes(showgrid=True, gridcolor='#f1f5f9', showticklabels=False)
            fig.update_yaxes(categoryorder='total ascending', tickfont=dict(size=11, color='#475569'))
            st.plotly_chart(fig, use_container_width=True)

            st.markdown(f"""
                <div class="insight-box">
                    <div class="insight-title">Informasi Wilayah: {kab_pilih}</div>
                    <p class="insight-text">
                        Data menunjukkan terdapat {total_ats:,} jiwa Anak Tidak Sekolah di wilayah ini. 
                        Prioritas alokasi sarana prasarana diarahkan pada mitigasi titik ATS tertinggi untuk menekan rasio putus sekolah.
                    </p>
                </div>
            """, unsafe_allow_html=True)

    st.markdown('<div style="height:60px;"></div>', unsafe_allow_html=True)
    
    st.markdown('<p style="font-size:12px; font-weight:800; color:#64748b; text-transform:uppercase; letter-spacing:0.1em; margin-bottom:20px;">Repository Data Wilayah</p>', unsafe_allow_html=True)
    st.dataframe(df_f, use_container_width=True)
    
    csv = df_f.to_csv(index=False).encode('utf-8')
    st.download_button(
        "Export CSV 📥", csv, file_name=f'data_si_pandai_{kab_pilih}.csv', mime='text/csv'
    )

elif st.session_state.page_view == "tentang_dashboard":
    st.markdown('<div class="insight-box" style="margin-top:0;">', unsafe_allow_html=True)
    st.markdown('### Mengenal SI-PANDAI')
    st.markdown("""
        **SI-PANDAI SUMUT** adalah sistem monitoring berbasis data untuk memetakan Anak Tidak Sekolah (ATS) disabilitas. 
        Sistem ini bertujuan untuk memberikan transparansi data bagi pengambil kebijakan di Dinas Pendidikan Provinsi Sumatera Utara.
        
        **Tujuan Utama:**
        - Memetakan sebaran anak disabilitas yang belum menempuh pendidikan.
        - Menjadi instrumen perencanaan pembangunan Unit Sekolah Baru (USB) atau Ruang Kelas Baru (RKB).
        - Menghasilkan data rujukan yang akurat bagi Bidang Pembinaan Pendidikan Khusus.
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("⬅️ Kembali ke Beranda"):
        st.session_state.page_view = "dashboard"
        st.rerun()

# ==================================
# Bagian Akhir: FOOTER
# ==================================
st.markdown('<div style="height:100px;"></div>', unsafe_allow_html=True)
st.divider()
st.markdown("""
    <div style="text-align: center; color: #94a3b8; font-size: 11px; padding: 40px 0px;">
        <p style="font-weight: 800; text-transform: uppercase; letter-spacing: 0.1em; color: #64748b; margin-bottom: 8px;">
            Dinas Pendidikan Provinsi Sumatera Utara
        </p>
        <p style="margin-bottom: 2px;">Jl. Teuku Cik Ditiro No.1-D, Madras Hulu, Kota Medan</p>
        <p>© 2026 SI-PANDAI | Hak Cipta Dilindungi</p>
    </div>
""", unsafe_allow_html=True)
