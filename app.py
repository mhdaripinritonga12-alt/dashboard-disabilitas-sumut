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
    page_icon="🚀",
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
# Bagian 1: CSS CUSTOM (Diringkas)
# ==================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
    html, body, [data-testid="stWidgetLabel"] { font-family: 'Inter', sans-serif !important; }
    .top-gradient-bar { position: fixed; top: 0; left: 0; width: 100%; height: 10px; background: linear-gradient(90deg, #ff8a00, #e52e71, #9c27b0, #1e88e5, #4caf50, #ffeb3b); z-index: 99; }
    .header-balloon-card { background: linear-gradient(90deg, #f0f7ff 0%, #d1e9ff 100%); border-radius: 0px 0px 15px 15px; padding: 15px; text-align: center; margin-bottom: 20px; border-bottom: 2px solid rgba(13, 71, 161, 0.1); }
    .metric-tile { padding: 20px; border-radius: 12px; color: white; margin-bottom: 15px; display: flex; align-items: center; gap: 15px; }
    .tile-orange { background: linear-gradient(135deg, #ff9800 0%, #f57c00 100%); }
    .tile-blue-light { background: linear-gradient(135deg, #03a9f4 0%, #0288d1 100%); }
    .tile-red-dark { background: linear-gradient(135deg, #ff4b2b 0%, #ff416c 100%); }
    .tile-green-light { background: linear-gradient(135deg, #4caf50 0%, #2e7d32 100%); }
    .tile-icon-svg { width: 35px; height: 35px; fill: white; }
    .tile-value { font-size: 24px; font-weight: 800; }
    .insight-box { background-color: #f0f7ff; border-radius: 8px; padding: 15px; margin-top: 10px; }
</style>
""", unsafe_allow_html=True)

def draw_tile_svg(label, value, svg_icon, style_class):
    st.markdown(f'<div class="metric-tile {style_class}"><div class="tile-icon-svg">{svg_icon}</div><div><div style="font-size:12px; font-weight:700; text-transform:uppercase;">{label}</div><div class="tile-value">{value}</div></div></div>', unsafe_allow_html=True)

# SVG Icons
svg_people = '<svg viewBox="0 0 16 16"><path d="M7 14s-1 0-1-1 1-4 5-4 5 3 5 4-1 1-1 1H7zm4-6a3 3 0 1 0 0-6 3 3 0 0 0 0 6z"/></svg>'
svg_cap = '<svg viewBox="0 0 16 16"><path d="M8.211 2.047a.5.5 0 0 0-.422 0l-7.5 3.5a.5.5 0 0 0 .025.917l7.5 3 7.5-3a.5.5 0 0 0 .025-.917l-7.5-3.5Z"/></svg>'
svg_warning = '<svg viewBox="0 0 16 16"><path d="M8.982 1.566a1.13 1.13 0 0 0-1.96 0L.165 13.233c-.457.778.091 1.767.98 1.767h13.713c.889 0 1.438-.99.98-1.767L8.982 1.566zM8 5c.535 0 .954.462.9.995l-.35 3.507a.552.552 0 0 1-1.1 0L7.1 5.995A.905.905 0 0 1 8 5zm.002 6a1 1 0 1 1 0 2 1 1 0 0 1 0-2z"/></svg>'
svg_chart = '<svg viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="3"><path d="M18 20V10M12 20V4M6 20v-6"/></svg>'

# ==================================
# Bagian 2: LOAD DATA
# ==================================
@st.cache_data
def load_all_data():
    try:
        df_ats = pd.read_csv("master_data_si_pandaiFix.csv")
        df_sch = pd.read_csv("master_data_sekolahFix.csv")
        df_ats.columns = df_ats.columns.str.strip().str.lower()
        df_sch.columns = df_sch.columns.str.strip().str.lower()
        return df_ats, df_sch
    except Exception as e:
        st.error(f"Gagal memuat CSV: {e}")
        return pd.DataFrame(), pd.DataFrame()

data_wilayah, data_sekolah = load_all_data()

# ==================================
# Bagian 3: SIDEBAR
# ==================================
with st.sidebar:
    st.markdown('<h2 style="color:white;">SI-PANDAI</h2>', unsafe_allow_html=True)
    
    menu = st.radio("Navigasi", ["🚀 Dashboard Utama", "ℹ️ Tentang Dashboard"], key="nav_menu")
    st.session_state.page_view = "dashboard" if "Dashboard" in menu else "tentang_dashboard"
    
    st.divider()
    st.header("🔎 Filter Wilayah")
    col_kab = "kab_kota" if "kab_kota" in data_wilayah.columns else data_wilayah.columns[0]
    opsi_kab = ["Semua"] + sorted(data_wilayah[col_kab].unique().tolist()) if not data_wilayah.empty else ["Semua"]
    kab_pilih = st.selectbox("Kabupaten / Kota", opsi_kab, key="selected_kab")

# ==================================
# Bagian 4: DASHBOARD LOGIC
# ==================================
st.markdown('<div class="top-gradient-bar"></div>', unsafe_allow_html=True)
st.markdown('<div class="header-balloon-card"><h2 style="color:#0d47a1; margin:0;">DASHBOARD SI-PANDAI SUMUT</h2><p style="margin:0; font-weight:600; color:#1565c0;">Sistem Informasi Pemetaan Anak Tidak Sekolah (ATS) Disabilitas</p></div>', unsafe_allow_html=True)

if st.session_state.page_view == "dashboard":
    # 1. Filter Data
    if kab_pilih == "Semua":
        df_f = data_wilayah
    else:
        df_f = data_wilayah[data_wilayah['kab_kota'] == kab_pilih]

    # 2. Perhitungan Berdasarkan Nama Kolom CSV Anda
    if not df_f.empty:
        # Mengambil data langsung dari kolom yang tepat
        populasi = int(df_f['estimasi_populasi_sasaran_usia_sekolah'].sum())
        siswa_belajar = int(df_f['jumlah_siswa_belajar'].sum())
        ats = int(df_f['jumlah_anak_tidak_sekolah'].sum())
        
        # Hitung Persentase Partisipasi
        v_aps_num = (siswa_belajar / populasi * 100) if populasi > 0 else 0
    else:
        populasi, siswa_belajar, ats, v_aps_num = 0, 0, 0, 0

    v_aps_label = f"{v_aps_num:.2f}%"

    # 3. Menampilkan Matriks (Visualisasi Kotak)
    m1, m2, m3, m4 = st.columns(4)
    
    with m1: 
        draw_tile_svg("Estimasi Populasi", f"{populasi:,}", svg_people, "tile-orange")
    with m2: 
        draw_tile_svg("Siswa Belajar", f"{siswa_belajar:,}", svg_cap, "tile-blue-light")
    with m3: 
        draw_tile_svg("Anak Tidak Sekolah", f"{ats:,}", svg_warning, "tile-red-dark")
    with m4: 
        draw_tile_svg("Persentase Partisipasi", v_aps_label, svg_chart, "tile-green-light")
    st.divider()

    # Visualisasi
    cv1, cv2 = st.columns([1.5, 1])
    with cv1:
        st.subheader("🗺️ Peta Sebaran ATS")
        if not df_f.empty and 'lat' in df_f.columns:
            fig_map = px.scatter_mapbox(df_f, lat="lat", lon="lon", size=df_f.columns[3], color=df_f.columns[3],
                                       color_continuous_scale="RdYlGn_r", zoom=7, height=400, mapbox_style="open-street-map")
            fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
            st.plotly_chart(fig_map, use_container_width=True)
    
    with cv2:
        st.subheader("📊 Top 5 Wilayah ATS")
        if not data_wilayah.empty:
            ats_col = data_wilayah.columns[3]
            df_top5 = data_wilayah.sort_values(by=ats_col, ascending=False).head(5)
            fig_bar = px.bar(df_top5, x=ats_col, y=col_kab, orientation='h', text=ats_col, color_discrete_sequence=['#1e88e5'])
            fig_bar.update_layout(height=300, margin=dict(l=0, r=0, t=0, b=0))
            st.plotly_chart(fig_bar, use_container_width=True)

    with st.expander("📋 Data Tabel Lengkap"):
        st.dataframe(df_f, use_container_width=True)

elif st.session_state.page_view == "tentang_dashboard":
    st.header("ℹ️ Tentang Sistem")
    st.info("SI-PANDAI SUMUT dikembangkan untuk mendigitalisasi data ATS Disabilitas di Sumatera Utara.")
    st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ") # Ganti dengan URL Anda

# Footer
st.markdown("<hr><p style='text-align:center; font-size:12px; color:gray;'>© 2026 Dinas Pendidikan Provinsi Sumatera Utara</p>", unsafe_allow_html=True)
