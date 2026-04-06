import streamlit as st
import pandas as pd
import plotly.express as px

# ==================================
# 1. KONFIGURASI HALAMAN
# ==================================
st.set_page_config(page_title="SI-PANDAI SUMUT", layout="wide")

# ==================================
# 2. CSS CUSTOM (SCOPED & SPECIFIC)
# ==================================
st.markdown("""
<style>
    /* Mengatur Font Global */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    * { font-family: 'Inter', sans-serif; }

    /* HEADER STYLE */
    .main-header { text-align: center; padding-bottom: 20px; }
    .main-header h1 { color: #0d47a1; font-weight: 800; margin-bottom: 0; }
    .main-header p { color: #64748b; font-size: 18px; }

    /* GRID KARTU METRIK */
    .metric-container {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 20px;
        margin-bottom: 30px;
    }

    /* BASE CARD STYLE */
    .card {
        padding: 20px;
        border-radius: 15px;
        color: white;
        position: relative;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }

    /* WARNA SPESIFIK TIAP KARTU (Sesuai Gambar) */
    .card-blue { background: linear-gradient(135deg, #2196f3 0%, #1976d2 100%); }
    .card-green { background: linear-gradient(135deg, #66bb6a 0%, #43a047 100%); }
    .card-red { background: linear-gradient(135deg, #ef5350 0%, #e53935 100%); }
    .card-purple { background: linear-gradient(135deg, #7e57c2 0%, #5e35b1 100%); }

    .card-label { font-size: 14px; font-weight: 600; opacity: 0.9; margin-bottom: 5px; }
    .card-value { font-size: 32px; font-weight: 800; }
    .card-delta { font-size: 12px; margin-top: 10px; background: rgba(255,255,255,0.2); padding: 2px 8px; border-radius: 10px; width: fit-content; }

    /* INSIGHT BOX */
    .insight-box {
        background-color: #f0f7ff;
        border-radius: 15px;
        padding: 20px;
        border: 1px solid #c2e0ff;
        margin-top: 20px;
    }
    .insight-title { color: #0d47a1; font-weight: 800; display: flex; align-items: center; gap: 10px; margin-bottom: 10px; }

    /* SIDEBAR COSTUMIZATION */
    [data-testid="stSidebar"] { background-color: #1565c0 !important; }
    [data-testid="stSidebar"] * { color: white !important; }
    
    /* Tombol Logout Merah Spesifik */
    .stButton>button[key="logout_btn"] {
        background: #ff5252 !important;
        border: none !important;
        color: white !important;
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# ==================================
# 3. HEADER
# ==================================
st.markdown("""
    <div class="main-header">
        <h1>SI-PANDAI SUMUT</h1>
        <p>Dashboard Pemetaan ATS Disabilitas</p>
    </div>
""", unsafe_allow_html=True)

# ==================================
# 4. ROW 1: KARTU METRIK (4 KOLOM)
# ==================================
# Menggunakan HTML langsung agar CSS tidak 'bocor' ke elemen Streamlit lainnya
st.markdown("""
    <div class="metric-container">
        <div class="card card-blue">
            <div class="card-label">👤 Penduduk Disabilitas</div>
            <div class="card-value">6,732</div>
        </div>
        <div class="card card-green">
            <div class="card-label">🎓 Siswa Belajar</div>
            <div class="card-value">4,573</div>
            <div class="card-delta">▲ 3% dari bulan lalu</div>
        </div>
        <div class="card card-red">
            <div class="card-label">⚠️ Anak Tidak Sekolah</div>
            <div class="card-value">2,716</div>
            <div class="card-delta">▲ 5% dari bulan lalu</div>
        </div>
        <div class="card card-purple">
            <div class="card-label">📈 Angka Partisipasi</div>
            <div class="card-value">67.93%</div>
            <div class="card-delta">▲ 2% dari bulan lalu</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# ==================================
# 5. ROW 2: MAP & CHART
# ==================================
col_left, col_right = st.columns([1.5, 1])

with col_left:
    st.subheader("🗺️ Peta Sebaran ATS")
    # Placeholder Map (Gunakan data asli Anda di sini)
    map_data = pd.DataFrame({'lat': [3.5952], 'lon': [98.6722]}) 
    st.map(map_data, zoom=7)

with col_right:
    st.subheader("📊 Grafik ATS Wilayah")
    # Contoh Data Grafik
    chart_data = pd.DataFrame({
        'Wilayah': ['Kab. Labuhanbatu Utara', 'Kab. Langkat', 'Kab. Labuhanbatu Selatan', 'Kab. Asahan', 'Kab. Karo'],
        'ATS': [365, 310, 293, 260, 201]
    })
    fig = px.bar(chart_data, x='ATS', y='Wilayah', orientation='h', 
                 color='ATS', color_continuous_scale='Reds')
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), height=300)
    st.plotly_chart(fig, use_container_width=True)

    # Insight Box di bawah grafik
    st.markdown("""
        <div class="insight-box">
            <div class="insight-title">🔍 Insight:</div>
            <p>Wilayah <b>Kab. Labuhanbatu Utara</b> memiliki jumlah ATS tertinggi sebanyak <b>365</b>. Perlu menjadi prioritas intervensi.</p>
        </div>
    """, unsafe_allow_html=True)

# ==================================
# 6. SIDEBAR
# ==================================
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/b/ba/Coat_of_arms_of_North_Sumatra.svg", width=80)
    st.title("SI-PANDAI SUMUT")
    st.write("Role: **ADMIN**")
    st.divider()
    
    st.selectbox("Pilih Kabupaten / Kota", ["Semua", "Medan", "Langkat", "Deli Serdang"])
    st.button("Reset Filter")
    st.download_button("Download Data (CSV)", data="...", file_name="data.csv")
    
    st.divider()
    # Gunakan key agar bisa di-target spesifik di CSS
    st.button("Logout 🚪", key="logout_btn")
