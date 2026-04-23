import streamlit as st
import pandas as pd
import plotly.express as px
import os
import base64

# ==================================
# 1. KONFIGURASI HALAMAN
# ==================================
st.set_page_config(
    page_title="SI-PANDAI SUMUT",
    layout="wide",
    page_icon="🎓",
    initial_sidebar_state="expanded"
)

# Inisialisasi State
if "page_view" not in st.session_state: st.session_state.page_view = "dashboard"
if "selected_kab" not in st.session_state: st.session_state.selected_kab = "Semua"

# ==================================
# 2. CSS CUSTOM (UI PROFESIONAL)
# ==================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
    
    /* Global Styles */
    html, body, [data-testid="stWidgetLabel"] { 
        font-family: 'Inter', sans-serif !important; 
    }
    
    .stApp { background-color: #f8fafc; }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e40af 0%, #1e3a8a 100%) !important;
        border-right: 1px solid rgba(255,255,255,0.1);
    }
    [data-testid="stSidebar"] * { color: white !important; }
    
    /* Top Header Bar */
    .top-bar {
        position: fixed;
        top: 0; left: 0; width: 100%; height: 5px;
        background: linear-gradient(90deg, #2563eb, #7c3aed);
        z-index: 999;
    }

    /* Professional Cards */
    .metric-card {
        background: white;
        padding: 24px;
        border-radius: 16px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.05);
        transition: transform 0.2s;
    }
    .metric-card:hover { transform: translateY(-2px); }
    
    .metric-label { font-size: 12px; font-weight: 800; color: #64748b; text-transform: uppercase; letter-spacing: 0.1em; }
    .metric-value { font-size: 28px; font-weight: 800; color: #1e293b; margin-top: 4px; }

    /* Custom Header */
    .header-section {
        background: white;
        padding: 20px 30px;
        border-radius: 0 0 24px 24px;
        border-bottom: 2px solid #2563eb;
        margin-bottom: 30px;
        box-shadow: 0 10px 15px -3px rgb(0 0 0 / 0.04);
    }
    
    /* Sidebar Selectbox Fix */
    div[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] {
        background-color: rgba(255,255,255,0.1) !important;
        border: 2px solid rgba(255,255,255,0.2) !important;
        border-radius: 12px !important;
    }
</style>
""", unsafe_allow_html=True)

# ==================================
# 3. MOCK DATA (Ganti dengan pd.read_csv anda)
# ==================================
KAB_DATA = [
    {"kab_kota": "Kota Medan", "belajar": 12500, "ats": 450, "lat": 3.59, "lon": 98.67},
    {"kab_kota": "Kab. Deli Serdang", "belajar": 9800, "ats": 380, "lat": 3.51, "lon": 98.81},
    {"kab_kota": "Kab. Langkat", "belajar": 5200, "ats": 310, "lat": 3.73, "lon": 98.34},
    {"kab_kota": "Kab. Asahan", "belajar": 4100, "ats": 280, "lat": 2.99, "lon": 99.61},
    {"kab_kota": "Kab. Simalungun", "belajar": 4900, "ats": 260, "lat": 2.85, "lon": 99.07}
]
df_ats = pd.DataFrame(KAB_DATA)

# ==================================
# 4. SIDEBAR PERMANEN
# ==================================
with st.sidebar:
    st.markdown("### 🎓 SI-PANDAI")
    st.markdown("---")
    
    # Navigasi
    st.markdown("#### 🧭 Menu Utama")
    if st.button("🚀 Dashboard Utama", use_container_width=True):
        st.session_state.page_view = "dashboard"
        st.session_state.selected_kab = "Semua"
        
    if st.button("ℹ️ Tentang Sistem", use_container_width=True):
        st.session_state.page_view = "about"

    st.markdown("---")
    
    # Filter
    st.markdown("#### 🔎 Filter Wilayah")
    kab_list = ["Semua"] + sorted(df_ats["kab_kota"].tolist())
    kab_pilih = st.selectbox("Pilih Kabupaten/Kota", kab_list, key="selected_kab")

# ==================================
# 5. CONTENT AREA
# ==================================
st.markdown('<div class="top-bar"></div>', unsafe_allow_html=True)

# Header
st.markdown(f"""
    <div class="header-section">
        <h1 style='color: #1e3a8a; margin:0; font-size: 24px; font-weight:800;'>SI-PANDAI SUMATERA UTARA</h1>
        <p style='color: #64748b; margin:0; font-size: 14px; font-weight:600;'>Sistem Pemetaan Anak Tidak Sekolah Disabilitas</p>
    </div>
""", unsafe_allow_html=True)

if st.session_state.page_view == "dashboard":
    # Filter Data
    df_filtered = df_ats.copy()
    if kab_pilih != "Semua":
        df_filtered = df_ats[df_ats["kab_kota"] == kab_pilih]
    
    # Matriks
    col1, col2, col3 = st.columns(3)
    
    with col1:
        sum_belajar = df_filtered["belajar"].sum()
        st.markdown(f"""
            <div class="metric-card" style="border-bottom: 4px solid #3b82f6;">
                <div class="metric-label">Siswa Belajar</div>
                <div class="metric-value">{sum_belajar:,}</div>
            </div>
        """, unsafe_allow_html=True)
        
    with col2:
        sum_ats = df_filtered["ats"].sum()
        st.markdown(f"""
            <div class="metric-card" style="border-bottom: 4px solid #ef4444;">
                <div class="metric-label">Anak Tidak Sekolah</div>
                <div class="metric-value">{sum_ats:,}</div>
            </div>
        """, unsafe_allow_html=True)
        
    with col3:
        rasio = (sum_belajar / (sum_belajar + sum_ats) * 100) if (sum_belajar + sum_ats) > 0 else 0
        st.markdown(f"""
            <div class="metric-card" style="border-bottom: 4px solid #10b981;">
                <div class="metric-label">Partisipasi</div>
                <div class="metric-value">{rasio:.2f}%</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Visualisasi
    c_left, c_right = st.columns([1.5, 1])
    
    with c_left:
        st.markdown("#### 🗺️ Peta Sebaran Wilayah")
        fig_map = px.scatter_mapbox(
            df_filtered, lat="lat", lon="lon", size="ats", color="ats",
            color_continuous_scale="RdYlGn_r", zoom=7, height=450
        )
        fig_map.update_layout(mapbox_style="open-street-map", margin={"r":0,"t":0,"l":0,"b":0})
        st.plotly_chart(fig_map, use_container_width=True)
        
    with c_right:
        st.markdown("#### 📊 Peringkat ATS Tertinggi")
        df_top = df_ats.sort_values("ats", ascending=False).head(5)
        fig_bar = px.bar(
            df_top, x="ats", y="kab_kota", orientation="h",
            labels={"ats": "Jumlah ATS", "kab_kota": ""},
            color="ats", color_continuous_scale="Blues"
        )
        fig_bar.update_layout(height=400, showlegend=False, coloraxis_showscale=False)
        st.plotly_chart(fig_bar, use_container_width=True)

    # Insight Box
    st.info(f"💡 **Rekomendasi Strategis**: Wilayah {kab_pilih} memerlukan penguatan pada Unit Layanan Disabilitas (ULD) untuk menurunkan angka ATS.")

    # Footer
    st.markdown("---")
    st.markdown("""
        <div style="text-align: center; color: #94a3b8; font-size: 12px; font-weight: 600;">
            © 2026 DINAS PENDIDIKAN PROVINSI SUMATERA UTARA | SI-PANDAI SUMUT
        </div>
    """, unsafe_allow_html=True)

elif st.session_state.page_view == "about":
    st.markdown("### ℹ️ Tentang SI-PANDAI")
    st.write("Sistem ini dirancang untuk mempermudah pimpinan dalam memetakan kebutuhan pendidikan khusus secara riil di lapangan.")
    st.button("⬅️ Kembali ke Dashboard", on_click=lambda: setattr(st.session_state, "page_view", "dashboard"))
