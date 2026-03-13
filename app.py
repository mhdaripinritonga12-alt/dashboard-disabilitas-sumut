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
    initial_sidebar_state="expanded"
)

# --- FUNGSI RESET LOGOUT (FIX ERROR) ---
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
# Bagian 1: CSS CUSTOM (LOCKED & FIXED)
# ==================================
st.markdown("""
<style>
    /* Pastikan header transparan tapi tetap ada (agar ikon > muncul) */
    header { background-color: rgba(0,0,0,0) !important; visibility: visible !important; }
    [data-testid="stHeader"] { background: none !important; }

    /* SIDEBAR GRADASI */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d47a1 0%, #1565c0 100%) !important;
    }
    [data-testid="stSidebar"] * { color: white !important; }

    /* FIX: TULISAN DI FILTER (SELECTBOX) TETAP HITAM */
    div[data-testid="stSelectbox"] div[data-baseweb="select"] * {
        color: #31333f !important;
    }

    /* TOMBOL UTAMA & LOGIN */
    div.stButton > button:not([key^="btn_"]) {
        background: linear-gradient(90deg, #1565c0 0%, #1e88e5 100%) !important;
        color: white !important; border-radius: 10px !important; 
        font-weight: 700 !important; height: 48px; border: none !important;
        width: 100%;
    }

    /* KARTU SEKOLAH */
    [data-testid="stVerticalBlockBorderWrapper"] > div {
        background: white !important;
        border-radius: 15px !important;
        padding: 20px !important;
        border: 1px solid #e2e8f0 !important;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1) !important;
    }

    /* STYLE UNTUK MATRIKS KOTAK BERWARNA */
    .metric-tile {
        padding: 20px; border-radius: 12px; color: white; margin-bottom: 15px;
        display: flex; align-items: center; gap: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .tile-orange { background: linear-gradient(135deg, #ff9800 0%, #f57c00 100%); }
    .tile-blue-light { background: linear-gradient(135deg, #03a9f4 0%, #0288d1 100%); }
    .tile-blue-dark { background: linear-gradient(135deg, #3f51b5 0%, #303f9f 100%); }
    .tile-icon-svg { width: 40px; height: 40px; fill: white; }
    .tile-label { font-size: 12px; font-weight: 600; opacity: 0.9; }
    .tile-value { font-size: 22px; font-weight: 800; }

    /* BALON STATUS WARNA */
    .rec-box { padding: 8px 12px; border-radius: 8px; font-size: 11px; font-weight: 700; margin-bottom: 12px; }
    .mendesak { background-color: #fee2e2 !important; color: #b91c1c !important; border-left: 5px solid #ef4444 !important; }
    .rehab { background-color: #fef3c7 !important; color: #b45309 !important; border-left: 5px solid #f59e0b !important; }
    .aman { background-color: #dcfce7 !important; color: #15803d !important; border-left: 5px solid #22c55e !important; }

    /* DOWNLOAD BUTTON */
    .stDownloadButton > button {
        background: linear-gradient(90deg, #2e7d32 0%, #4caf50 100%) !important;
        color: white !important; border-radius: 10px !important; 
        font-weight: 700 !important; width: 100% !important; height: 48px !important;
    }
</style>
""", unsafe_allow_html=True)

# --- FUNGSI RENDER TILE ---
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
svg_people = '<svg viewBox="0 0 16 16"><path d="M7 14s-1 0-1-1 1-4 5-4 5 3 5 4-1 1-1 1H7zm4-6a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm-5.784 6A2.238 2.238 0 0 1 5 13c0-1.355.68-2.75 1.936-3.72A6.325 6.325 0 0 0 5 9c-4 0-5 3-5 4s1 1 1 1h4.216zM4.5 8a2.5 2.5 0 1 0 0-5 2.5 2.5 0 0 0 0 5z"/></svg>'
svg_cap = '<svg viewBox="0 0 16 16"><path d="M8.211 2.047a.5.5 0 0 0-.422 0l-7.5 3.5a.5.5 0 0 0 .025.917l7.5 3 7.5-3a.5.5 0 0 0 .025-.917l-7.5-3.5Z"/><path d="M4.176 9.032a.5.5 0 0 0-.656.327l-.5 1.7a.5.5 0 0 0 .254.539l1.5.75A.5.5 0 0 0 5.25 12h5.5a.5.5 0 0 0 .476-.346l.5-1.7a.5.5 0 0 0-.656-.327L10 10.25l-.117-.043-4 .876L4.176 9.032Z"/><path d="M14 11h2v2h-2v-2Z"/></svg>'
svg_warning = '<svg viewBox="0 0 16 16"><path d="M8.982 1.566a1.13 1.13 0 0 0-1.96 0L.165 13.233c-.457.778.091 1.767.98 1.767h13.713c.889 0 1.438-.99.98-1.767L8.982 1.566zM8 5c.535 0 .954.462.9.995l-.35 3.507a.552.552 0 0 1-1.1 0L7.1 5.995A.905.905 0 0 1 8 5zm.002 6a1 1 0 1 1 0 2 1 1 0 0 1 0-2z"/></svg>'

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
# Bagian 3: HALAMAN LOGIN
# =========================
if "login" not in st.session_state: st.session_state.login = False

if not st.session_state.login:
    _, col_logo, _ = st.columns([2, 0.6, 2])
    with col_logo:
        if os.path.exists("logo_sumut.png"): st.image("logo_sumut.png", width=100)
    
    _, col_card, _ = st.columns([1.5, 2, 1.5])
    with col_card:
        with st.container(border=True):
            col_l, col_r = st.columns([1, 1.5])
            with col_l:
                if os.path.exists("logo_sipandai.png"): st.image("logo_sipandai.png", use_container_width=True)
            with col_r:
                st.markdown("<h3 style='color:#0d47a1; margin-bottom:0;'>LOGIN USER</h3>", unsafe_allow_html=True)
                st.caption("Dashboard SI-PANDAI SUMUT")
                u = st.text_input("Username", placeholder="Username", label_visibility="collapsed")
                p = st.text_input("Password", type="password", placeholder="Password", label_visibility="collapsed")
                if st.button("MASUK KE DASHBOARD"):
                    if u == "admin" and p == "admin":
                        st.session_state.login = True
                        st.rerun()
                    else: st.error("Login Gagal")
    st.stop()

# ==================================
# Bagian 4: DASHBOARD & DETAIL
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

opsi_kab = ["Semua"] + sorted(data_wilayah["kab_kota"].unique().tolist())
kab_pilih = st.sidebar.selectbox("Pilih Kabupaten / Kota", opsi_kab, key="selected_kab")

st.sidebar.divider()
df_dl = data_wilayah.copy() if kab_pilih == "Semua" else data_wilayah[data_wilayah["kab_kota"] == kab_pilih]
csv_data = df_dl.to_csv(index=False).encode('utf-8')
st.sidebar.download_button("Download Data (CSV) ⬇️", csv_data, f"data_sipandai_{kab_pilih}.csv", "text/csv")

st.sidebar.divider()
st.sidebar.button("Logout 🚪", use_container_width=True, on_click=proses_logout)

if st.session_state.page_view == "dashboard":
    st.markdown('<p style="font-size:26px; font-weight:800; color:#0d47a1;">🚀 Dashboard Utama</p>', unsafe_allow_html=True)
    st.markdown('<p style="color: #546e7a; font-size: 14px; margin-top: -5px;">Sistem Informasi Pemetaan ATS Disabilitas Sumatera Utara</p>', unsafe_allow_html=True)
    st.divider()

    df_f = data_wilayah.copy()
    if kab_pilih != "Semua":
        df_f = df_f[df_f["kab_kota"] == kab_pilih]

    st.subheader("📌 Matriks Capaian Sektoral")
    st.markdown("""<div class="source-box-ui"><p style="font-size: 13px; color: #0d47a1; margin: 0;"><b>ℹ️ Sumber Data:</b> Bidang PK - LPPD & TIKP Provsu 2025</p></div>""", unsafe_allow_html=True)

    # MATRIKS 4 KOLOM
    m1, m2, m3, m4 = st.columns(4)
    val_penduduk = f"{int(df_f['jumlah_penduduk'].sum()):,}"
    val_siswa = f"{int(df_f['jumlah_siswa'].sum()):,}"
    val_ats = f"{int(df_f['ats_disabilitas'].sum()):,}"
    
    # Hitung APS sederhana
    if df_f['jumlah_penduduk'].sum() > 0:
        val_APS = f"{(df_f['jumlah_siswa'].sum() / df_f['jumlah_penduduk'].sum() * 100):.2f}%"
    else:
        val_APS = "0%"

    with m1: draw_tile_svg("Penduduk Disabilitas", val_penduduk, svg_people, "tile-orange")
    with m2: draw_tile_svg("Siswa Belajar", val_siswa, svg_cap, "tile-blue-light")
    with m3: draw_tile_svg("Anak Tidak Sekolah", val_ats, svg_warning, "tile-blue-dark")
    with m4: draw_tile_svg("Angka Partisipasi", val_APS, svg_cap, "tile-blue-light")

    if kab_pilih != "Semua":
        st.divider()
        st.subheader(f"🏫 Satuan Pendidikan di {kab_pilih}")
        sekolah_wilayah = data_sekolah[data_sekolah['kab_kota'] == kab_pilih]
        
        if not sekolah_wilayah.empty:
            cols_sch = st.columns(3)
            for i, row in enumerate(sekolah_wilayah.itertuples()):
                with cols_sch[i % 3]:
                    with st.container(border=True):
                        if row.rusak_berat > 0:
                            st.markdown(f"<div class='rec-box rehab'>🛠️ PRIORITAS REHAB: {row.rusak_berat} Ruang</div>", unsafe_allow_html=True)
                        elif row.jumlah_rombel > row.jumlah_ruang_kelas:
                            st.markdown(f"<div class='rec-box mendesak'>⚠️ MENDESAK: Butuh RKB</div>", unsafe_allow_html=True)
                        else:
                            st.markdown("<div class='rec-box aman'>✅ KONDISI STABIL</div>", unsafe_allow_html=True)
                        
                        if st.button(row.nama_sekolah.upper(), key=f"btn_{row.npsn}"):
                            st.session_state.selected_school_data = row._asdict()
                            st.session_state.page_view = "detail"
                            st.rerun()
                        st.caption(f"NPSN: {row.npsn}")

    st.divider()
    cv1, cv2 = st.columns([1.5, 1])
    with cv1:
        st.subheader("🗺️ Peta Sebaran ATS")
        df_f['map_size'] = df_f['ats_disabilitas'] * 30
        st.map(df_f, latitude="lat", longitude="lon", size="map_size", use_container_width=True)
    with cv2:
        st.subheader("📊 Grafik ATS Wilayah")
        fig = px.bar(df_f.sort_values("ats_disabilitas", ascending=False).head(10), x='ats_disabilitas', y='kab_kota', orientation='h', color='ats_disabilitas', color_continuous_scale='Blues')
        fig.update_layout(height=350, margin=dict(l=0, r=0, t=0, b=0))
        st.plotly_chart(fig, use_container_width=True)

else:
    sch = st.session_state.selected_school_data
    if st.button("⬅️ Kembali ke Dashboard"):
        st.session_state.page_view = "dashboard"
        st.rerun()
    st.markdown(f"<h1 style='color:#0d47a1; margin-bottom:0;'>🏫 {sch['nama_sekolah'].upper()}</h1>", unsafe_allow_html=True)
