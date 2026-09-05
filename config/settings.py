"""
File ini menyimpan semua nilai tetap (konstanta)
yang digunakan di seluruh aplikasi.
"""

# ============================================================
# INFORMASI APLIKASI
# ============================================================

APP_TITLE = "GrowthCore"

APP_SUBTITLE = "Toddler Nutritional Status Screening"

APP_DESCRIPTION = (
    "Masukkan data antropometri balita sesuai hasil pengukuran terbaru "
    "untuk memperoleh hasil klasifikasi status gizi."
)

# ============================================================
# PATH MODEL
# ============================================================

MODEL_PATH = "models/model_random_forest_stunting.pkl"

# ============================================================
# LABEL KELAS TARGET
# ============================================================

LABELS = {
    0: "Normal",
    1: "Stunting",
}

# ============================================================
# OPSI INPUT
# ============================================================

OPSI_JENIS_KELAMIN = [
    "Laki-laki",
    "Perempuan",
]

# ============================================================
# MAPPING ENCODING
# ============================================================

# Encoding jenis kelamin yang digunakan pada model:
#
# Laki-laki = 0
# Perempuan = 1

MAPPING_JENIS_KELAMIN = {
    "Laki-laki": 0,
    "Perempuan": 1,
}

# ============================================================
# FITUR MODEL FINAL
# ============================================================

# Urutan fitur HARUS sama dengan urutan saat model dilatih.

FITUR_MODEL = [
    "JK",
    "Usia (Bulan)",
    "Berat",
    "Tinggi",
    "LiLA",
]

# ============================================================
# RANGE VALIDASI INPUT
# ============================================================

RANGE_VALIDASI = {
    "usia_bulan": {
        "min": 0,
        "max": 59,
        "label": "Usia (bulan)",
        "placeholder": "Contoh: 24",
    },

    "berat": {
        "min": 2.0,
        "max": 20.8,
        "label": "Berat badan saat ini (kg)",
        "placeholder": "Contoh: 11.5",
    },

    "tinggi": {
        "min": 38.0,
        "max": 120.0,
        "label": "Tinggi badan saat ini (cm)",
        "placeholder": "Contoh: 85.0",
    },

    "lila": {
        "min": 5.0,
        "max": 30.0,
        "label": "LiLA (cm)",
        "placeholder": "Contoh: 14.5",
    },
}

# ============================================================
# DISCLAIMER
# ============================================================

DISCLAIMER_TEXT = (
    "Disclaimer: Hasil analisis ini merupakan alat bantu "
    "skrining awal dan tidak menggantikan diagnosis resmi "
    "tenaga medis."
)

FOOTER_COPYRIGHT = "© 2026 GrowthCore • Sistem Klasifikasi Status Gizi Balita"