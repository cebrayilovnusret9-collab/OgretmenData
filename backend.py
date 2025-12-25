from flask import Flask, jsonify, request
import csv
import os

app = Flask(__name__)

def search_ogretmen(isim=None, il=None, brans=None, limit=50):
    """CSV'de öğretmen arama (hafıza dostu)"""
    results = []
    count = 0
    
    with open('178kogretmen.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        
        for row in reader:
            if len(row) >= 8:
                # CSV yapısı: ID, İsim, İl, İlçe, Okul, Branş, Telefon, Tarih
                match = True
                
                if isim and isim.upper() not in row[1].upper():
                    match = False
                    
                if il and il.upper() not in row[2].upper():
                    match = False
                    
                if brans and brans.upper() not in row[5].upper():
                    match = False
                
                if match:
                    results.append({
                        'id': row[0],
                        'isim': row[1],
                        'il': row[2],
                        'ilce': row[3],
                        'okul': row[4],
                        'brans': row[5],
                        'telefon': row[6],
                        'kayit_tarihi': row[7]
                    })
                    count += 1
                    
                    if count >= limit:
                        break
    
    return results

@app.route('/')
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head><title>178K Öğretmen API</title><meta charset="utf-8"></head>
    <body>
        <h1>👨‍🏫 178K Öğretmen Veritabanı API</h1>
        <p><strong>Kurucu:</strong> @sukazatkinis</p>
        <p><strong>Telegram:</strong> @f3system</p>
        <p><strong>API Endpoint'leri:</strong></p>
        <ul>
            <li><code>/f3system/api/ogretmen?isim=ahmet</code></li>
            <li><code>/f3system/api/ogretmen?il=istanbul&brans=Matematik</code></li>
            <li><code>/f3system/api/ogretmen?ilce=kadıköy&limit=10</code></li>
        </ul>
    </body>
    </html>
    """

@app.route('/f3system/api/ogretmen')
def ogretmen_api():
    isim = request.args.get('isim', '')
    il = request.args.get('il', '')
    ilce = request.args.get('ilce', '')
    brans = request.args.get('brans', '')
    okul = request.args.get('okul', '')
    limit = min(int(request.args.get('limit', 50)), 100)
    
    results = search_ogretmen(isim=isim, il=il, brans=brans, limit=limit)
    
    # İlçe ve okul filtrelemesi (sonradan)
    filtered = []
    for ogretmen in results:
        match = True
        
        if ilce and ilce.upper() not in ogretmen['ilce'].upper():
            match = False
            
        if okul and okul.upper() not in ogretmen['okul'].upper():
            match = False
            
        if match:
            filtered.append(ogretmen)
    
    return jsonify({
        'sorgu': {'isim': isim, 'il': il, 'ilce': ilce, 'brans': brans, 'okul': okul},
        'bulunan': len(filtered),
        'sonuclar': filtered,
        'kurucu': '@sukazatkinis',
        'telegram': '@f3system',
        'aciklama': '178.000 öğretmen verisi - Sadece eğitim amaçlıdır'
    })

@app.route('/f3system/api/ogretmen/<int:ogretmen_id>')
def ogretmen_by_id(ogretmen_id):
    with open('178kogretmen.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] == str(ogretmen_id):
                return jsonify({
                    'id': row[0],
                    'isim': row[1],
                    'il': row[2],
                    'ilce': row[3],
                    'okul': row[4],
                    'brans': row[5],
                    'telefon': row[6],
                    'kayit_tarihi': row[7],
                    'kurucu': '@sukazatkinis',
                    'telegram': '@f3system'
                })
    
    return jsonify({'error': 'Öğretmen bulunamadı'}), 404

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
