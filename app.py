import streamlit as st
import pandas as pd
import plotly.express as px
import os
import base64
import streamlit.components.v1 as components

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
if "selected_kab" not in st.session_state: st.session_state.selected_kab = "Semua"
if "selected_school_data" not in st.session_state: st.session_state.selected_school_data = None

def proses_logout():
    st.session_state.selected_kab = "Semua"
    st.session_state.login = False
    st.session_state.page_view = "dashboard"
    st.rerun()

def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

# ==================================
# Bagian 1: CSS CUSTOM (MODERN SIDEBAR & HEADER)
# ==================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
    html, body, [data-testid="stWidgetLabel"] { font-family: 'Inter', sans-serif !important; }

    /* --- SIDEBAR GRADIENT --- */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e88e5 0%, #0d47a1 100%) !important;
        background-attachment: fixed !important;
    }
    [data-testid="stSidebar"] * { color: white !important; }
    div[data-testid="stSelectbox"] div[data-baseweb="select"] * { color: #31333f !important; }

    /* --- TOP HEADER CONTENT --- */
    .top-header-container {
        background-color: white !important;
        padding: 15px 25px !important;
        border-radius: 15px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: space-between !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08) !important;
        margin-bottom: 25px !important;
        border: 1px solid #f0f0f0 !important;
    }

    /* --- MENU UTAMA (SIDEBAR CARDS) --- */
    div[data-testid="stSidebar"] div.stRadio > div { gap: 10px !important; }
    div[data-testid="stSidebar"] div.stRadio label {
        background: rgba(255, 255, 255, 0.15) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 12px !important;
        padding: 12px 15px !important;
        transition: 0.3s;
