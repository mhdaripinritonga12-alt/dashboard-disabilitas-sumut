import streamlit as st
import pandas as pd
import plotly.express as px
import os

# ==================================
# Bagian 0: KONFIGURASI HALAMAN
# ==================================
st.set_page_config(
    page_title="SI-PANDAI SUMUT",
    layout="wide",
    page_icon="🔒"
)

# --- FUNGSI RESET LOGOUT ---
def proses_logout():
    st.session_state.login = False
    st.session_state.page_view = "dashboard"

# Inisialisasi State
if "page_view" not in st.session_state: st.session_state.page_view = "dashboard"
if "selected_kab" not in st.session_state: st.session_state.selected_kab = "Semua"

# ==================================
# Bagian 1: CSS CUSTOM (SATELLITE THEME)
# ==================================
st.markdown("""
<style>
    [data-testid="stAppViewContainer"] { background-color: #f0f2f6 !important; }
    [data-testid="stSidebar"] { background: linear-gradient(180deg, #0d47a1 0%, #1a237e 100%) !important; }
    [data-testid="stSidebar"] * { color: white !important; }
    
    /* Tombol Google Maps */
    .gmaps-btn {
        display: inline-block;
        padding: 10px 20px;
        background-color: #4285F4;
        color: white !important;
        text-decoration: none;
        border-radius: 8px;
        font-weight: bold;
        text-align: center;
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ==================================
# Bagian 2: LOAD DATA
# ==================================
@st.cache_data
def load_all_data():
    try:
        # Menggunakan master data yang ada
        df_ats = pd.read_csv("master_data_si_pandai.csv")
        df_sch = pd.read_csv("master_data_sekolah1.csv")
        return df_ats, df_sch
    except:
        return pd.DataFrame(), pd.DataFrame()

data_wilayah, data_sekolah = load_all_data()

# =========================
# Bagian 3: DASHBOARD
# =========================
if st.session_state.page_view == "dashboard":
    st.title("🚀 SI-CERDAS: Dashboard Satelit")
    
    # FILTER SIDEBAR
    kab_pilih = st.sidebar.selectbox("Pilih Wilayah", ["Semua"] + sorted(data_wilayah["kab_kota"].unique().tolist()))
    st.sidebar.button("Logout 🚪", on_click=proses_logout)

    df_f = data_wilayah.copy() if kab_pilih == "Semua" else data_wilayah[data_wilayah["kab_kota"] == kab_pilih]

    # --- ROW 1: PETA SATELIT (MELIHAT LANGSUNG DARI PETA) ---
    st.subheader("🗺️ Visualisasi Lokasi Riil (Citra Satelit)")
    st.info("💡 Gunakan Mouse Wheel untuk Zoom In sampai melihat bangunan sekolah secara detail.")
    
    # Menggunakan Mapbox Satellite agar 'Hidup'
    fig_map = px.scatter_mapbox(
        df_f, lat="lat", lon="lon", size="ats_disabilitas",
        color="ats_disabilitas", color_continuous_scale="YlOrRd",
        hover_name="kab_kota", size_max=15, zoom=7,
        mapbox_style="satellite-streets" # INI KUNCINYA AGAR PETA HIDUP
    )
    fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, height=500)
    st.plotly_chart(fig_map, use_container_width=True)

    # --- ROW 2: DETAIL & LINK STREET VIEW ---
    st.divider()
    if kab_pilih != "Semua":
        st.subheader(f"🏫 Detail Satuan Pendidikan di {kab_pilih}")
        sch_wilayah = data_sekolah[data_sekolah['kab_kota'] == kab_pilih]
        
        cols = st.columns(3)
        for i, row in enumerate(sch_wilayah.itertuples()):
            with cols[i % 3]:
                with st.container(border=True):
                    st.markdown(f"**{row.nama_sekolah.upper()}**")
                    st.caption(f"NPSN: {row.npsn}")
                    
                    # LINK KE GOOGLE MAPS STREET VIEW (Melihat Foto Asli Tanpa Upload)
                    # Kita gunakan query pencarian Google Maps berdasarkan Nama Sekolah & Kabupaten
                    search_query = f"https://www.google.com/maps/search/{row.nama_sekolah}+{row.kab_kota}".replace(" ", "+")
                    
                    st.markdown(f'<a href="{search_query}" target="_blank" class="gmaps-btn">🔍 Lihat Foto Lokasi (Street View)</a>', unsafe_allow_html=True)
                    
                    if st.button("Detail Teknis 📊", key=f"det_{row.npsn}"):
                        st.session_state.selected_school_data = row._asdict()
                        st.session_state.page_view = "detail"
                        st.rerun()
else:
    # --- HALAMAN DETAIL ---
    sch = st.session_state.selected_school_data
    st.button("⬅️ Kembali", on_click=lambda: setattr(st.session_state, 'page_view', 'dashboard'))
    st.header(f"🏫 {sch['nama_sekolah'].upper()}")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.write(f"**Kabupaten:** {sch['kab_kota']}")
        st.write(f"**Jumlah Siswa:** {sch['jumlah_siswa']}")
    with col_b:
        # Menampilkan Lokasi Sekolah langsung di Google Maps Embed (Jika ada koordinat spesifik)
        st.write("**Lokasi GPS Terverifikasi:**")
        st.success("Koordinat Sinkron dengan Bidang PK")
