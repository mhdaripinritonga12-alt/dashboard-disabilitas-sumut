import streamlit as st
import pandas as pd
import plotly.express as px
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

# --- FUNGSI RESET LOGOUT ---
def proses_logout():
    st.session_state.selected_kab = "Semua"
    st.session_state.login = False
    st.session_state.page_view = "dashboard"

if "page_view" not in st.session_state: st.session_state.page_view = "dashboard"
if "selected_kab" not in st.session_state: st.session_state.selected_kab = "Semua"

# ==================================
# Bagian 1: CSS CUSTOM (STABIL & BERSIH)
# ==================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&display=swap');
    html, body, [data-testid="stWidgetLabel"] { font-family: 'Inter', sans-serif !important; }
    [data-testid="stAppViewContainer"] { background-color: #f8fafc !important; }
    header {visibility: hidden;}

    /* 1. SIDEBAR NAVY GRADIENT */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d47a1 0%, #1e3a8a 100%) !important;
    }
    [data-testid="stSidebar"] * { color: white !important; }
    
    /* FIX: TEKS FILTER TETAP HITAM */
    div[data-testid="stSelectbox"] div[data-baseweb="select"] * { color: #1e293b !important; }

    /* 2. MATRIX KOTAK (TILE STYLE) */
    .metric-box {
        background: white; padding: 20px; border-radius: 12px;
        border-top: 6px solid #0d47a1; box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        text-align: center; margin-bottom: 10px;
    }
    .m-label { font-size: 13px; color: #64748b; font-weight: 700; margin-bottom: 5px; }
    .m-value { font-size: 30px; color: #0d47a1; font-weight: 800; }

    /* 3. BALON WARNA SEKOLAH (FIXED) */
    .status-balon { padding: 10px; border-radius: 8px; font-size: 12px; font-weight: 800; text-align: center; margin-bottom: 15px; }
    .mendesak { background-color: #fee2e2 !important; color: #dc2626 !important; border: 1px solid #dc2626; }
    .rehab { background-color: #fef3c7 !important; color: #d97706 !important; border: 1px solid #d97706; }
    .aman { background-color: #dcfce7 !important; color: #16a34a !important; border: 1px solid #16a34a; }

    /* 4. TOMBOL NAMA SEKOLAH */
    div.stButton > button[key^="btn_"] {
        background: transparent !important; color: #0d47a1 !important;
        font-size: 18px !important; font-weight: 800 !important;
        text-align: left !important; padding: 0 !important; box-shadow: none !important;
    }

    /* 5. DOWNLOAD BUTTON (HIJAU) */
    .stDownloadButton > button {
        background: linear-gradient(90deg, #16a34a 0%, #22c55e 100%) !important;
        color: white !important; border-radius: 10px !important; font-weight: 700 !important;
        height: 48px !important; width: 100% !important; border: none !important;
    }
</style>
""", unsafe_allow_html=True)

# --- FUNGSI RENDER KOTAK ---
def draw_box(label, value):
    st.markdown(f'<div class="metric-box"><div class="m-label">{label}</div><div class="m-value">{value}</div></div>', unsafe_allow_html=True)

# ==================================
# Bagian 2: LOAD DATA
# ==================================
@st.cache_data
def load_all_data():
    try:
        df_ats = pd.read_csv("master_data_si_pandai.csv")
        df_sch = pd.read_csv("master_data_sekolah1.csv")
        return df_ats, df_sch
    except:
        return pd.DataFrame(), pd.DataFrame()

data_wilayah, data_sekolah = load_all_data()

# =========================
# Bagian 3: LOGIN
# =========================
if "login" not in st.session_state: st.session_state.login = False
if not st.session_state.login:
    _, col_card, _ = st.columns([1, 1.2, 1])
    with col_card:
        with st.container(border=True):
            st.markdown("<h2 style='text-align:center; color:#0d47a1;'>LOGIN SI-PANDAI</h2>", unsafe_allow_html=True)
            u = st.text_input("Username")
            p = st.text_input("Password", type="password")
            if st.button("MASUK KE SISTEM"):
                if u == "admin" and p == "admin":
                    st.session_state.login = True
                    st.rerun()
                else: st.error("Akses Ditolak")
    st.stop()

# ==================================
# Bagian 4: DASHBOARD UTAMA
# ==================================

# SIDEBAR
st.sidebar.markdown("### 🏛️ PANEL KONTROL")
st.sidebar.write(f"👤 User: **FRAYOGI ADITIYA**")
st.sidebar.divider()
opsi_kab = ["Semua"] + sorted(data_wilayah["kab_kota"].unique().tolist())
kab_pilih = st.sidebar.selectbox("Pilih Kabupaten / Kota", opsi_kab, key="selected_kab")
st.sidebar.divider()
df_dl = data_wilayah.copy() if kab_pilih == "Semua" else data_wilayah[data_wilayah["kab_kota"] == kab_pilih]
st.sidebar.download_button("Download Data (CSV) ⬇️", df_dl.to_csv(index=False).encode('utf-8'), f"data_sipandai_{kab_pilih}.csv", "text/csv")
st.sidebar.divider()
st.sidebar.button("Logout 🚪", use_container_width=True, on_click=proses_logout)

# KONTEN
if st.session_state.page_view == "dashboard":
    st.markdown('<p style="font-size:26px; font-weight:800; color:#0d47a1;">🚀 Dashboard Utama Si-Cerdas</p>', unsafe_allow_html=True)
    st.divider()

    df_f = data_wilayah.copy() if kab_pilih == "Semua" else data_wilayah[data_wilayah["kab_kota"] == kab_pilih]

    # 1. MATRIX KOTAK (TILE)
    st.subheader("📌 Matriks Capaian")
    m1, m2, m3 = st.columns(3)
    if kab_pilih == "Semua":
        with m1: draw_box("PENDUDUK DISABILITAS", "6.732")
        with m2: draw_box("SISWA AKTIF", "4.573")
        with m3: draw_box("APS SUMUT", "67.93%")
    else:
        with m1: draw_box("PENDUDUK DISABILITAS", f"{int(df_f['jumlah_penduduk'].sum()):,}")
        with m2: draw_box("SISWA AKTIF", f"{int(df_f['jumlah_siswa'].sum()):,}")
        with m3: draw_box("ATS WILAYAH", f"{int(df_f['ats_disabilitas'].sum()):,}")

    # 2. PETA HIDUP (SATELIT BERWARNA)
    st.divider()
    cv1, cv2 = st.columns([1.6, 1])
    with cv1:
        st.subheader("🗺️ Visualisasi Satelit (Lokasi Riil)")
        fig_map = px.scatter_mapbox(
            df_f, lat="lat", lon="lon", size="ats_disabilitas",
            color="ats_disabilitas", color_continuous_scale="Reds",
            size_max=20, zoom=7, mapbox_style="open-street-map"
        )
        # Menambahkan layer citra satelit berwarna
        fig_map.update_layout(
            mapbox_layers=[{
                "below": 'traces', "sourcetype": "raster",
                "source": ["https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"]
            }],
            margin={"r":0,"t":0,"l":0,"b":0}, height=500
        )
        st.plotly_chart(fig_map, use_container_width=True)

    with cv2:
        st.subheader("📊 Grafik ATS")
        fig_bar = px.bar(df_f.sort_values("ats_disabilitas", ascending=False).head(10), 
                         x='ats_disabilitas', y='kab_kota', orientation='h', color_discrete_sequence=['#0d47a1'])
        fig_bar.update_layout(height=400, margin=dict(l=0, r=0, t=0, b=0))
        st.plotly_chart(fig_bar, use_container_width=True)

    # 3. DAFTAR SEKOLAH (BALON STATUS)
    if kab_pilih != "Semua":
        st.divider()
        st.subheader(f"🏫 Satuan Pendidikan di {kab_pilih}")
        sch_wil = data_sekolah[data_sekolah['kab_kota'] == kab_pilih]
        cols = st.columns(3)
        for i, row in enumerate(sch_wil.itertuples()):
            with cols[i % 3]:
                with st.container(border=True):
                    if row.rusak_berat > 0: st.markdown(f"<div class='status-balon mendesak'>⚠️ RUSAK BERAT: {row.rusak_berat} RUANG</div>", unsafe_allow_html=True)
                    else: st.markdown("<div class='status-balon aman'>✅ KONDISI STABIL</div>", unsafe_allow_html=True)
                    
                    if st.button(row.nama_sekolah.upper(), key=f"btn_{row.npsn}"):
                        st.session_state.selected_school_data = row._asdict()
                        st.session_state.page_view = "detail"
                        st.rerun()
                    st.caption(f"🆔 NPSN: {row.npsn}")

    # 4. TABEL BERWARNA
    st.divider()
    with st.expander("📋 Tabel Detail Data"):
        st.dataframe(
            df_f[['kab_kota', 'jumlah_penduduk', 'jumlah_siswa', 'ats_disabilitas']]
            .style.set_table_styles([{'selector': 'th', 'props': [('background-color', '#0d47a1'), ('color', 'white')]}])
            .set_properties(**{'background-color': '#ffffff', 'color': '#1e293b'}),
            use_container_width=True
        )

else:
    # --- HALAMAN DETAIL ---
    sch = st.session_state.selected_school_data
    if st.button("⬅️ Kembali ke Dashboard"):
        st.session_state.page_view = "dashboard"
        st.rerun()
    st.markdown(f"<h1 style='color:#0d47a1;'>🏫 {sch['nama_sekolah'].upper()}</h1>")
    st.divider()
    c1, c2 = st.columns(2)
    with c1:
        with st.container(border=True):
            st.subheader("📌 Profil")
            st.write(f"**Jumlah Siswa:** {sch.get('jumlah_siswa', '0')} Orang")
            st.write(f"**Internet:** {sch.get('akses_internet', '-')}")
    with c2:
        with st.container(border=True):
            st.subheader("🏗️ Sarana")
            st.write(f"**Rusak Berat:** {sch['rusak_berat']} Ruang")
            st.write(f"**Listrik:** {sch.get('daya_listrik', '-')}")
