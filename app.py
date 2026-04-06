import streamlit as st
import pandas as pd
import plotly.express as px
import base64
import os

# ==================================
# 1. KONFIGURASI HALAMAN & STATE
# ==================================
st.set_page_config(page_title="SI-PANDAI SUMUT", layout="wide", initial_sidebar_state="expanded")

if "selected_kab" not in st.session_state: st.session_state.selected_kab = "Semua"

# ==================================
# 2. LOAD DATA
# ==================================
@st.cache_data
def load_data():
    # Menggunakan file yang Anda upload
    df_sch = pd.read_csv("master_data_sekolah1.csv")
    # Mapping koordinat sederhana untuk Kabupaten di Sumut agar peta tidak lari
    coords = {
        'Kab. Asahan': [2.98, 99.62], 'Kab. Batubara': [3.17, 99.50], 'Kab. Dairi': [2.85, 98.26],
        'Kab. Deli Serdang': [3.50, 98.70], 'Kota Medan': [3.59, 98.67], 'Kab. Langkat': [3.75, 98.22],
        'Kab. Karo': [3.11, 98.50], 'Kab. Labuhanbatu Utara': [2.33, 99.63]
    }
    # Menambahkan koordinat ke dataframe jika belum ada
    df_sch['lat'] = df_sch['Kab_Kota'].map(lambda x: coords.get(x, [2.11, 99.13])[0])
    df_sch['lon'] = df_sch['Kab_Kota'].map(lambda x: coords.get(x, [2.11, 99.13])[1])
    return df_sch

df = load_data()

# ==================================
# 3. CSS CUSTOM (SCOPED / SPESIFIK)
# ==================================
st.markdown("""
<style>
    /* 1. Sidebar Styling */
    [data-testid="stSidebar"] { background-color: #1565c0 !important; }
    [data-testid="stSidebar"] * { color: white !important; }
    div[data-testid="stSelectbox"] div[data-baseweb="select"] * { color: #31333f !important; }

    /* 2. Card Metrics (Unique Classes) */
    .metric-row { display: flex; gap: 20px; margin-bottom: 25px; }
    .custom-card {
        flex: 1; padding: 20px; border-radius: 15px; color: white;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1); position: relative;
    }
    .c-blue { background: linear-gradient(135deg, #2196f3 0%, #1976d2 100%); }
    .c-green { background: linear-gradient(135deg, #66bb6a 0%, #43a047 100%); }
    .c-red { background: linear-gradient(135deg, #ef5350 0%, #e53935 100%); }
    .c-purple { background: linear-gradient(135deg, #7e57c2 0%, #5e35b1 100%); }
    
    .c-label { font-size: 14px; font-weight: 600; opacity: 0.9; }
    .c-value { font-size: 28px; font-weight: 800; margin-top: 5px; }
    
    /* 3. Specific Buttons */
    .stButton>button[key="logout_btn"] {
        background: #ff5252 !important; color: white !important; width: 100%; border: none; border-radius: 8px;
    }
    
    /* 4. Insight Box */
    .insight-container {
        background-color: #e3f2fd; border-radius: 12px; padding: 15px;
        border-left: 5px solid #1565c0; margin-top: 15px;
    }
</style>
""", unsafe_allow_html=True)

# ==================================
# 4. SIDEBAR LAYOUT
# ==================================
with st.sidebar:
    st.markdown("### 🛡️ SI-PANDAI SUMUT")
    st.write(f"👤 Role: **ADMIN**")
    st.divider()
    
    kab_list = ["Semua"] + sorted(df['Kab_Kota'].unique().tolist())
    kab_pilih = st.selectbox("Pilih Kabupaten / Kota", kab_list)
    
    st.button("🔄 Reset Filter", use_container_width=True)
    st.download_button("📥 Download Data (CSV)", df.to_csv().encode('utf-8'), "data.csv", use_container_width=True)
    
    # Box Insight di Sidebar
    st.markdown("""
    <div class="insight-container" style="color: #0d47a1; font-size: 12px;">
        <b>🔍 Insight Cepat:</b><br>
        Wilayah dengan kerusakan ruang kelas terbanyak saat ini terdeteksi di Kab. Asahan.
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    st.button("Logout 🚪", key="logout_btn")

# ==================================
# 5. MAIN CONTENT
# ==================================
st.title("SI-PANDAI SUMUT")
st.caption("Dashboard Pemetaan ATS & Satuan Pendidikan Khusus")

# Filter Data
df_f = df if kab_pilih == "Semua" else df[df['Kab_Kota'] == kab_pilih]

# ROW 1: KARTU METRIK
total_siswa = df_f['Jumlah_Siswa'].sum()
m1, m2, m3, m4 = st.columns(4)

with m1:
    st.markdown(f'<div class="custom-card c-blue"><div class="c-label">👤 Penduduk Disabilitas</div><div class="c-value">6,732</div></div>', unsafe_allow_html=True)
with m2:
    st.markdown(f'<div class="custom-card c-green"><div class="c-label">🎓 Siswa Belajar</div><div class="c-value">{total_siswa:,}</div></div>', unsafe_allow_html=True)
with m3:
    st.markdown(f'<div class="custom-card c-red"><div class="c-label">⚠️ Anak Tidak Sekolah</div><div class="c-value">2,716</div></div>', unsafe_allow_html=True)
with m4:
    st.markdown(f'<div class="custom-card c-purple"><div class="c-label">📈 Angka Partisipasi</div><div class="c-value">67.9%</div></div>', unsafe_allow_html=True)

st.divider()

# ROW 2: MAP & CHART
col_map, col_chart = st.columns([1.5, 1])

with col_map:
    st.subheader("🗺️ Peta Sebaran Satuan Pendidikan")
    # MEMPERBAIKI PETA: Fokus di Tengah Sumatera Utara
    fig_map = px.scatter_mapbox(
        df_f, lat="lat", lon="lon", size="Jumlah_Siswa", color="Jumlah_Siswa",
        hover_name="Nama_Sekolah", zoom=7,
        center={"lat": 2.1121, "lon": 99.1342}, # Kunci Koordinat SUMUT
        mapbox_style="carto-positron", height=400
    )
    fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig_map, use_container_width=True)

with col_chart:
    st.subheader("📊 Statistik Per Wilayah")
    chart_data = df_f.groupby('Kab_Kota')['Jumlah_Siswa'].sum().reset_index().sort_values('Jumlah_Siswa', ascending=False).head(5)
    fig_bar = px.bar(chart_data, x='Jumlah_Siswa', y='Kab_Kota', orientation='h', color='Jumlah_Siswa', color_continuous_scale='Blues')
    fig_bar.update_layout(height=300, margin=dict(l=0, r=0, t=0, b=0))
    st.plotly_chart(fig_bar, use_container_width=True)
    
    st.markdown("""
    <div class="insight-container">
        <b>💡 Rekomendasi:</b><br>
        Fokus pada peningkatan sarana prasarana di wilayah dengan jumlah siswa disabilitas tertinggi.
    </div>
    """, unsafe_allow_html=True)

# TABEL DETAIL
with st.expander("📋 Lihat Detail Tabel Sekolah"):
    st.dataframe(df_f, use_container_width=True)
