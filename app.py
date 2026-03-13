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

# --- INISIALISASI STATE (FIXED) ---
if "login" not in st.session_state: st.session_state.login = False
if "page_view" not in st.session_state: st.session_state.page_view = "dashboard"
if "selected_kab" not in st.session_state: st.session_state.selected_kab = "Semua"
if "selected_school_data" not in st.session_state: st.session_state.selected_school_data = None

def proses_logout():
    st.session_state.selected_kab = "Semua"
    st.session_state.login = False
    st.session_state.page_view = "dashboard"

# ==================================
# 1. CSS CUSTOM (UI LOCKED)
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

# ==================================
# 3. LOGIN PAGE
# ==================================
if not st.session_state.login:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    _, col_card, _ = st.columns([1.5, 2, 1.5])
    with col_card:
        with st.container(border=True):
            st.markdown("<h3 style='text-align:center; color:#0d47a1;'>LOGIN SI-PANDAI</h3>", unsafe_allow_html=True)
            u = st.text_input("Username", placeholder="admin")
            p = st.text_input("Password", type="password", placeholder="admin")
            if st.button("MASUK KE DASHBOARD"):
                if u == "admin" and p == "admin": 
                    st.session_state.login = True
                    st.rerun()
                else: st.error("Login Gagal")
    st.stop()

# ==================================
# 4. SIDEBAR (FILTER)
# ==================================
st.sidebar.markdown('<p style="font-size: 20px; font-weight: 800; color: white;">SI-PANDAI SUMUT</p>', unsafe_allow_html=True)
st.sidebar.divider()
kab_col = "kab_kota"
if not data_wilayah.empty:
    opsi = ["Semua"] + sorted(data_wilayah[kab_col].unique().tolist())
    kab_pilih = st.sidebar.selectbox("Pilih Kabupaten / Kota", opsi, key="selected_kab")
    st.sidebar.button("Logout 🚪", use_container_width=True, on_click=proses_logout)

# ==================================
# 5. DASHBOARD UTAMA
# ==================================
if st.session_state.page_view == "dashboard":
    st.markdown(f'<p style="font-size:26px; font-weight:800; color:#0d47a1;">🚀 Dashboard Utama - {kab_pilih}</p>', unsafe_allow_html=True)
    
    df_f = data_wilayah.copy()
    if kab_pilih != "Semua":
        df_f = df_f[df_f[kab_col] == kab_pilih]

    # Matriks Capaian
    m1, m2, m3, m4 = st.columns(4)
    with m1: st.metric("Disabilitas", f"{int(df_f.iloc[:,1].sum()):,}")
    with m2: st.metric("Siswa Belajar", f"{int(df_f.iloc[:,2].sum()):,}")
    with m3: st.metric("ATS", f"{int(df_f.iloc[:,3].sum()):,}")
    with m4:
        val_aps = (int(df_f.iloc[:,2].sum()) / int(df_f.iloc[:,1].sum()) * 100) if not df_f.empty and int(df_f.iloc[:,1].sum()) > 0 else 0
        st.metric("Angka Partisipasi", f"{val_aps:.2f}%")

    st.divider()
    cv1, cv2 = st.columns([1.8, 1])
    
    with cv1:
        # --- PETA SEBARAN SEKOLAH (MULTI-DOT) ---
        st.subheader(f"🗺️ Sebaran Sekolah di {kab_pilih}")
        df_map = data_sekolah.copy()
        if kab_pilih != "Semua":
            df_map = df_map[df_map[kab_col] == kab_pilih]
        
        if not df_map.empty:
            # Gunakan kolom latitude/longitude dari CSV
            st.map(df_map, latitude="latitude", longitude="longitude", use_container_width=True)
        else:
            st.info("Data titik koordinat belum tersedia.")

    with cv2:
        st.subheader("📊 Statistik Wilayah")
        if not df_f.empty:
            st.plotly_chart(px.bar(df_f.head(10), x=df_f.columns[3], y=kab_col, orientation='h', color_discrete_sequence=['#0d47a1']), use_container_width=True)

    # Unit Pendidikan
    if kab_pilih != "Semua":
        st.subheader(f"🏫 Daftar Unit Pendidikan")
        sch_wil = data_sekolah[data_sekolah[kab_col] == kab_pilih]
        if not sch_wil.empty:
            cols = st.columns(3)
            for i, row in enumerate(sch_wil.itertuples()):
                with cols[i % 3]:
                    with st.container(border=True):
                        # Logika Warning Status (Sesuai Urutan Mendesak)
                        if getattr(row, 'jumlah_rombel', 0) > getattr(row, 'jumlah_ruang_kelas', 0):
                            st.markdown("<div class='rec-box mendesak'>⚠️ MENDESAK: Butuh RKB</div>", unsafe_allow_html=True)
                        elif getattr(row, 'rusak_berat', 0) > 0:
                            st.markdown("<div class='rec-box rehab'>🛠️ PRIORITAS REHAB</div>", unsafe_allow_html=True)
                        elif getattr(row, 'rusak_sedang', 0) > 0:
                            st.markdown("<div class='rec-box rehab' style='background-color:#fff7ed; color:#c2410c;'>⚠️ REHAB SEDANG</div>", unsafe_allow_html=True)
                        else:
                            st.markdown("<div class='rec-box aman'>✅ KONDISI STABIL</div>", unsafe_allow_html=True)
                        
                        # Simpan ke State saat diklik
                        if st.button(getattr(row, 'nama_sekolah', 'SEKOLAH').upper(), key=f"btn_{i}"):
                            st.session_state.selected_school_data = row._asdict()
                            st.session_state.page_view = "detail"
                            st.rerun()
                        st.caption(f"NPSN: {getattr(row, 'npsn', '-')}")

# ==================================
# 6. HALAMAN DETAIL (STREET VIEW EMBED)
# ==================================
else:
    sch = st.session_state.selected_school_data
    if st.button("⬅️ Kembali ke Dashboard"):
        st.session_state.page_view = "dashboard"
        st.rerun()
    
    st.markdown(f"<h1 style='color:#0d47a1; margin-bottom:0;'>🏫 {sch['nama_sekolah'].upper()}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='color:#546e7a;'>Wilayah: <b>{sch['kab_kota']}</b> | NPSN: <b>{sch['npsn']}</b></p>", unsafe_allow_html=True)
    
    # Street View Style Embed
    q = f"{sch['nama_sekolah'].replace(' ', '+')}+{sch['kab_kota'].replace(' ', '+')}"
    components.html(f'<iframe width="100%" height="350" frameborder="0" src="https://www.google.com/maps?q={q}&output=embed" style="border-radius:15px; border:1px solid #ddd;"></iframe>', height=370)
    
    st.divider()
    c1, c2 = st.columns(2)
    with c1:
        with st.container(border=True):
            st.subheader("📌 Profil Sekolah")
            st.write(f"**Alamat:** {sch.get('alamat', '-')}")
            st.write(f"**Siswa:** {sch.get('jumlah_siswa', 0)} Orang")
            st.write(f"**Internet:** {sch.get('akses_internet', '-')}")
    with c2:
        with st.container(border=True):
            st.subheader("🏗️ Sarana Prasarana")
            st.write(f"**Rombel:** {sch.get('jumlah_rombel', 0)} | **Kelas:** {sch.get('jumlah_ruang_kelas', 0)}")
            st.write(f"**Rusak Sedang:** {sch.get('rusak_sedang', 0)} Ruang")
            st.write(f"**Rusak Berat:** {sch.get('rusak_berat', 0)} Ruang")
            st.write(f"**Listrik:** {sch.get('daya_listrik', '-')}")
