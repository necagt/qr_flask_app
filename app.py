import os
import sqlite3
import uuid
from flask import Flask, request, redirect, url_for, render_template, send_file
import qrcode

app = Flask(__name__)

DB_PATH = "veritabani.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS entries (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            department TEXT NOT NULL
        );
    """)
    conn.commit()
    conn.close()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form["name"]
        department = request.form["department"]
        unique_id = str(uuid.uuid4())

        # DB'ye ekle
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO entries (id, name, department) VALUES (?, ?, ?)", (unique_id, name, department))
        conn.commit()
        conn.close()

        # QR kod oluştur
        qr_url = request.url_root + "veri/" + unique_id
        qr = qrcode.make(qr_url)

        qr_path = f"static/{unique_id}.png"
        qr.save(qr_path)

        return render_template("qrcode.html", qr_image=qr_path, qr_url=qr_url)

    return render_template("form.html")

@app.route("/veri/<entry_id>")
def veri(entry_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name, department FROM entries WHERE id = ?", (entry_id,))
    row = cursor.fetchone()
    conn.close()

    if row:
        name, department = row
        return render_template("index.html", name=name, department=department)
    else:
        return "Veri bulunamadı", 404

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)
