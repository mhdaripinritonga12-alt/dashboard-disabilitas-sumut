import streamlit as st
import pandas as pd
import plotly.express as px

# ==================================
# 1. KONFIGURASI HALAMAN
# ==================================
st.set_page_config(page_title="SI-PANDAI SUMUT", layout="wide")

# ==================================
# 2. LOAD & CLEANING DATA (PROTEKSI TOTAL)
# ==================================
@st.cache_data
def load_clean_data():
    try:
        # Load data
        df = pd.read_csv("master_data_sekolah1.csv")
        
        # 1. Bersihkan Nama Kolom
        df.columns = df.columns.str.strip()
        
        # 2. Pastikan Jumlah_Siswa adalah angka
        df['Jumlah_Siswa'] = pd.to_numeric(df['Jumlah_Siswa'], errors='coerce').fillna(0)
        
        # 3. Kamus Koordinat (Lengkap)
        coords = {
            'Kab. Asahan': [2.98, 99.62], 'Kab. Batubara': [3.17, 99.50], 
            'Kab. Dairi': [2.85, 98.26], 'Kab. Deli Serdang': [3.50, 98.70], 
            'Kota Medan': [3.59, 98.67], 'Kab. Langkat': [3.75, 98.22],
            'Kab. Karo': [3.11, 98.50], 'Kab. Labuhanbatu Utara': [2.33, 99.63],
            'Kota Padangsidimpuan': [1.37, 99.26], 'Kab. Labuhanbatu Selatan': [1.97, 100.10],
            'Kab. Simalungun': [2.95, 99.06], 'Kota Binjai': [3.60, 98.48]
        }
        
        # 4. Paksa buat kolom lat dan lon agar TIDAK KeyError
        df['lat'] = df['Kab_Kota'].apply(lambda x: coords.get(x.strip(), [2.11, 99.13])[0])
        df['lon'] = df['Kab_Kota'].apply(lambda x: coords.get(x.strip(), [2.11, 99.13])[1])
        
        return df
    except Exception as e:
        st.error(f"Gagal baca CSV: {e}")
        return pd.DataFrame()

df = load_clean_data()

# ==================================
# 3. CSS CUSTOM (SCOPED)
# ==================================
st.markdown("""
<style>
    [data-testid="stSidebar"] { background-color: #1565c0 !important; }
    [data-testid="stSidebar"] * { color: white !important; }
    .kartu { padding: 20px; border-radius: 15px; color: white; margin-bottom: 10px; }
    .b-blue { background: linear-gradient(135deg, #2196f3, #1565c0); }
    .b-green { background: linear-gradient(135deg, #66bb6a, #2e7d32); }
    .b-red { background: linear-gradient(135deg, #ef5350, #c62828); }
    .b-purple { background: linear-gradient(135deg, #7e57c2, #4527a0); }
    .val { font-size: 26px; font-weight: 800; }
    .stButton>button[key="logout"] { background-color: #ff4b4b !important; color: white !important; width: 100%; border: none; }
</style>
""", unsafe_allow_html=True)

# ==================================
# 4. LOGIKA FILTER
# ==================================
if not df.empty:
    with st.sidebar:
        st.header("SI-PANDAI SUMUT")
        st.caption("Admin Dashboard")
        st.divider()
        list_wilayah = ["Semua"] + sorted(df['Kab_Kota'].unique().tolist())
        pilihan = st.selectbox("Pilih Kabupaten/Kota", list_wilayah)
        st.divider()
        st.button("Logout 🚪", key="logout")

    # Filter data
    df_f = df if pilihan == "Semua" else df[df['Kab_Kota'] == pilihan]

    # ==================================
    # 5. TAMPILAN UTAMA
    # ==================================
    st.markdown("<h2 style='color:#1565c0;'>🚀 Dashboard Utama</h2>", unsafe_allow_html=True)

    # Metrics
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown(f'<div class="kartu b-blue">Disabilitas<br><span class="val">6,732</span></div>', unsafe_allow_html=True)
    with c2: st.markdown(f'<div class="kartu b-green">Siswa Belajar<br><span class="val">{int(df_f["Jumlah_Siswa"].sum()):,}</span></div>', unsafe_allow_html=True)
    with c3: st.markdown(f'<div class="kartu b-red">ATS<br><span class="val">2,716</span></div>', unsafe_allow_html=True)
    with c4: st.markdown(f'<div class="kartu b-purple">Partisipasi<br><span class="val">67.9%</span></div>', unsafe_allow_html=True)

    st.divider()

    # Map & Chart
    col_map, col_chart = st.columns([1.5, 1])

    with col_map:
        st.subheader("🗺️ Sebaran Wilayah")
        # PROTEKSI: Cek apakah kolom 'lat' benar-benar ada sebelum gambar peta
        if 'lat' in df_f.columns and not df_f.empty:
            fig_peta = px.scatter_mapbox(
                df_f, lat="lat", lon="lon", size="Jumlah_Siswa", color="Status",
                hover_name="Nama_Sekolah", zoom=6.5,
                center={"lat": 2.11, "lon": 99.13},
                mapbox_style="carto-positron", height=450
            )
            fig_peta.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
            st.plotly_chart(fig_peta, use_container_width=True)
        else:
            st.warning("Data lokasi tidak tersedia untuk wilayah ini.")

    with col_chart:
        st.subheader("📊 Statistik Sekolah")
        if not df_f.empty:
            df_bar = df_f.groupby('Kab_Kota')['Jumlah_Siswa'].sum().reset_index()
            fig_bar = px.bar(df_bar, x='Jumlah_Siswa', y='Kab_Kota', orientation='h', color='Jumlah_Siswa', color_continuous_scale='Blues')
            fig_bar.update_layout(height=350, margin=dict(l=0, r=0, t=0, b=0))
            st.plotly_chart(fig_bar, use_container_width=True)

    # Tabel
    with st.expander("🔍 Lihat Detail Tabel"):
        st.dataframe(df_f, use_container_width=True)
else:
    st.error("File 'master_data_sekolah1.csv' tidak terbaca atau kosong.")
