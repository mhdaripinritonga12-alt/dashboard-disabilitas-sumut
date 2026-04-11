<style>
    /* --- MENAIKKAN POSISI SELURUH KONTEN --- */
    .block-container {
        padding-top: 0.5rem !important; /* Sangat mepet ke atas */
        padding-bottom: 0rem !important;
    }

    /* --- BAR GRADASI PELANGI --- */
    .top-gradient-bar {
        position: fixed;
        top: 0; left: 0; width: 100%; height: 8px;
        background: linear-gradient(90deg, #ff8a00, #e52e71, #9c27b0, #1e88e5, #4caf50, #ffeb3b);
        z-index: 999999;
    }

    /* --- KOTAK HEADER (DIPERPANJANG & DIPERSEMPIT) --- */
    .header-balloon-card {
        background: rgba(255, 255, 255, 0.8) !important;
        backdrop-filter: blur(8px);
        border-radius: 15px;
        padding: 10px 20px; /* Padding atas-bawah diperkecil agar tidak terlalu tebal */
        border: 1px solid rgba(255, 255, 255, 0.5);
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        text-align: center;
        margin-top: -15px; /* Menaikkan kotak ke arah bar gradasi */
        margin-bottom: 20px;
        width: 98%; /* Diperpanjang secara horizontal */
        margin-left: auto;
        margin-right: auto;
    }

    /* GARIS BIRU DI DALAM KOTAK */
    .gradient-line-inner {
        height: 3px;
        background: linear-gradient(90deg, #0d47a1 0%, #42a5f5 50%, #0d47a1 100%);
        border-radius: 2px;
        margin: 5px auto;
        width: 50%;
    }
</style>
