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
    page_title="SI-PANDAI SUMUT | Executive Dashboard",
    layout="wide",
    page_icon="🎓",
    initial_sidebar_state="expanded"
)

# Inisialisasi State (Menjamin fitur tidak hilang)
if "login" not in st.session_state: st.session_state.login = False
if "page_view" not in st.session_state: st.session_state.page_view = "dashboard"
if "selected_kab" not in st.session_state: st.session_state.selected_kab = "Semua"
if "selected_school_data" not in st.session_state: st.session_state.selected_school_data = None

# ==================================
# 1. CSS KORPORAT (UI/UX MODERN)
# ==================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    /* Base Styles */
    html, body, [data-testid="stWidgetLabel"] { font-family: 'Inter', sans-serif !important; }
    .stApp { background-color: #f8fafc; }
    
    /* Tidy Sidebar */
    [data-testid="stSidebar"] {
        background-color: #0f172a !important; /* Navy Dark Corporate */
        border-right: 1px solid #1e293b;
    }
    [data-testid="stSidebar"] * { color: #f1f5f9 !important; }
    [data-testid="stSidebarNav"] { padding-top: 20px; }
    
    /* Sidebar Navigation Buttons */
    .nav-btn {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 12px 16px;
        border-radius: 10px;
        margin-bottom: 8px;
        cursor: pointer;
        transition: 0.3s;
        border: 1px solid transparent;
        background: rgba(255,255,255,0.05);
        color: white;
        text-decoration: none;
        font-weight: 500;
        font-size: 14px;
    }
    .nav-btn:hover { background: rgba(255,255,255,0.1); border-color: #3b82f6; }
    .active-nav { background: #2563eb !important; font-weight: 700; border-color: #60a5fa; }

    /* Top Navigation Bar */
    .stHeader { display: none !important; }
    .header-banner {
        background: white;
        padding: 24px 32px;
        border-radius: 0 0 20px 20px;
        border-bottom: 3px solid #2563eb;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
        margin-bottom: 30px;
    }

    /* Metric Cards */
    .metric-container {
        background: white;
        padding: 24px;
        border-radius: 20px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1);
        display: flex;
        align-items: center;
        gap: 20px;
    }
    .m-icon {
        width: 54px; height: 54px;
        background: #eff6ff;
        border-radius: 14px;
        display: flex; align-items: center; justify-content: center;
        color: #2563eb; font-size: 24px;
    }
    .m-label { font-size: 13px; font-weight: 700; color: #64748b; text-transform: uppercase; letter-spacing: 0.05em; }
    .m-value { font-size: 28px; font-weight: 800; color: #0f172a; margin-top: 2px; }

    /* Professional Elements */
    div[data-testid="stExpander"] { background: white !important; border-radius: 12px !important; border: 1px solid #e2e8f0 !important; }
    .insight-card {
        background: #f0f7ff;
        border-left: 5px solid #2563eb;
        padding: 20px;
        border-radius: 12px;
        margin: 20px 0;
    }
    
    /* Tampilan Grid Sekolah */
    .school-card-btn {
        width: 100%;
        text-align: left;
        background: white;
        padding: 15px;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        transition: 0.2s;
        cursor: pointer;
    }
    .school-card-btn:hover { border-color: #3b82f6; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1); }
</style>
""", unsafe_allow_html=True)

# --- Helper Functions ---
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

# ==================================
# 2. DATA ENGINE (Logic Terjaga)
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
        # Dummy data untuk demo jika file tidak ada
        return pd.DataFrame(), pd.DataFrame()

data_wilayah, data_sekolah = load_all_data()

# ==================================
# 3. SIDEBAR (RAPID & TIDY)
# ==================================
with st.sidebar:
    # Logo & Brand
    logo_b64 = get_base64_image("logo_sumut.png")
    st.markdown(f"""
        <div style="display:flex; align-items:center; gap:16px; padding: 10px 0 30px 0;">
            <img src="data:image/png;base64,{logo_b64 if logo_b64 else ''}" width="60" style="filter: brightness(1.2);">
            <div>
                <div style="font-size:18px; font-weight:800; line-height:1.1;">SI-PANDAI</div>
                <div style="font-size:11px; font-weight:600; opacity:0.7; letter-spacing:0.1em;">SUMATERA UTARA</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Navigation Section
    st.markdown("<p style='font-size:11px; font-weight:700; color:#64748b; margin-bottom:12px;'>MENU UTAMA</p>", unsafe_allow_html=True)
    
    # Custom Navigation Logic
    nav_options = {
        "dashboard": "🚀 Dashboard Utama",
        "about": "ℹ️ Informasi Sistem"
    }
    
    for key, val in nav_options.items():
        is_active = "active-nav" if st.session_state.page_view == key or (key == "dashboard" and st.session_state.page_view == "detail") else ""
        if st.button(val, key=f"nav_{key}", use_container_width=True):
            st.session_state.page_view = key
            if key == "dashboard": st.session_state.selected_kab = "Semua"
            st.rerun()

    st.markdown("<br><p style='font-size:11px; font-weight:700; color:#64748b; margin-bottom:12px;'>KONTROL WILAYAH</p>", unsafe_allow_html=True)
    
    col_kab = "kab_kota" if not data_wilayah.empty and "kab_kota" in data_wilayah.columns else data_wilayah.columns[0]
    opsi = ["Semua"] + sorted(data_wilayah[col_kab].unique().tolist()) if not data_wilayah.empty else ["Semua"]
    kab_pilih = st.selectbox("Pilih Kabupaten/Kota", opsi, key="selected_kab")

    st.markdown("<div style='position: fixed; bottom: 20px; font-size:10px; color:#64748b;'>Update: April 2026<br>© DISDIK SUMUT</div>", unsafe_allow_html=True)

# ==================================
# 4. CONTENT WRAPPER
# ==================================

# Header
st.markdown(f"""
    <div class="header-banner">
        <div style="display:flex; justify-content:between; align-items:center;">
            <div>
                <h1 style='color: #0f172a; margin:0; font-size: 26px; font-weight:800; letter-spacing:-0.02em;'>
                    {'DASHBOARD ANALITIK' if st.session_state.page_view == 'dashboard' else 'PROFIL PENDIDIKAN' if st.session_state.page_view == 'detail' else 'DOKUMENTASI SISTEM'}
                </h1>
                <p style="color:#64748b; margin:0; font-size:14px; font-weight:600;">Wilayah: {kab_pilih.upper() if kab_pilih != 'Semua' else 'PROVINSI SUMATERA UTARA'}</p>
            </div>
            <div style="margin-left: auto; text-align:right;">
                <span style="background:#eff6ff; color:#2563eb; padding:8px 16px; border-radius:10px; font-size:12px; font-weight:700; border:1px solid #dbeafe;">Versi 2.1.0</span>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Main Page Logic
if st.session_state.page_view == "dashboard":
    # 1. Matriks Sektoral
    df_f = data_wilayah.copy()
    if kab_pilih != "Semua": df_f = df_f[df_f[col_kab] == kab_pilih]
    
    v_belajar = int(df_f.iloc[:,2].sum()) if not df_f.empty else 0
    v_ats = int(df_f.iloc[:,3].sum()) if not df_f.empty else 0
    v_persen = f"{(v_belajar / (v_belajar + v_ats) * 100):.2f}%" if (v_belajar + v_ats) > 0 else "0.00%"

    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(f"""
            <div class="metric-container">
                <div class="m-icon">🎓</div>
                <div><div class="m-label">Siswa Belajar</div><div class="m-value">{v_belajar:,}</div></div>
            </div>
        """, unsafe_allow_html=True)
    with m2:
        st.markdown(f"""
            <div class="metric-container" style="border-left-color: #ef4444;">
                <div class="m-icon" style="background:#fef2f2; color:#ef4444;">⚠️</div>
                <div><div class="m-label">Anak Tidak Sekolah</div><div class="m-value">{v_ats:,}</div></div>
            </div>
        """, unsafe_allow_html=True)
    with m3:
        st.markdown(f"""
            <div class="metric-container" style="border-left-color: #10b981;">
                <div class="m-icon" style="background:#f0fdf4; color:#10b981;">📈</div>
                <div><div class="m-label">Rasio Partisipasi</div><div class="m-value">{v_persen}</div></div>
            </div>
        """, unsafe_allow_html=True)

    # 2. Filter Wilayah Detail
    if kab_pilih != "Semua":
        st.markdown(f"<h4 style='margin-top:40px; margin-bottom:20px;'>🏫 Satuan Pendidikan di {kab_pilih}</h4>", unsafe_allow_html=True)
        sch_wil = data_sekolah[data_sekolah[col_kab] == kab_pilih] if not data_sekolah.empty else pd.DataFrame()
        if not sch_wil.empty:
            cols = st.columns(3)
            for i, row in enumerate(sch_wil.itertuples()):
                with cols[i % 3]:
                    if st.button(f"🏢 {getattr(row, 'nama_sekolah', 'Sekolah')}", key=f"sch_{i}", use_container_width=True):
                        st.session_state.selected_school_data = row._asdict()
                        st.session_state.page_view = "detail"
                        st.rerun()

    # 3. Visualisasi Spasial & Analitik
    st.markdown("<br>", unsafe_allow_html=True)
    col_map, col_chart = st.columns([1.6, 1])
    
    with col_map:
        st.markdown("##### 🗺️ Distribusi Spasial ATS")
        if not df_f.empty:
            ats_col = df_f.columns[3]
            fig_map = px.scatter_mapbox(
                df_f, lat="lat", lon="lon", size=ats_col, color=ats_col,
                color_continuous_scale="RdYlGn_r", hover_name=col_kab, 
                zoom=8, height=500
            )
            fig_map.update_layout(mapbox_style="open-street-map", margin={"r":0,"t":0,"l":0,"b":0}, coloraxis_showscale=False)
            st.plotly_chart(fig_map, use_container_width=True)

    with col_chart:
        st.markdown("##### 📊 Wilayah Prioritas (Top 5)")
        if not df_f.empty:
            df_top5 = df_f.sort_values(by=df_f.columns[3], ascending=False).head(5)
            fig_bar = px.bar(df_top5, x=df_f.columns[3], y=col_kab, orientation='h', color=df_f.columns[3], color_continuous_scale="Blues")
            fig_bar.update_layout(height=400, coloraxis_showscale=False, margin=dict(l=0, r=0, t=10, b=10))
            st.plotly_chart(fig_bar, use_container_width=True)
            
            # Corporate Recommendation Box
            st.markdown(f"""
                <div class="insight-card">
                    <p style="margin:0; font-size:12px; font-weight:800; color:#2563eb; text-transform:uppercase;">💡 Business Insight</p>
                    <p style="margin:8px 0; font-size:14px; font-weight:600; color:#1e293b;">
                        Wilayah <b>{kab_pilih if kab_pilih != 'Semua' else df_top5.iloc[0][col_kab]}</b> memerlukan intervensi alokasi dana sarana prasarana sebesar 15% lebih tinggi untuk percepatan akses pendidikan inklusif.
                    </p>
                </div>
            """, unsafe_allow_html=True)

    # 4. Data Control
    with st.expander("📁 Master Repository Data"):
        st.dataframe(df_f, use_container_width=True)
        st.download_button("Download Report (CSV) 📥", df_f.to_csv(index=False).encode('utf-8'), file_name=f"report_{kab_pilih}.csv")

elif st.session_state.page_view == "detail":
    sch = st.session_state.selected_school_data
    col_back, col_title = st.columns([1, 4])
    with col_back:
        if st.button("⬅️ DASHBOARD", use_container_width=True):
            st.session_state.page_view = "dashboard"
            st.rerun()
    
    st.markdown(f"### 🏫 {sch['nama_sekolah'].upper()}")
    st.caption(f"NPSN: {sch['npsn']} | Alamat: {sch.get('alamat','-')}")
    
    # Map & Profil
    c1, c2 = st.columns([2, 1])
    with c1:
        query = f"{sch['nama_sekolah'].replace(' ', '+')}+{sch['kab_kota'].replace(' ', '+')}"
        map_url = f"https://www.google.com/maps?q={query}&output=embed"
        components.html(f'<iframe width="100%" height="450" src="{map_url}" style="border-radius:20px; border:1px solid #e2e8f0;"></iframe>', height=470)
    
    with c2:
        with st.container(border=True):
            st.markdown("##### 📌 Statistik Utama")
            st.write(f"**Total Siswa:** {sch.get('jumlah_siswa', 0)} Orang")
            st.write(f"**Status:** {sch.get('status', 'Negeri')}")
            st.markdown("---")
            st.markdown("##### 🏗️ Fasilitas")
            st.write(f"**Rombel:** {sch.get('jumlah_rombel', 0)}")
            st.write(f"**Internet:** {sch.get('akses_internet', '-')}")
            st.write(f"**Listrik:** {sch.get('daya_listrik', '-')}")

elif st.session_state.page_view == "about":
    st.markdown("### ℹ️ Tentang Sistem SI-PANDAI")
    
    c_info, c_media = st.columns([1.5, 1])
    with c_info:
        with st.expander("🖥️ Deskripsi Teknis", expanded=True):
            st.markdown("Platform ini menggunakan metadata spasial untuk menganalisis kesenjangan pendidikan khusus di Sumatra Utara.")
        with st.expander("🎯 Objektif Strategis"):
            st.markdown("1. Pemetaan Akurat ATS\n2. Optimasi Anggaran Infrastruktur\n3. Instrumen Pengambilan Kebijakan Real-time")
        
        st.markdown("##### 🎬 Video Panduan")
        st.video("https://youtu.be/Wa4C8Ci3Iys?si=vbJRAa-G2dr2kYw8")

    with c_media:
        st.success("Sesuai Rancangan Aktualisasi 2025: Digitasi Data Menjadi Informasi Strategis.")
        with st.container(border=True):
            st.markdown("##### 👤 Developer")
            st.info("**Ima Safitri Sianipar, S.Kom**\nDinas Pendidikan Provinsi Sumatera Utara")
        
        if os.path.exists("barcode_video.png"):
            st.image("barcode_video.png", caption="Scan for Tutorial", width=180)
        else:
            st.markdown("<div style='padding:40px; background:#f8fafc; border:2px dashed #e2e8f0; text-align:center;'>[ QR CODE ]</div>", unsafe_allow_html=True)

# --- FOOTER (TIDY & CORPORATE) ---
st.markdown("<br><br>", unsafe_allow_html=True)
st.divider()
f1, f2, f3 = st.columns([1,2,1])
with f2:
    st.markdown("""
        <div style="text-align:center;">
            <p style="font-weight:800; color:#0f172a; margin-bottom:0;">DINAS PENDIDIKAN PROVINSI SUMATERA UTARA</p>
            <p style="font-size:11px; color:#64748b;">Jl. Teuku Cik Ditiro No.1-D, Kota Medan, Sumatera Utara 20152</p>
            <div style="display:flex; justify-content:center; gap:20px; margin-top:10px;">
                <a href="#"><img src="https://cdn-icons-png.flaticon.com/512/174/174855.png" width="18"></a>
                <a href="#"><img src="https://cdn-icons-png.flaticon.com/512/1006/1006771.png" width="18"></a>
                <a href="#"><img src="https://cdn-icons-png.flaticon.com/512/1384/1384060.png" width="18"></a>
            </div>
            <p style="font-size:10px; color:#94a3b8; margin-top:20px;">© 2026 SI-PANDAI SUMUT | Bidang Pembinaan Pendidikan Khusus</p>
        </div>
    """, unsafe_allow_html=True)
