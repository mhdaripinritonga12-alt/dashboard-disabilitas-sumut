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

# Inisialisasi State agar navigasi lancar
if "page_view" not in st.session_state: st.session_state.page_view = "dashboard"
if "selected_kab" not in st.session_state: st.session_state.selected_kab = "Semua"
if "selected_school_data" not in st.session_state: st.session_state.selected_school_data = None

def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

# ==================================
# Bagian 1: CSS CUSTOM (SIDEBAR PERMANEN & UI MODERN)
# ==================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
    html, body, [data-testid="stWidgetLabel"] { font-family: 'Inter', sans-serif !important; }

    /* PAKSA SIDEBAR TETAP MUNCUL */
    button[kind="headerNoPadding"] { display: none !important; }
    [data-testid="stSidebarNav"] { display: none !important; }

    .block-container { padding-top: 1rem !important; padding-left: 2rem !important; padding-right: 2rem !important; }
    [data-testid="stHeader"] { display: none !important; }

    /* SIDEBAR STYLING */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f8f9fa 0%, #e3f2fd 100%) !important;
        border-right: 1px solid #e0e0e0 !important;
        min-width: 300px !important;
    }
    
    /* HEADER STYLING */
    .header-card {
        background: linear-gradient(135deg, #ffffff 0%, #f0f7ff 100%);
        padding: 30px; border-radius: 15px; border-bottom: 5px solid #0d47a1;
        text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.05); margin-bottom: 30px;
    }

    /* METRIC TILES */
    .metric-tile {
        padding: 20px; border-radius: 12px; color: white;
        display: flex; align-items: center; gap: 15px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1); min-height: 100px;
    }
    .tile-blue { background: linear-gradient(135deg, #03a9f4 0%, #0288d1 100%); }
    .tile-red { background: linear-gradient(135deg, #ff4b2b 0%, #ff416c 100%); }
    .tile-green { background: linear-gradient(135deg, #4caf50 0%, #2e7d32 100%); }
    .tile-value { font-size: 24px; font-weight: 800; line-height: 1; }
    .tile-label { font-size: 11px; font-weight: 700; text-transform: uppercase; opacity: 0.9; }

    /* INSIGHT BOX */
    .insight-box { 
        background-color: #ffffff !important; border-radius: 12px; 
        padding: 15px; border-left: 6px solid #0d47a1; 
        box-shadow: 0 2px 10px rgba(0,0,0,0.05); margin-top: 15px;
    }
</style>
""", unsafe_allow_html=True)

# ==================================
# Bagian 2: LOAD DATA (FITUR UTAMA)
# ==================================
@st.cache_data
def load_all_data():
    try:
        df_ats = pd.read_csv("master_data_si_pandai.csv")
        df_sch = pd.read_csv("master_data_sekolah1.csv")
        for df in [df_ats, df_sch]:
            df.columns = df.columns.str.strip().str.lower()
        return df_ats, df_sch
    except:
        return pd.DataFrame(), pd.DataFrame()

data_wilayah, data_sekolah = load_all_data()

# ==================================
# Bagian 3: SIDEBAR (NAVIGASI & FILTER)
# ==================================
with st.sidebar:
    logo_b64 = get_base64_image("logo_sumut.png")
    if logo_b64:
        st.markdown(f'<div style="text-align:center;"><img src="data:image/png;base64,{logo_b64}" width="80"></div>', unsafe_allow_html=True)
    
    st.markdown("<h2 style='text-align:center; color:#0d47a1;'>SI-PANDAI</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Navigasi Utama
    nav_choice = st.radio("🧭 MENU UTAMA", ["🚀 Dashboard Utama", "ℹ️ Tentang Dashboard"])
    st.session_state.page_view = "dashboard" if "Dashboard" in nav_choice else "tentang_dashboard"
    
    st.markdown("---")
    st.markdown("### 🔎 FILTER WILAYAH")
    col_kab = "kab_kota" if "kab_kota" in data_wilayah.columns else (data_wilayah.columns[0] if not data_wilayah.empty else "")
    
    if not data_wilayah.empty:
        opsi = ["Semua"] + sorted(data_wilayah[col_kab].unique().tolist())
        kab_pilih = st.selectbox("Pilih Kabupaten/Kota", opsi, key="selected_kab")
    else:
        kab_pilih = "Semua"

    st.markdown("<br><br>" * 3, unsafe_allow_html=True)
    st.caption("Inovator: Ima Safitri Sianipar, S.Kom")

# ==================================
# Bagian 4: MAIN HEADER
# ==================================
st.markdown(f"""
    <div class="header-card">
        <h1 style='color: #0d47a1; margin: 0; font-size: 2.2rem; font-weight: 800;'>DASHBOARD SI-PANDAI SUMUT</h1>
        <p style='color: #1565c0; font-size: 1rem; font-weight: 600; margin-top: 5px;'>
            Sistem Informasi Pemetaan Anak Tidak Sekolah (ATS) Disabilitas
        </p>
    </div>
""", unsafe_allow_html=True)

# ==================================
# Bagian 5: LOGIKA HALAMAN
# ==================================

# --- A. HALAMAN DASHBOARD ---
if st.session_state.page_view == "dashboard":
    df_f = data_wilayah.copy()
    if kab_pilih != "Semua": df_f = df_f[df_f[col_kab] == kab_pilih]

    # GRID 3 METRIK PROPORSIONAL
    st.markdown('<h4 style="color:#0d47a1; font-weight:700;">📊 Matriks Capaian Sektoral</h4>', unsafe_allow_html=True)
    m1, m2, m3 = st.columns(3)
    
    v_belajar = int(df_f.iloc[:,2].sum()) if not df_f.empty else 0
    v_ats = int(df_f.iloc[:,3].sum()) if not df_f.empty else 0
    v_total = int(df_f.iloc[:,1].sum()) if not df_f.empty else 0
    v_perc = f"{(v_belajar / v_total * 100):.2f}%" if v_total > 0 else "0%"

    with m1:
        st.markdown(f'<div class="metric-tile tile-blue"><div><div class="tile-label">Siswa Belajar</div><div class="tile-value">{v_belajar:,}</div></div></div>', unsafe_allow_html=True)
    with m2:
        st.markdown(f'<div class="metric-tile tile-red"><div><div class="tile-label">Anak Tidak Sekolah</div><div class="tile-value">{v_ats:,}</div></div></div>', unsafe_allow_html=True)
    with m3:
        st.markdown(f'<div class="metric-tile tile-green"><div><div class="tile-label">Persentase</div><div class="tile-value">{v_perc}</div></div></div>', unsafe_allow_html=True)

    # VISUALISASI UTAMA
    st.divider()
    cv1, cv2 = st.columns([1.6, 1.1])
    
    with cv1:
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

    with cv2:
        st.subheader("📊 Peringkat ATS Tertinggi")
        if not df_f.empty:
            ats_col = df_f.columns[3]
            df_top5 = df_f.sort_values(by=ats_col, ascending=False).head(5)
            fig_bar = px.bar(df_top5, x=ats_col, y=col_kab, orientation='h', color=ats_col,
                             color_continuous_scale="Blues", text=ats_col)
            fig_bar.update_layout(height=350, margin=dict(l=0, r=0, t=20, b=0), showlegend=False, coloraxis_showscale=False)
            st.plotly_chart(fig_bar, use_container_width=True)

    # FITUR SEKOLAH (MUNCUL JIKA KABUPATEN DIPILIH)
    if kab_pilih != "Semua":
        st.divider()
        st.subheader(f"🏫 Satuan Pendidikan di {kab_pilih}")
        sch_wil = data_sekolah[data_sekolah[col_kab] == kab_pilih] if not data_sekolah.empty else pd.DataFrame()
        if not sch_wil.empty:
            cols = st.columns(3)
            for i, row in enumerate(sch_wil.itertuples()):
                with cols[i % 3]:
                    with st.container(border=True):
                        if st.button(getattr(row, 'nama_sekolah', 'SEKOLAH').upper(), key=f"sch_{i}"):
                            st.session_state.selected_school_data = row._asdict()
                            st.session_state.page_view = "detail"
                            st.rerun()
                        st.caption(f"NPSN: {getattr(row, 'npsn', '-')}")

    # TABEL DATA
    with st.expander("📋 Lihat & Download Data Tabel"):
        st.dataframe(df_f, use_container_width=True)

# --- B. HALAMAN DETAIL SEKOLAH ---
elif st.session_state.page_view == "detail":
    sch = st.session_state.selected_school_data
    if sch:
        st.button("⬅️ Kembali", on_click=lambda: setattr(st.session_state, 'page_view', 'dashboard'))
        st.header(f"🏫 {sch['nama_sekolah'].upper()}")
        
        c1, c2 = st.columns(2)
        with c1:
            with st.container(border=True):
                st.subheader("📌 Profil Umum")
                st.write(f"**NPSN:** {sch.get('npsn', '-')}")
                st.write(f"**Alamat:** {sch.get('alamat', '-')}")
        with c2:
            with st.container(border=True):
                st.subheader("🏗️ Sarana Prasarana")
                st.write(f"**Rombel:** {sch.get('jumlah_rombel', '0')}")
                st.write(f"**Siswa:** {sch.get('jumlah_siswa', '0')}")

# --- C. HALAMAN TENTANG ---
elif st.session_state.page_view == "tentang_dashboard":
    st.header("ℹ️ Informasi Sistem SI-PANDAI")
    st.markdown("""
    **SI-PANDAI SUMUT** adalah platform digital untuk memetakan Anak Tidak Sekolah (ATS) Disabilitas.
    Sistem ini dirancang untuk mendukung pengambilan kebijakan berbasis data di Dinas Pendidikan Sumatera Utara.
    """)
    st.video("https://youtu.be/Wa4C8Ci3Iys?si=vbJRAa-G2dr2kYw8")

# ==================================
# Bagian Akhir: FOOTER
# ==================================
st.markdown("<br><hr>", unsafe_allow_html=True)
st.markdown("""
    <div style="text-align: center; color: #666; font-size: 12px;">
        © 2026 DINAS PENDIDIKAN PROVINSI SUMATERA UTARA | Bidang Pembinaan Pendidikan Khusus
    </div>
""", unsafe_allow_html=True)
