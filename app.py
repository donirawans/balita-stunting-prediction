"""
Server Flask untuk aplikasi skrining status gizi balita (GrowthCore).

Rute utama:
- GET  /          : menampilkan form input skrining.
- POST /predict   : memproses data antropometri, menjalankan model
                    machine learning, lalu menampilkan hasil klasifikasi.
"""

from flask import Flask, render_template, request

from config.settings import (
    OPSI_JENIS_KELAMIN,
)
from utils.validators import validasi_form
from utils.preprocessing import preprocess_input
from utils.predictor import predict
from utils.recommendation import get_interpretation, get_recommendation

app = Flask(__name__)


# ============================================================
# PETA JUDUL REKOMENDASI (sesuai referensi layar hasil)
# ============================================================

JUDUL_REKOMENDASI = {
    "Nutrisi": "Rekomendasi Nutrisi",
    "Pemantauan pertumbuhan": "Pemantauan Pertumbuhan",
    "Tindak lanjut": "Tindak Lanjut Medis",
}


# ============================================================
# BANTUAN
# ============================================================

def _form_kosong():
    """Membuat kamus data form dengan nilai kosong."""

    return {
        "jenis_kelamin": "",
        "usia_bulan": "",
        "berat": "",
        "tinggi": "",
        "lila": "",
    }


def _ambil_data_form():
    """Mengambil data mentah dari request.form."""

    return {
        "jenis_kelamin": request.form.get("jenis_kelamin", "").strip(),
        "usia_bulan": request.form.get("usia_bulan", "").strip(),
        "berat": request.form.get("berat", "").strip(),
        "tinggi": request.form.get("tinggi", "").strip(),
        "lila": request.form.get("lila", "").strip(),
    }


def _susun_rekomendasi(label: str):
    """Menyusun rekomendasi berurutan dengan judul tampilan."""

    daftar = get_recommendation(label)

    return [
        {
            "judul": JUDUL_REKOMENDASI.get(
                kategori,
                kategori,
            ),
            "poin": poin,
        }
        for kategori, poin in daftar.items()
    ]


# ============================================================
# RUTE: FORM INPUT
# ============================================================

@app.route("/", methods=["GET"])
def index():

    return render_template(
        "index.html",
        opsi_jenis_kelamin=OPSI_JENIS_KELAMIN,
        data=_form_kosong(),
        errors=[],
        warnings=[],
    )


# ============================================================
# RUTE: PREDIKSI
# ============================================================

@app.route("/predict", methods=["POST"], endpoint="predict")
def predict_route():

    data_mentah = _ambil_data_form()

    # --------------------------------------------------------
    # 1. Validasi input
    # --------------------------------------------------------

    valid, daftar_error, warnings = validasi_form(
        data_mentah
    )

    if not valid:

        return render_template(
            "index.html",
            opsi_jenis_kelamin=OPSI_JENIS_KELAMIN,
            data=data_mentah,
            errors=daftar_error,
            warnings=warnings,
        ), 400

    # --------------------------------------------------------
    # 2. Preprocessing dan prediksi
    # --------------------------------------------------------

    try:

        df_input = preprocess_input(
            data_mentah
        )

        hasil = predict(
            df_input
        )

    except Exception:

        return render_template(
            "index.html",
            opsi_jenis_kelamin=OPSI_JENIS_KELAMIN,
            data=data_mentah,
            errors=[
                "Terjadi kesalahan saat memproses data. "
                "Silakan periksa kembali input Anda."
            ],
            warnings=warnings,
        ), 500

    # --------------------------------------------------------
    # 3. Menyusun data tampilan hasil
    # --------------------------------------------------------

    label = hasil["label"]

    return render_template(
        "result.html",
        label=label,
        prob_normal=hasil.get("probabilitas_normal"),
        prob_stunting=hasil.get("probabilitas_stunting"),
        interpretasi=get_interpretation(label),
        rekomendasi=_susun_rekomendasi(label),
    )


# ============================================================
# MENJALANKAN SERVER
# ============================================================

if __name__ == "__main__":
    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000,
    )
