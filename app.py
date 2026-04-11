# ==================================
# Bagian 4: SIDEBAR & NAVIGASI BARU
# ==================================
with st.sidebar:
    # 1. LOGO & JUDUL
    logo_b64 = get_base64_image("logo_sumut.png")
    if logo_b64:
        st.markdown(f'<div style="display:flex;align-items:center;gap:12px;padding-bottom:15px;"><img src="data:image/png;base64,{logo_b64}" width="40"><span style="font-size:16px;font-weight:800;color:white;">SI-PANDAI SUMUT</span></div>', unsafe_allow_html=True)
    
    # 2. TOMBOL ROLE ADMIN (Menjadi Full-Width "Balloon")
    st.markdown('<div class="full-width-role-btn">', unsafe_allow_html=True)
    if st.button("👤 Role: ADMIN", key="role_admin_btn", use_container_width=True): # use_container_width=True adalah kuncinya
        st.session_state.page_view = "admin_profile"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
        
    st.divider()

    # 3. JUDUL MENU UTAMA (Gunakan Markdown Modern)
    st.markdown(
        """
        <div class="modern-sidebar-header">
            <span style="color: #ff9800; font-size: 24px; font-weight: bold;">⊞</span>
            <span style="color: white; font-size: 1.25rem; font-weight: 700;">Menu Utama</span>
        </div>
        """, 
        unsafe_allow_html=True
    )

    # 4. NAVIGASI BARU (Mengganti st.radio dengan slim-width buttons) (Permintaan 2)
    st.markdown('<div class="slim-nav-container">', unsafe_allow_html=True)
    
    # Tombol Dashboard Utama
    div_class = "slim-nav-btn-active" if st.session_state.page_view == "dashboard" else "slim-nav-btn"
    st.markdown(f'<div class="{div_class}">', unsafe_allow_html=True)
    if st.button("🚀 Dashboard Utama", key="nav_dash", use_container_width=True):
        st.session_state.page_view = "dashboard"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # Tombol Pendidikan Khusus
    div_class = "slim-nav-btn-active" if st.session_state.page_view == "tentang_pk" else "slim-nav-btn"
    st.markdown(f'<div class="{div_class}">', unsafe_allow_html=True)
    if st.button("🎓 Pendidikan Khusus", key="nav_pk", use_container_width=True):
        st.session_state.page_view = "tentang_pk"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # Tombol Tentang Dashboard
    div_class = "slim-nav-btn-active" if st.session_state.page_view == "tentang_dashboard" else "slim-nav-btn"
    st.markdown(f'<div class="{div_class}">', unsafe_allow_html=True)
    if st.button("ℹ️ Tentang Dashboard", key="nav_about", use_container_width=True):
        st.session_state.page_view = "tentang_dashboard"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True) # Tutup slim-nav-container

    st.divider()

    # 5. FILTER WILAYAH (Judul Modern)
    st.markdown(
        """
        <div class="modern-sidebar-header">
            <span style="color: #00e5ff; font-size: 24px; font-weight: bold;">⌕</span>
            <span style="color: white; font-size: 1.25rem; font-weight: 700;">Filter Wilayah</span>
        </div>
        """, 
        unsafe_allow_html=True
    )
    col_kab = "kab_kota" if "kab_kota" in data_wilayah.columns else data_wilayah.columns[0] if not data_wilayah.empty else ""
    opsi = ["Semua"] + sorted(data_wilayah[col_kab].unique().tolist()) if not data_wilayah.empty else ["Semua"]
    # Widget Selectbox yang sekarang tulisannya sudah hitam berkat CSS Bagian 1
    kab_pilih = st.selectbox("Kabupaten / Kota", opsi, key="selected_kab", label_visibility="collapsed")

    st.divider()

    # 6. LOGOUT (Full-Width, Berwarna Merah berkat CSS Bagian 1)
    if st.button("Logout 🚪", key="logout_btn", use_container_width=True):
        proses_logout()
