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
if "selected_school_data" not in st.session_state: st.session_state.selected_school_data = None

def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

# ==================================
# Bagian 1: CSS CUSTOM
# ==================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
    html, body, [data-testid="stWidgetLabel"] { font-family: 'Inter', sans-serif !important; }

    .block-container {
        padding-top: 0rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }
    [data-testid="stHeader"] { display: none !important; }

    .top-gradient-bar {
        position: fixed;
        top: 0; left: 0; width: 100%; height: 10px;
        background: linear-gradient(90deg, #ff8a00, #e52e71, #9c27b0, #1e88e5, #4caf50, #ffeb3b);
        z-index: 999999;
    }

    div[data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] div { color: black !important; }
    
    div.stButton > button:not([key^="btn_"]) {
        background: linear-gradient(90deg, #1565c0 0%, #1e88e5 100%) !important;
        color: white !important; border-radius: 10px !important; 
        font-weight: 700 !important; height: 48px; border: none !important; width: 100%;
    }

    [data-testid="stSidebar"] { background: linear-gradient(180deg, #1e88e5 0%, #0d47a1 100%) !important; }
    [data-testid="stSidebar"] * { color: white !important; }

    .header-balloon-card {
        background: linear-gradient(90deg, #f0f7ff 0%, #d1e9ff 100%) !important;
        border-radius: 0px 0px 15px 15px;
        padding: 5px 0px;
        border-bottom: 2px solid rgba(13, 71, 161, 0.1);
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        text-align: center;
        margin-top: 2px;
        margin-bottom: 20px;
    }

    .metric-tile { padding: 20px; border-radius: 12px; color: white; margin-bottom: 15px; display: flex; align-items: center; gap: 15px; }
    .tile-orange { background: linear-gradient(135deg, #ff9800 0%, #f57c00 100%); }
    .tile-blue-light { background: linear-gradient(135deg, #03a9f4 0%, #0288d1 100%); }
    .tile-red-dark { background: linear-gradient(135deg, #ff4b2b 0%, #ff416c 100%); }
    .tile-green-light { background: linear-gradient(135deg, #4caf50 0%, #2e7d32 100%); }
    .tile-label { font-size: 14px; font-weight: 800; text-transform: uppercase; }
    .tile-value { font-size: 22px; font-weight: 800; }

    .insight-box { background-color: #e3f2fd !important; border-radius: 8px; border-left: 4px solid #0d47a1; padding: 10px 12px; margin-top: 10px; }
    .insight-title { color: #0d47a1; font-weight: 800; font-size: 14px; text-transform: uppercase; }
    .insight-text { color: #333 !important; font-size: 13px; line-height: 1.5; }
    
    div[data-testid="stExpander"] details summary {
        background: linear-gradient(90deg, #4caf50 0%, #2e7d32 100%) !important;
        color: white !important; border-radius: 10px !important; padding: 10px 15px !important;
    }
</style>
""", unsafe_allow_html=True)

def draw_tile_svg(label, value, svg_icon, style_class):
    st.markdown(f'<div class="metric-tile {style_class}"><div style="width:42px;height:42px;">{svg_icon}</div><div><div class="tile-label">{label}</div><div class="tile-value">{value}</div></div></div>', unsafe_allow_html=True)

svg_people = '<svg viewBox="0 0 16 16" fill="white"><path d="M7 14s-1 0-1-1 1-4 5-4 5 3 5 4-1 1-1 1H7zm4-6a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm-5.784 6A2.238 2.238 0 0 1 5 13c0-1.355.68-2.75 1.936-3.72A6.325 6.325 0 0 0 5 9c-4 0-5 3-5 4s1 1 1 1h4.216zM4.5 8a2.5 2.5 0 1 0 0-5 2.5 2.5 0 0 0 0 5z"/></svg>'
svg_cap = '<svg viewBox="0 0 16 16" fill="white"><path d="M8.211 2.047a.5.5 0 0 0-.422 0l-7.5 3.5a.5.5 0 0 0 .025.917l7.5 3 7.5-3a.5.5 0 0 0 .025-.917l-7.5-3.5Z"/><path d="M4.176 9.032a.5.5 0 0 0-.656.327l-.5 1.7a.5.5 0 0 0 .254.539l1.5.75A.5.5 0 0 0 5.25 12h5.5a.5.5 0 0 0 .476-.346l.5-1.7a.5.5 0 0 0-.656-.327L10 10.25l-.117-.043-4 .876L4.176 9.032Z"/></svg>'
svg_warning = '<svg viewBox="0 0 16 16" fill="white"><path d="M8.982 1.566a1.13 1.13 0 0 0-1.96 0L.165 13.233c-.457.778.091 1.767.98 1.767h13.713c.889 0 1.438-.99.98-1.767L8.982 1.566zM8 5c.535 0 .954.462.9.995l-.35 3.507a.552.552 0 0 1-1.1 0L7.1 5.995A.905.905 0 0 1 8 5zm.002 6a1 1 0 1 1 0 2 1 1 0 0 1 0-2z"/></svg>'
svg_chart = '<svg viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M18 20V10M12 20V4M6 20v-6"/></svg>'

# ==================================
# Bagian 2: LOAD DATA
# ==================================
@st.cache_data
def load_all_data():
    try:
        df_ats = pd.read_csv("master_data_si_pandaiFix.csv")
        df_sch = pd.read_csv("master_data_sekolahFix.csv")
        for df in [df_ats, df_sch]:
            df.columns = df.columns.str.strip().str.lower()
        return df_ats, df_sch
    except: return pd.DataFrame(), pd.DataFrame()

data_wilayah, data_sekolah = load_all_data()

# ==================================
# Bagian 3: SIDEBAR & NAVIGASI
# ==================================
with st.sidebar:
    logo_b64 = get_base64_image("logo_sumut.png")
    if logo_b64:
        st.markdown(f'''<div style="display:flex;align-items:center;gap:12px;padding-bottom:15px;"><img src="data:image/png;base64,{logo_b64}" width="80"><span style="font-size:20px;font-weight:800;color:white;">SI-PANDAI SUMUT</span></div>''', unsafe_allow_html=True)
    
    def ubah_halaman():
        if "nav_radio" in st.session_state:
            pilihan = st.session_state.nav_radio
            if "🚀 Dashboard Utama" in pilihan: 
                st.session_state.page_view = "dashboard"
                st.session_state.selected_kab = "Semua" 
            elif "ℹ️ Tentang Dashboard" in pilihan: 
                st.session_state.page_view = "tentang_dashboard"

    st.sidebar.header("🧭 Navigasi Sistem")
    st.sidebar.radio("Klik :", ["🚀 Dashboard Utama", "ℹ️ Tentang Dashboard"], key="nav_radio", on_change=ubah_halaman)
    st.sidebar.divider()
    
   st.sidebar.divider()
st.sidebar.header("🔎 Filter Wilayah")
col_kab = "kab_kota" if "kab_kota" in data_wilayah.columns else data_wilayah.columns[0]
opsi = ["Semua"] + sorted(data_wilayah[col_kab].unique().tolist()) if not data_wilayah.empty else ["Semua"]
kab_pilih = st.sidebar.selectbox("Kabupaten / Kota", opsi, key="selected_kab")


# ==================================
# Bagian 4: HEADER
# ==================================
st.markdown('<div class="top-gradient-bar"></div>', unsafe_allow_html=True)
st.markdown("""<div class="header-balloon-card"><h2 style='color: #0d47a1; font-weight:800; margin: 0; font-size: 2rem;'>DASHBOARD SI-PANDAI SUMUT</h2><div style="height: 2px; background: linear-gradient(90deg, transparent, #0d47a1, transparent); margin: 3px auto; width: 50%; opacity: 0.3;"></div><p style='color: #1565c0; font-size: 15px; font-weight: 700; margin: 0;'>Sistem Informasi Pemetaan Anak Tidak Sekolah (ATS) Disabilitas Bidang Pembinaan Pendidikan Khusus Dinas Pendidikan Provinsi Sumatera Utara</p></div>""", unsafe_allow_html=True)

# ==================================
# Bagian 5: LOGIKA HALAMAN
# ==================================

# --- A. HALAMAN DASHBOARD ---
if st.session_state.page_view == "dashboard":
    st.markdown('<p style="font-size:26px; font-weight:800; color:#0d47a1;">Matriks Capaian Sektoral</p>', unsafe_allow_html=True)
    df_f = data_wilayah.copy()
    if kab_pilih != "Semua": df_f = df_f[df_f[col_kab] == kab_pilih]

    # Matriks - Menyesuaikan nama kolom sesuai file CSV Anda
    c_pop = 'estimasi populasi usia sekolah'
    c_sis = 'jumlah_siswa'
    c_ats = 'ats_disabilitas'
    
    v_p = int(df_f[c_pop].sum()) if not df_f.empty else 0
    v_s = int(df_f[c_sis].sum()) if not df_f.empty else 0
    v_a = int(df_f[c_ats].sum()) if not df_f.empty else 0
    v_aps_num = (v_s / v_p * 100) if v_p > 0 else 0
    v_aps = f"{v_aps_num:.2f}%"

    m1, m2, m3, m4 = st.columns(4)
    with m1: draw_tile_svg("Estimasi Populasi Sasaran", f"{v_p:,}", svg_people, "tile-orange")
    with m2: draw_tile_svg("Siswa Belajar", f"{v_s:,}", svg_cap, "tile-blue-light")
    with m3: draw_tile_svg("Anak Tidak Sekolah", f"{v_a:,}", svg_warning, "tile-red-dark")
    with m4: draw_tile_svg("Persentase", v_aps, svg_chart, "tile-green-light")

    if kab_pilih != "Semua":
        st.divider()
        st.subheader(f"🏫 Satuan Pendidikan di {kab_pilih}")
        sch_wil = data_sekolah[data_sekolah[col_kab] == kab_pilih] if not data_sekolah.empty else pd.DataFrame()
        if not sch_wil.empty:
            cols = st.columns(3)
            for i, row in enumerate(sch_wil.itertuples()):
                with cols[i % 3]:
                    with st.container(border=True):
                        if st.button(getattr(row, 'nama_sekolah', 'SEKOLAH').upper(), key=f"btn_{i}"):
                            st.session_state.selected_school_data = row._asdict()
                            st.session_state.page_view = "detail"
                            st.rerun()
                        st.caption(f"NPSN: {getattr(row, 'npsn', '-')}")

    st.divider()
    cv1, cv2 = st.columns([1.6, 1.1])
    with cv1:
        st.subheader("🗺️ Peta Sebaran ATS")
        if not df_f.empty:
            fig_map = px.scatter_mapbox(df_f, lat="lat", lon="lon", size=c_ats, color=c_ats, color_continuous_scale="RdYlGn_r", hover_name=col_kab, zoom=9, height=450)
            fig_map.update_layout(mapbox_style="open-street-map", margin={"r":0,"t":0,"l":0,"b":0}, coloraxis_showscale=False)
            st.plotly_chart(fig_map, use_container_width=True)

    with cv2:
        st.subheader("📊 5 Peringkat ATS Tertinggi")
        if not df_f.empty:
            df_top5 = data_wilayah.sort_values(by=c_ats, ascending=False).head(5)
            fig = px.bar(df_top5, x=c_ats, y=col_kab, orientation='h', color=c_ats, color_continuous_scale=[[0, '#00d2ff'], [1, '#3a7bd5']], text=c_ats)
            fig.update_layout(height=350, showlegend=False, coloraxis_showscale=False, yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig, use_container_width=True)

            p_insight = f"🚨 Jumlah ATS di {kab_pilih} sangat tinggi ({v_a:,} jiwa)." if v_a > 100 else f"💡 Wilayah {kab_pilih} terpantau stabil."
            st.markdown(f'<div class="insight-box"><div class="insight-title">Insight: {kab_pilih}</div><p class="insight-text">{p_insight}</p></div>', unsafe_allow_html=True)

    with st.expander("📋 Lihat & Download Data Tabel"):
        st.dataframe(df_f, use_container_width=True)
        csv = df_f.to_csv(index=False).encode('utf-8')
        st.download_button("Download CSV 📥", csv, file_name=f'data_ats_{kab_pilih}.csv', mime='text/csv')

# --- B. HALAMAN DETAIL SEKOLAH ---
elif st.session_state.page_view == "detail":
    sch = st.session_state.selected_school_data   
    st.markdown(f"<h3 style='color:#0d47a1;'>🏫 {sch['nama_sekolah'].upper()}</h3>")
    st.markdown(f"<p style='color:gray;'>Wilayah: {sch['kab_kota']} | NPSN: {sch['npsn']}</p>", unsafe_allow_html=True)
    
    query = f"{sch['nama_sekolah'].replace(' ', '+')}+{sch['kab_kota'].replace(' ', '+')}"
    components.html(f'<iframe width="100%" height="400" src="https://maps.google.com/maps?q={query}&output=embed" style="border-radius:15px; border:1px solid #ddd;"></iframe>', height=420)
    
    st.divider()
    c1, c2 = st.columns(2)
    with c1:
        with st.container(border=True):
            st.subheader("📌 Profil Umum")
            st.write(f"**Status:** {sch.get('status', '-')}")
            st.write(f"**Alamat:** {sch.get('alamat', '-')}")
            st.write(f"**Jumlah Siswa:** {sch.get('jumlah_siswa', '0')} Orang")
    with c2:
        with st.container(border=True):
            st.subheader("🏗️ Sarana Prasarana")
            st.write(f"**Rombel:** {sch.get('jumlah_rombel', '0')}")
            st.write(f"**Daya Listrik:** {sch.get('daya_listrik', '-')}")
            st.write(f"**Akses Internet:** {sch.get('akses_internet', '-')}")

    if st.button("⬅️ Kembali ke Dashboard"):
        st.session_state.page_view = "dashboard"
        st.rerun()

# --- C. HALAMAN TENTANG DASHBOARD ---
elif st.session_state.page_view == "tentang_dashboard":
    st.markdown('<p style="font-size:26px; font-weight:800; color:#0d47a1;">Informasi Sistem SI-PANDAI SUMUT</p>', unsafe_allow_html=True)
    col_info1, col_info2 = st.columns([1.5, 1])
    
    with col_info1:
        with st.expander("🖥️ Deskripsi Sistem", expanded=True):
            st.markdown("""**SI-PANDAI SUMUT** adalah platform analitik digital untuk mengintegrasikan data anak tidak sekolah dengan kebutuhan sarana prasarana pendidikan khusus di Sumatera Utara.""")
        
        with st.expander("🎯 Tujuan Dashboard"):
            st.markdown("1. Memetakan sebaran ATS disabilitas.\n2. Instrumen pengambilan kebijakan.\n3. Efisiensi perencanaan sarpras.")

        st.markdown("##### 🎬 Video Panduan")
        st.video("https://www.youtube.com/watch?v=example123")
        
    with col_info2:
        st.success("Dashboard ini berperan sebagai Instrumen Pengambilan Kebijakan (Policy Tool).")
        with st.container(border=True):
            st.markdown("##### 👤 Inovator Sistem")
            st.markdown("**Ima Safitri Sianipar, S.Kom**\nDinas Pendidikan Provinsi Sumatera Utara")

    if st.button("⬅️ Kembali Utama", key="btn_back"):
        st.session_state.page_view = "dashboard"
        st.rerun()

# ==================================
# Bagian 6: FOOTER
# ==================================
st.divider()
st.markdown("""<div style="text-align: center; margin-top: -20px;"><h4 style="color: #0d47a1; font-weight: 800; margin:0;">DINAS PENDIDIKAN PROVINSI SUMATERA UTARA</h4><p style="font-size: 11px; color: #666; margin:0;">Jl. Teuku Cik Ditiro No.1-D, Madras Hulu, Kota Medan</p><p style="font-size: 10px; color: #9e9e9e;">© 2026 SI-PANDAI SUMUT | Bidang Pembinaan Pendidikan Khusus</p></div>""", unsafe_allow_html=True)
