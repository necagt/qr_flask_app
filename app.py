from flask import Flask, request, render_template, redirect, url_for
import qrcode
import uuid
import os

app = Flask(__name__)

# Verileri tutmak için geçici bellek (deploy kapanınca sıfırlanır)
data_store = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_qr', methods=['POST'])
def generate_qr():
    # Form verilerini al
    cihaz_adi = request.form['cihaz_adi']
    cihaz_kodu = request.form['cihaz_kodu']
    tarih = request.form['tarih']
    raf_kodu = request.form['raf_kodu']
    emniyet_stogu = request.form['emniyet_stogu']
    aciklama = request.form['aciklama']

    # Benzersiz kimlik (UUID)
    cihaz_id = str(uuid.uuid4())

    # Bellekte sakla
    data_store[cihaz_id] = {
        'cihaz_adi': cihaz_adi,
        'cihaz_kodu': cihaz_kodu,
        'tarih': tarih,
        'raf_kodu': raf_kodu,
        'emniyet_stogu': emniyet_stogu,
        'aciklama': aciklama
    }

    # QR kod linki
    link = url_for('cihaz_bilgileri', cihaz_id=cihaz_id, _external=True)

    # QR kodu oluştur
    qr = qrcode.make(link)
    qr_path = f'static/qr_{cihaz_id}.png'
    os.makedirs('static', exist_ok=True)
    qr.save(qr_path)

    return render_template('show_qr.html', qr_image=qr_path)

@app.route('/cihaz/<cihaz_id>')
def cihaz_bilgileri(cihaz_id):
    cihaz = data_store.get(cihaz_id)
    if not cihaz:
        return "Cihaz bulunamadı.", 404
    return render_template('cihaz.html', cihaz=cihaz)

if __name__ == '__main__':
    app.run(debug=True)
