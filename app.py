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

# --- FUNGSI RESET LOGOUT ---
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
# Bagian 1: CSS CUSTOM (LOCKED & VIVID)
# ==================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&display=swap');
    html, body, [data-testid="stWidgetLabel"] { font-family: 'Inter', sans-serif !important; }
    [data-testid="stAppViewContainer"] { background-color: #f4f7f9 !important; }
    header {visibility: hidden;}

    /* SIDEBAR NAVY */
    [data-testid="stSidebar"] { background: linear-gradient(180deg, #0d47a1 0%, #1565c0 100%) !important; }
    [data-testid="stSidebar"] * { color: white !important; }
    div[data-testid="stSelectbox"] div[data-baseweb="select"] * { color: #31333f !important; }

    /* KOTAK MATRIKS (TILE) */
    .metric-container {
        background: white; padding: 20px; border-radius: 12px;
        border-top: 5px solid #0d47a1; box-shadow: 0 4px 10px rgba(0,0,0,0.08);
        text-align: center; margin-bottom: 10px;
    }
    .metric-value { font-size: 28px; color: #0d47a1; font-weight: 800; }

    /* BALON STATUS (WARNA HIDUP) */
    .rec-box { padding: 8px 12px; border-radius: 8px; font-size: 11px; font-weight: 700; margin-bottom: 12px; text-align: center; }
    .mendesak { background-color: #ef4444 !important; color: white !important; }
    .rehab { background-color: #f59e0b !important; color: white !important; }
    .aman { background-color: #22c55e !important; color: white !important; }

    /* PHOTO PREVIEW BOX */
    .photo-card {
        background: white; border-radius: 15px; padding: 10px;
        border: 2px solid #0d47a1; box-shadow: 0 4px 6px rgba(0,0,0,0.1);
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
        return df_ats, df_sch
    except:
        return pd.DataFrame(), pd.DataFrame()

data_wilayah, data_sekolah = load_all_data()

# =========================
# Bagian 3: LOGIN
# =========================
if "login" not in st.session_state: st.session_state.login = False
if not st.session_state.login:
    _, col_card, _ = st.columns([1, 1.5, 1])
    with col_card:
        with st.container(border=True):
            st.markdown("<h2 style='text-align:center; color:#0d47a1;'>LOGIN SI-PANDAI</h2>", unsafe_allow_html=True)
            u = st.text_input("Username", placeholder="Username")
            p = st.text_input("Password", type="password", placeholder="Password")
            if st.button("MASUK KE DASHBOARD"):
                if u == "admin" and p == "admin":
                    st.session_state.login = True
                    st.rerun()
                else: st.error("Login Gagal")
    st.stop()

# ==================================
# Bagian 4: DASHBOARD UTAMA
# ==================================

# SIDEBAR
st.sidebar.markdown(f"### 🏛️ PANEL KONTROL")
st.sidebar.write(f"👤 Role: **ADMIN**")
st.sidebar.divider()
opsi_kab = ["Semua"] + sorted(data_wilayah["kab_kota"].unique().tolist())
kab_pilih = st.sidebar.selectbox("Pilih Kabupaten / Kota", opsi_kab, key="selected_kab")
st.sidebar.divider()
df_dl = data_wilayah.copy() if kab_pilih == "Semua" else data_wilayah[data_wilayah["kab_kota"] == kab_pilih]
st.sidebar.download_button("Download Data (CSV) ⬇️", df_dl.to_csv(index=False).encode('utf-8'), f"data_sipandai_{kab_pilih}.csv", "text/csv")
st.sidebar.divider()
st.sidebar.button("Logout 🚪", use_container_width=True, on_click=proses_logout)

# KONTEN
if st.session_state.page_view == "dashboard":
    st.markdown('<p style="font-size:26px; font-weight:800; color:#0d47a1;">🚀 Monitoring ATS Disabilitas</p>', unsafe_allow_html=True)
    
    df_filter = data_wilayah.copy()
    if kab_pilih != "Semua":
        df_filter = df_filter[df_filter["kab_kota"] == kab_pilih]

    # 1. Matriks Kotak
    m1, m2, m3 = st.columns(3)
    with m1: st.markdown(f'<div class="metric-container"><div class="metric-value">{int(df_filter["jumlah_penduduk"].sum()):,}</div><div style="font-size:12px; color:gray;">PENDUDUK DISABILITAS</div></div>', unsafe_allow_html=True)
    with m2: st.markdown(f'<div class="metric-container"><div class="metric-value">{int(df_filter["jumlah_siswa"].sum()):,}</div><div style="font-size:12px; color:gray;">SISWA BELAJAR</div></div>', unsafe_allow_html=True)
    with m3: st.markdown(f'<div class="metric-container"><div class="metric-value">{int(df_filter["ats_disabilitas"].sum()):,}</div><div style="font-size:12px; color:gray;">ANAK TIDAK SEKOLAH</div></div>', unsafe_allow_html=True)

    # 2. GIS MAP (VIVID STYLE) & FOTO PREVIEW
    st.divider()
    col_map, col_photo = st.columns([1.8, 1])
    
    with col_map:
        st.subheader("🗺️ Peta Interaktif Sebaran ATS")
        fig_map = px.scatter_mapbox(
            df_filter, lat="lat", lon="lon", size="ats_disabilitas",
            color="ats_disabilitas", color_continuous_scale="Viridis",
            size_max=20, zoom=7, mapbox_style="open-street-map" # MAP LEBIH HIDUP
        )
        fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        st.plotly_chart(fig_map, use_container_width=True)

    with col_photo:
        st.subheader("📸 Foto Lokasi Sekolah")
        sekolah_list = data_sekolah[data_sekolah['kab_kota'] == kab_pilih] if kab_pilih != "Semua" else data_sekolah.head(10)
        selected_preview = st.selectbox("Pilih Sekolah untuk Preview", sekolah_list['nama_sekolah'].tolist())
        
        # Simulasi Tampilan Foto (Ganti URL dengan kolom foto dari CSV jika ada)
        st.markdown(f'<div class="photo-card">', unsafe_allow_html=True)
        st.image("https://via.placeholder.com/400x250.png?text=Foto+Lokasi+SLB", caption=f"Kondisi Bangunan: {selected_preview}")
        st.markdown(f'</div>', unsafe_allow_html=True)
        st.write("📍 **Lokasi Terverifikasi Bidang PK**")

    # 3. Daftar Sekolah & Balon Status
    if kab_pilih != "Semua":
        st.divider()
        st.subheader(f"🏫 Satuan Pendidikan di {kab_pilih}")
        cols_sch = st.columns(3)
        for i, row in enumerate(sekolah_list.itertuples()):
            with cols_sch[i % 3]:
                with st.container(border=True):
                    if row.rusak_berat > 0: st.markdown(f"<div class='rec-box mendesak'>⚠️ RUSAK BERAT</div>", unsafe_allow_html=True)
                    else: st.markdown("<div class='rec-box aman'>✅ KONDISI STABIL</div>", unsafe_allow_html=True)
                    
                    if st.button(row.nama_sekolah.upper(), key=f"btn_{row.npsn}"):
                        st.session_state.selected_school_data = row._asdict()
                        st.session_state.page_view = "detail"
                        st.rerun()
                    st.caption(f"NPSN: {row.npsn}")

else:
    # --- HALAMAN DETAIL ---
    sch = st.session_state.selected_school_data
    if st.button("⬅️ Kembali ke Dashboard"):
        st.session_state.page_view = "dashboard"
        st.rerun()
    st.markdown(f"<h1 style='color:#0d47a1;'>🏫 {sch['nama_sekolah'].upper()}</h1>", unsafe_allow_html=True)
    st.divider()
    
    cd1, cd2 = st.columns([1.5, 1])
    with cd1:
        with st.container(border=True):
            st.subheader("📊 Data Teknis Sarpras")
            st.write(f"**Jumlah Siswa:** {sch.get('jumlah_siswa', '0')} Orang")
            st.write(f"**Rusak Berat:** {sch['rusak_berat']} Ruang")
            st.write(f"**Akses Internet:** {sch.get('akses_internet', '-')}")
            st.write(f"**Daya Listrik:** {sch.get('daya_listrik', '-')}")
    with cd2:
        st.subheader("🖼️ Dokumentasi Visual")
        st.image("https://via.placeholder.com/400x300.png?text=Foto+Kondisi+Sekolah", caption="Bukti Foto Kerusakan Ruang Kelas")
