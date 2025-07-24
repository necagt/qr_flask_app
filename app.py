from flask import Flask, render_template, request, redirect, url_for, send_file
import qrcode
import os
from database import init_db, insert_entry, get_entry

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/qr_codes'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

init_db()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        entry_id = insert_entry(name, description)

        qr_url = request.host_url + entry_id
        qr_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{entry_id}.png")
        img = qrcode.make(qr_url)
        img.save(qr_path)

        return render_template("form.html", qr_image=url_for('static', filename=f'qr_codes/{entry_id}.png'))
    return render_template("form.html")

@app.route('/<entry_id>')
def show_entry(entry_id):
    data = get_entry(entry_id)
    if data:
        name, description = data
        return render_template("index.html", name=name, description=description)
    return "Veri bulunamadı.", 404

if __name__ == '__main__':
    app.run(debug=True)
