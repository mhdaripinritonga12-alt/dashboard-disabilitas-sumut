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

# Inisialisasi State yang Benar
if "login" not in st.session_state: st.session_state.login = False
if "page_view" not in st.session_state: st.session_state.page_view = "dashboard"
if "selected_kab" not in st.session_state: st.session_state.selected_kab = "Semua"
if "selected_school_data" not in st.session_state: st.session_state.selected_school_data = None

def proses_logout():
    st.session_state.login = False
    st.session_state.page_view = "dashboard"
    st.rerun()

def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

# ==================================
# Bagian 1: CSS CUSTOM (SANGAT PENTING)
# ==================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
    html, body, [data-testid="stWidgetLabel"] { font-family: 'Inter', sans-serif !important; }
    .block-container { padding-top: 0rem !important; padding-left: 1rem !important; padding-right: 1rem !important; }
    [data-testid="stHeader"] { display: none !important; }
    .top-gradient-bar { position: fixed; top: 0; left: 0; width: 100%; height: 10px; background: linear-gradient(90deg, #ff8a00, #e52e71, #9c27b0, #1e88e5, #4caf50, #ffeb3b); z-index: 999999; }
    [data-testid="stSidebar"] { background: linear-gradient(180deg, #1e88e5 0%, #0d47a1 100%) !important; }
    [data-testid="stSidebar"] * { color: white !important; }
    .header-balloon-card { background: linear-gradient(90deg, #f0f7ff 0%, #d1e9ff 100%) !important; border-radius: 0px 0px 15px 15px; padding: 15px 0px; text-align: center; margin-bottom: 20px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }
    div[data-testid="stPlotlyChart"] svg g.plots g.barlayer g.tracepath path { rx: 18px !important; ry: 18px !important; }
    .metric-tile { padding: 20px; border-radius: 12px; color: white; margin-bottom: 15px; display: flex; align-items: center; gap: 15px; }
    .tile-orange { background: linear-gradient(135deg, #ff9800 0%, #f57c00 100%); }
    .tile-blue-light { background: linear-gradient(135deg, #03a9f4 0%, #0288d1 100%); }
    .tile-red-dark { background: linear-gradient(135deg, #ff4b2b 0%, #ff416c 100%); }
    .tile-green-light { background: linear-gradient(135deg, #4caf50 0%, #2e7d32 100%); }
</style>
""", unsafe_allow_html=True)

def draw_tile_svg(label, value, svg_icon, style_class):
    st.markdown(f'<div class="metric-tile {style_class}"><div style="width:42px;height:42px;fill:white;">{svg_icon}</div><div><div style="font-size:14px; font-weight:800;">{label}</div><div style="font-size:22px; font-weight:800;">{value}</div></div></div>', unsafe_allow_html=True)

# SVG Icons
svg_people = '<svg viewBox="0 0 16 16"><path d="M7 14s-1 0-1-1 1-4 5-4 5 3 5 4-1 1-1 1H7zm4-6a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm-5.784 6A2.238 2.238 0 0 1 5 13c0-1.355.68-2.75 1.936-3.72A6.325 6.325 0 0 0 5 9c-4 0-5 3-5 4s1 1 1 1h4.216zM4.5 8a2.5 2.5 0 1 0 0-5 2.5 2.5 0 0 0 0 5z"/></svg>'
svg_cap = '<svg viewBox="0 0 16 16"><path d="M8.211 2.047a.5.5 0 0 0-.422 0l-7.5 3.5a.5.5 0 0 0 .025.917l7.5 3 7.5-3a.5.5 0 0 0 .025-.917l-7.5-3.5Z"/><path d="M4.176 9.032a.5.5 0 0 0-.656.327l-.5 1.7a.5.5 0 0 0 .254.539l1.5.75A.5.5 0 0 0 5.25 12h5.5a.5.5 0 0 0 .476-.346l.5-1.7a.5.5 0 0 0-.656-.327L10 10.25l-.117-.043-4 .876L4.176 9.032Z"/></svg>'
svg_warning = '<svg viewBox="0 0 16 16"><path d="M8.982 1.566a1.13 1.13 0 0 0-1.96 0L.165 13.233c-.457.778.091 1.767.98 1.767h13.713c.889 0 1.438-.99.98-1.767L8.982 1.566zM8 5c.535 0 .954.462.9.995l-.35 3.507a.552.552 0 0 1-1.1 0L7.1 5.995A.905.905 0 0 1 8 5zm.002 6a1 1 0 1 1 0 2 1 1 0 0 1 0-2z"/></svg>'
svg_chart = '<svg viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M18 20V10M12 20V4M6 20v-6"/></svg>'

# ==================================
# Bagian 2: DATA LOADING
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

# =========================
# Bagian 3: LOGIN
# =========================
if not st.session_state.login:
    _, col_logo, _ = st.columns([2, 0.6, 2])
    with col_logo:
        if os.path.exists("logo_sumut.png"): st.image("logo_sumut.png", width=100)
    _, col_card, _ = st.columns([1.5, 2, 1.5])
    with col_card:
        with st.container(border=True):
            st.markdown("<h3 style='text-align:center; color:#0d47a1;'>LOGIN USER</h3>", unsafe_allow_html=True)
            u = st.text_input("Username")
            p = st.text_input("Password", type="password")
            if st.button("MASUK", use_container_width=True):
                if u == "admin" and p == "admin": 
                    st.session_state.login = True
                    st.rerun()
    st.stop()

# ==================================
# Bagian 4: SIDEBAR & NAVIGASI (FIX)
# ==================================
def fungsi_navigasi():
    pilihan = st.session_state.nav_radio
    if "Dashboard" in pilihan: st.session_state.page_view = "dashboard"
    elif "Pendidikan Khusus" in pilihan: st.session_state.page_view = "tentang_pk"
    elif "Tentang Dashboard" in pilihan: st.session_state.page_view = "tentang_dashboard"

with st.sidebar:
    logo_b64 = get_base64_image("logo_sumut.png")
    if logo_b64:
        st.markdown(f'<center><img src="data:image/png;base64,{logo_b64}" width="80"><br><b>SI-PANDAI SUMUT</b></center>', unsafe_allow_html=True)
    
    st.sidebar.radio(
        "Navigasi:", 
        ["🚀 Dashboard", "🎓 Pendidikan Khusus", "ℹ️ Tentang Dashboard"],
        key="nav_radio",
        on_change=fungsi_navigasi
    )
    st.sidebar.divider()
    
    col_kab = "kab_kota" if "kab_kota" in data_wilayah.columns else data_wilayah.columns[0]
    opsi = ["Semua"] + sorted(data_wilayah[col_kab].unique().tolist()) if not data_wilayah.empty else ["Semua"]
    kab_pilih = st.sidebar.selectbox("Filter Wilayah", opsi, key="selected_kab")
    
    st.sidebar.button("Logout ⏻", use_container_width=True, on_click=proses_logout)

# ==================================
# Bagian 5: HEADER & MAIN CONTENT (THE FIX)
# ==================================
st.markdown('<div class="top-gradient-bar"></div>', unsafe_allow_html=True)

# --- 1. HALAMAN DASHBOARD ---
if st.session_state.page_view == "dashboard":
    st.markdown("""
        <div class="header-balloon-card">
            <h2 style='color: #0d47a1; font-weight:800; margin: 0;'>DASHBOARD SI-PANDAI SUMUT</h2>
            <p style='color: #1565c0; font-size: 14px; font-weight: 700; margin: 0;'>
                Pemetaan Anak Tidak Sekolah Disabilitas Sumatera Utara
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<p style="font-size:24px; font-weight:800; color:#0d47a1;">Matriks Capaian Sektoral</p>', unsafe_allow_html=True)
    
    df_f = data_wilayah.copy()
    if kab_pilih != "Semua": df_f = df_f[df_f[col_kab] == kab_pilih]

    # Tiles
    m1, m2, m3, m4 = st.columns(4)
    v_a = int(df_f.iloc[:,3].sum()) if not df_f.empty else 0
    with m1: draw_tile_svg("Disabilitas", f"{int(df_f.iloc[:,1].sum()):,}", svg_people, "tile-orange")
    with m2: draw_tile_svg("Siswa", f"{int(df_f.iloc[:,2].sum()):,}", svg_cap, "tile-blue-light")
    with m3: draw_tile_svg("ATS", f"{v_a:,}", svg_warning, "tile-red-dark")
    with m4: draw_tile_svg("Partisipasi", "85%", svg_chart, "tile-green-light")

    st.divider()
    cv1, cv2 = st.columns([1.6, 1.1])
    with cv1:
        st.subheader("🗺️ Peta Sebaran")
        if not df_f.empty:
            fig_map = px.scatter_mapbox(df_f, lat="lat", lon="lon", size=df_f.columns[3], color=df_f.columns[3],
                                        color_continuous_scale="RdYlGn_r", zoom=8, height=450)
            fig_map.update_layout(mapbox_style="open-street-map", margin={"r":0,"t":0,"l":0,"b":0})
            st.plotly_chart(fig_map, use_container_width=True)
    with cv2:
        st.subheader("📊 Top 5 Wilayah")
        if not df_f.empty:
            df_top5 = df_f.sort_values(by=df_f.columns[3], ascending=False).head(5)
            fig_bar = px.bar(df_top5, x=df_f.columns[3], y=col_kab, orientation='h', 
                             color_continuous_scale='Viridis', text=df_f.columns[3])
            fig_bar.update_traces(width=0.7)
            fig_bar.update_layout(height=350, bargap=0.1, showlegend=False)
            st.plotly_chart(fig_bar, use_container_width=True)

# --- 2. HALAMAN TENTANG DASHBOARD ---
elif st.session_state.page_view == "tentang_dashboard":
    st.markdown('<p style="font-size:28px; font-weight:800; color:#0d47a1; margin-top:20px;">ℹ️ Tentang SI-PANDAI SUMUT</p>', unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown("""
        ### 🖥️ Deskripsi Sistem
        **SI-PANDAI SUMUT** (Sistem Informasi Pemetaan Anak Tidak Sekolah Disabilitas) adalah platform analitik digital yang dirancang untuk mengintegrasikan data anak tidak sekolah dengan kebutuhan sarana prasarana pendidikan khusus di Provinsi Sumatera Utara.

        ### 🎯 Tujuan Dashboard
        1. **Memetakan Sebaran ATS:** Mengidentifikasi koordinat tepat di mana anak-anak disabilitas yang belum sekolah berada.
        2. **Optimalisasi Kebijakan:** Memberikan rekomendasi data yang akurat bagi pengambil kebijakan di Dinas Pendidikan.
        3. **Efisiensi Anggaran:** Memastikan bantuan RKB (Ruang Kelas Baru) atau rehabilitasi sekolah tepat sasaran.

        ### 🚀 Fitur Utama
        * **Geospatial Mapping:** Peta interaktif sebaran ATS berbasis koordinat lat/lon.
        * **Real-time Metrics:** Matriks otomatis untuk penduduk disabilitas, jumlah siswa, dan angka partisipasi.
        """)
        st.divider()
        if st.button("⬅️ KEMBALI KE DASHBOARD", use_container_width=True):
            st.session_state.page_view = "dashboard"
            st.rerun()

# --- 3. HALAMAN PENDIDIKAN KHUSUS ---
elif st.session_state.page_view == "tentang_pk":
    st.markdown('### 🎓 Kebijakan Pendidikan Khusus')
    st.info("Program Bidang Pembinaan PK Sumatera Utara.")
    if st.button("⬅️ Kembali"):
        st.session_state.page_view = "dashboard"
        st.rerun()

# --- 4. PROFIL ADMIN ---
elif st.session_state.page_view == "admin_profile":
    st.markdown("### 👤 Profil Administrator")
    with st.container(border=True):
        st.write("**Nama:** Ima Safitri Sianipar")
        st.write("**Instansi:** Dinas Pendidikan Provinsi Sumatera Utara")
    if st.button("⬅️ Kembali"):
        st.session_state.page_view = "dashboard"
        st.rerun()

# --- 5. DETAIL SEKOLAH ---
elif st.session_state.page_view == "detail":
    sch = st.session_state.selected_school_data
    st.markdown(f"### 🏫 {sch['nama_sekolah'].upper()}")
    st.write(f"Daya Listrik: {sch.get('daya_listrik', '-')}")
    if st.button("⬅️ Kembali"):
        st.session_state.page_view = "dashboard"
        st.rerun()
