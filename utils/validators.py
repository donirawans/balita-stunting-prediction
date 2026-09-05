"""
Berisi fungsi-fungsi untuk memvalidasi input dari form
sebelum diproses lebih lanjut.

Dipisah dari UI supaya logika validasi dapat diuji
secara independen dari tampilan Streamlit.
"""

from config.settings import (
    RANGE_VALIDASI,
    OPSI_JENIS_KELAMIN,
)


# ============================================================
# KONVERSI INPUT NUMERIK
# ============================================================

def to_float_or_none(nilai_teks):
    """
    Mengubah input menjadi float.

    Mengembalikan:
    - None jika kosong
    - "invalid" jika bukan angka
    - float jika valid
    """

    if nilai_teks is None:
        return None

    nilai_teks = (
        str(nilai_teks)
        .strip()
        .replace(",", ".")
    )

    if nilai_teks == "":
        return None

    try:
        return float(nilai_teks)

    except ValueError:
        return "invalid"


# ============================================================
# VALIDASI RANGE
# ============================================================

def validasi_range(nilai, kunci_range: str):
    """
    Mengecek apakah nilai berada dalam rentang
    yang ditentukan pada RANGE_VALIDASI.

    Returns
    -------
    tuple
        (valid, pesan_error)
    """

    if kunci_range not in RANGE_VALIDASI:
        return False, (
            f"Konfigurasi validasi untuk "
            f"'{kunci_range}' tidak ditemukan."
        )

    batas = RANGE_VALIDASI[kunci_range]

    if nilai is None:
        return False, (
            f"{batas['label']} "
            "tidak boleh kosong."
        )

    if nilai == "invalid":
        return False, (
            f"{batas['label']} "
            "harus berupa angka."
        )

    if nilai < 0:
        return False, (
            f"{batas['label']} "
            "tidak boleh bernilai negatif."
        )

    if not (
        batas["min"]
        <= nilai
        <= batas["max"]
    ):
        return False, (
            f"{batas['label']} harus berada "
            f"pada rentang "
            f"{batas['min']} - {batas['max']}."
        )

    return True, ""


# ============================================================
# VALIDASI FORM
# ============================================================

def validasi_form(data: dict):
    """
    Menjalankan validasi seluruh field pada form.

    Input yang diperiksa:
    - jenis_kelamin
    - usia_bulan
    - berat
    - tinggi
    - lila

    Returns
    -------
    tuple
        (
            semua_valid,
            daftar_error,
            daftar_peringatan
        )
    """

    daftar_error = []
    peringatan = []

    # ========================================================
    # 1. FIELD NUMERIK
    # ========================================================

    field_numerik = [
        "usia_bulan",
        "berat",
        "tinggi",
        "lila",
    ]

    # --------------------------------------------------------
    # Konversi ke float
    # --------------------------------------------------------

    for field in field_numerik:
        data[field] = to_float_or_none(
            data.get(field)
        )

    # --------------------------------------------------------
    # Validasi range
    # --------------------------------------------------------

    for field in field_numerik:
        valid, pesan = validasi_range(
            data.get(field),
            field
        )

        if not valid:
            daftar_error.append(pesan)

    # ========================================================
    # 2. VALIDASI JENIS KELAMIN
    # ========================================================

    jenis_kelamin = data.get("jenis_kelamin")

    if not jenis_kelamin:
        daftar_error.append(
            "Jenis kelamin wajib dipilih."
        )

    elif jenis_kelamin not in OPSI_JENIS_KELAMIN:
        daftar_error.append(
            "Jenis kelamin tidak dikenali."
        )

    # ========================================================
    # 3. VALIDASI LOGIKA ANTROPOMETRI DASAR
    # ========================================================

    usia_bulan = data.get("usia_bulan")
    berat = data.get("berat")
    tinggi = data.get("tinggi")
    lila = data.get("lila")

    # --------------------------------------------------------
    # Peringatan kombinasi data yang perlu diperiksa ulang
    # --------------------------------------------------------

    if (
        isinstance(usia_bulan, float)
        and isinstance(berat, float)
        and isinstance(tinggi, float)
        and isinstance(lila, float)
    ):
        if (
            berat <= 0
            or tinggi <= 0
            or lila <= 0
        ):
            daftar_error.append(
                "Berat, tinggi badan, dan LiLA "
                "harus lebih dari 0."
            )

    # ========================================================
    # 4. HASIL VALIDASI
    # ========================================================

    semua_valid = (
        len(daftar_error) == 0
    )

    return (
        semua_valid,
        daftar_error,
        peringatan,
    )