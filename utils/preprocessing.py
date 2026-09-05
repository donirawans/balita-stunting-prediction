"""
Berisi fungsi untuk mengubah input dari form menjadi format
yang sesuai dengan model Random Forest hasil penelitian.
"""

import pandas as pd

from config.settings import (
    MAPPING_JENIS_KELAMIN,
    FITUR_MODEL,
)


# ============================================================
# PREPROCESSING INPUT
# ============================================================

def preprocess_input(data: dict) -> pd.DataFrame:
    """
    Mengubah input pengguna menjadi DataFrame dengan urutan
    fitur yang sama seperti saat training model Random Forest.

    Input pengguna:
    - jenis_kelamin
    - usia_bulan
    - berat
    - tinggi
    - lila

    Fitur model yang dihasilkan:
    1. JK
    2. Usia (Bulan)
    3. Berat
    4. Tinggi
    5. LiLA
    """

    # ========================================================
    # 1. MENGAMBIL INPUT PENGGUNA
    # ========================================================

    jenis_kelamin = data["jenis_kelamin"]
    usia_bulan = float(data["usia_bulan"])
    berat = float(data["berat"])
    tinggi = float(data["tinggi"])
    lila = float(data["lila"])

    # ========================================================
    # 2. ENCODING JENIS KELAMIN
    # ========================================================

    if jenis_kelamin not in MAPPING_JENIS_KELAMIN:
        raise ValueError(
            "Jenis kelamin tidak dikenali: "
            f"{jenis_kelamin}"
        )

    jk_encoded = MAPPING_JENIS_KELAMIN[
        jenis_kelamin
    ]

    # ========================================================
    # 3. MEMBENTUK DATAFRAME MODEL
    # ========================================================

    df = pd.DataFrame([
        {
            "JK": jk_encoded,
            "Usia (Bulan)": usia_bulan,
            "Berat": berat,
            "Tinggi": tinggi,
            "LiLA": lila,
        }
    ])

    # ========================================================
    # 4. MEMASTIKAN SELURUH FITUR MODEL TERSEDIA
    # ========================================================

    kolom_hilang = [
        kolom
        for kolom in FITUR_MODEL
        if kolom not in df.columns
    ]

    if kolom_hilang:
        raise ValueError(
            "Fitur model belum lengkap: "
            f"{kolom_hilang}"
        )

    # ========================================================
    # 5. MENYESUAIKAN URUTAN FITUR
    # ========================================================

    df = df[FITUR_MODEL].copy()

    # ========================================================
    # 6. VERIFIKASI JUMLAH FITUR
    # ========================================================

    if df.shape[1] != len(FITUR_MODEL):
        raise ValueError(
            "Jumlah fitur hasil preprocessing "
            "tidak sesuai dengan model."
        )

    # ========================================================
    # 7. VERIFIKASI NILAI KOSONG
    # ========================================================

    if df.isnull().any().any():
        raise ValueError(
            "Terdapat nilai kosong pada "
            "hasil preprocessing."
        )

    # ========================================================
    # 8. VERIFIKASI SELURUH FITUR NUMERIK
    # ========================================================

    for kolom in FITUR_MODEL:
        if not pd.api.types.is_numeric_dtype(
            df[kolom]
        ):
            raise ValueError(
                f"Fitur '{kolom}' harus berupa nilai numerik."
            )

    return df