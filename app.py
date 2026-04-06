import streamlit as st
import pandas as pd
import plotly.express as px

# ==================================
# 1. KONFIGURASI HALAMAN
# ==================================
st.set_page_config(page_title="SI-PANDAI SUMUT", layout="wide")

# ==================================
# 2. LOAD DATA & CLEANING (ANTI-ERROR)
# ==================================
@st.cache_data
def load_data():
    try:
        # Load data
        df_sch = pd.read_csv("master_data_sekolah1.csv")
        
        # MEMBERSIHKAN NAMA KOLOM (Menghapus spasi di awal/akhir)
        df_sch.columns = df_sch.columns.str.strip()
        
        # Koordinat Tengah Kabupaten Sumut (Agar Peta Akurat)
        coords = {
            'Kab. Asahan': [2.98, 99.62], 'Kab. Batubara': [3.17, 99.50], 'Kab. Dairi': [2.85, 98.26],
            'Kab. Deli Serdang': [3.50, 98.70], 'Kota Medan': [3.59, 98.67], 'Kab. Langkat': [3.75, 98.22],
            'Kab. Karo': [3.11, 98.50], 'Kab. Labuhanbatu Utara': [2.33, 99.63], 'Kab. Labuhanbatu Selatan': [1.97, 100.10],
            'Kota Padangsidimpuan': [1.37, 99.26]
        }
        
        # Tambahkan koordinat ke dataframe
        df_sch['lat'] = df_sch['Kab_Kota'].map(lambda x: coords.get(x, [2.11, 99.13])[0])
        df_sch['lon'] = df_sch['Kab_Kota'].map(lambda x: coords.get(x, [2.11, 99.13])[1])
        
        return df_sch
    except Exception as e:
        st.error(f"Gagal memuat file CSV: {e}")
        return pd.DataFrame()

df = load_data()

# ==================================
# 3. CSS CUSTOM (SCOPED)
# ==================================
st.markdown("""
<style>
    [data-testid="stSidebar"] { background-color: #1565c0 !important; }
    [data-testid="stSidebar"] * { color: white !important; }
    .custom-card { padding: 20px; border-radius: 15px; color: white; margin-bottom: 10px; }
    .c-blue { background: linear-gradient(135deg, #2196f3 0%, #1976d2 100%); }
    .c-green { background: linear-gradient(135deg, #66bb6a 0%, #43a047 100%); }
    .c-red { background: linear-gradient(135deg, #ef5350 0%, #e53935 100%); }
    .c-purple { background: linear-gradient(135deg, #7e57c2 0%, #5e35b1 100%); }
    .c-value { font-size: 24px; font-weight: 800; }
    .stButton>button[key="logout_btn"] { background: #ff5252 !important; color: white !important; width: 100%; border: none; }
</style>
""", unsafe_allow_html=True)

# ==================================
# 4. SIDEBAR
# ==================================
if not df.empty:
    with st.sidebar:
        st.markdown("### 🛡️ SI-PANDAI SUMUT")
        st.write("Role: **ADMIN**")
        st.divider()
        
        # Gunakan nama kolom hasil strip()
        kab_list = ["Semua"] + sorted(df['Kab_Kota'].unique().tolist())
        kab_pilih = st.selectbox("Pilih Kabupaten / Kota", kab_list)
        
        st.button("🔄 Reset Filter", use_container_width=True)
        st.divider()
        st.button("Logout 🚪", key="logout_btn")

    # Filter Data
    df_f = df if kab_pilih == "Semua" else df[df['Kab_Kota'] == kab_pilih]

    # ==================================
    # 5. MAIN DASHBOARD
    # ==================================
    st.title("SI-PANDAI SUMUT")
    
    # Row 1: Metrics
    m1, m2, m3, m4 = st.columns(4)
    with m1: st.markdown('<div class="custom-card c-blue">Penduduk Disabilitas<div class="c-value">6,732</div></div>', unsafe_allow_html=True)
    with m2: st.markdown(f'<div class="custom-card c-green">Siswa Belajar<div class="c-value">{int(df_f["Jumlah_Siswa"].sum()):,}</div></div>', unsafe_allow_html=True)
    with m3: st.markdown('<div class="custom-card c-red">Anak Tidak Sekolah<div class="c-value">2,716</div></div>', unsafe_allow_html=True)
    with m4: st.markdown('<div class="custom-card c-purple">Angka Partisipasi<div class="c-value">67.9%</div></div>', unsafe_allow_html=True)

    # Row 2: Map & Chart
    c_map, c_chart = st.columns([1.5, 1])
    
    with c_map:
        st.subheader("🗺️ Peta Sebaran Satuan Pendidikan")
        fig_map = px.scatter_mapbox(
            df_f, lat="lat", lon="lon", 
            size="Jumlah_Siswa", 
            color="Jumlah_Siswa",
            hover_name="Nama_Sekolah",
            center={"lat": 2.11, "lon": 99.13}, 
            zoom=6.5,
            mapbox_style="carto-positron",
            color_continuous_scale="Viridis",
            height=450
        )
        fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        st.plotly_chart(fig_map, use_container_width=True)

    with c_chart:
        st.subheader("📊 Statistik Siswa")
        top_5 = df_f.groupby('Kab_Kota')['Jumlah_Siswa'].sum().nlargest(5).reset_index()
        fig_bar = px.bar(top_5, x='Jumlah_Siswa', y='Kab_Kota', orientation='h', color='Jumlah_Siswa')
        fig_bar.update_layout(height=300, margin=dict(l=0, r=0, t=0, b=0))
        st.plotly_chart(fig_bar, use_container_width=True)

    st.dataframe(df_f[['Kab_Kota', 'Nama_Sekolah', 'Status', 'Jumlah_Siswa', 'Akses_Internet']], use_container_width=True)
else:
    st.warning("Silakan pastikan file 'master_data_sekolah1.csv' berada di folder yang sama dengan script.")
