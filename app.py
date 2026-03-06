import streamlit as st
from PIL import Image
import pandas as pd

st.set_page_config(
    page_title="SI-PANDAI",
    layout="wide"
)

# ==============================
# STYLE LOGIN
# ==============================
st.markdown("""
<style>

[data-testid="stAppViewContainer"]{
background-color:white;
}

.login-box{
width:350px;
margin:auto;
padding:30px;
border-radius:10px;
border:1px solid #e0e0e0;
box-shadow:0px 4px 15px rgba(0,0,0,0.1);
text-align:center;
background:white;
}

.title{
font-size:28px;
font-weight:700;
margin-top:10px;
}

.subtitle{
font-size:16px;
color:gray;
margin-bottom:20px;
}

</style>
""", unsafe_allow_html=True)


# ==============================
# SESSION LOGIN
# ==============================
if "login" not in st.session_state:
    st.session_state.login = False


# ==============================
# HALAMAN LOGIN
# ==============================
if st.session_state.login == False:

    st.write("")
    st.write("")
    st.write("")
    st.write("")

    col1, col2, col3 = st.columns([2,1,2])

    with col2:

        st.markdown('<div class="login-box">', unsafe_allow_html=True)

        logo = Image.open("logo_sipandai.png")
        st.image(logo, width=120)

        st.markdown('<div class="title">SI-PANDAI</div>', unsafe_allow_html=True)
        st.markdown('<div class="subtitle">Sistem Informasi Penyandang Disabilitas</div>', unsafe_allow_html=True)

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login", use_container_width=True):

            if username == "admin" and password == "12345":
                st.session_state.login = True
                st.rerun()
            else:
                st.error("Username atau Password salah")

        st.markdown('</div>', unsafe_allow_html=True)


# ==============================
# DASHBOARD
# ==============================
else:

    col1,col2 = st.columns([1,8])

    with col1:
        logo = Image.open("LOGO PEMPROV SUMUT WARNA.png")
        st.image(logo, width=80)

    with col2:
        st.title("Dashboard SI-PANDAI")
        st.write("Pemerintah Provinsi Sumatera Utara")

    st.divider()

    df = pd.read_csv("KOTA_MEDAN_LENGKAP_KELURAHAN.csv")

    st.subheader("Data Penyandang Disabilitas")
    st.dataframe(df, use_container_width=True)

    col1,col2,col3 = st.columns(3)

    with col1:
        st.metric("Total Data", len(df))

    with col2:
        st.metric("Jumlah Kolom", len(df.columns))

    with col3:
        st.metric("Jumlah Kecamatan", df.iloc[:,0].nunique())

    st.sidebar.title("Menu")

    if st.sidebar.button("Logout"):
        st.session_state.login = False
        st.rerun()
