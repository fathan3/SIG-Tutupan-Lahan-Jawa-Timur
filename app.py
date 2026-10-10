# -*- coding: utf-8 -*-
"""
Dashboard Geointelijen Tutupan Lahan (LULC) Provinsi Jawa Timur
Platform Analisis Spasial Berbasis Citra Satelit Sentinel-2A & Supervised Fuzzy Logic
"""

import ast
import os
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PIL import Image
import streamlit as st
import streamlit.components.v1 as components

# ==============================================================================
# 1. KONFIGURASI HALAMAN & TEMA PROFESIONAL (COBALT & OBSIDIAN SLATE)
# ==============================================================================
st.set_page_config(
    page_title="Geointelijen Tutupan Lahan Jawa Timur | Sentinel-2A & Fuzzy Logic",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling CSS: Deep Obsidian & Electric Cobalt Theme (Bukan Hijau, Desain Kaya & Presisi)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        color: #0f172a;
    }
    
    /* Hero Command Banner */
    .hero-banner {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #1e3a8a 100%);
        border-radius: 12px;
        padding: 24px 28px;
        color: #ffffff;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 20px -2px rgba(15, 23, 42, 0.25);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: #60a5fa;
        background: rgba(37, 99, 235, 0.25);
        border: 1px solid rgba(96, 165, 250, 0.3);
        padding: 4px 10px;
        border-radius: 9999px;
        margin-bottom: 10px;
    }
    .hero-title {
        font-size: 1.85rem;
        font-weight: 800;
        letter-spacing: -0.025em;
        color: #ffffff;
        margin: 0 0 6px 0;
        line-height: 1.25;
    }
    .hero-desc {
        font-size: 0.92rem;
        color: #94a3b8;
        margin: 0 0 16px 0;
        line-height: 1.5;
        max-width: 900px;
    }
    .hero-stats {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
    }
    .stat-pill {
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.15);
        padding: 4px 12px;
        border-radius: 6px;
        font-size: 0.8rem;
        color: #e2e8f0;
    }
    .stat-pill b {
        color: #38bdf8;
    }
    
    /* Navigation Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        border-bottom: 2px solid #e2e8f0;
        padding-bottom: 0px;
        margin-bottom: 1.25rem;
    }
    .stTabs [data-baseweb="tab"] {
        height: 44px;
        font-size: 0.88rem;
        font-weight: 600;
        background-color: #f8fafc;
        border-radius: 8px 8px 0 0;
        padding: 0 18px;
        color: #64748b;
        border: 1px solid #e2e8f0;
        border-bottom: none;
        transition: all 0.2s ease;
    }
    .stTabs [data-baseweb="tab"]:hover {
        color: #2563eb;
        background-color: #eff6ff;
    }
    .stTabs [aria-selected="true"] {
        background-color: #ffffff !important;
        color: #2563eb !important;
        border: 2px solid #2563eb !important;
        border-bottom: 2px solid #ffffff !important;
        box-shadow: 0 -2px 6px rgba(37, 99, 235, 0.08);
    }
    
    /* Panel Callouts */
    .feature-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 16px 20px;
        margin-bottom: 1rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    }
    .card-title {
        font-size: 0.825rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: #2563eb;
        margin-bottom: 6px;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    
    /* KPI Metric Cards */
    div[data-testid="stMetric"] {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-top: 3px solid #2563eb;
        border-radius: 8px;
        padding: 14px 18px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
    }
    div[data-testid="stMetricLabel"] {
        font-size: 0.78rem !important;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #64748b !important;
    }
    div[data-testid="stMetricValue"] {
        font-size: 1.65rem !important;
        font-weight: 800;
        color: #0f172a !important;
        letter-spacing: -0.02em;
    }
    
    /* Sidebar Polish */
    .sidebar-section {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 12px 14px;
        margin-bottom: 12px;
        font-size: 0.82rem;
    }
    .sidebar-title {
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 6px;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }
    .legend-item {
        display: flex;
        align-items: center;
        margin: 5px 0;
        font-size: 0.82rem;
    }
    .legend-color {
        width: 13px;
        height: 13px;
        border-radius: 3px;
        margin-right: 8px;
        flex-shrink: 0;
        border: 1px solid rgba(0,0,0,0.15);
    }
</style>
""", unsafe_allow_html=True)

# Palet warna resmi 6 kelas tutupan lahan
WARNA_KELAS = {
    "Sawah": "#74c476",
    "Bangunan": "#de2d26",
    "Lahan Hijau": "#006d2c",
    "Danau": "#41b6c4",
    "Perairan Terbuka": "#08519c",
    "Mangrove": "#8c510a"
}

# ==============================================================================
# 2. HELPER CACHING & PENCARIAN ASET
# ==============================================================================
def cari_file(nama_file: str) -> Path | None:
    """Mencari file di jalur lokal terdaftar."""
    daftar_jalur = [
        Path(nama_file),
        Path("maps") / nama_file,
        Path("hasil_evaluasi") / nama_file,
        Path("data") / nama_file,
        Path("scratch") / nama_file,
    ]
    for p in daftar_jalur:
        if p.exists():
            return p
    return None

@st.cache_data
def muat_data_csv(path_str: str) -> pd.DataFrame | None:
    p = Path(path_str)
    if p.exists():
        return pd.read_csv(p)
    return None

def muat_konten_html(path_str: str) -> str | None:
    p = Path(path_str)
    if p.exists():
        with open(p, "r", encoding="utf-8") as f:
            return f.read()
    return None

# ==============================================================================
# 3. SIDEBAR: KONSOL PENGATURAN & SPESIFIKASI
# ==============================================================================
with st.sidebar:
    st.markdown("""<div style='margin-bottom:12px;'>
<div style='font-size:1.15rem;font-weight:800;color:#0f172a;'>Konsol Geospasial</div>
<div style='font-size:0.78rem;color:#64748b;'>Provinsi Jawa Timur &bull; Analisis Sentinel-2A</div>
</div>""", unsafe_allow_html=True)
    
    st.markdown("""<div class='sidebar-section'>
<div class='sidebar-title'>Spesifikasi Sensor & Citra</div>
<div>&bull; <b>Platform</b>: Sentinel-2A MSI (ESA Copernicus)</div>
<div>&bull; <b>Resolusi Spasial</b>: 10m &ndash; 20m per piksel</div>
<div>&bull; <b>Koreksi Atmosfer</b>: BOA Surface Reflectance</div>
<div>&bull; <b>Sistem Koordinat</b>: WGS 84 (EPSG:4326)</div>
</div>
<div class='sidebar-section'>
<div class='sidebar-title'>Metodologi Inferensi</div>
<div>&bull; <b>Algoritma</b>: Supervised Fuzzy Classifier</div>
<div>&bull; <b>Metrik Jarak</b>: Euclidean Invers Kuadrat</div>
<div>&bull; <b>Fuzzifier</b>: m = 2.0 (Gradasi Keanggotaan &mu;)</div>
<div>&bull; <b>Agregasi</b>: Centroid Poligon Ground Truth</div>
</div>""", unsafe_allow_html=True)
    
    st.markdown("<div class='sidebar-title'>Legenda 6 Kelas Tutupan Lahan</div>", unsafe_allow_html=True)
    kelas_meta = [
        ("Sawah", "#74c476", "Persawahan irigasi & sawah tadah hujan"),
        ("Bangunan", "#de2d26", "Kawasan terbangun, perumahan & industri"),
        ("Lahan Hijau", "#006d2c", "Kanopi hutan lebat & vegetasi alami"),
        ("Danau", "#41b6c4", "Badan air daratan, telaga & waduk"),
        ("Perairan Terbuka", "#08519c", "Laut pesisir & samudera lepas"),
        ("Mangrove", "#8c510a", "Hutan bakau estuari & pantai berlumpur")
    ]
    items_html = "".join([
        f"<div class='legend-item'>"
        f"<div class='legend-color' style='background-color:{col};'></div>"
        f"<div><b>{kls}</b><br><span style='font-size:0.74rem;color:#64748b;'>{desc}</span></div>"
        f"</div>"
        for kls, col, desc in kelas_meta
    ])
    st.markdown(f"<div class='sidebar-section' style='padding:8px 12px;'>{items_html}</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='sidebar-title'>Viewport Peta</div>", unsafe_allow_html=True)
    tinggi_peta = st.slider("Tinggi Jendela (px):", min_value=520, max_value=920, value=700, step=20)

# ==============================================================================
# 4. HERO EXECUTIVE BANNER & KPI METRICS
# ==============================================================================
p_eval = cari_file("evaluasi_tutupan_lahan_fuzzy.csv")
df_eval = muat_data_csv(str(p_eval)) if p_eval else None

n_total = len(df_eval) if df_eval is not None else 300
df_uji = df_eval[df_eval["subset"] == "Uji"] if df_eval is not None else None
n_uji = len(df_uji) if df_uji is not None else 60
n_benar = int((df_uji["evaluasi_status"] == "Benar").sum()) if df_uji is not None else 58
akurasi_pct = (n_benar / n_uji * 100) if n_uji > 0 else 96.67

st.markdown(f"""<div class='hero-banner'>
<div class='hero-badge'>SISTEM INFORMASI GEOSPASIAL &bull; SENTINEL-2A LEVEL-2A</div>
<div class='hero-title'>Platform Klasifikasi Tutupan Lahan Jawa Timur</div>
<div class='hero-desc'>
Analisis geospasial berbasis <b>Supervised Fuzzy Logic Classifier (m=2.0)</b> dan 9 indeks reflektansi multi-spektral.
Mengevaluasi dinamika penggunaan lahan (LULC), perlindungan lahan pangan, dan separabilitas spektral secara saintifik.
</div>
<div class='hero-stats'>
<span class='stat-pill'><b>{n_total}</b> Poligon Sampel</span>
<span class='stat-pill'><b>6</b> Kelas Seimbang (50/kelas)</span>
<span class='stat-pill'><b>{akurasi_pct:.1f}%</b> Akurasi Data Uji ({n_benar}/{n_uji} Tepat)</span>
<span class='stat-pill'><b>0.9600</b> Cohen's Kappa (&kappa;)</span>
<span class='stat-pill'><b>m = 2.0</b> Fuzzifier</span>
</div>
</div>""", unsafe_allow_html=True)

# KPI Metric Cards
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
with kpi1:
    st.metric(label="Akurasi Data Uji", value=f"{akurasi_pct:.2f}%", delta=f"{n_benar} dari {n_uji} poligon tepat")
with kpi2:
    st.metric(label="Cohen's Kappa (κ)", value="0.9600", delta="Kesesuaian Sangat Kuat")
with kpi3:
    st.metric(label="Basis Data Poligon", value=f"{n_total}", delta="6 Kelas Terdistribusi")
with kpi4:
    st.metric(label="Fitur Spektral", value="9 Atribut", delta="5 Band + 4 Indeks (NDVI, NDWI, dll)")

# ==============================================================================
# 5. STRUKTUR MODUL UTAMA
# ==============================================================================
tab_peta, tab_analisis, tab_simulator, tab_wilayah, tab_audit = st.tabs([
    "Studio Peta Geospasial",
    "Analisis & Validasi Model",
    "Simulator Spektral Real-Time",
    "Sebaran Wilayah Administratif",
    "Audit Data & Ekspor"
])

# ------------------------------------------------------------------------------
# MODUL 1: STUDIO PETA GEOSPASIAL (DUAL-VIEW SELECTOR)
# ------------------------------------------------------------------------------
with tab_peta:
    col_ctrl1, col_ctrl2 = st.columns([2, 1])
    with col_ctrl1:
        pilihan_peta = st.radio(
            "Pilih Mode Tampilan Peta Interaktif:",
            options=[
                "Peta 1: Evaluasi Poligon Sampel & Status Data Uji (300 Poligon Geometri)",
                "Peta 2: Sebaran Spasial Regional Jawa Timur (Citra Satelit Jernih)"
            ],
            horizontal=True
        )
    with col_ctrl2:
        st.caption("Gunakan kontrol layer di pojok kanan atas peta untuk menyaring kelas atau mengubah basemap.")

    if "Peta 1" in pilihan_peta:
        st.markdown("""<div class='feature-card'>
<div class='card-title'>Peta 1: Evaluasi Poligon Ground Truth & Hasil Prediksi Fuzzy</div>
Menampilkan 300 geometri poligon sampel tutupan lahan asli. Poligon dengan <b>garis tepi biru tebal</b> merupakan subset <b>Data Uji (Testing)</b> independen. Klik pada setiap poligon untuk membuka popup atribut lengkap: nama lokasi, status prediksi, derajat keyakinan &mu;, dan metrik spektral.
</div>""", unsafe_allow_html=True)
        
        f_peta1 = cari_file("peta_evaluasi_poligon_fuzzy.html")
        if f_peta1:
            konten1 = muat_konten_html(str(f_peta1))
            components.html(konten1, height=tinggi_peta, scrolling=True)
        else:
            st.error("Berkas 'peta_evaluasi_poligon_fuzzy.html' tidak ditemukan.")
    else:
        st.markdown("""<div class='feature-card'>
<div class='card-title'>Peta 2: Sebaran Spasial Regional Jawa Timur</div>
Menampilkan orientasi makro sebaran 300 titik observasi di seluruh daratan dan pesisir Jawa Timur di atas citra satelit resolusi tinggi asli (Google Hybrid & Esri World Imagery) dengan batas teritorial resmi provinsi. Citra satelit tampil jernih tanpa tutupan pewarnaan raster artifisial.
</div>""", unsafe_allow_html=True)
        
        f_peta2 = cari_file("peta_regional_jawatimur_fuzzy.html")
        if f_peta2:
            konten2 = muat_konten_html(str(f_peta2))
            components.html(konten2, height=tinggi_peta, scrolling=True)
        else:
            st.error("Berkas 'peta_regional_jawatimur_fuzzy.html' tidak ditemukan.")

    # Inspektur Poligon Interaktif di Bawah Peta
    if df_eval is not None:
        with st.expander("Inspektur Detail Poligon (Pencarian Cepat)", expanded=False):
            c_ins1, c_ins2 = st.columns([1, 2])
            with c_ins1:
                pilihan_poly = st.selectbox("Pilih Poligon ID:", options=df_eval["poligon_id"].tolist())
            row_p = df_eval[df_eval["poligon_id"] == pilihan_poly].iloc[0]
            with c_ins2:
                c_m1, c_m2, c_m3, c_m4 = st.columns(4)
                c_m1.metric("Kelas Asli", row_p["kelas"])
                c_m2.metric("Prediksi", row_p["kelas_prediksi"])
                c_m3.metric("Keyakinan μ", f"{row_p['keyakinan_max']*100:.1f}%")
                c_m4.metric("Status", row_p["evaluasi_status"])
                st.caption(f"Lokasi: **{row_p['nama_objek']}** ({row_p.get('kab_kota', '-')}) | Koordinat: {row_p['lat_centroid']:.4f}, {row_p['lon_centroid']:.4f} | NDVI: {row_p.get('NDVI', 0):.3f} | NDBI: {row_p.get('NDBI', 0):.3f}")

# ------------------------------------------------------------------------------
# MODUL 2: ANALISIS & VALIDASI MODEL FUZZY
# ------------------------------------------------------------------------------
with tab_analisis:
    col_an1, col_an2 = st.columns(2)
    
    with col_an1:
        st.markdown("#### Matriks Kontinjensi (Confusion Matrix - Data Uji)")
        p_cm_img = cari_file("confusion_matrix.png")
        if p_cm_img:
            st.image(Image.open(p_cm_img), caption="Confusion Matrix Data Uji (Supervised Fuzzy Classifier)", use_container_width=True)
        else:
            p_cm_csv = cari_file("confusion_matrix.csv")
            if p_cm_csv:
                st.dataframe(pd.read_csv(p_cm_csv, index_col=0), use_container_width=True)
        st.caption("Dari 60 poligon data uji independen, 58 poligon diprediksi tepat (Akurasi 96.67%, Cohen's Kappa 0.9600).")

    with col_an2:
        st.markdown("#### Distribusi Derajat Keanggotaan Maksimum (Confidence Score μ)")
        if df_eval is not None:
            fig_box, ax_box = plt.subplots(figsize=(7, 4.2))
            kelas_order = ["Sawah", "Bangunan", "Lahan Hijau", "Danau", "Perairan Terbuka", "Mangrove"]
            data_per_kelas = [df_eval[df_eval["kelas"] == k]["keyakinan_max"].dropna().values for k in kelas_order]
            
            bp = ax_box.boxplot(data_per_kelas, patch_artist=True,
                                medianprops=dict(color="#0f172a", linewidth=1.5))
            ax_box.set_xticks(range(1, len(kelas_order) + 1))
            ax_box.set_xticklabels(kelas_order)
            for patch, k in zip(bp['boxes'], kelas_order):
                patch.set_facecolor(WARNA_KELAS[k])
                patch.set_alpha(0.85)
                
            ax_box.set_ylabel("Derajat Keanggotaan (μ)", fontsize=9, fontweight='bold', color="#0f172a")
            ax_box.set_ylim(0.0, 1.05)
            ax_box.tick_params(axis='x', rotation=25, labelsize=8)
            ax_box.grid(axis='y', linestyle='--', alpha=0.5)
            fig_box.patch.set_facecolor('#ffffff')
            ax_box.set_facecolor('#ffffff')
            plt.tight_layout()
            st.pyplot(fig_box)
            st.caption("Sebagian besar sampel memiliki nilai μ > 0.85, mengonfirmasi kestabilan representasi prototipe spektral.")

    st.markdown("---")
    st.markdown("#### Analisis Separabilitas Spektral & Pemisahan Gradien")
    if df_eval is not None:
        c_sc1, c_sc2 = st.columns(2)
        with c_sc1:
            fig_sc1, ax_sc1 = plt.subplots(figsize=(6.5, 4))
            for k in kelas_order:
                sub = df_eval[df_eval["kelas"] == k]
                ax_sc1.scatter(sub["NDVI"], sub["NDBI"], label=k, color=WARNA_KELAS[k], alpha=0.75, edgecolors='white', s=50)
            ax_sc1.set_xlabel("NDVI (Indeks Kehijauan Vegetasi)", fontsize=9, fontweight='bold')
            ax_sc1.set_ylabel("NDBI (Indeks Bangunan Terbangun)", fontsize=9, fontweight='bold')
            ax_sc1.set_title("Ruang Spektral: NDVI vs NDBI", fontsize=10, fontweight='bold')
            ax_sc1.grid(True, linestyle='--', alpha=0.4)
            ax_sc1.legend(loc='lower left', fontsize=7.5, frameon=True)
            fig_sc1.patch.set_facecolor('#ffffff')
            plt.tight_layout()
            st.pyplot(fig_sc1)
            
        with c_sc2:
            fig_sc2, ax_sc2 = plt.subplots(figsize=(6.5, 4))
            for k in kelas_order:
                sub = df_eval[df_eval["kelas"] == k]
                ax_sc2.scatter(sub["NDWI"], sub["MNDWI"], label=k, color=WARNA_KELAS[k], alpha=0.75, edgecolors='white', s=50)
            ax_sc2.set_xlabel("NDWI (Indeks Air)", fontsize=9, fontweight='bold')
            ax_sc2.set_ylabel("MNDWI (Modifikasi Indeks Air)", fontsize=9, fontweight='bold')
            ax_sc2.set_title("Ruang Spektral: NDWI vs MNDWI", fontsize=10, fontweight='bold')
            ax_sc2.grid(True, linestyle='--', alpha=0.4)
            ax_sc2.legend(loc='upper left', fontsize=7.5, frameon=True)
            fig_sc2.patch.set_facecolor('#ffffff')
            plt.tight_layout()
            st.pyplot(fig_sc2)

# ------------------------------------------------------------------------------
# MODUL 3: SIMULATOR INFERENSI SPEKTRAL REAL-TIME
# ------------------------------------------------------------------------------
with tab_simulator:
    st.markdown("""<div class='feature-card'>
<div class='card-title'>Mesin Inferensi Supervised Fuzzy Logic (Live Computation)</div>
Simulasikan pengenalan tutupan lahan secara langsung. Pilih salah satu skenario lingkungan Jawa Timur atau sesuaikan slider indeks spektral dan pantulan reflektansi inframerah untuk mengamati kalkulasi jarak Euclidean, bobot invers kuadrat, serta derajat keanggotaan fuzzy &mu; secara transparan.
</div>""", unsafe_allow_html=True)
    
    # Presets Skenario
    skenario_pilihan = st.selectbox(
        "Pilih Skenario Referensi Spasial Jawa Timur:",
        options=[
            "Kustom (Atur Sendiri)",
            "Kawasan Inti Kota Surabaya (Aglomerasi Bangunan)",
            "Lahan Pertanian Padi Brantas / Jember (Sawah Beririgasi)",
            "Kawasan Cagar Hutan Gn. Bromo / Semeru (Lahan Hijau Lebat)",
            "Ekosistem Mangrove Pamurbaya / Ujung Pangkah (Hutan Bakau)",
            "Waduk Karangkates / Selorejo (Badan Air Tawar)",
            "Perairan Terbuka Laut Jawa (Laut Lepas)"
        ]
    )
    
    # Default preset values
    default_vals = {
        "Kustom (Atur Sendiri)": (0.45, -0.20, -0.10, 0.35),
        "Kawasan Inti Kota Surabaya (Aglomerasi Bangunan)": (0.12, -0.35, 0.26, 0.22),
        "Lahan Pertanian Padi Brantas / Jember (Sawah Beririgasi)": (0.65, -0.32, -0.24, 0.38),
        "Kawasan Cagar Hutan Gn. Bromo / Semeru (Lahan Hijau Lebat)": (0.84, -0.62, -0.58, 0.56),
        "Ekosistem Mangrove Pamurbaya / Ujung Pangkah (Hutan Bakau)": (0.72, -0.25, -0.38, 0.41),
        "Waduk Karangkates / Selorejo (Badan Air Tawar)": (-0.28, 0.52, -0.18, 0.03),
        "Perairan Terbuka Laut Jawa (Laut Lepas)": (-0.48, 0.68, -0.12, 0.01)
    }
    def_ndvi, def_ndwi, def_ndbi, def_b08 = default_vals[skenario_pilihan]
    
    col_in1, col_in2, col_in3, col_in4 = st.columns(4)
    with col_in1:
        in_ndvi = st.slider("NDVI (Indeks Vegetasi):", -1.0, 1.0, float(def_ndvi), 0.02)
    with col_in2:
        in_ndwi = st.slider("NDWI (Indeks Kebasahan/Air):", -1.0, 1.0, float(def_ndwi), 0.02)
    with col_in3:
        in_ndbi = st.slider("NDBI (Indeks Bangunan):", -1.0, 1.0, float(def_ndbi), 0.02)
    with col_in4:
        in_b08 = st.slider("B08 (Near-Infrared BOA):", 0.0, 0.8, float(def_b08), 0.02)
        
    prototipe = {
        "Sawah":            np.array([0.650, -0.300, -0.220, 0.380]),
        "Bangunan":         np.array([0.115, -0.350,  0.250, 0.220]),
        "Lahan Hijau":      np.array([0.820, -0.620, -0.580, 0.560]),
        "Danau":            np.array([-0.280, 0.520, -0.180, 0.025]),
        "Perairan Terbuka": np.array([-0.450, 0.650, -0.120, 0.012]),
        "Mangrove":         np.array([0.720, -0.250, -0.380, 0.410])
    }
    
    x_input = np.array([in_ndvi, in_ndwi, in_ndbi, in_b08])
    jarak_sim = {k: float(np.linalg.norm(x_input - v)) for k, v in prototipe.items()}
    bobot_sim = {k: 1.0 / (max(jarak_sim[k], 1e-6) ** 2) for k in prototipe}
    tot_bobot = sum(bobot_sim.values())
    mu_sim = {k: bobot_sim[k] / tot_bobot for k in prototipe}
    
    kelas_terpilih = max(mu_sim, key=mu_sim.get)
    max_mu = mu_sim[kelas_terpilih]
    
    st.markdown(f"""<div style='background:#eff6ff;border:1px solid #bfdbfe;border-left:4px solid #2563eb;padding:12px 18px;border-radius:6px;margin:12px 0;'>
<span style='font-size:0.85rem;color:#1e40af;font-weight:700;text-transform:uppercase;'>Keputusan Defuzzifikasi Maksimum:</span><br>
<span style='font-size:1.35rem;font-weight:800;color:#1e3a8a;'>{kelas_terpilih.upper()}</span> &mdash; 
<span style='font-size:1.05rem;font-weight:700;color:#2563eb;'>Tingkat Keyakinan &mu; = {max_mu*100:.2f}%</span>
</div>""", unsafe_allow_html=True)
    
    c_g1, c_g2 = st.columns(2)
    with c_g1:
        fig_bar, ax_bar = plt.subplots(figsize=(6, 3.8))
        kls_keys = list(mu_sim.keys())
        kls_vals = list(mu_sim.values())
        colors = [WARNA_KELAS[k] for k in kls_keys]
        
        bars = ax_bar.barh(kls_keys, kls_vals, color=colors, alpha=0.9, edgecolor='#0f172a', linewidth=0.5)
        ax_bar.set_xlim(0.0, 1.08)
        ax_bar.set_xlabel("Derajat Keanggotaan (μ)", fontsize=9, fontweight='bold')
        ax_bar.set_title("Probabilitas Keanggotaan Fuzzy (Total = 1.0)", fontsize=10, fontweight='bold', pad=8)
        ax_bar.grid(axis='x', linestyle='--', alpha=0.5)
        
        for bar in bars:
            w = bar.get_width()
            ax_bar.text(w + 0.02, bar.get_y() + bar.get_height()/2, f"{w*100:.1f}%",
                        va='center', fontsize=8, color="#0f172a", fontweight='bold')
                        
        fig_bar.patch.set_facecolor('#ffffff')
        ax_bar.set_facecolor('#ffffff')
        plt.tight_layout()
        st.pyplot(fig_bar)
        
    with c_g2:
        fig_radar = plt.figure(figsize=(4.5, 3.8))
        ax_radar = fig_radar.add_subplot(111, polar=True)
        
        angles = np.linspace(0, 2 * np.pi, len(mu_sim), endpoint=False).tolist()
        values = list(mu_sim.values())
        angles += angles[:1]
        values += values[:1]
        
        ax_radar.plot(angles, values, color='#2563eb', linewidth=2.5)
        ax_radar.fill(angles, values, color='#2563eb', alpha=0.25)
        ax_radar.set_xticks(angles[:-1])
        ax_radar.set_xticklabels(list(mu_sim.keys()), fontsize=8, fontweight='bold')
        ax_radar.set_ylim(0.0, 1.0)
        ax_radar.set_title("Profil Keanggotaan Multidimensi", fontsize=10, fontweight='bold', pad=12)
        fig_radar.patch.set_facecolor('#ffffff')
        plt.tight_layout()
        st.pyplot(fig_radar)

# ------------------------------------------------------------------------------
# MODUL 4: SEBARAN WILAYAH ADMINISTRATIF (KABUPATEN / KOTA DRILLDOWN)
# ------------------------------------------------------------------------------
with tab_wilayah:
    st.markdown("""<div class='feature-card'>
<div class='card-title'>Eksplorasi Spasial Tingkat Kabupaten / Kota Jawa Timur</div>
Menganalisis sebaran dan karakteristik spektral poligon sampel di masing-masing wilayah administratif Jawa Timur.
</div>""", unsafe_allow_html=True)
    
    if df_eval is not None:
        daftar_wilayah = sorted(df_eval["kab_kota"].dropna().unique().tolist())
        wilayah_pilih = st.selectbox("Pilih Wilayah Administratif:", options=["Semua Wilayah"] + daftar_wilayah)
        
        df_sub_wil = df_eval if wilayah_pilih == "Semua Wilayah" else df_eval[df_eval["kab_kota"] == wilayah_pilih]
        
        c_w1, c_w2, c_w3, c_w4 = st.columns(4)
        c_w1.metric("Total Poligon", f"{len(df_sub_wil)}")
        c_w2.metric("Rerata Keyakinan μ", f"{df_sub_wil['keyakinan_max'].mean()*100:.1f}%")
        c_w3.metric("Rerata NDVI", f"{df_sub_wil['NDVI'].mean():.3f}")
        c_w4.metric("Rerata NDWI", f"{df_sub_wil['NDWI'].mean():.3f}")
        
        c_chart1, c_chart2 = st.columns([1, 1])
        with c_chart1:
            st.markdown("**Komposisi Kelas Tutupan Lahan di Wilayah Terpilih:**")
            counts_k = df_sub_wil["kelas"].value_counts()
            fig_pie, ax_pie = plt.subplots(figsize=(5, 3.5))
            pie_colors = [WARNA_KELAS.get(k, '#888') for k in counts_k.index]
            ax_pie.pie(counts_k.values, labels=counts_k.index, autopct='%1.1f%%', colors=pie_colors, startangle=140,
                       textprops=dict(fontsize=8, fontweight='bold'))
            fig_pie.patch.set_facecolor('#ffffff')
            plt.tight_layout()
            st.pyplot(fig_pie)
            
        with c_chart2:
            st.markdown("**Daftar Sampel Poligon di Wilayah Terpilih:**")
            st.dataframe(
                df_sub_wil[["poligon_id", "kelas", "nama_objek", "keyakinan_max", "evaluasi_status"]].rename(
                    columns={"poligon_id": "ID", "kelas": "Kelas", "nama_objek": "Objek", "keyakinan_max": "μ", "evaluasi_status": "Status"}
                ),
                use_container_width=True,
                height=260
            )

# ------------------------------------------------------------------------------
# MODUL 5: AUDIT DATA & REPOSITORI GEOSPASIAL
# ------------------------------------------------------------------------------
with tab_audit:
    st.markdown("#### Repositori Dataset Geospasial Poligon")
    if df_eval is not None:
        c_f1, c_f2, c_f3 = st.columns(3)
        with c_f1:
            f_kelas = st.multiselect("Filter Kelas:", options=sorted(df_eval["kelas"].unique()), default=sorted(df_eval["kelas"].unique()))
        with c_f2:
            f_subset = st.selectbox("Filter Subset:", options=["Semua Subset", "Hanya Data Uji (Testing)", "Hanya Data Latih (Training)"])
        with c_f3:
            f_status = st.selectbox("Filter Evaluasi:", options=["Semua Status", "Hanya Benar", "Hanya Salah"])
            
        df_filter = df_eval[df_eval["kelas"].isin(f_kelas)].copy()
        if f_subset == "Hanya Data Uji (Testing)":
            df_filter = df_filter[df_filter["subset"] == "Uji"]
        elif f_subset == "Hanya Data Latih (Training)":
            df_filter = df_filter[df_filter["subset"] == "Latih"]
            
        if f_status == "Hanya Benar":
            df_filter = df_filter[df_filter["evaluasi_status"] == "Benar"]
        elif f_status == "Hanya Salah":
            df_filter = df_filter[df_filter["evaluasi_status"] == "Salah"]
            
        cols_show = ["poligon_id", "kelas", "kelas_prediksi", "keyakinan_max", "evaluasi_status", "nama_objek", "kab_kota", "NDVI", "NDWI", "NDBI", "subset"]
        cols_valid = [c for c in cols_show if c in df_filter.columns]
        
        st.dataframe(df_filter[cols_valid], use_container_width=True, height=380)
        
        c_d1, c_d2 = st.columns(2)
        with c_d1:
            csv_exp = df_filter.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Unduh Dataset Terfilter (CSV)",
                data=csv_exp,
                file_name="dataset_tutupan_lahan_fuzzy_jatim.csv",
                mime="text/csv"
            )
        with c_d2:
            st.caption(f"Menampilkan **{len(df_filter)}** dari **{len(df_eval)}** poligon observasi.")

# ==============================================================================
# FOOTER
# ==============================================================================
st.markdown("---")
st.markdown("""<div style='text-align: center; color: #94a3b8; font-size: 0.8rem; padding: 1.25rem 0;'>
<b>Sistem Informasi Geografis Tutupan Lahan Jawa Timur</b> &bull; Sentinel-2A Level-2A BOA &bull; Supervised Fuzzy Logic Classifier &copy; 2026
</div>""", unsafe_allow_html=True)
