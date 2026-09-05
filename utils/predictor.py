"""
Fungsi untuk memuat model Random Forest
dan melakukan prediksi status gizi balita.
"""

import joblib
import pandas as pd

from config.settings import (
    MODEL_PATH,
    LABELS,
    FITUR_MODEL,
)


# ============================================================
# MEMUAT PAKET MODEL
# ============================================================

paket_model = joblib.load(
    MODEL_PATH
)


# ============================================================
# MENGAMBIL MODEL DAN METADATA
# ============================================================

if not isinstance(
    paket_model,
    dict
):
    raise TypeError(
        "Format file model tidak sesuai. "
        "File deployment harus berupa dictionary."
    )

if "model" not in paket_model:
    raise KeyError(
        "Objek model tidak ditemukan "
        "di dalam file deployment."
    )

model = paket_model["model"]

fitur_model_pkl = paket_model.get(
    "fitur"
)

if fitur_model_pkl is None:
    raise KeyError(
        "Metadata fitur tidak ditemukan "
        "di dalam file deployment."
    )


# ============================================================
# VERIFIKASI MODEL FINAL
# ============================================================

# Model deployment final harus menggunakan tepat 5 fitur.
if model.n_features_in_ != len(FITUR_MODEL):
    raise ValueError(
        "Model yang dimuat bukan model final 5 fitur. "
        f"Model membutuhkan {model.n_features_in_} fitur, "
        f"sedangkan aplikasi membutuhkan {len(FITUR_MODEL)} fitur."
    )


# ============================================================
# VERIFIKASI METADATA FITUR
# ============================================================

if len(fitur_model_pkl) != len(FITUR_MODEL):
    raise ValueError(
        "Jumlah fitur pada metadata model "
        "tidak sesuai dengan konfigurasi aplikasi."
    )


if list(fitur_model_pkl) != list(FITUR_MODEL):
    raise ValueError(
        "Urutan atau nama fitur pada file model "
        "tidak sesuai dengan FITUR_MODEL di settings.py.\n"
        f"Fitur model : {list(fitur_model_pkl)}\n"
        f"Fitur aplikasi : {list(FITUR_MODEL)}"
    )


# ============================================================
# PREDIKSI
# ============================================================

def predict(
    df_input: pd.DataFrame
) -> dict:
    """
    Melakukan prediksi status gizi balita menggunakan
    model Random Forest terbaik.

    Parameters
    ----------
    df_input : pandas.DataFrame
        Data input yang sudah melalui preprocessing
        dan memiliki 5 fitur sesuai model final.

    Returns
    -------
    dict
        Hasil prediksi berupa:
        - kelas
        - label
        - probabilitas kelas terpilih
        - probabilitas Normal
        - probabilitas Stunting
    """

    # ========================================================
    # 1. VALIDASI TIPE INPUT
    # ========================================================

    if not isinstance(
        df_input,
        pd.DataFrame
    ):
        raise TypeError(
            "Input prediksi harus berupa "
            "pandas DataFrame."
        )

    if df_input.empty:
        raise ValueError(
            "Data input prediksi kosong."
        )


    # ========================================================
    # 2. MEMASTIKAN FITUR LENGKAP
    # ========================================================

    fitur_hilang = [
        fitur
        for fitur in FITUR_MODEL
        if fitur not in df_input.columns
    ]

    if fitur_hilang:
        raise ValueError(
            "Fitur input belum lengkap: "
            f"{fitur_hilang}"
        )


    # ========================================================
    # 3. MEMERIKSA FITUR TAMBAHAN
    # ========================================================

    fitur_tambahan = [
        fitur
        for fitur in df_input.columns
        if fitur not in FITUR_MODEL
    ]

    if fitur_tambahan:
        raise ValueError(
            "Terdapat fitur yang tidak digunakan "
            "oleh model final: "
            f"{fitur_tambahan}"
        )


    # ========================================================
    # 4. MENYESUAIKAN URUTAN FITUR
    # ========================================================

    df_model = df_input[
        FITUR_MODEL
    ].copy()


    # ========================================================
    # 5. VERIFIKASI JUMLAH FITUR
    # ========================================================

    if (
        df_model.shape[1]
        != model.n_features_in_
    ):
        raise ValueError(
            "Jumlah fitur input tidak sesuai "
            "dengan model Random Forest."
        )


    # ========================================================
    # 6. VERIFIKASI NILAI KOSONG
    # ========================================================

    if df_model.isnull().any().any():
        raise ValueError(
            "Terdapat nilai kosong pada "
            "data yang akan diprediksi."
        )


    # ========================================================
    # 7. VERIFIKASI DATA NUMERIK
    # ========================================================

    for kolom in FITUR_MODEL:
        if not pd.api.types.is_numeric_dtype(
            df_model[kolom]
        ):
            raise ValueError(
                f"Fitur '{kolom}' harus berupa nilai numerik."
            )


    # ========================================================
    # 8. PREDIKSI KELAS
    # ========================================================

    prediksi = model.predict(
        df_model
    )[0]

    prediksi = int(
        prediksi
    )

    if prediksi not in LABELS:
        raise ValueError(
            f"Label hasil prediksi tidak dikenali: {prediksi}"
        )


    # ========================================================
    # 9. PROBABILITAS MODEL
    # ========================================================

    probabilitas = None
    probabilitas_normal = None
    probabilitas_stunting = None

    if hasattr(
        model,
        "predict_proba"
    ):

        proba = model.predict_proba(
            df_model
        )[0]

        classes = list(
            model.classes_
        )

        if 0 in classes:
            index_normal = classes.index(
                0
            )

            probabilitas_normal = float(
                proba[
                    index_normal
                ]
            )

        if 1 in classes:
            index_stunting = classes.index(
                1
            )

            probabilitas_stunting = float(
                proba[
                    index_stunting
                ]
            )

        if prediksi in classes:
            index_prediksi = classes.index(
                prediksi
            )

            probabilitas = float(
                proba[
                    index_prediksi
                ]
            )


    # ========================================================
    # 10. HASIL PREDIKSI
    # ========================================================

    return {
        "kelas": prediksi,

        "label": LABELS[
            prediksi
        ],

        "probabilitas": (
            round(
                probabilitas,
                4
            )
            if probabilitas is not None
            else None
        ),

        "probabilitas_normal": (
            round(
                probabilitas_normal,
                4
            )
            if probabilitas_normal is not None
            else None
        ),

        "probabilitas_stunting": (
            round(
                probabilitas_stunting,
                4
            )
            if probabilitas_stunting is not None
            else None
        ),
    }