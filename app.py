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

# Fungsi bantuan untuk metrik (agar kode tidak error saat running)
def draw_metric_card(label, value, color):
    st.markdown(f"""
        <div style="background-color: white; padding: 20px; border-radius: 15px; border-left: 5px solid {color}; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
            <p style="margin:0; color: #64748b; font-size: 12px; font-weight: 700; text-transform: uppercase;">{label}</p>
            <h2 style="margin:0; color: #0f172a; font-weight: 800;">{value}</h2>
        </div>
    """, unsafe_allow_html=True)

# ==================================
# Bagian 1: CSS CUSTOM (DIPERBAIKI UNTUK MUNCULKAN SIDEBAR)
# ==================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
    html, body, [data-testid="stWidgetLabel"] { font-family: 'Inter', sans-serif !important; }

    .block-container {
        padding-top: 0.5rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
    }
    
    /* Tombol sidebar dimunculkan kembali */
    [data-testid="collapsedControl"] {
        display: flex !important;
    }

    .top-gradient-bar {
        position: fixed;
        top: 0; left: 0; width: 100%; height: 5px;
        background: #1e88e5;
        z-index: 999999;
    }

    /* Memastikan konten sidebar terlihat (Warna Biru Gradien) */
    [data-testid="stSidebar"] { 
        background: linear-gradient(180deg, #1e88e5 0%, #0d47a1 100%) !important; 
    }
    
    /* Memaksa teks di dalam sidebar berwarna putih agar kontras */
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] label, [data-testid="stSidebar"] span {
        color: white !important;
    }
    
    /* Fix untuk warna dropdown/selectbox di sidebar agar tidak putih-diatas-putih */
    div[data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] div {
        color: #1e293b !important;
    }

    .header-balloon-card {
        background: linear-gradient(90deg, #f0f7ff 0%, #d1e9ff 100%) !important;
        border-radius: 0px 0px 15px 15px;
        padding: 5px 0px;
        border-bottom: 2px solid rgba(13, 71, 161, 0.1);
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        text-align: center;
        margin-top: 2px;
        margin-bottom: 20px;
        width: 100% !important;
        display: block;
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
        for df in [df_ats, df_sch]:
            df.columns = df.columns.str.strip().str.lower()
        return df_ats, df_sch
    except: return pd.DataFrame(), pd.DataFrame()

data_wilayah, data_sekolah = load_all_data()

# ==================================
# Bagian 4: SIDEBAR & NAVIGASI
# ==================================
with st.sidebar:
    logo_b64 = get_base64_image("logo_sumut.png")
    if logo_b64:
        st.markdown(f'''
            <div style="display:flex;align-items:center;gap:12px;padding-bottom:15px;">
                <img src="data:image/png;base64,{logo_b64}" width="80">
                <span style="font-size:20px;font-weight:800;color:white;">SI-PANDAI SUMUT</span>
            </div>
        ''', unsafe_allow_html=True)
       
      
def ubah_halaman():
    # Tambahkan pengecekan ini agar tidak error saat logout
    if "nav_radio" in st.session_state:
        pilihan = st.session_state.nav_radio
        if "Dashboard Utama" in pilihan: 
            st.session_state.page_view = "dashboard"
             # Paksa filter kembali ke "Semua" saat menu Dashboard diklik
            st.session_state.selected_kab = "Semua" 
        elif "Pendidikan Khusus" in pilihan: 
            st.session_state.page_view = "tentang_pk"
        elif "Tentang Dashboard" in pilihan: 
            st.session_state.page_view = "tentang_dashboard"

st.sidebar.header("🧭 Navigasi Sistem")
st.sidebar.radio(
    "Klik :", 
    ["🚀 Dashboard Utama", "ℹ️ Tentang Dashboard"],
    key="nav_radio",
    on_change=ubah_halaman
)

st.sidebar.divider()
st.sidebar.header("🔎 Filter Wilayah")
col_kab = "kab_kota" if "kab_kota" in data_wilayah.columns else data_wilayah.columns[0]
opsi = ["Semua"] + sorted(data_wilayah[col_kab].unique().tolist()) if not data_wilayah.empty else ["Semua"]
kab_pilih = st.sidebar.selectbox("Kabupaten / Kota", opsi, key="selected_kab")

st.sidebar.divider()

# ==================================
# Bagian 5: HEADER
# ==================================
st.markdown('<div class="top-gradient-bar"></div>', unsafe_allow_html=True)
st.markdown("""
    <div class="header-balloon-card">
        <h2 style='color: #0d47a1; font-weight:800; margin: 0; font-size: 2rem;'>DASHBOARD SI-PANDAI SUMUT</h2>
        <div class="gradient-line-inner"></div>
        <p style='color: #1565c0; font-size: 15px; font-weight: 700; margin: 0;'>
            Sistem Informasi Pemetaan Anak Tidak Sekolah (ATS) 
        </p>
    </div>
""", unsafe_allow_html=True)

# --- A. HALAMAN DASHBOARD ---
if st.session_state.page_view == "dashboard":
    st.markdown('<p style="font-size:26px; font-weight:800; color:#0d47a1;">Matriks Capaian Sektoral</p>', unsafe_allow_html=True)
    
    df_f = data_wilayah.copy()
    if kab_pilih != "Semua": df_f = df_f[df_f[col_kab] == kab_pilih]

    # Matriks
    m1, m2, m3, m4 = st.columns(4)
    v_a = int(df_f.iloc[:,3].sum()) if not df_f.empty else 0
    v_aps_num = (int(df_f.iloc[:,2].sum()) / int(df_f.iloc[:,1].sum()) * 100) if not df_f.empty and int(df_f.iloc[:,1].sum()) > 0 else 0
    v_aps = f"{v_aps_num:.2f}%"

    with m1: draw_tile_svg("Estimasi Populasi Sasaran Usia Sekolah", f"{int(df_f.iloc[:,1].sum()):,}" if not df_f.empty else "0", svg_people, "tile-orange")
    with m2: draw_tile_svg("Siswa Belajar", f"{int(df_f.iloc[:,2].sum()):,}" if not df_f.empty else "0", svg_cap, "tile-blue-light")
    with m3: draw_tile_svg("Anak Tidak Sekolah", f"{v_a:,}", svg_warning, "tile-red-dark")
    with m4: draw_tile_svg("Persentase", v_aps, svg_chart, "tile-green-light")

    if kab_pilih != "Semua":
        st.divider()
        st.subheader(f"🏫 Satuan Pendidikan di {kab_pilih}")
        sch_wil = data_sekolah[data_sekolah[col_kab] == kab_pilih] if not data_sekolah.empty else pd.DataFrame()
        if not sch_wil.empty:
            cols = st.columns(3)
            for i, row in enumerate(sch_wil.itertuples()):
                with cols[i % 3]:
                    with st.container(border=True):
                      
                        if st.button(getattr(row, 'nama_sekolah', 'SEKOLAH').upper(), key=f"btn_{i}"):
                            st.session_state.selected_school_data = row._asdict()
                            st.session_state.page_view = "detail"
                            st.rerun()
                        st.caption(f"NPSN: {getattr(row, 'npsn', '-')}")

    st.divider()
    cv1, cv2 = st.columns([1.6, 1.1])
    with cv1:
        st.subheader("🗺️ Peta Sebaran ATS")
        if not df_f.empty:
            ats_col_name = df_f.columns[3]
            fig_map = px.scatter_mapbox(
                df_f, lat="lat", lon="lon", size=ats_col_name, color=ats_col_name,
                color_continuous_scale="RdYlGn_r", hover_name=col_kab, 
                hover_data={ats_col_name: True, "lat": False, "lon": False},
                zoom=9, height=450
            )
            fig_map.update_layout(mapbox_style="open-street-map", margin={"r":0,"t":0,"l":0,"b":0}, coloraxis_showscale=False)
            st.plotly_chart(fig_map, use_container_width=True)
            
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
            ats_col = df_f.columns[3]
            df_top5 = df_f.sort_values(by=ats_col, ascending=False).head(5)
            max_val = df_top5[ats_col].max() if not df_top5.empty else 100

            fig = px.bar(
                df_top5, 
                x=ats_col, 
                y=col_kab, 
                orientation='h', 
                color=ats_col,
                # Gradasi Biru Cerah ke Biru Royal (Sesuai contoh Balon)
                color_continuous_scale=[[0, '#00d2ff'], [1, '#3a7bd5']], 
                text=ats_col
            )
            
            fig.update_traces(
                textposition='outside',
                textfont=dict(color='black', size=13, family="Inter", weight="bold"),
                marker=dict(line=dict(width=0)),
                width=0.85 # Membuat batang gemuk/padat
            )

            fig.update_layout(
                height=350, 
                margin=dict(l=10, r=130, t=20, b=10),
                bargap=0, # Menghilangkan jarak antar slot bar
                showlegend=False, 
                plot_bgcolor='rgba(0,0,0,0)', 
                paper_bgcolor='rgba(0,0,0,0)',
                coloraxis_showscale=False
            )

            # Sumbu X & Y (Teks Nama Wilayah Warna Hitam)
            fig.update_xaxes(range=[0, max_val * 1.4], showticklabels=False, showgrid=False)
            fig.update_yaxes(
                tickfont=dict(color='black', size=12, family="Inter", weight="bold"),
                categoryorder='total ascending'
            )
            
            st.plotly_chart(fig, use_container_width=True)

            # Insight Box
            jml_sekolah = len(data_sekolah[data_sekolah[col_kab] == kab_pilih]) if kab_pilih != "Semua" else len(data_sekolah)
            if kab_pilih != "Semua" and v_a > 0 and jml_sekolah == 0:
                p_insight, p_tindakan, warna_box = f" ⚠️ MASALAH UTAMA: Masih tingginya jumlah Anak Tidak Sekolah (ATS) Disabilitas di wilayah {kab_pilih} sebanyak {v_a:,} jiwa, namun BELUM ADA SLB.", "Mendesak untuk pembukaan Unit Sekolah Baru.", "#b71c1c"
            elif v_a == 0:
                p_insight, p_tindakan, warna_box = f"✅ Di wilayah {kab_pilih} saat ini bersih dari ATS.", "Pertahankan status ini dengan penguatan sistem deteksi dini.", "#4caf50"
            elif v_a > 100:
                p_insight, p_tindakan, warna_box = f"🚨 Jumlah ATS di {kab_pilih} sangat tinggi ({v_a:,} jiwa).", "Segera lakukan validasi lapangan dan prioritaskan bantuan.", "#ef4444"
            else:
                p_insight, p_tindakan, warna_box = f"💡 Di Wilayah {kab_pilih} jumlah Anak Tidak Sekolah (ATS) Disabilitas sebanyak {v_a:,} jiwa dengan partisipasi {v_aps}.", "Optimalkan sekolah terdekat.", "#0d47a1"
            
            st.markdown(f"""
                <div class="insight-box" style="border-left: 6px solid {warna_box}; padding: 8px 12px;">
                    <div class="insight-title" style="color:{warna_box}; margin-bottom: 2px; font-size: 14px;">
                        💡 Insight & Rekomendasi: {kab_pilih}
                    </div>
                    <p class="insight-text" style="margin: 1; line-height: 1.3; font-size: 13px;">{p_insight}</p>
                    <div style="margin-top: 6px; padding-top: 8px; border-top: 1px solid rgba(0,0,0,0.05); font-size: 13px; font-weight: 700; color: {warna_box};">
                        Tindakan: <span style="font-weight: 700; color: #333;">{p_tindakan}</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            st.divider()

   # Lokasi baru: Tepat sebelum expander Tabel
    st.markdown(f"""
        <p style="font-size: 11px; color: #666; font-style: italic; margin-bottom: -10px; margin-left: 5px;">
            ℹ️ <b>Rekomendasi Data:</b> Sumber data berasal dari Bidang Pembinaan Pendidikan Khusus & TIKP 2025. 
            
        </p>
    """, unsafe_allow_html=True)

    with st.expander("📋 Lihat & Download Data Tabel"):
        st.dataframe(df_f, use_container_width=True)
        csv = df_f.to_csv(index=False).encode('utf-8')
        st.download_button("Download CSV 📥", csv, file_name=f'data_ats_{kab_pilih}.csv', mime='text/csv')


elif st.session_state.page_view == "detail":
    sch = st.session_state.selected_school_data   
    st.markdown(f"<h3 style='color:#0d47a1; margin-bottom:0;'>🏫 {sch['nama_sekolah'].upper()}</h3>", unsafe_allow_html=True)
    st.markdown(f"<p style='color:gray;'>Wilayah: {sch['kab_kota']} | NPSN: {sch['npsn']}</p>", unsafe_allow_html=True)
    query = f"{sch['nama_sekolah'].replace(' ', '+')}+{sch['kab_kota'].replace(' ', '+')}"
    map_url = f"https://www.google.com/maps?q={query}&output=embed"
    components.html(f'<iframe width="100%" height="400" src="{map_url}" style="border-radius:15px; border:1px solid #ddd;"></iframe>', height=420)
    st.divider()
    c1, c2 = st.columns(2)
    with c1:
        with st.container(border=True):
            st.subheader("📌 Profil Umum")
            st.write(f"**Status:** {sch.get('status', 'Negeri')}")
            st.write(f"**Alamat:** {sch.get('alamat', '-')}")
            st.write(f"**Jumlah Siswa:** {sch.get('jumlah_siswa', '0')} Orang")
            
    with c2:
        with st.container(border=True):
            st.subheader("🏗️ Sarana Prasarana")
            st.write(f"**Rombel:** {sch.get('jumlah_rombel', '0')}")
            st.write(f"**Akses Internet:** {sch.get('akses_internet', '-')}")
            st.write(f"**Daya Listrik:** {sch.get('daya_listrik', '-')}")

    st.divider()
    if st.button("⬅️ Kembali ke Dashboard"):
        st.session_state.page_view = "dashboard"
        st.rerun()

# --- C. HALAMAN TENTANG DASHBOARD ---
elif st.session_state.page_view == "tentang_dashboard":
    st.markdown('<p style="font-size:26px; font-weight:800; color:#0d47a1;">Informasi Sistem SI-PANDAI SUMUT</p>', unsafe_allow_html=True)
    
    col_info1, col_info2 = st.columns([1.5, 1])
    
    with col_info1:
        # Deskripsi Sistem (Balon Hijau)
        with st.expander("🖥️ Deskripsi Sistem", expanded=True):
            st.markdown("""
            **SI-PANDAI SUMUT** (*Sistem Informasi Pemetaan Anak Tidak Sekolah Disabilitas*) merupakan sebuah platform dashboard interaktif yang dirancang untuk mendigitalisasi data Anak Tidak Sekolah (ATS) khusus disabilitas. 
            
            Sistem ini mengintegrasikan data spasial (titik koordinat) dengan data atribut sekolah untuk memberikan gambaran komprehensif mengenai kondisi pendidikan khusus di Provinsi Sumatera Utara.
            """)
            
        # Tujuan Dashboard (Balon Hijau)
        with st.expander("🎯 Tujuan Dashboard"):
            st.markdown("""
            1. **Optimalisasi Pemetaan:** Mengidentifikasi sebaran titik lokasi Anak Tidak Sekolah (ATS) disabilitas secara akurat.
            2. **Instrumen Kebijakan:** Menyediakan basis data yang valid bagi pimpinan dalam menentukan arah kebijakan pendidikan inklusif.
            3. **Efisiensi Perencanaan:** Membantu Bidang Pendidikan Khusus dalam merencanakan pemenuhan sarana prasarana sekolah (RKB/Rehabilitasi) agar tepat sasaran.
            """)

        # Fitur Utama (Balon Hijau)
        with st.expander("🚀 Fitur Utama"):
            st.markdown("""
            * **Peta Sebaran Interaktif:** Visualisasi titik lokasi ATS disabilitas berbasis koordinat *latitude* dan *longitude*.
            * **Matriks Real-Time:** Ringkasan otomatis Estimasi Populasi Sasaran Usia Sekolah, Persentase, dan jumlah ATS.
            * **Analitik Satuan Pendidikan:** Informasi detail sekolah untuk pendukung bantuan infrastruktur.
            * **Top 5 Ranking:** Identifikasi wilayah dengan tingkat ATS tertinggi untuk prioritas penanganan.
            """)
        # Petunjuk Penggunaan (Balon Hijau Baru)
        with st.expander("📖 Petunjuk Penggunaan Dashboard"):
            st.markdown("""
            1. **Filter Wilayah:** Gunakan dropdown di sidebar kiri untuk memfilter data berdasarkan Kabupaten/Kota.
            2. **Eksplorasi Peta:** Klik atau arahkan kursor pada titik di peta untuk melihat detail koordinat dan jumlah ATS.
            3. **Analisis Grafik:** Pantau grafik batang untuk melihat 5 wilayah dengan prioritas penanganan tertinggi.
            4. **Detail Sekolah:** Pada filter wilayah tertentu, klik tombol nama sekolah untuk melihat sarana prasarana sekolah tersebut.
            5. **Download Data:** Gunakan fitur 'Lihat & Download Data Tabel' di bagian bawah dashboard untuk mengunduh laporan.
            """)
# VIDEO YOUTUBE DI SINI
        st.markdown("##### 🎬 Video Panduan Penggunaan")
        # Ganti link di bawah dengan link video youtube kamu
        st.video("https://youtu.be/Wa4C8Ci3Iys?si=vbJRAa-G2dr2kYw8")
    with col_info2:
        # Peran Dashboard
        st.markdown("##### 💡 Peran Dashboard")
        st.success("""
        Sesuai dengan **Rancangan Aktualisasi**, dashboard ini diharapkan berperan sebagai **Instrumen Pengambilan Kebijakan (Policy Tool)**. 
        
        Dashboard ini mengubah data manual yang tersebar menjadi informasi visual yang mudah dipahami, sehingga pimpinan dapat merespon kendala pendidikan khusus di pelosok daerah dengan lebih cepat dan transparan.
        """)
        
        st.divider()
        # Bingkai Segi Empat untuk Barcode Video
        st.markdown("##### 📹 Barcode Tutorial Video")
        with st.container(border=True):
            # Cek apakah file barcode ada
            if os.path.exists("barcode_video.png"):
                st.image("barcode_video.png", caption="Scan Barcode untuk Tutorial Video", width=200)
            else:
                # Tampilan kotak jika file belum diupload
                st.markdown("""
                    <div style="border: 2px solid #2e7d32; border-radius: 10px; padding: 20px; text-align: center; background-color: #f1f8e9;">
                        <span style="font-size: 50px;">📲</span>
                        <p style="color: #2e7d32; font-weight: 800; margin-top: 10px;">Tempat Barcode Video</p>
                        <p style="font-size: 11px; color: #666;">(Upload file barcode_video.png)</p>
                    </div>
                """, unsafe_allow_html=True)
        
        st.divider()
        # Informasi Inovator
        st.markdown("##### 👤 Inovator Sistem")
        st.markdown(f"""
        <div style="background-color: #f8f9fa; border-left: 5px solid #2e7d32; padding: 15px; border-radius: 8px;">
            <p style='margin:0;'><b>Nama:</b> Ima Safitri Sianipar, S.Kom</p>
            <p style='margin:0;'><b>Instansi:</b> Dinas Pendidikan Provinsi Sumatera Utara</p>
            <p style='margin:0;'><b>Jabatan:</b> Penata Kelola Sistem dan Teknologi Informasi</p>
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    if st.button("⬅️ Kembali ke Dashboard Utama", key="btn_back_dashboard_final"):
        st.session_state.page_view = "dashboard"
        st.rerun()
elif st.session_state.page_view == "tentang_dashboard":
    st.markdown('### ℹ️ Tentang SI-PANDAI')
    st.write("Sistem Informasi Analitik Pendidikan Khusus Sumatera Utara.")
    with st.container(border=True):
        st.markdown("""
        ### 🖥️ Deskripsi Sistem
        **SI-PANDAI SUMUT** (Sistem Informasi Pemetaan Anak Tidak Sekolah Disabilitas) adalah platform analitik digital yang dirancang untuk mengintegrasikan data anak tidak sekolah dengan kebutuhan sarana prasarana pendidikan khusus di Provinsi Sumatera Utara.

        ### 🎯 Tujuan Dashboard
        1. **Memetakan Sebaran ATS:** Mengidentifikasi koordinat tepat di mana anak-anak disabilitas yang belum sekolah berada.
        2. **Optimalisasi Kebijakan:** Memberikan rekomendasi data yang akurat bagi pengambil kebijakan di Dinas Pendidikan.
        3. **Efisiensi Anggaran:** Memastikan bantuan RKB (Ruang Kelas Baru) atau rehabilitasi sekolah tepat sasaran.

        ### 🚀 Fitur Utama
        * **Geospatial Mapping:** Peta interaktif sebaran ATS berbasis koordinat lat/lon.
        * **Real-time Metrics:** Matriks otomatis untuk estimasi populasi sasaran usia sekolah, jumlah siswa, dan persentase.
        * **School Analytics:** Detail sekolah.
        * **Top 5 Analysis:** Ranking wilayah dengan prioritas penanganan tertinggi.

        ### 💡 Manfaat
        * Mempermudah monitoring data pendidikan khusus secara transparan.
        * Mempercepat respon terhadap temuan anak tidak sekolah di pelosok daerah.
        * Sinkronisasi data sarpras sekolah dengan kebutuhan riil di lapangan.

        ### 📖 Cara Menggunakan Dashboard
        1.  **Filter Wilayah:** Gunakan menu drop-down di sidebar kiri untuk memilih Kabupaten/Kota.
        2.  **Pantau Matriks:** Lihat perubahan angka pada tile berwarna untuk mendapatkan ringkasan data.
        3.  **Eksplorasi Peta:** Arahkan kursor ke titik peta untuk melihat detail wilayah.
        4.  **Detail Sekolah:** Klik pada kartu nama sekolah untuk melihat detail profil dan kondisi sarpras bangunan.
        """)
        
        st.divider()
        if st.button("⬅️ Kembali ke Dashboard"):
            st.session_state.page_view = "dashboard"
            st.rerun()

# ==================================
# Bagian Akhir: FOOTER (SUPER RAPAT)
# ==================================
st.divider()

# 1. LOGO KOLABORASI
col_c1, col_c2, col_c3 = st.columns([2.2, 1, 1.9])
with col_c2:
    if os.path.exists("banner_kolaborasi.png"):
        st.image("banner_kolaborasi.png", width=150) 
    else:
        st.markdown("<p style='text-align:center; color:gray; font-size:10px;'>[ Logo Kolaborasi ]</p>", unsafe_allow_html=True)

# CSS PAKSA RAPAT (Margin Negatif)
st.markdown("""
    <style>
        .footer-container {
            text-align: center;
            font-family: 'Inter', sans-serif;
            margin-top: -25px; /* Menarik teks ke atas mendekati logo */
        }
    </style>
    <div class="footer-container">
        <h4 style="margin: 0; color: #0d47a1; font-weight: 800; font-size: 16px; padding-bottom: 2px;">
            DINAS PENDIDIKAN PROVINSI SUMATERA UTARA
        </h4>
        <p style="margin: 0; color: #666; font-size: 11px; line-height: 1.2;">
            Jl. Teuku Cik Ditiro No.1-D, Madras Hulu, Kec. Medan Polonia, Kota Medan, Sumatera Utara 20152
        </p>
        <p style="margin: 0; color: #0d47a1; font-size: 11px; font-weight: 600;">
            Email: <a href="mailto:disdik@sumutprov.go.id" style="text-decoration: none; color: #0d47a1;">disdik@sumutprov.go.id</a>
        </p>
    </div>
""", unsafe_allow_html=True)

# 3. IKON SOSIAL MEDIA (Juga dibuat rapat)
link_instagram = "https://www.instagram.com/disdiksumut"
link_web = "https://disdik.sumutprov.go.id"
link_youtube = "https://www.youtube.com/@Disdikprovsumut"

st.markdown(f"""
    <div style="text-align: center; margin-top: 5px; margin-bottom: 5px;">
        <a href="{link_instagram}" target="_blank" style="margin: 0 10px; text-decoration: none;">
            <img src="https://cdn-icons-png.flaticon.com/512/174/174855.png" width="20" height="20">
        </a>
        <a href="{link_web}" target="_blank" style="margin: 0 10px; text-decoration: none;">
            <img src="https://cdn-icons-png.flaticon.com/512/1006/1006771.png" width="20" height="20">
        </a>
        <a href="{link_youtube}" target="_blank" style="margin: 0 10px; text-decoration: none;">
            <img src="https://cdn-icons-png.flaticon.com/512/1384/1384060.png" width="20" height="20">
        </a>
    </div>
""", unsafe_allow_html=True)

# 4. WATERMARK COPYRIGHT
st.markdown("""
    <hr style="margin: 5px 0 5px 0; opacity: 0.1;">
    <div style="text-align: center; color: #9e9e9e; font-size: 10px; padding-bottom: 20px;">
        © 2026 SI-PANDAI SUMUT | Digitalisasi Pemetaan ATS Disabilitas | Bidang Pembinaan Pendidikan Khusus
    </div>
""", unsafe_allow_html=True)
