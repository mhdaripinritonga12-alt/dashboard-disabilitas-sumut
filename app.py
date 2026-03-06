import streamlit as st
from PIL import Image
import pandas as pd

st.set_page_config(
    page_title="SI-PANDAI Dashboard",
    layout="wide"
)

# ===============================
# BACKGROUND STYLE
# ===============================
page_bg = """
<style>

[data-testid="stAppViewContainer"]{
background: linear-gradient(135deg,#0f2027,#203a43,#2c5364);
background-size: cover;
}

.login-box{
background: rgba(255,255,255,0.08);
backdrop-filter: blur(12px);
padding:40px;
border-radius:20px;
text-align:center;
box-shadow:0px 10px 30px rgba(0,0,0,0.4);
}

.title{
color:white;
font-size:38px;
font-weight:700;
}

.subtitle{
color:#dddddd;
font-size:18px;
margin-bottom:20px;
}

.center{
display:flex;
justify-content:center;
}

</style>
"""

st.markdown(page_bg, unsafe_allow_html=True)

# ===============================
# SESSION LOGIN
# ===============================
if "login" not in st.session_state:
    st.session_state.login = False


# ===============================
# HALAMAN LOGIN
# ===============================
if st.session_state.login == False:

    col1, col2, col3 = st.columns([1,2,1])

    with col2:

        st.markdown('<div class="login-box">', unsafe_allow_html=True)

        logo = Image.open("logo_sipandai.png")
        st.image(logo, width=180)

        st.markdown('<div class="title">SI-PANDAI</div>', unsafe_allow_html=True)
        st.markdown('<div class="subtitle">Sistem Informasi Penyandang Disabilitas</div>', unsafe_allow_html=True)

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):

            if username == "admin" and password == "12345":
                st.session_state.login = True
                st.rerun()
            else:
                st.error("Username atau password salah")

        st.markdown('</div>', unsafe_allow_html=True)



# ===============================
# DASHBOARD
# ===============================
else:

    logo_sumut = Image.open("LOGO PEMPROV SUMUT WARNA.png")

    col1,col2 = st.columns([1,8])

    with col1:
        st.image(logo_sumut, width=80)

    with col2:
        st.title("Dashboard Disabilitas Sumatera Utara")
        st.write("Pemerintah Provinsi Sumatera Utara")

    st.divider()

    # LOAD DATA
    df = pd.read_csv("KOTA_MEDAN_LENGKAP_KELURAHAN.csv")

    st.subheader("Data Penyandang Disabilitas")

    st.dataframe(df, use_container_width=True)

    st.subheader("Statistik")

    col1,col2,col3 = st.columns(3)

    with col1:
        st.metric("Total Data", len(df))

    with col2:
        st.metric("Jumlah Kolom", len(df.columns))

    with col3:
        st.metric("Jumlah Kecamatan", df["kecamatan"].nunique())

    st.subheader("Visualisasi")

    if "jenis_disabilitas" in df.columns:
        chart = df["jenis_disabilitas"].value_counts()
        st.bar_chart(chart)

    st.sidebar.title("Menu")

    if st.sidebar.button("Logout"):
        st.session_state.login = False
        st.rerun()
