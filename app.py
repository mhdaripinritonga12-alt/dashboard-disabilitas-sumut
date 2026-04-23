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
    page_icon="🎓",
    initial_sidebar_state="expanded"
)

# Inisialisasi State
if "page_view" not in st.session_state: st.session_state.page_view = "dashboard"
if "selected_kab" not in st.session_state: st.session_state.selected_kab = "Semua"
if "selected_school_data" not in st.session_state: st.session_state.selected_school_data = None

def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

# ==================================
# Bagian 1: CSS CUSTOM (MODERN & PERMANENT SIDEBAR)
# ==================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
    html, body, [data-testid="stWidgetLabel"] { font-family: 'Inter', sans-serif !important; }

    /* MEMBUAT SIDEBAR PERMANEN (Hiding Toggle Buttons) */
    [data-testid="sidebar-close-button"] { display: none !important; }
    [data-testid="collapsedControl"] { display: none !important; }
    
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 0rem !important;
    }
    
    [data-testid="stHeader"] { display: none !important; }

    /* SIDEBAR STYLING */
    [data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #e0e0e0 !important;
        min-width: 320px !important;
    }
    
    /* HEADER CARD */
    .header-card {
        background: linear-gradient(135deg, #f8fbff 0%, #ffffff 100%);
        padding: 25px;
        border-radius: 15px;
        border-bottom: 5px solid #0d47a1;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        margin-bottom: 30px;
    }

    /* GRID METRIK PROPORSIONAL */
    .metric-tile {
        padding: 22px;
        border-radius: 12px;
        color: white;
        display: flex;
        align-items: center;
        gap: 15px;
        box-shadow: 0 6px 12px rgba(0,0,0,0.08);
        min-height: 110px;
        transition: transform 0.2s ease;
    }
    .metric-tile:hover { transform: translateY(-3px); }
    
    .tile-blue { background: linear-gradient(135deg, #0288d1 0%, #03a9f4 100%); }
    .tile-red { background: linear-gradient(135deg, #d32f2f 0%, #f44336 100%); }
    .tile-green { background: linear-gradient(135deg, #2e7d32 0%, #4caf50 100%); }
    
    .tile-value { font-size: 28px; font-weight: 800; line-height: 1; }
    .tile-label { font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; opacity: 0.9; }
    .tile-icon-svg { width: 40px; height: 40px; fill: white; opacity: 0.8; }

    /* INSIGHT BOX */
    .insight-box { 
        background-color: #ffffff !important; border-radius: 12px; 
        padding: 15px; border-left: 6px solid #0d47a1; 
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)

# ==================================
# Bagian 2: LOAD DATA
# ==================================
@st.cache_data
def load_all_data():
    try:
        df_ats = pd.read_csv("master_data_si_pandai.csv")
        df_sch = pd.read_csv("master_data_sekolah1.csv")
        for df in [df_ats, df_sch]:
            df.columns = df.columns.str.strip().str.lower()
        return df_ats, df_sch
    except: return pd.DataFrame(), pd.DataFrame()

data_wilayah, data_sekolah = load_all_data()

# ==================================
# Bagian 3: SIDEBAR (PERMANEN & PROFESIONAL)
# ==================================
with st.sidebar:
    logo_b64 = get_base64_image("logo_sumut.png")
    if logo_b64:
        st.markdown(f'<div style="text-align:center;"><img src="data:image/png;base64,{logo_b64}" width="100"></div>', unsafe_allow_html=True)
    
    st.markdown("""
        <div style="text-align:center; margin-top:15px; margin-bottom:10px;">
            <h2 style="color:#0d47a1; font-weight:800; margin-bottom:0;">SI-PANDAI</h2>
            <p style="font-size:12px; color:#666; font-weight:600; letter-spacing:1px;">DINAS PENDIDIKAN SUMUT</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Navigasi Menu
    st.markdown("##### 🧭 Navigasi Sistem")
    nav_choice = st.radio("Pilih Halaman:", ["🚀 Dashboard Utama", "ℹ️ Tentang Dashboard"], label_visibility="collapsed")
    
    if "Dashboard Utama" in nav_choice:
        st.session_state.page_view = "dashboard"
    else:
        st.session_state.page_view = "tentang_dashboard"
    
    st.markdown("---")
    
    # Filter Wilayah
    st.markdown("##### 🔎 Filter Wilayah")
    col_kab = "kab_kota" if not data_wilayah.empty and "kab_kota" in data_wilayah.columns else data_wilayah.columns[0]
    opsi = ["Semua"] + sorted(data_wilayah[col_kab].unique().tolist()) if not data_wilayah.empty else ["Semua"]
    kab_pilih = st.selectbox("Pilih Kabupaten / Kota", opsi, key="selected_kab", label_visibility="collapsed")
    
    st.markdown("<br>" * 5, unsafe_allow_html=True)
    st.divider()
    st.markdown(f"""
        <div style="background-color:#f8f9fa; padding:12px; border-radius:8px; border-left:4px solid #0d47a1;">
            <p style="font-size:11px; margin:0; color:#444;"><b>Inovator Sistem:</b><br>Ima Safitri Sianipar, S.Kom</p>
            <p style="font-size:10px; margin:0; color:#888; margin-top:5px;">Jabatan: Penata Kelola IT</p>
        </div>
    """, unsafe_allow_html=True)

# ==================================
# Bagian 4: HEADER & LOGIKA HALAMAN
# ==================================
st.markdown(f"""
    <div class="header-card">
        <h1 style='color: #0d47a1; margin: 0; font-size: 2.4rem; font-weight: 800;'>DASHBOARD SI-PANDAI SUMUT</h1>
        <p style='color: #1565c0; font-size: 1.1rem; font-weight: 600; margin-top: 8px;'>
            Sistem Informasi Pemetaan Anak Tidak Sekolah (ATS) Disabilitas
        </p>
    </div>
""", unsafe_allow_html=True)

if st.session_state.page_view == "dashboard":
    df_f = data_wilayah.copy()
    if kab_pilih != "Semua": df_f = df_f[df_f[col_kab] == kab_pilih]

    # --- GRID 3 METRIK PROPORSIONAL ---
    st.markdown('<h4 style="color:#333; font-weight:700; margin-bottom:15px;">Matriks Capaian Sektoral</h4>', unsafe_allow_html=True)
    m1, m2, m3 = st.columns(3)
    
    v_belajar = int(df_f.iloc[:,2].sum()) if not df_f.empty else 0
    v_ats = int(df_f.iloc[:,3].sum()) if not df_f.empty else 0
    v_total = int(df_f.iloc[:,1].sum()) if not df_f.empty else 0
    v_perc = f"{(v_belajar / v_total * 100):.2f}%" if v_total > 0 else "0.00%"

    with m1:
        st.markdown(f"""<div class="metric-tile tile-blue">
            <div class="tile-icon-svg"><svg viewBox="0 0 16 16"><path d="M8.211 2.047a.5.5 0 0 0-.422 0l-7.5 3.5a.5.5 0 0 0 .025.917l7.5 3 7.5-3a.5.5 0 0 0 .025-.917l-7.5-3.5Z"/></svg></div>
            <div><div class="tile-label">Siswa Belajar</div><div class="tile-value">{v_belajar:,}</div></div>
        </div>""", unsafe_allow_html=True)
        
    with m2:
        st.markdown(f"""<div class="metric-tile tile-red">
            <div class="tile-icon-svg"><svg viewBox="0 0 16 16"><path d="M8.982 1.566a1.13 1.13 0 0 0-1.96 0L.165 13.233c-.457.778.091 1.767.98 1.767h13.713c.889 0 1.438-.99.98-1.767L8.982 1.566zM8 5c.535 0 .954.462.9.995l-.35 3.507a.552.552 0 0 1-1.1 0L7.1 5.995A.905.905 0 0 1 8 5zm.002 6a1 1 0 1 1 0 2 1 1 0 0 1 0-2z"/></svg></div>
            <div><div class="tile-label">Anak Tidak Sekolah</div><div class="tile-value">{v_ats:,}</div></div>
        </div>""", unsafe_allow_html=True)
        
    with m3:
        st.markdown(f"""<div class="metric-tile tile-green">
            <div class="tile-icon-svg"><svg viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M18 20V10M12 20V4M6 20v-6"/></svg></div>
            <div><div class="tile-label">Persentase</div><div class="tile-value">{v_perc}</div></div>
        </div>""", unsafe_allow_html=True)

    # --- VISUALISASI DATA ---
    st.divider()
    c_map, c_chart = st.columns([1.6, 1.1])
    
    with c_map:
        st.subheader("🗺️ Peta Sebaran ATS")
        if not df_f.empty and "lat" in df_f.columns:
            ats_col_name = df_f.columns[3]
            fig_map = px.scatter_mapbox(
                df_f, lat="lat", lon="lon", size=ats_col_name, color=ats_col_name,
                color_continuous_scale="RdYlGn_r", hover_name=col_kab, 
                zoom=7, height=450
            )
            fig_map.update_layout(mapbox_style="carto-positron", margin={"r":0,"t":0,"l":0,"b":0})
            st.plotly_chart(fig_map, use_container_width=True)

    with c_chart:
        st.subheader("📊 5 Tertinggi ATS")
        if not df_f.empty:
            ats_col = df_f.columns[3]
            df_top5 = df_f.sort_values(by=ats_col, ascending=False).head(5)
            fig_bar = px.bar(df_top5, x=ats_col, y=col_kab, orientation='h', color=ats_col,
                             color_continuous_scale="Blues", text=ats_col)
            fig_bar.update_layout(height=380, margin=dict(l=0, r=0, t=10, b=0), showlegend=False, coloraxis_showscale=False)
            st.plotly_chart(fig_bar, use_container_width=True)

    # --- FITUR SEKOLAH ---
    if kab_pilih != "Semua":
        st.divider()
        st.subheader(f"🏫 Satuan Pendidikan di {kab_pilih}")
        sch_wil = data_sekolah[data_sekolah[col_kab] == kab_pilih] if not data_sekolah.empty else pd.DataFrame()
        if not sch_wil.empty:
            cols = st.columns(3)
            for i, row in enumerate(sch_wil.itertuples()):
                with cols[i % 3]:
                    with st.container(border=True):
                        if st.button(getattr(row, 'nama_sekolah', 'SEKOLAH').upper(), key=f"sch_{i}", use_container_width=True):
                            st.session_state.selected_school_data = row._asdict()
                            st.session_state.page_view = "detail"
                            st.rerun()
                        st.caption(f"NPSN: {getattr(row, 'npsn', '-')}")

    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("📋 Tabel Data Lengkap"):
        st.dataframe(df_f, use_container_width=True)

elif st.session_state.page_view == "tentang_dashboard":
    st.header("ℹ️ Tentang SI-PANDAI")
    st.info("Sesuai dengan Rancangan Aktualisasi, dashboard ini berperan sebagai Instrumen Pengambilan Kebijakan (Policy Tool).")
    st.video("https://youtu.be/Wa4C8Ci3Iys?si=vbJRAa-G2dr2kYw8")
    if st.button("⬅️ Kembali ke Dashboard"):
        st.session_state.page_view = "dashboard"
        st.rerun()

# ==================================
# Bagian 5: FOOTER
# ==================================
st.markdown("<br><hr>", unsafe_allow_html=True)
st.markdown("""
    <div style="text-align: center; color: #888; font-size: 11px; padding-bottom: 20px;">
        © 2026 DINAS PENDIDIKAN PROVINSI SUMATERA UTARA | Digitalisasi Pendidikan Khusus
    </div>
""", unsafe_allow_html=True)
