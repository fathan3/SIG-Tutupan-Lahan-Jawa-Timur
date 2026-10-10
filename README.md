# Sistem Informasi Geografis: Klasifikasi Tutupan Lahan (LULC) Provinsi Jawa Timur
## Analisis Spasial Multi-Spektral Berbasis Citra Sentinel-2A dan Supervised Fuzzy Logic

Aplikasi Sistem Informasi Geografis (SIG) interaktif untuk analisis dan pemetaan tutupan serta penggunaan lahan (*Land Use and Land Cover* - LULC) skala regional di Provinsi Jawa Timur. Proyek ini memadukan data reflektansi spektral satelit optik **Sentinel-2A Level-2A** (*Bottom-of-Atmosphere* / BOA Surface Reflectance) dengan metode **Supervised Fuzzy Logic Classifier** berbasis jarak Euclidean terbobot (*Distance-Based Membership*).

---

### Fitur Utama Sistem
1. **Peta Evaluasi Poligon (Vector Layer):**
   * Visualisasi interaktif berbasis Leaflet/Folium menampilkan 300 poligon sampel representatif dari 6 kelas tutupan lahan.
   * Penandaan khusus untuk poligon data uji independen (outline biru).
   * Panel interaktif popup yang menyajikan metadata lokasi, kelas prediksi, derajat keanggotaan fuzzy maksimum (*confidence score*), dan indeks spektral (NDVI, NDWI, NDBI).
2. **Peta Sebaran Regional Jawa Timur:**
   * Integrasi ubin citra satelit resolusi tinggi (Google Hybrid dan Esri World Imagery).
   * Sebaran titik observasi geospasial di seluruh kabupaten dan kota di Jawa Timur.
3. **Metrik Evaluasi & Matriks Kontinjensi:**
   * Analisis Confusion Matrix data uji independen.
   * Distribusi fungsi keanggotaan fuzzy per kelas tutupan lahan.
4. **Data Tabular & Ekspor:**
   * Filter interaktif berbasis kelas tutupan lahan dan subset data (latih/uji).
   * Fitur ekspor data terintegrasi ke format CSV.
5. **Kalkulator Inferensi Logika Fuzzy (Live Computation):**
   * Parameter dinamis untuk indeks NDVI, NDWI, NDBI, dan saluran inframerah B08 (NIR).
   * Perhitungan otomatis fungsi keanggotaan dengan visualisasi diagram batang dan profil radar multidimensi.

---

### Struktur Direktori Proyek
```text
psd-uas/
│
├── .streamlit/
│   └── config.toml               # Konfigurasi tema dan server Streamlit
│
├── hasil_evaluasi/
│   ├── evaluasi_tutupan_lahan_fuzzy.csv   # Dataset poligon lengkap dengan probabilitas fuzzy
│   ├── prediksi_data_uji.csv              # Data uji independen (30% subset)
│   ├── confusion_matrix.csv               # Matriks kontinjensi numerik
│   └── confusion_matrix.png               # Grafik heatmap confusion matrix
│
├── peta_evaluasi_poligon_fuzzy.html       # Visualisasi peta evaluasi vektor (Folium)
├── peta_regional_jawatimur_fuzzy.html     # Visualisasi peta sebaran regional (Folium)
│
├── app.py                        # Skrip aplikasi dashboard Streamlit
├── requirements.txt              # Daftar dependensi runtime Python
├── psd.ipynb                     # Notebook alur analisis data end-to-end
└── README.md                     # Dokumentasi teknis proyek
```

---

### Panduan Menjalankan di Komputer Lokal

1. Buka terminal atau PowerShell pada direktori kerja proyek:
   ```bash
   cd d:\psd-uas
   ```

2. Pasang dependensi yang tercantum pada file requirements:
   ```bash
   pip install -r requirements.txt
   ```

3. Jalankan aplikasi Streamlit:
   ```bash
   streamlit run app.py
   ```

4. Akses antarmuka pada peramban melalui alamat: `http://localhost:8501`.

---

### Panduan Publikasi ke Streamlit Community Cloud

1. Inisialisasi Git dan dorong perubahan ke repositori GitHub:
   ```bash
   git init
   git add app.py requirements.txt .streamlit/ hasil_evaluasi/ peta_evaluasi_poligon_fuzzy.html peta_regional_jawatimur_fuzzy.html README.md .gitignore
   git commit -m "feat: inisialisasi aplikasi SIG tutupan lahan jawa timur"
   git branch -M main
   git remote add origin https://github.com/<username-anda>/<nama-repo-anda>.git
   git push -u origin main
   ```

2. Buka dashboard di [share.streamlit.io](https://share.streamlit.io/) dan pilih repositori Anda.
3. Tetapkan file utama sebagai `app.py`, kemudian pilih **Deploy**.
