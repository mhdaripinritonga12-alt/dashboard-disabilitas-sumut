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

def proses_logout():
    st.session_state.selected_kab = "Semua"
    st.session_state.login = False
    st.session_state.page_view = "dashboard"

if "page_view" not in st.session_state:
    st.session_state.page_view = "dashboard"
if "selected_school_data" not in st.session_state:
    st.session_state.selected_school_data = None
if "selected_kab" not in st.session_state:
    st.session_state.selected_kab = "Semua"

def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

# ==================================
# Bagian 1: CSS
# ==================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&display=swap');
    html, body { font-family: 'Inter', sans-serif !important; }
    [data-testid="stAppViewContainer"] { background-color: #f4f7f9 !important; }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d47a1 0%, #1565c0 100%) !important;
    }
    [data-testid="stSidebar"] * { color: white !important; }

    .source-box-ui {
        background-color: #e3f2fd;
        padding: 15px;
        border-radius: 10px;
        border-left: 6px solid #0d47a1;
        margin-bottom: 25px;
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
        return df_ats, df_sch
    except:
        return pd.DataFrame(), pd.DataFrame()

data_wilayah, data_sekolah = load_all_data()

# =========================
# Bagian 3: LOGIN
# =========================
if "login" not in st.session_state:
    st.session_state.login = False

if not st.session_state.login:

    _, col_logo, _ = st.columns([2,0.6,2])
    with col_logo:
        if os.path.exists("logo_sumut.png"):
            st.image("logo_sumut.png", width=100)

    _, col_card, _ = st.columns([1.5,2,1.5])
    with col_card:

        st.markdown("### LOGIN USER")

        u = st.text_input("Username")
        p = st.text_input("Password", type="password")

        if st.button("MASUK KE DASHBOARD"):
            if u=="admin" and p=="admin":
                st.session_state.login=True
                st.rerun()
            else:
                st.error("Login Gagal")

    st.stop()

# ==================================
# SIDEBAR
# ==================================
st.sidebar.write("👤 Role: ADMIN")

opsi_kab = ["Semua"] + sorted(data_wilayah["kab_kota"].unique().tolist())
kab_pilih = st.sidebar.selectbox("Pilih Kabupaten / Kota", opsi_kab)

# ==================================
# DASHBOARD
# ==================================
if st.session_state.page_view == "dashboard":

    st.title("🚀 Dashboard SI-PANDAI SUMUT")
    st.caption("Sistem Informasi Pemetaan ATS Disabilitas")

    df_filter = data_wilayah.copy()

    if kab_pilih != "Semua":
        df_filter = df_filter[df_filter["kab_kota"] == kab_pilih]

# ==================================
# 1. MATRIKS CAPAIAN
# ==================================

    st.subheader("📌 Matriks Capaian Sektoral")

    st.markdown("""
    <div class="source-box-ui">
    ℹ️ Sumber Data: Bidang PK - LPPD & TIKP Provsu 2025
    </div>
    """, unsafe_allow_html=True)

    m1,m2,m3 = st.columns(3)

    if kab_pilih=="Semua":

        m1.metric(
            "👥 Total Penduduk Disabilitas",
            "6.732"
        )

        m2.metric(
            "🎓 Total Siswa Disabilitas",
            "4.573"
        )

        m3.metric(
            "📈 Angka Partisipasi Sekolah",
            "67.93%",
            delta="🎯 Target Sektoral"
        )

    else:

        m1.metric(
            "👥 Penduduk Disabilitas",
            int(df_filter["jumlah_penduduk"].sum())
        )

        m2.metric(
            "🎓 Siswa Belajar",
            int(df_filter["jumlah_siswa"].sum())
        )

        m3.metric(
            "⚠️ Anak Tidak Sekolah (ATS)",
            int(df_filter["ats_disabilitas"].sum()),
            delta_color="inverse"
        )

# ==================================
# 2. VISUALISASI
# ==================================

    st.divider()

    cv1,cv2 = st.columns([1.5,1])

# ==================================
# PETA (lebih hidup)
# ==================================

    with cv1:

        st.subheader("🗺️ Peta Sebaran ATS Disabilitas")
        st.caption("Ukuran dan warna lingkaran menunjukkan jumlah ATS")

        df_filter["map_size"] = df_filter["ats_disabilitas"] * 40
        df_filter["color"] = df_filter["ats_disabilitas"]

        st.map(
            df_filter,
            latitude="lat",
            longitude="lon",
            size="map_size",
            color="color",
            use_container_width=True
        )

# ==================================
# GRAFIK ATS
# ==================================

    with cv2:

        st.subheader("📊 Grafik ATS Wilayah")

        df_chart = df_filter.sort_values("ats_disabilitas",ascending=False).head(10)

        fig = px.bar(
            df_chart,
            x="ats_disabilitas",
            y="kab_kota",
            orientation="h",
            color="ats_disabilitas",
            color_continuous_scale="Blues"
        )

        fig.update_layout(
            height=350,
            margin=dict(l=0,r=0,t=0,b=0)
        )

        st.plotly_chart(fig,use_container_width=True)

# ==================================
# TOP ATS TERTINGGI
# ==================================

        st.markdown("### 🔥 Wilayah ATS Tertinggi")

        top_ats = data_wilayah.sort_values(
            "ats_disabilitas",
            ascending=False
        ).head(5)

        for i,row in enumerate(top_ats.itertuples(),1):

            st.markdown(
                f"""
                <div style="
                background:#ffffff;
                padding:8px 12px;
                border-radius:8px;
                margin-bottom:6px;
                border-left:5px solid #ef4444;">
                <b>{i}. {row.kab_kota}</b> — ATS: <b>{row.ats_disabilitas}</b>
                </div>
                """,
                unsafe_allow_html=True
            )

# ==================================
# TABEL
# ==================================

    st.divider()

    with st.expander("📋 Lihat Detail Tabel"):

        st.dataframe(
            df_filter[[
                "kab_kota",
                "jumlah_penduduk",
                "jumlah_siswa",
                "ats_disabilitas"
            ]],
            use_container_width=True
        )
