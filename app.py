import streamlit as st
import pandas as pd
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

# Inisialisasi State
if "login" not in st.session_state: st.session_state.login = False
if "page_view" not in st.session_state: st.session_state.page_view = "dashboard"

# ==================================
# Bagian 1: CSS INJECTION (FULL GRADIENT & CARD UI)
# ==================================
st.markdown("""
<style>
    /* 1. Reset & Sidebar Background */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d47a1 0%, #1565c0 45%, #1976d2 100%) !important;
        background-attachment: fixed !important;
        border-right: none !important;
        color: white !important;
    }
    
    /* Menghilangkan elemen abu-abu default Streamlit */
    [data-testid="stSidebar"] > div:first-child {
        background: transparent !important;
    }

    /* 2. Header Style */
    .sidebar-header {
        display: flex;
        align-items: center;
        gap: 15px;
        padding: 10px 0 20px 0;
    }
    .header-text h2 {
        color: white !important;
        font-size: 1.2rem !important;
        margin: 0 !important;
        font-weight: 800 !important;
    }
    .header-text p {
        color: rgba(255,255,255,0.8) !important;
        font-size: 0.85rem !important;
        margin: 0 !important;
    }

    /* 3. Navigation Menu (Radio styled as Cards) */
    div[data-testid="stSidebar"] .stRadio > label {
        display: none !important; /* Sembunyikan label Navigasi: */
    }
    
    div[data-testid="stSidebar"] div[role="radiogroup"] {
        gap: 10px !important;
        padding-top: 10px !important;
    }

    div[data-testid="stSidebar"] div[role="radiogroup"] label {
        background: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 12px !important;
        padding: 12px 18px !important;
        color: white !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
    }

    div[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
        background: rgba(255, 255, 255, 0.2) !important;
        transform: translateX(5px);
    }

    /* Style menu saat dipilih */
    div[data-testid="stSidebar"] div[role="radiogroup"] label[data-selected="true"] {
        background: rgba(255, 255, 255, 0.25) !important;
        border: 1px solid white !important;
        font-weight: 700 !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2) !important;
    }

    /* 4. Filter Wilayah Card (Light Blue Card) */
    .filter-section {
        background: #448aff !important; /* Warna biru cerah sesuai gambar */
        padding: 20px !important;
        border-radius: 18px !important;
        margin: 25px 0 !important;
        box-shadow: 0 8px 20px rgba(0,0,0,0.15) !important;
    }
    
    .filter-title {
        color: white !important;
        font-weight: 700 !important;
        margin-bottom: 12px !important;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    /* Styling Dropdown di dalam Sidebar */
    div[data-testid="stSidebar"] div[data-baseweb="select"] > div {
        background: white !important;
        border-radius: 10px !important;
        color: #1565c0 !important;
        border: none !important;
    }

    /* Tombol Reset Filter */
    .stButton > button[key="reset_btn"] {
        background: rgba(255,255,255,0.2) !important;
        border: 1px solid rgba(255,255,255,0.4) !important;
        color: white !important;
        width: 100% !important;
        border-radius: 10px !important;
        font-size: 0.8rem !important;
        margin-top: 10px !important;
    }

    /* 5. Logout Button (Orange Gradient) */
    div[data-testid="stSidebar"] .stButton > button[key="logout_btn"] {
        background: linear-gradient(90deg, #ff7043 0%, #ff5722 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 15px !important;
        height: 50px !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        margin-top: 20px !important;
        box-shadow: 0 4px 15px rgba(255, 87, 34, 0.4) !important;
        width: 100% !important;
    }

</style>
""", unsafe_allow_html=True)

# ==================================
# Bagian 2: SIDEBAR IMPLEMENTATION
# ==================================
with st.sidebar:
    # 1. Header (Logo + Judul)
    st.markdown(f"""
    <div class="sidebar-header">
        <img src="https://upload.wikimedia.org/wikipedia/commons/e/e0/Logo_Sumatera_Utara.png" width="50">
        <div class="header-text">
            <h2>SI-PANDAI SUMUT</h2>
            <p>Role: <b>ADMIN</b></p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<hr style='border-color: rgba(255,255,255,0.1)'>", unsafe_allow_html=True)

    # 2. Menu Utama (Radio Button styled as Cards)
    st.markdown("<p style='font-weight:600; font-size: 0.9rem;'>🏠 Menu Utama</p>", unsafe_allow_html=True)
    
    # Fungsi navigasi
    def nav_callback():
        pilih = st.session_state.nav_radio
        if "Dashboard" in pilih: st.session_state.page_view = "dashboard"
        elif "Pendidikan" in pilih: st.session_state.page_view = "tentang_pk"
        else: st.session_state.page_view = "tentang_dashboard"

    st.radio(
        "Navigasi:",
        ["🏠 Dashboard Utama", "🎓 Pendidikan Khusus", "ℹ️ Tentang Dashboard"],
        key="nav_radio",
        on_change=nav_callback
    )

    # 3. Filter Wilayah (Card)
    st.markdown("""
    <div class="filter-section">
        <div class="filter-title">🔍 Filter Wilayah</div>
    """, unsafe_allow_html=True)
    
    st.selectbox("Pilih Kabupaten / Kota", ["Semua", "Medan", "Deli Serdang", "Langkat"], key="kab_pilih")
    
    if st.button("🔄 Reset Filter", key="reset_btn"):
        st.rerun()
        
    st.markdown("</div>", unsafe_allow_html=True)

    # 4. Logout Button
    st.button("🚪 Logout", key="logout_btn")

# ==================================
# Bagian 3: MAIN CONTENT
# ==================================
if st.session_state.page_view == "dashboard":
    st.title("🚀 Dashboard Utama")
    st.write("Konten utama dashboard Anda di sini.")
elif st.session_state.page_view == "tentang_pk":
    st.title("🎓 Tentang Pendidikan Khusus")
else:
    st.title("ℹ️ Tentang Dashboard")
