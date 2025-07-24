from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import qrcode
import os
from datetime import datetime

app = Flask(__name__)
QR_FOLDER = "static/qrcodes"
os.makedirs(QR_FOLDER, exist_ok=True)

DB_FILE = "veritabani.db"

def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cihazlar (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cihaz_adi TEXT,
                cihaz_kodu TEXT,
                tarih TEXT,
                raf_kodu TEXT,
                emniyet_stogu INTEGER,
                aciklama TEXT
            )
        """)
        conn.commit()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        cihaz_adi = request.form["cihaz_adi"]
        cihaz_kodu = request.form["cihaz_kodu"]
        tarih = request.form["tarih"]
        raf_kodu = request.form["raf_kodu"]
        emniyet_stogu = request.form["emniyet_stogu"]
        aciklama = request.form["aciklama"]

        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO cihazlar (cihaz_adi, cihaz_kodu, tarih, raf_kodu, emniyet_stogu, aciklama)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (cihaz_adi, cihaz_kodu, tarih, raf_kodu, emniyet_stogu, aciklama))
            cihaz_id = cursor.lastrowid
            conn.commit()

        # QR içeriği: oluşturulan cihaz sayfası linki
        qr_url = request.url_root + "cihaz/" + str(cihaz_id)
        qr = qrcode.make(qr_url)
        qr_filename = f"qr_{cihaz_id}.png"
        qr.save(os.path.join(QR_FOLDER, qr_filename))

        return render_template("index.html", qr_filename=qr_filename)

    return render_template("index.html", qr_filename=None)

@app.route("/cihaz/<int:cihaz_id>")
def cihaz_goster(cihaz_id):
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM cihazlar WHERE id=?", (cihaz_id,))
        cihaz = cursor.fetchone()

    if cihaz:
        cihaz_dict = {
            "cihaz_adi": cihaz[1],
            "cihaz_kodu": cihaz[2],
            "tarih": cihaz[3],
            "raf_kodu": cihaz[4],
            "emniyet_stogu": cihaz[5],
            "aciklama": cihaz[6]
        }
        return render_template("show.html", cihaz=cihaz_dict)
    else:
        return "Cihaz bulunamadı.", 404

if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
