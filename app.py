import streamlit as st
import pandas as pd
import plotly.express as px

# ==================================
# 1. KONFIGURASI HALAMAN
# ==================================
st.set_page_config(page_title="SI-PANDAI SUMUT", layout="wide")

# ==================================
# 2. LOAD & CLEANING DATA (PROTEKSI ERROR)
# ==================================
@st.cache_data
def load_clean_data():
    try:
        # Load data
        df = pd.read_csv("master_data_sekolah1.csv")
        
        # BERSIHKAN KOLOM: Hapus spasi dan buat huruf kecil semua agar konsisten
        df.columns = df.columns.str.strip()
        
        # PASTIKAN ANGKA: Ubah Jumlah_Siswa jadi angka (jika ada teks, jadi 0)
        df['Jumlah_Siswa'] = pd.to_numeric(df['Jumlah_Siswa'], errors='coerce').fillna(0)
        
        # KOORDINAT LENGKAP: Agar titik di peta tidak menumpuk di satu tempat
        coords = {
            'Kab. Asahan': [2.98, 99.62], 
            'Kab. Batubara': [3.17, 99.50], 
            'Kab. Dairi': [2.85, 98.26],
            'Kab. Deli Serdang': [3.50, 98.70], 
            'Kota Medan': [3.59, 98.67], 
            'Kab. Langkat': [3.75, 98.22],
            'Kab. Karo': [3.11, 98.50], 
            'Kab. Labuhanbatu Utara': [2.33, 99.63],
            'Kota Padangsidimpuan': [1.37, 99.26]
        }
        
        # Tambahkan Lat/Lon berdasarkan Kab_Kota
        df['lat'] = df['Kab_Kota'].map(lambda x: coords.get(x, [2.11, 99.13])[0])
        df['lon'] = df['Kab_Kota'].map(lambda x: coords.get(x, [2.11, 99.13])[1])
        
        return df
    except Exception as e:
        st.error(f"⚠️ Waduh, ada masalah baca file: {e}")
        return pd.DataFrame()

df = load_clean_data()

# ==================================
# 3. CSS KHUSUS (TIDAK AKAN MERUSAK ELEMENT LAIN)
# ==================================
st.markdown("""
<style>
    /* Sidebar Biru */
    [data-testid="stSidebar"] { background-color: #1565c0 !important; }
    [data-testid="stSidebar"] * { color: white !important; }
    
    /* Kartu Dashboard (Class Unik) */
    .kartu-info { padding: 20px; border-radius: 15px; color: white; margin-bottom: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    .biru { background: linear-gradient(135deg, #2196f3 0%, #1976d2 100%); }
    .hijau { background: linear-gradient(135deg, #66bb6a 0%, #43a047 100%); }
    .merah { background: linear-gradient(135deg, #ef5350 0%, #e53935 100%); }
    .ungu { background: linear-gradient(135deg, #7e57c2 0%, #5e35b1 100%); }
    
    .label-kartu { font-size: 14px; font-weight: 600; opacity: 0.9; }
    .angka-kartu { font-size: 28px; font-weight: 800; margin-top: 5px; }

    /* Tombol Logout Spesifik */
    .stButton>button[key="btn_logout"] { background-color: #ff5252 !important; color: white !important; width: 100%; border: none; }
</style>
""", unsafe_allow_html=True)

# ==================================
# 4. SIDEBAR & FILTER
# ==================================
if not df.empty:
    with st.sidebar:
        st.title("SI-PANDAI SUMUT")
        st.write("Role: **ADMIN**")
        st.divider()
        
        list_kab = ["Semua"] + sorted(df['Kab_Kota'].unique().tolist())
        pilihan = st.selectbox("Pilih Wilayah", list_kab)
        
        st.divider()
        st.button("Keluar / Logout 🚪", key="btn_logout")

    # Filter Data berdasarkan pilihan
    df_f = df if pilihan == "Semua" else df[df['Kab_Kota'] == pilihan]

    # ==================================
    # 5. HALAMAN UTAMA
    # ==================================
    st.markdown("<h2 style='color:#1565c0; text-align:center;'>DASHBOARD PEMETAAN SUMUT</h2>", unsafe_allow_html=True)

    # BARIS 1: KARTU METRIK
