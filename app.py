import streamlit as st
import pandas as pd
import plotly.express as px

# --- 1. DATA CONTOH (Hapus jika Anda menggunakan data asli) ---
# Saya membuat data contoh untuk 5 daerah teratas
data = pd.DataFrame({
    'Kecamatan': ['Medan Area', 'Medan Barat', 'Medan Belawan', 'Medan Deli', 'Medan Denai'],
    'Jumlah ATS': [15, 12, 10, 8, 7]
})

st.subheader("📊 5 Peringkat ATS Tertinggi")

# --- 2. LOGIKA GRAFIK YANG SLIM & BERWARNA ---

# Definisi urutan warna kustom:
# Maroon, Hijau, Orens Gelap, Biru Gelap, Biru Muda
custom_colors = ['#800000', '#008000', '#FF8C00', '#00008B', '#ADD8E6']

fig = px.bar(data, 
             x='Jumlah ATS', 
             y='Kecamatan', 
             orientation='h',
             color='Kecamatan', # Petakan warna ke kategori agar warna-warni
             color_discrete_sequence=custom_colors, # Gunakan warna kustom
             text='Jumlah ATS', # Tampilkan angka di bar
             labels={'Jumlah ATS': 'Jumlah Anak'}
             )

# Pengaturan agar grafik terlihat Slim dan Bersih
fig.update_layout(
    height=300, # Mengurangi tinggi grafik agar lebih Slim (Standar ~400)
    margin=dict(l=20, r=20, t=30, b=20), # Jarak margin yang ketat
    bargap=0.3, # Mengatur jarak antar batang agar batang terlihat ramping
    xaxis_title=None, # Sembunyikan judul sumbu X agar lebih slim
    yaxis_title=None, # Sembunyikan judul sumbu Y
    showlegend=False, # Sembunyikan legend (karena nama daerah sudah ada di Y)
    plot_bgcolor='rgba(0,0,0,0)', # Latar belakang transparan
)

# Menampilkan angka di luar bar
fig.update_traces(textposition='outside')

# Tampilkan grafik
st.plotly_chart(fig, use_container_width=True)
