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
        
        # 1. Bersihkan Nama Kolom (Wajib agar tidak KeyError)
        df.columns = df.columns.str.strip()
        
        # 2. Pastikan Jumlah_Siswa adalah angka (supaya kartu tidak error)
        df['Jumlah_Siswa'] = pd.to_numeric(df['Jumlah_Siswa'], errors='coerce').fillna(0)
        
        # 3. Kamus Koordinat Kabupaten (Agar Peta Fokus di Sumut)
        coords = {
            'Kab. Asahan': [2.98, 99.62], 'Kab. Batubara': [3.17, 99.50], 
            'Kab. Dairi': [2.85, 98.26], 'Kab. Deli Serdang': [3.50, 98.70], 
            'Kota Medan': [3.59, 98.67], 'Kab. Langkat': [3.75, 98.22],
            'Kab. Karo': [3.11, 98.50], 'Kab. Labuhanbatu Utara': [2.33, 99.63],
            'Kota Padangsidimpuan': [1.37, 99.26], 'Kab. Labuhanbatu Selatan': [1.97, 100.10]
        }
        
        # 4. Buat Kolom Lat/Lon (Proteksi: kalau kab tidak ada di kamus, pakai titik tengah Sumut)
        df['lat'] = df['Kab_Kota'].apply(lambda x: coords.get(x.strip(), [2.11, 99.13])[0])
        df['lon'] = df['Kab_Kota'].apply(lambda x: coords.get(x.strip(), [2.11, 99.13])[1])
        
        return df
    except Exception as e:
        st.error(f"Error pembacaan CSV: {e}")
        return pd.DataFrame()

df = load_clean_data()

# ==================================
# 3. CSS CUSTOM (SCOPED)
# ==================================
st.markdown("""
<style>
    [data-testid="stSidebar"] { background-color: #1565c0 !important; }
    [data-testid="stSidebar"] * { color: white !important; }
    .kartu { padding: 20px; border-radius: 15px; color: white; margin-bottom: 10px; box-shadow: 2px 2px 10px rgba(0,0,0,0.1); }
    .c-biru { background: linear-gradient(135deg, #2196f3, #1565c0); }
    .c-hijau { background: linear-gradient(135deg, #66bb6a, #2e7d32); }
    .c-merah { background: linear-gradient(135deg, #ef5350, #c62828); }
    .c-ungu { background: linear-gradient(135deg, #7e57c2, #4527a0); }
    .txt-val { font-size: 24px; font-weight: 800; display: block; margin-top: 5px; }
    .stButton>button[key="logout"] { background-color: #ff4b4b !important; color: white !important; width: 100%; border: none; }
</style>
""", unsafe_allow_html=True)

# ==================================
# 4. LOGIKA DASHBOARD
# ==================================
if not df.empty:
    # --- Sidebar ---
    with st.sidebar:
        st.header("🛡️ SI-PANDAI")
        st.write("Role: **ADMIN**")
        st.divider()
        list_wil = ["Semua"] + sorted(df['Kab_Kota'].unique().tolist())
        pilihan = st.selectbox("Pilih Wilayah", list_wil)
        st.divider()
        st.button("Keluar 🚪", key="logout")

    # --- Filter Data ---
    df_f = df if pilihan == "Semua" else df[df['Kab_Kota'] == pilihan]

    # --- Main UI ---
    st.title("🚀 Dashboard Utama Sumatera Utara")
    
    # Baris 1: Kartu Metrik (Seperti Gambar Anda)
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown(f'<div class="kartu c-biru">Penduduk Disabilitas<span class="txt-val">6,732</span></div>', unsafe_allow_html=True)
    with c2: st.markdown(f'<div class="kartu c-hijau">Siswa Belajar<span class="txt-val">{int(df_f["Jumlah_Siswa"].sum()):,}</span></div>', unsafe_allow_html=True)
    with c3: st.markdown(f'<div class="kartu c-merah">Anak Tidak Sekolah<span class="txt-val">2,716</span></div>', unsafe_allow_html=True)
    with c4: st.markdown(f'<div class="kartu c-ungu">Angka Partisipasi<span class="txt-val">67.9%</span></div>', unsafe_allow_html=True)

    st.divider()

    # Baris 2: Peta & Grafik
    col_map, col_chart = st.columns([1.5, 1])

    with col_map:
        st.subheader("🗺️ Peta Lokasi Satuan Pendidikan")
        # PERBAIKAN UTAMA: Menggunakan 'open-street-map' agar tidak error
        fig_peta = px.scatter_mapbox(
            df_f, lat="lat", lon="lon", size="Jumlah_Siswa", color="Status",
            hover_name="Nama_Sekolah", zoom=6.5,
            center={"lat": 2.11, "lon": 99.13},
            mapbox_style="open-street-map", # INI YANG DIGANTI
            height=450
        )
        fig_peta.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        st.plotly_chart(fig_peta, use_container_width=True)

    with col_chart:
        st.subheader("📊 Statistik Sekolah")
        if not df_f.empty:
            df_bar = df_f.groupby('Kab_Kota')['Jumlah_Siswa'].sum().reset_index()
            fig_bar = px.bar(df_bar, x='Jumlah_Siswa', y='Kab_Kota', orientation='h', color='Jumlah_Siswa', color_continuous_scale='Blues')
            fig_bar.update_layout(height=350, margin=dict(l=0, r=0, t=0, b=0))
            st.plotly_chart(fig_bar, use_container_width=True)

    # Baris 3: Tabel
    with st.expander("📋 Lihat Detail Data"):
        st.dataframe(df_f, use_container_width=True)
else:
    st.error("File 'master_data_sekolah1.csv' tidak ditemukan. Pastikan file ada di folder yang sama.")
