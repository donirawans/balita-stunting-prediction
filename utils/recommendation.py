"""
Modul rekomendasi berbasis rule-based.

Rekomendasi yang ditampilkan disusun sebagai informasi edukatif
untuk mendukung hasil prediksi status gizi balita. Rekomendasi ini
tidak dimaksudkan sebagai pengganti diagnosis, pemeriksaan, maupun
penanganan oleh tenaga kesehatan.

Dasar penyusunan rekomendasi:
- World Health Organization (WHO), 2023
- Kementerian Kesehatan Republik Indonesia, 2022
"""


# ============================================================
# REKOMENDASI STATUS NORMAL
# ============================================================

REKOMENDASI_NORMAL = {
    "Nutrisi": [
        "Pertahankan pola makan yang beragam, bergizi, dan sesuai dengan usia balita.",
        "Lanjutkan pemberian ASI dan/atau makanan pendamping ASI sesuai usia serta kebutuhan gizi balita.",
    ],

    "Pemantauan pertumbuhan": [
        "Lakukan pemantauan pertumbuhan secara rutin melalui Posyandu atau fasilitas pelayanan kesehatan.",
        "Pantau berat badan dan tinggi badan secara berkala untuk memantau pertumbuhan balita.",
    ],

    "Tindak lanjut": [
        "Pertahankan pola hidup bersih dan sehat serta praktik pemberian makanan yang aman.",
        "Apabila terdapat perubahan atau masalah pada pertumbuhan balita, konsultasikan kepada tenaga kesehatan.",
    ],
}


# ============================================================
# REKOMENDASI STATUS STUNTING
# ============================================================

REKOMENDASI_STUNTING = {
    "Nutrisi": [
        "Tingkatkan asupan makanan bergizi seimbang dengan mengutamakan kecukupan protein hewani sesuai usia balita.",
        "Konsultasikan kebutuhan nutrisi balita kepada tenaga kesehatan guna memperoleh pendampingan pola makan yang tepat.",
    ],

    "Pemantauan pertumbuhan": [
        "Lakukan pemantauan pertumbuhan secara rutin dan intensif melalui Posyandu atau fasilitas pelayanan kesehatan.",
        "Ukur berat dan tinggi badan secara berkala untuk mengevaluasi tren perbaikan pertumbuhan balita.",
    ],

    "Tindak lanjut": [
        "Segera konsultasikan kondisi balita ke fasilitas pelayanan kesehatan untuk mendapatkan pemeriksaan dan penanganan komprehensif.",
        "Patuhi seluruh anjuran nutrisi, tata laksana medis, serta jadwal evaluasi berkala yang ditetapkan.",
    ],
}


# ============================================================
# INTERPRETASI HASIL PREDIKSI
# ============================================================

INTERPRETASI = {
    "Normal": (
        "Berdasarkan data yang dimasukkan, status gizi balita diprediksi "
        "berada pada kategori normal. Pertumbuhan tetap perlu dipantau "
        "secara berkala agar tetap sesuai dengan usianya."
    ),

    "Stunting": (
        "Berdasarkan data antropometri yang dimasukkan, balita terindikasi "
        "berada pada kategori stunting. Disarankan untuk segera melakukan "
        "pemeriksaan lebih lanjut ke fasilitas kesehatan guna memperoleh "
        "penanganan yang sesuai."
    ),
}


# ============================================================
# FUNGSI INTERPRETASI
# ============================================================

def get_interpretation(label: str) -> str:
    """
    Mengembalikan teks interpretasi berdasarkan
    hasil prediksi model.
    """

    return INTERPRETASI.get(
        label,
        "Interpretasi tidak tersedia untuk label ini."
    )


# ============================================================
# FUNGSI REKOMENDASI
# ============================================================

def get_recommendation(label: str) -> dict:
    """
    Mengembalikan rekomendasi berdasarkan
    label hasil prediksi model.
    """

    if label == "Normal":
        return REKOMENDASI_NORMAL

    if label == "Stunting":
        return REKOMENDASI_STUNTING

    return {
        "Umum": [
            "Rekomendasi tidak tersedia untuk label ini."
        ]
    }