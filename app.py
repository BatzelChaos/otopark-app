"""
Otopark Projesi - Flask Web API (App)

Bu modül, otopark sisteminin web arayüzünü ve REST API'sini sağlar.
Kullanıcılar tarayıcı üzerinden otopark durumunu görüp araç işlemleri yapabilirler.
"""

from flask import Flask, render_template, request, jsonify
from models import Otopark
from datetime import datetime

# Flask uygulamasını oluştur
app = Flask(__name__)

# Global otopark nesnesi
otopark = None


def otopark_olustur(adi="Çankiri Merkez Otopark", kapasite=30):
    """Otopark nesnesini oluşturur"""
    global otopark
    otopark = Otopark(adi, kapasite)
    return otopark


@app.route('/')
def anasayfa():
    """Anasayfa - Otopark durumunu gösterir"""
    if not otopark:
        return jsonify({"hata": "Otopark başlatılmamış"}), 500

    durumu = otopark.otopark_durumu()
    araclar = otopark.araclari_listele()
    alanlar = otopark.alan_durumlari()

    return jsonify({
        "sayfa": "Otopark Durumu",
        "otopark_durumu": durumu,
        "otoparkta_araclar": araclar,
        "alanlar": alanlar
    })


@app.route('/api/durum', methods=['GET'])
def durum():
    """GET /api/durum - Otopark durumunu JSON formatında döndürür"""
    if not otopark:
        return jsonify({"hata": "Otopark başlatılmamış"}), 500

    return jsonify(otopark.otopark_durumu())


@app.route('/api/araclar', methods=['GET'])
def araclar_listesi():
    """GET /api/araclar - Otoparkta bulunan araçları listeler"""
    if not otopark:
        return jsonify({"hata": "Otopark başlatılmamış"}), 500

    return jsonify({
        "toplam": len(otopark.araclari_listele()),
        "araclar": otopark.araclari_listele()
    })


@app.route('/api/alanlar', methods=['GET'])
def alanlar():
    """GET /api/alanlar - Tüm park alanlarının durumunu döndürür"""
    if not otopark:
        return jsonify({"hata": "Otopark başlatılmamış"}), 500

    durumu = otopark.otopark_durumu()
    alanlar_info = otopark.alan_durumlari()

    return jsonify({
        "otopark": durumu['otopark_adi'],
        "toplam_kapasite": durumu['toplam_kapasite'],
        "alanlar": alanlar_info
    })


@app.route('/api/arac/gir', methods=['POST'])
def arac_gir():
    """POST /api/arac/gir - Araç otoparka girer"""
    if not otopark:
        return jsonify({"hata": "Otopark başlatılmamış"}), 500

    veri = request.get_json()
    plaka = veri.get('plaka')
    tercih_edilen_alan = veri.get('tercih_edilen_alan')

    if not plaka:
        return jsonify({"hata": "Plaka girilmesi gerekli", "basarili": False}), 400

    basarili, alan_id, mesaj = otopark.arac_ekle(plaka, tercih_edilen_alan)

    return jsonify({
        "basarili": basarili,
        "plaka": plaka,
        "alan_id": alan_id,
        "mesaj": mesaj,
        "otopark_durumu": otopark.otopark_durumu()
    }), (200 if basarili else 400)


@app.route('/api/arac/cik', methods=['POST'])
def arac_cik():
    """POST /api/arac/cik - Araç otoparktan çıkar"""
    if not otopark:
        return jsonify({"hata": "Otopark başlatılmamış"}), 500

    veri = request.get_json()
    plaka = veri.get('plaka')

    if not plaka:
        return jsonify({"hata": "Plaka girilmesi gerekli", "basarili": False}), 400

    basarili, alan_id, park_suresi, mesaj = otopark.arac_cikar(plaka)

    return jsonify({
        "basarili": basarili,
        "plaka": plaka,
        "alan_id": alan_id,
        "park_suresi_dakika": park_suresi,
        "mesaj": mesaj,
        "otopark_durumu": otopark.otopark_durumu()
    }), (200 if basarili else 400)


@app.route('/api/alanlar/<int:alan_id>', methods=['GET'])
def alan_detay(alan_id):
    """GET /api/alanlar/<alan_id> - Belirli bir alanın detaylı durumunu döndürür"""
    if not otopark:
        return jsonify({"hata": "Otopark başlatılmamış"}), 500

    if alan_id not in otopark.alanlar:
        return jsonify({"hata": f"Alan {alan_id} bulunamadı", "basarili": False}), 404

    alan = otopark.alanlar[alan_id]
    return jsonify({
        "basarili": True,
        "alan": alan.durum_kontrol()
    })


@app.route('/api/istatistikler', methods=['GET'])
def istatistikler():
    """GET /api/istatistikler - Sistem istatistiklerini döndürür"""
    if not otopark:
        return jsonify({"hata": "Otopark başlatılmamış"}), 500

    durumu = otopark.otopark_durumu()

    return jsonify({
        "otopark_adi": durumu['otopark_adi'],
        "toplam_kapasite": durumu['toplam_kapasite'],
        "dolu_alan_sayisi": durumu['dolu_alan'],
        "bos_alan_sayisi": durumu['bos_alan'],
        "doluluk_orani_yuzde": float(durumu['doluluk_orani'].rstrip('%')),
        "otoparkta_arac_sayisi": len(otopark.araclari_listele()),
        "sorgulama_zamani": durumu['zamanstampa']
    })


@app.errorhandler(404)
def sayfa_bulunamadi(error):
    """404 hatasını işler"""
    return jsonify({
        "hata": "Sayfa bulunamadı",
        "kod": 404,
        "mesaj": "İstenen endpoint mevcut değil"
    }), 404


@app.errorhandler(500)
def sunucu_hatasi(error):
    """500 hatasını işler"""
    return jsonify({
        "hata": "Sunucu hatası",
        "kod": 500,
        "mesaj": str(error)
    }), 500


if __name__ == '__main__':
    # Otopark oluştur
    otopark_olustur("Çankırı Merkez Otopark", 30)

    # Test verisi ekle
    otopark.arac_ekle("34-ABC-1234")
    otopark.arac_ekle("06-XYZ-5678")
    otopark.arac_ekle("35-DEF-9012")

    # Flask uygulamasını başlat
    print("\n" + "="*60)
    print("Otopark Web API Başlatılıyor")
    print("="*60)
    print("Adres: http://127.0.0.1:5000")
    print("Doküman için: http://127.0.0.1:5000/api/durum")
    print("="*60 + "\n")

    app.run(debug=True, host='127.0.0.1', port=5000)