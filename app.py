# ==================================
# Bagian 5: HEADER
# ==================================
st.markdown('<div class="top-gradient-bar"></div>', unsafe_allow_html=True)
st.markdown("""
    <div class="header-balloon-card">
        <h2 style='color: #0d47a1; font-weight:800; margin: 0; font-size: 2rem;'>DASHBOARD SI-PANDAI SUMUT</h2>
        <div class="gradient-line-inner"></div>
        <p style='color: #1565c0; font-size: 15px; font-weight: 700; margin: 0;'>
            Sistem Informasi Pemetaan Anak Tidak Sekolah (ATS) Disabilitas Bidang Pembinaan Pendidikan Khusus Dinas Pendidikan Provinsi Sumatera Utara
        </p>
    </div>
""", unsafe_allow_html=True)

# --- A. HALAMAN DASHBOARD ---
if st.session_state.page_view == "dashboard":
    st.markdown('<p style="font-size:26px; font-weight:800; color:#0d47a1;">Matriks Capaian Sektoral</p>', unsafe_allow_html=True)
    
    df_f = data_wilayah.copy()
    if kab_pilih != "Semua": df_f = df_f[df_f[col_kab] == kab_pilih]

    # Matriks (Fix Penamaan Kolom)
    m1, m2, m3, m4 = st.columns(4)
    c_pop = 'estimasi populasi usia sekolah'
    c_sis = 'jumlah_siswa'
    c_ats = 'ats_disabilitas'
    
    v_p = int(df_f[c_pop].sum()) if not df_f.empty else 0
    v_s = int(df_f[c_sis].sum()) if not df_f.empty else 0
    v_a = int(df_f[c_ats].sum()) if not df_f.empty else 0
    v_aps_num = (v_s / v_p * 100) if v_p > 0 else 0
    v_aps = f"{v_aps_num:.2f}%"

    with m1: draw_tile_svg("Estimasi Populasi Sasaran", f"{v_p:,}", svg_people, "tile-orange")
    with m2: draw_tile_svg("Siswa Belajar", f"{v_s:,}", svg_cap, "tile-blue-light")
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
            fig_map = px.scatter_mapbox(
                df_f, lat="lat", lon="lon", size=c_ats, color=c_ats,
                color_continuous_scale="RdYlGn_r", hover_name=col_kab, 
                zoom=9, height=450
            )
            fig_map.update_layout(mapbox_style="open-street-map", margin={"r":0,"t":0,"l":0,"b":0})
            st.plotly_chart(fig_map, use_container_width=True)

    with cv2:
        st.subheader("📊 5 Peringkat ATS Tertinggi")
        if not df_f.empty:
            df_top5 = df_f.sort_values(by=c_ats, ascending=False).head(5)
            fig = px.bar(df_top5, x=c_ats, y=col_kab, orientation='h', color=c_ats,
                         color_continuous_scale=[[0, '#00d2ff'], [1, '#3a7bd5']], text=c_ats)
            fig.update_layout(height=350, showlegend=False, coloraxis_showscale=False)
            st.plotly_chart(fig, use_container_width=True)

            # Insight
            p_insight = f"🚨 Jumlah ATS di {kab_pilih} tercatat {v_a:,} jiwa." if v_a > 100 else f"💡 Wilayah {kab_pilih} relatif stabil."
            st.markdown(f'<div class="insight-box"><div class="insight-title">Insight: {kab_pilih}</div><p class="insight-text">{p_insight}</p></div>', unsafe_allow_html=True)

    with st.expander("📋 Lihat & Download Data Tabel"):
        st.dataframe(df_f, use_container_width=True)
        csv = df_f.to_csv(index=False).encode('utf-8')
        st.download_button("Download CSV 📥", csv, file_name=f'data_ats_{kab_pilih}.csv', mime='text/csv')

elif st.session_state.page_view == "detail":
    sch = st.session_state.selected_school_data   
    st.markdown(f"<h3 style='color:#0d47a1;'>🏫 {sch['nama_sekolah'].upper()}</h3>", unsafe_allow_html=True)
    st.divider()
    c1, c2 = st.columns(2)
    with c1:
        with st.container(border=True):
            st.subheader("📌 Profil Umum")
            st.write(f"**Status:** {sch.get('status', '-')}")
            st.write(f"**Alamat:** {sch.get('alamat', '-')}")
            st.write(f"**Siswa:** {sch.get('jumlah_siswa', '0')}")
    with c2:
        with st.container(border=True):
            st.subheader("🏗️ Sarpras")
            st.write(f"**Rombel:** {sch.get('jumlah_rombel', '0')}")
            st.write(f"**Daya Listrik:** {sch.get('daya_listrik', '-')}")
    
    if st.button("⬅️ Kembali"):
        st.session_state.page_view = "dashboard"
        st.rerun()

elif st.session_state.page_view == "tentang_dashboard":
    st.markdown('<p style="font-size:26px; font-weight:800; color:#0d47a1;">Informasi SI-PANDAI SUMUT</p>', unsafe_allow_html=True)
    with st.expander("🖥️ Deskripsi Sistem", expanded=True):
        st.write("SI-PANDAI SUMUT adalah platform pemetaan digital untuk Anak Tidak Sekolah (ATS) disabilitas di Sumatera Utara.")
    if st.button("⬅️ Kembali Utama"):
        st.session_state.page_view = "dashboard"
        st.rerun()
