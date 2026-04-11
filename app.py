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
# Bagian 1: CSS CUSTOM (HIJAU MUDA INSIGHT)
# ==================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
    html, body, [data-testid="stWidgetLabel"] { font-family: 'Inter', sans-serif !important; }

    .block-container { padding-top: 0rem !important; padding-left: 1rem !important; padding-right: 1rem !important; }
    [data-testid="stHeader"] { display: none !important; }

    .top-gradient-bar {
        position: fixed; top: 0; left: 0; width: 100%; height: 10px;
        background: linear-gradient(90deg, #ff8a00, #e52e71, #9c27b0, #1e88e5, #4caf50, #ffeb3b);
        z-index: 999999;
    }

    /* SIDEBAR STYLING */
    [data-testid="stSidebar"] { background: linear-gradient(180deg, #1e88e5 0%, #0d47a1 100%) !important; }
    [data-testid="stSidebar"] * { color: white !important; }
    div[data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] div { color: black !important; }
    div[data-baseweb="popover"] li { color: black !important; }

    /* TILES METRIC */
    .metric-tile { padding: 20px; border-radius: 12px; color: white; margin-bottom: 15px; display: flex; align-items: center; gap: 15px; }
    .tile-orange { background: linear-gradient(135deg, #ff9800 0%, #f57c00 100%); }
    .tile-blue-light { background: linear-gradient(135deg, #03a9f4 0%, #0288d1 100%); }
    .tile-red-dark { background: linear-gradient(135deg, #ff4b2b 0%, #ff416c 100%); }
    .tile-green-light { background: linear-gradient(135deg, #4caf50 0%, #2e7d32 100%); }
    
    /* KOTAK INSIGHT (HIJAU MUDA) */
    .insight-box { 
        background-color: #e8f5e9 !important; 
        border-radius: 10px; 
        padding: 15px; 
        margin-top: 15px; 
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    .insight-title { font-weight: 800; font-size: 14px; text-transform: uppercase; margin-bottom: 5px; }
    .insight-text { color: #333 !important; font-size: 13px; line-height: 1.5; }

    .source-box-ui { background-color: #fff3e0 !important; padding: 8px 12px; border-radius: 8px; border-left: 5px solid #ff9800; margin-bottom: 0px; }
</style>
""", unsafe_allow_html=True)

def draw_tile_svg(label, value, svg_icon, style_class):
    st.markdown(f'<div class="metric-tile {style_class}"><div style="width:42px;height:42px;fill:white;">{svg_icon}</div><div><div style="font-size:14px;font-weight:800;text-transform:uppercase;">{label}</div><div style="font-size:22px;font-weight:800;">{value}</div></div></div>', unsafe_allow_html=True)

svg_people = '<svg viewBox="0 0 16 16"><path d="M7 14s-1 0-1-1 1-4 5-4 5 3 5 4-1 1-1 1H7zm4-6a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm-5.784 6A2.238 2.238 0 0 1 5 13c0-1.355.68-2.75 1.936-3.72A6.325 6.325 0 0 0 5 9c-4 0-5 3-5 4s1 1 1 1h4.216zM4.5 8a2.5 2.5 0 1 0 0-5 2.5 2.5 0 0 0 0 5z"/></svg>'
svg_cap = '<svg viewBox="0 0 16 16"><path d="M8.211 2.047a.5.5 0 0 0-.422 0l-7.5 3.5a.5.5 0 0 0 .025.917l7.5 3 7.5-3a.5.5 0 0 0 .025-.917l-7.5-3.5Z"/><path d="M4.176 9.032a.5.5 0 0 0-.656.327l-.5 1.7a.5.5 0 0 0 .254.539l1.5.75A.5.5 0 0 0 5.25 12h5.5a.5.5 0 0 0 .476-.346l.5-1.7a.5.5 0 0 0-.656-.327L10 10.25l-.117-.043-4 .876L4.176 9.032Z"/></svg>'
svg_warning = '<svg viewBox="0 0 16 16"><path d="M8.982 1.566a1.13 1.13 0 0 0-1.96 0L.165 13.233c-.457.778.091 1.767.98 1.767h13.713c.889 0 1.438-.99.98-1.767L8.982 1.566zM8 5c.535 0 .954.462.9.995l-.35 3.507a.552.552 0 0 1-1.1 0L7.1 5.995A.905.905 0 0 1 8 5zm.002 6a1 1 0 1 1 0 2 1 1 0 0 1 0-2z"/></svg>'
svg_chart = '<svg viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M18 20V10M12 20V4M6 20v-6"/></svg>'

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

# =========================
# Bagian 3: LOGIN
# =========================
if not st.session_state.login:
    _, col_card, _ = st.columns([1.5, 2, 1.5])
    with col_card:
        with st.container(border=True):
            st.markdown("<h3 style='color:#0d47a1; text-align:center;'>LOGIN USER</h3>", unsafe_allow_html=True)
            u = st.text_input("Username", placeholder="Username")
            p = st.text_input("Password", type="password", placeholder="Password")
            if st.button("MASUK KE DASHBOARD", use_container_width=True):
                if u == "admin" and p == "admin": 
                    st.session_state.login = True
                    st.rerun()
                else: st.error("Login Gagal")
    st.stop()

# ==================================
# Bagian 4: SIDEBAR
# ==================================
with st.sidebar:
    logo_b64 = get_base64_image("logo_sumut.png")
    if logo_b64:
        st.markdown(f'<div style="display:flex;align-items:center;gap:12px;padding-bottom:15px;"><img src="data:image/png;base64,{logo_b64}" width="80"><span style="font-size:20px;font-weight:800;color:white;">SI-PANDAI SUMUT</span></div>', unsafe_allow_html=True)
    
    if st.button("👤 Role: Admin", key="role_admin_btn", use_container_width=True):
        st.session_state.page_view = "admin_profile"; st.rerun()
    st.divider()

    st.header("⊞ Menu Utama")
    # PERBAIKAN: Gunakan radio tanpa key duplikat
    nav = st.radio("Navigasi:", ["🚀 Dashboard Utama", "🎓 Pendidikan Khusus", "ℹ️ Tentang Dashboard"], label_visibility="collapsed")
    if "Dashboard" in nav: st.session_state.page_view = "dashboard"
    elif "Pendidikan" in nav: st.session_state.page_view = "tentang_pk"
    else: st.session_state.page_view = "tentang_dashboard"

    st.divider()
    st.header("🔎 Filter Wilayah")
    col_kab = "kab_kota" if "kab_kota" in data_wilayah.columns else data_wilayah.columns[0]
    opsi = ["Semua"] + sorted(data_wilayah[col_kab].unique().tolist()) if not data_wilayah.empty else ["Semua"]
    kab_pilih = st.selectbox("Kabupaten / Kota", opsi, key="selected_kab", label_visibility="collapsed")

    st.divider()
    if st.button("Logout ⏻", use_container_width=True): proses_logout()

# ==================================
# Bagian 5: HEADER & DASHBOARD
# ==================================
st.markdown('<div class="top-gradient-bar"></div>', unsafe_allow_html=True)
st.markdown("""<div class="header-balloon-card"><h2 style='color: #0d47a1; font-weight:800; margin: 0; font-size: 2rem;'>DASHBOARD SI-PANDAI SUMUT</h2><p style='color: #1565c0; font-size: 14px; font-weight: 700; margin: 0;'>Sistem Informasi Pemetaan Anak Tidak Sekolah Disabilitas Sumatera Utara</p></div>""", unsafe_allow_html=True)

if st.session_state.page_view == "dashboard":
    st.markdown('<p style="font-size:26px; font-weight:800; color:#0d47a1;">Matriks Capaian Sektoral</p>', unsafe_allow_html=True)
    st.markdown("""<div class="source-box-ui"><p style="font-size: 12px; color: #e65100; margin: 0; font-weight: 700;"><b>ℹ️ Sumber Data:</b> Bidang PK, LPPD Disdik & TIKP Provsu 2025</p></div>""", unsafe_allow_html=True)
    st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)

    df_f = data_wilayah.copy()
    if kab_pilih != "Semua": df_f = df_f[df_f[col_kab] == kab_pilih]

    # Hitung Matriks
    v_p = int(df_f.iloc[:,1].sum()) if not df_f.empty else 0
    v_s = int(df_f.iloc[:,2].sum()) if not df_f.empty else 0
    v_a = int(df_f.iloc[:,3].sum()) if not df_f.empty else 0
    v_aps = f"{(v_s / v_p * 100):.2f}%" if v_p > 0 else "0%"
    
    m1, m2, m3, m4 = st.columns(4)
    with m1: draw_tile_svg("Penduduk Disabilitas", f"{v_p:,}", svg_people, "tile-orange")
    with m2: draw_tile_svg("Siswa Belajar", f"{v_s:,}", svg_cap, "tile-blue-light")
    with m3: draw_tile_svg("Anak Tidak Sekolah", f"{v_a:,}", svg_warning, "tile-red-dark")
    with m4: draw_tile_svg("Angka Partisipasi", v_aps, svg_chart, "tile-green-light")

    st.divider()
    cv1, cv2 = st.columns([1.5, 1])

    with cv1:
        st.subheader("🗺️ Peta Sebaran ATS (Warna-Warni)")
        if not df_f.empty:
            ats_col = df_f.columns[3]
            fig_map = px.scatter_mapbox(
                df_f, lat="lat", lon="lon", size=ats_col, color=ats_col,
                color_continuous_scale="RdYlGn_r", hover_name=col_kab, 
                hover_data={ats_col: True, "lat": False, "lon": False},
                zoom=7, height=450
            )
            fig_map.update_layout(mapbox_style="open-street-map", margin={"r":0,"t":0,"l":0,"b":0}, coloraxis_showscale=False)
            st.plotly_chart(fig_map, use_container_width=True)
            
            # --- LEGENDA CUSTOM DI BAWAH KIRI PETA ---
            st.markdown("""
                <div style="display: flex; gap: 15px; margin-top: -50px; margin-left: 10px; position: relative; z-index: 999; background: rgba(255,255,255,0.9); padding: 8px 12px; border-radius: 8px; width: fit-content; border: 1px solid #ddd;">
                    <div style="display: flex; align-items: center; gap: 6px;"><div style="width: 12px; height: 12px; background-color: #1a9641; border-radius: 50%;"></div><span style="font-size: 11px; font-weight: 800; color: #333;">RENDAH</span></div>
                    <div style="display: flex; align-items: center; gap: 6px;"><div style="width: 12px; height: 12px; background-color: #ffffbf; border-radius: 50%; border: 1px solid #ccc;"></div><span style="font-size: 11px; font-weight: 800; color: #333;">SEDANG</span></div>
                    <div style="display: flex; align-items: center; gap: 6px;"><div style="width: 12px; height: 12px; background-color: #d7191c; border-radius: 50%;"></div><span style="font-size: 11px; font-weight: 800; color: #333;">TINGGI</span></div>
                </div>
                <div style="margin-bottom: 20px;"></div>
            """, unsafe_allow_html=True)

    with cv2:
        st.subheader("📊 5 Peringkat ATS Tertinggi")
        if not df_f.empty:
            df_top5 = df_f.sort_values(by=ats_col, ascending=False).head(5)
            custom_colors = ['#800000', '#008000', '#FF8C00', '#00008B', '#ADD8E6']
            fig_bar = px.bar(df_top5, x=ats_col, y=col_kab, orientation='h', color=col_kab, color_discrete_sequence=custom_colors, text=ats_col)
            fig_bar.update_layout(height=300, margin=dict(l=10, r=50, t=30, b=10), bargap=0.4, xaxis_title=None, yaxis_title=None, showlegend=False, plot_bgcolor='rgba(0,0,0,0)')
            fig_bar.update_traces(textposition='outside')
            st.plotly_chart(fig_bar, use_container_width=True)
            
            # INSIGHT DINAMIS
            jml_sekolah = len(data_sekolah[data_sekolah[col_kab] == kab_pilih]) if kab_pilih != "Semua" else len(data_sekolah)
            if kab_pilih != "Semua" and v_a > 0 and jml_sekolah == 0:
                p_insight, p_tindakan, warna_aksen = f"🚨 <b>PERINGATAN KRITIS:</b> Di <b>{kab_pilih}</b> terdapat <b>{v_a:,}</b> ATS, namun <b>BELUM ADA</b> SLB.", "Mendesak untuk pembukaan Unit Sekolah Baru.", "#b71c1c"
            elif v_a == 0:
                p_insight, p_tindakan, warna_aksen = f"✅ <b>{kab_pilih}</b> saat ini bersih dari Anak Tidak Sekolah (ATS).", "Pertahankan status ini dengan deteksi dini.", "#2e7d32"
            elif v_a > 100:
                p_insight, p_tindakan, warna_aksen = f"⚠️ Jumlah ATS di <b>{kab_pilih}</b> sangat tinggi (<b>{v_a:,}</b> jiwa).", "Segera lakukan validasi lapangan.", "#ef4444"
            else:
                p_insight, p_tindakan, warna_aksen = f"💡 Wilayah <b>{kab_pilih}</b> memiliki <b>{v_a:,}</b> ATS.", "Optimalkan sekolah terdekat.", "#0d47a1"

            st.markdown(f"""
                <div class="insight-box" style="border-left: 6px solid {warna_aksen};">
                    <div class="insight-title" style="color: {warna_aksen};">💡 Insight & Rekomendasi: {kab_pilih}</div>
                    <p class="insight-text">{p_insight}</p>
                    <hr style="margin: 8px 0; border: 0; border-top: 1px solid {warna_aksen}; opacity: 0.2;">
                    <p class="insight-text" style="font-size: 12px; font-weight: 700; color: {warna_aksen};"><b>Tindakan:</b> {p_tindakan}</p>
                </div>
            """, unsafe_allow_html=True)

    st.divider()
    with st.expander("📋 Lihat & Download Data Tabel"):
        st.dataframe(df_f, use_container_width=True)
        csv = df_f.to_csv(index=False).encode('utf-8')
        st.download_button("Download CSV 📥", csv, file_name=f'data_ats_{kab_pilih}.csv', mime='text/csv')

elif st.session_state.page_view == "admin_profile":
    st.markdown("### 👤 Profil Administrator")
    if st.button("⬅️ Kembali ke Dashboard"): st.session_state.page_view = "dashboard"; st.rerun()
