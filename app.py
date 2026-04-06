import streamlit as st
import pandas as pd
import plotly.express as px

# ==================================
# 1. KONFIGURASI HALAMAN
# ==================================
st.set_page_config(page_title="SI-PANDAI SUMUT", layout="wide")

# ==================================
# 2. FUNGSI LOAD DATA (SANGAT AMAN)
# ==================================
@st.cache_data
def load_data_aman():
    try:
        df = pd.read_csv("master_data_sekolah1.csv")
        # Bersihkan spasi di nama kolom
        df.columns = df.columns.str.strip()
        
        # Pastikan kolom Jumlah_Siswa jadi angka
        df['Jumlah_Siswa'] = pd.to_numeric(df['Jumlah_Siswa'], errors='coerce').fillna(0)
        
        # Kamus Koordinat (Penting agar peta tidak error)
        coords = {
            'KAB. ASAHAN': [2.98, 99.62], 
            'KAB. BATUBARA': [3.17, 99.50], 
            'KAB. DAIRI': [2.85, 98.26],
            'KAB. DELI SERDANG': [3.50, 98.70], 
            'KOTA MEDAN': [3.59, 98.67], 
            'KAB. LANGKAT': [3.75, 98.22],
            'KAB. KARO': [3.11, 98.50], 
            'KAB. LABUHANBATU UTARA': [2.33, 99.63],
            'KOTA PADANGSIDIMPUAN': [1.37, 99.26], 
            'KAB. LABUHANBATU SELATAN': [1.97, 100.10]
        }
        
        # Buat kolom lat dan lon (Case Insensitive / Tidak sensitif huruf besar kecil)
        df['lat'] = df['Kab_Kota'].str.upper().str.strip().map(lambda x: coords.get(x, [2.11, 99.13])[0])
        df['lon'] = df['Kab_Kota'].str.upper().str.strip().map(lambda x: coords.get(x, [2.11, 99.13])[1])
        
        return df
    except Exception as e:
        st.error(f"Gagal memuat data: {e}")
        return pd.DataFrame()

df = load_data_aman()

# ==================================
# 3. CSS CUSTOM (UNIK & TERISOLASI)
# ==================================
st.markdown("""
<style>
    /* Sidebar */
    [data-testid="stSidebar"] { background-color: #0d47a1 !important; }
    [data-testid="stSidebar"] * { color: white !important; }

    /* Kartu Dashboard - Menggunakan ID unik agar tidak merusak elemen lain */
    .dashboard-card {
        padding: 20px; border-radius: 15px; color: white; 
        margin-bottom: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .bg-biru { background: linear-gradient(135deg, #1e88e5, #1565c0); }
    .bg-hijau { background: linear-gradient(135deg, #4caf50, #2e7d32); }
    .bg-merah { background: linear-gradient(135deg, #f44336, #c62828); }
    .bg-ungu { background: linear-gradient(135deg, #9c27b0, #6a1b9a); }
    
    .card-title { font-size: 14px; font-weight: 600; opacity: 0.9; }
    .card-value { font-size: 26px; font-weight: 800; margin-top: 5px; }

    /* Tombol Logout Merah */
    button[key="logout_final"] {
        background-color: #ff5252 !important; color: white !important;
        border: none !important; width: 100% !important;
    }
</style>
""", unsafe_allow_html=True)

# ==================================
# 4. SIDEBAR
# ==================================
if not df.empty:
    with st.sidebar:
        st.title("🛡️ SI-PANDAI")
        st.subheader("Dashboard Admin")
        st.divider()
        
        opsi_wilayah = ["Semua"] + sorted(df['Kab_Kota'].unique().tolist())
        pilih = st.selectbox("Pilih Wilayah", opsi_wilayah)
        
        st.divider()
        st.button("Logout 🚪", key="logout_final")

    # Filter data
    df_f = df if pilih == "Semua" else df[df['Kab_Kota'] == pilih]

    # ==================================
    # 5. TAMPILAN DASHBOARD
    # ==================================
    st.markdown("<h2 style='color:#0d47a1; text-align:center;'>DASHBOARD MONITORING SUMATERA UTARA</h2>", unsafe_allow_html=True)

    # Baris 1: Kartu Metrik
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown('<div class="dashboard-card bg-biru"><div class="card-title">Disabilitas</div><div class="card-value">6,732</div></div>', unsafe_allow_html=True)
    with c2: st.markdown(f'<div class="dashboard-card bg-hijau"><div class="card-title">Siswa Belajar</div><div class="card-value">{int(df_f["Jumlah_Siswa"].sum()):,}</div></div>', unsafe_allow_html=True)
    with c3: st.markdown('<div class="dashboard-card bg-merah"><div class="card-title">Anak Tidak Sekolah</div><div class="card-value">2,716</div></div>', unsafe_allow_html=True)
    with c4: st.markdown('<div class="dashboard-card bg-ungu"><div class="card-title">Partisipasi</div><div class="card-value">67.9%</div></div>', unsafe_allow_html=True)

    st.divider()

    # Baris 2: Peta dan Grafik
    col_kiri, col_kanan = st.columns([1.5, 1])

    with col_kiri:
        st.subheader("🗺️ Sebaran Satuan Pendidikan")
        try:
            # Gunakan 'open-street-map' karena ini yang paling aman dari error
            fig_peta = px.scatter_mapbox(
                df_f, lat="lat", lon="lon", size="Jumlah_Siswa", color="Status",
                hover_name="Nama_Sekolah", zoom=7,
                center={"lat": 2.11, "lon": 99.13}, # Tengah Sumut
                mapbox_style="open-street-map", 
                height=450
            )
            fig_peta.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
            st.plotly_chart(fig_peta, use_container_width=True)
        except Exception as map_err:
            st.warning(f"Gagal menampilkan peta: {map_err}. Tapi data tetap aman.")

    with col_kanan:
        st.subheader("📊 Statistik Siswa")
        top_kab = df_f.groupby('Kab_Kota')['Jumlah_Siswa'].sum().reset_index()
        fig_bar = px.bar(top_kab, x='Jumlah_Siswa', y='Kab_Kota', orientation='h', color='Jumlah_Siswa', color_continuous_scale='Blues')
        fig_bar.update_layout(height=350, margin=dict(l=0, r=0, t=0, b=0))
        st.plotly_chart(fig_bar, use_container_width=True)

    # Baris 3: Tabel Detail
    with st.expander("📋 Lihat Detail Tabel"):
        st.dataframe(df_f, use_container_width=True)
else:
    st.error("Data tidak ditemukan atau CSV salah format.")
