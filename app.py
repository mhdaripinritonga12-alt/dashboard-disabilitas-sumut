import pydeck as pdk
import streamlit as st
import pandas as pd
import plotly.express as px
import os
import base64
import streamlit.components.v1 as components

# ==================================
# CONFIG
# ==================================
st.set_page_config(
    page_title="SI-PANDAI SUMUT",
    layout="wide",
    page_icon="🔒",
    initial_sidebar_state="expanded"
)

# STATE
if "login" not in st.session_state: st.session_state.login = False
if "page_view" not in st.session_state: st.session_state.page_view = "dashboard"
if "selected_kab" not in st.session_state: st.session_state.selected_kab = "Semua"
if "selected_school_data" not in st.session_state: st.session_state.selected_school_data = None

def proses_logout():
    st.session_state.selected_kab = "Semua"
    st.session_state.login = False
    st.session_state.page_view = "dashboard"

def get_base64_image(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

# ==================================
# CSS
# ==================================
st.markdown("""
<style>
[data-testid="stSidebar"] {background: linear-gradient(180deg,#0d47a1,#1565c0);}
.metric {padding:15px;border-radius:12px;color:white;margin-bottom:10px;}
.orange{background:#f57c00;}
.blue{background:#0288d1;}
.red{background:#303f9f;}
.green{background:#2e7d32;}
</style>
""", unsafe_allow_html=True)

def tile(label, val, cls):
    st.markdown(f"<div class='metric {cls}'><b>{label}</b><br><h3>{val}</h3></div>", unsafe_allow_html=True)

# ==================================
# LOAD DATA
# ==================================
@st.cache_data
def load():
    try:
        df1 = pd.read_csv("master_data_si_pandai.csv")
        df2 = pd.read_csv("master_data_sekolah1.csv")
        df1.columns = df1.columns.str.lower()
        df2.columns = df2.columns.str.lower()
        return df1, df2
    except:
        return pd.DataFrame(), pd.DataFrame()

data_wilayah, data_sekolah = load()

# ==================================
# LOGIN
# ==================================
if not st.session_state.login:
    st.title("LOGIN")
    u = st.text_input("Username")
    p = st.text_input("Password", type="password")
    if st.button("Login"):
        if u == "admin" and p == "admin":
            st.session_state.login = True
            st.rerun()
        else:
            st.error("Salah")
    st.stop()

# ==================================
# SIDEBAR
# ==================================
st.sidebar.title("SI-PANDAI SUMUT")
st.sidebar.write("ADMIN")

col_kab = "kab_kota"
opsi = ["Semua"] + list(data_wilayah[col_kab].unique()) if not data_wilayah.empty else ["Semua"]
kab = st.sidebar.selectbox("Kabupaten", opsi)

st.sidebar.button("Logout", on_click=proses_logout)

# ==================================
# DASHBOARD
# ==================================
df_f = data_wilayah.copy()
if kab != "Semua":
    df_f = df_f[df_f[col_kab] == kab]

st.title("Dashboard")

# KPI
c1,c2,c3,c4 = st.columns(4)
val_p = int(df_f.iloc[:,1].sum()) if not df_f.empty else 0
val_s = int(df_f.iloc[:,2].sum()) if not df_f.empty else 0
val_a = int(df_f.iloc[:,3].sum()) if not df_f.empty else 0
val_APS = (val_s/val_p*100) if val_p>0 else 0

with c1: tile("Disabilitas", val_p,"orange")
with c2: tile("Siswa", val_s,"blue")
with c3: tile("ATS", val_a,"red")
with c4: tile("APS", f"{val_APS:.2f}%","green")

# ==================================
# INSIGHT
# ==================================
if not df_f.empty:
    col_ats = df_f.columns[3]
    top = df_f.loc[df_f[col_ats].idxmax(), col_kab]
    st.info(f"Wilayah tertinggi ATS: {top}")

# ==================================
# PETA + GRAFIK
# ==================================
cv1,cv2 = st.columns(2)

with cv1:
    st.subheader("Peta")
    if not df_f.empty:
        try:
            layer = pdk.Layer(
                "ScatterplotLayer",
                data=df_f,
                get_position='[lon, lat]',
                get_radius=5000,
                get_fill_color='[200,0,0,160]'
            )
            st.pydeck_chart(pdk.Deck(layers=[layer]))
        except:
            st.map(df_f)

with cv2:
    st.subheader("Grafik")
    if not df_f.empty:
        col_ats = df_f.columns[3]
        df_top = df_f.sort_values(by=col_ats, ascending=False).head(10)

        fig = px.bar(df_top, x=col_ats, y=col_kab, orientation='h')
        st.plotly_chart(fig, use_container_width=True)

# ==================================
# SEKOLAH
# ==================================
if kab != "Semua":
    st.subheader("Sekolah")
    df_s = data_sekolah[data_sekolah[col_kab]==kab]
    for i,row in df_s.iterrows():
        if st.button(row["nama_sekolah"], key=i):
            st.session_state.selected_school_data = row
            st.session_state.page_view="detail"
            st.rerun()

# ==================================
# DETAIL
# ==================================
if st.session_state.page_view=="detail":
    s = st.session_state.selected_school_data
    st.title(s["nama_sekolah"])
    st.write(s)

# ==================================
# KESIMPULAN
# ==================================
st.success("Dashboard siap digunakan untuk pengambilan kebijakan")
