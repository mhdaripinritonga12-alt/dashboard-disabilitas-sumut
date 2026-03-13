import streamlit as st
import pandas as pd
import plotly.express as px
import os
import base64
import streamlit.components.v1 as components

# ==================================
# 0. KONFIGURASI HALAMAN
# ==================================
st.set_page_config(
    page_title="SI-PANDAI SUMUT",
    layout="wide",
    page_icon="🔒",
    initial_sidebar_state="expanded"
)

# --- INISIALISASI STATE (WAJIB) ---
if "login" not in st.session_state: st.session_state.login = False
if "page_view" not in st.session_state: st.session_state.page_view = "dashboard"
if "selected_kab" not in st.session_state: st.session_state.selected_kab = "Semua"
if "selected_school_data" not in st.session_state: st.session_state.selected_school_data = None

def proses_logout():
    st.session_state.selected_kab = "Semua"
    st.session_state.login = False
    st.session_state.page_view = "dashboard"

def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

# ==================================
# 1. CSS CUSTOM (FIXED UI)
# ==================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&display=swap');
    html, body, [data-testid="stWidgetLabel"] { font-family: 'Inter', sans-serif !important; }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d47a1 0%, #1565c0 100%) !important;
    }
    [data-testid="stSidebar"] * { color: white !important; }

    div.stButton > button:not([key^="btn_"]) {
        background: linear-gradient(90deg, #1565c0 0%, #1e88e5 100%) !important;
        color: white !important; border-radius: 10px !important; 
        font-weight: 700 !important; height: 48px; width: 100%; border: none;
    }

    .metric-tile {
        padding: 20px; border-radius: 12px; color: white; margin-bottom: 15px;
        display: flex; align-items: center; gap: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .tile-orange { background: linear-gradient(135deg, #ff9800 0%, #f57c00 100%); }
    .tile-blue-light { background: linear-gradient(135deg, #03a9f4 0%, #0288d1 100%); }
    .tile-blue-dark { background: linear-gradient(135deg, #3f51b5 0%, #303f9f 100%); }
    .tile-green-light { background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%); }

    div.stButton > button[key^="btn_"] {
        background: linear-gradient(90deg, #0d47a1 0%, #1976d2 100%) !important;
        color: white !important; border-radius: 20px !important; 
        font-size: 14px !important; font-weight: 700 !important;
        width: 100% !important; border: none !important;
    }

    .rec-box { padding: 8px 12px; border-radius: 8px; font-size: 11px; font-weight: 700; margin-bottom: 12px; }
    .mendesak { background-color: #fee2e2 !important; color: #b91c1c !important; border-left: 5px solid #ef4444 !important; }
    .rehab { background-color: #fef3c7 !important; color: #b45309 !important; border-left: 5px solid #f59e0b !important; }
    .aman { background-color: #dcfce7 !important; color: #15803d !important; border-left: 5px solid #22c55e !important; }
</style>
""", unsafe_allow_html=True)

def draw_tile_svg(label, value, svg_icon, style_class):
    st.markdown(f'<div class="metric-tile {style_class}"><div class="tile-icon-svg">{svg_icon}</div><div><div class="tile-label">{label}</div><div class="tile-value">{value}</div></div></div>', unsafe_allow_html=True)

svg_people = '<svg viewBox="0 0 16 16"><path d="M7 14s-1 0-1-1 1-4 5-4 5 3 5 4-1 1-1 1H7zm4-6a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm-5.784 6A2.238 2.238 0 0 1 5 13c0-1.355.68-2.75 1.936-3.72A6.325 6.325 0 0 0 5 9c-4 0-5 3-5 4s1 1 1 1h4.216zM4.5 8a2.5 2.5 0 1 0 0-5 2.5 2.5 0 0 0 0 5z"/></svg>'
svg_cap = '<svg viewBox="0 0 16 16"><path d="M8.211 2.047a.5.5 0 0 0-.422 0l-7.5 3.5a.5.5 0 0 0 .025.917l7.5 3 7.5-3a.5.5 0 0 0 .025-.917l-7.5-3.5Z"/><path d="M4.176 9.032a.5.5 0 0 0-.656.327l-.5 1.7a.5.5 0 0 0 .254.539l1.5.75A.5.5 0 0 0 5.25 12h5.5a.5.5 0 0 0 .476-.346l.5-1.7a.5.5 0 0 0-.656-.327L10 10.25l-.117-.043-4 .876L4.176 9.032Z"/></svg>'
svg_warning = '<svg viewBox="0 0 16 16"><path d="M8.982 1.566a1.13 1.13 0 0 0-1.96 0L.165 13.233c-.457.778.091 1.767.98 1.767h13.713c.889 0 1.438-.99.98-1.767L8.982 1.566zM8 5c.535 0 .954.462.9.995l-.35 3.507a.552.552 0 0 1-1.1 0L7.1 5.995A.905.905 0 0 1 8 5zm.002 6a1 1 0 1 1 0 2 1 1 0 0 1 0-2z"/></svg>'

# ==================================
# 2. LOAD DATA
# ==================================
@st.cache_data
def load_all_data():
    try:
        df_ats = pd.read_csv("master_data_si_pandai.csv")
        df_sch = pd.read_csv("master_data_sekolah1.csv")
        for df in [df_ats, df_sch]:
            df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
        return df_ats, df_sch
    except: return pd.DataFrame(), pd.DataFrame()

data_wilayah, data_sekolah = load_all_data()

# =========================
# 3. LOGIN PAGE
# =========================
if not st.session_state.login:
    _, col_card, _ = st.columns([1.5, 2, 1.5])
    with col_card:
        with st.container(border=True):
            st.markdown("<h3 style='text-align:center; color:#0d47a1;'>LOGIN SI-PANDAI</h3>", unsafe_allow_html=True)
            u = st.text_input("Username", placeholder="admin")
            p = st.text_input("Password", type="password", placeholder="admin")
            if st.button("MASUK"):
                if u == "admin" and p == "admin": 
                    st.session_state.login = True
                    st.rerun()
                else: st.error("Login Gagal")
    st.stop()

# ==================================
# 4. SIDEBAR
# ==================================
st.sidebar.markdown('<p style="font-size: 20px; font-weight: 800; color: white;">SI-PANDAI SUMUT</p>', unsafe_allow_html=True)
st.sidebar.divider()
target_col = "kab_kota"
opsi = ["Semua"] + sorted(data_wilayah[target_col].unique().tolist()) if not data_wilayah.empty else ["Semua"]
kab_pilih = st.sidebar.selectbox("Pilih Kabupaten / Kota", opsi, key="selected_kab")
st.sidebar.button("Logout 🚪", use_container_width=True, on_click=proses_logout)

# ==================================
# 5. HALAMAN DASHBOARD
# ==================================
if st.session_state.page_view == "dashboard":
    st.markdown(f'<p style="font-size:26px; font-weight:800; color:#0d47a1;">🚀 Dashboard Utama - {kab_pilih}</p>', unsafe_allow_html=True)
    st.divider()

    df_f = data_wilayah.copy()
    if kab_pilih != "Semua": df_f = df_f[df_f[target_col] == kab_pilih]

    # Metrics
    m1, m2, m3, m4 = st.columns(4)
    with m1: draw_tile_svg("Disabilitas", f"{int(df_f.iloc[:,1].sum()):,}", svg_people, "tile-orange")
    with m2: draw_tile_svg("Siswa", f"{int(df_f.iloc[:,2].sum()):,}", svg_cap, "tile-blue-light")
    with m3: draw_tile_svg("ATS", f"{int(df_f.iloc[:,3].sum()):,}", svg_warning, "tile-blue-dark")
    with m4:
        val_aps = (int(df_f.iloc[:,2].sum()) / int(df_f.iloc[:,1].sum()) * 100) if not df_f.empty and int(df_f.iloc[:,1].sum()) > 0 else 0
        draw_tile_svg("Partisipasi", f"{val_aps:.2f}%", svg_cap, "tile-green-light")

    st.divider()
    cv1, cv2 = st.columns([1.8, 1])
    
    with cv1:
        # Peta Multi-Dot Dashboard
        st.subheader(f"🗺️ Sebaran Sekolah di {kab_pilih}")
        df_map = data_sekolah.copy()
        if kab_pilih != "Semua": df_map = df_map[df_map[target_col] == kab_pilih]
        
        if not df_map.empty:
            st.map(df_map, latitude="latitude", longitude="longitude", use_container_width=True)
        else:
            st.info("Data koordinat belum tersedia.")

    with cv2:
        st.subheader("📊 Statistik Wilayah")
        if not df_f.empty:
            st.plotly_chart(px.bar(df_f.head(10), x=df_f.columns[3], y=target_col, orientation='h', color_discrete_sequence=['#0d47a1']), use_container_width=True)

    if kab_pilih != "Semua":
        st.subheader(f"🏫 Unit Pendidikan")
        sch_wil = data_sekolah[data_sekolah[target_col] == kab_pilih]
        if not sch_wil.empty:
            cols = st.columns(3)
            for i, row in enumerate(sch_wil.itertuples()):
                with cols[i % 3]:
                    with st.container(border=True):
                        # Logika Status
                        if getattr(row, 'jumlah_rombel', 0) > getattr(row, 'jumlah_ruang_kelas', 0):
                            st.markdown("<div class='rec-box mendesak'>⚠️ MENDESAK: Butuh RKB</div>", unsafe_allow_html=True)
                        elif getattr(row, 'rusak_berat', 0) > 0:
                            st.markdown("<div class='rec-box rehab'>🛠️ PRIORITAS REHAB</div>", unsafe_allow_html=True)
                        else:
                            st.markdown("<div class='rec-box aman'>✅ KONDISI STABIL</div>", unsafe_allow_html=True)
                        
                        if st.button(getattr(row, 'nama_sekolah', 'SEKOLAH').upper(), key=f"btn_{i}"):
                            st.session_state.selected_school_data = row._asdict()
                            st.session_state.page_view = "detail"
                            st.rerun()
                        st.caption(f"NPSN: {getattr(row, 'npsn', '-')}")

# ==================================
# 6. HALAMAN DETAIL (DENGAN STREET VIEW)
# ==================================
else:
    sch = st.session_state.selected_school_data
    if st.button("⬅️ Kembali ke Dashboard"):
        st.session_state.page_view = "dashboard"
        st.rerun()
    
    st.markdown(f"<h1 style='color:#0d47a1; margin-bottom:0;'>🏫 {sch['nama_sekolah'].upper()}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='color:#546e7a;'>Wilayah: <b>{sch['kab_kota']}</b> | NPSN: <b>{sch['npsn']}</b></p>", unsafe_allow_html=True)
    
    # Street View Style Embed (Hanya di Detail)
    q_map = f"{sch['nama_sekolah'].replace(' ', '+')}+{sch['kab_kota'].replace(' ', '+')}"
    components.html(f'<iframe width="100%" height="350" frameborder="0" src="https://www.google.com/maps?q={q_map}&output=embed" style="border-radius:15px; border:1px solid #ddd;"></iframe>', height=370)
    
    st.divider()
    c1, c2 = st.columns(2)
    with c1:
        with st.container(border=True):
            st.subheader("📌 Profil")
            st.write(f"**Alamat:** {sch.get('alamat', '-')}")
            st.write(f"**Siswa:** {sch.get('jumlah_siswa', 0)} Orang")
    with c2:
        with st.container(border=True):
            st.subheader("🏗️ Sarpras")
            st.write(f"**Rombel:** {sch.get('jumlah_rombel', 0)} | **Kelas:** {sch.get('jumlah_ruang_kelas', 0)}")
            st.write(f"**Rusak Berat:** {sch.get('rusak_berat', 0)} Ruang")

    st.markdown('<div style="background-color:#e3f2fd; padding:15px; border-radius:10px; border-left:6px solid #0d47a1;"><p style="margin:0; color:#0d47a1;"><b>Rekomendasi:</b> Sekolah ini memerlukan perhatian pada digitalisasi & sarpras sesuai data Bidang PK.</p></div>', unsafe_allow_html=True)
