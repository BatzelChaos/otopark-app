[README.md](https://github.com/user-attachments/files/26067038/README.md)
# Otopark Projesi - Parking Lot Management System

Otopark Projesi, otoparkta boş ve dolu alanların yazılım aracılığıyla yönetilmesini sağlayan bir Python + Flask uygulamasıdır.

## 📋 Proje Amacı ve Kapsamı

Bu projenin temel amacı, otoparklarda boş ve dolu alanların yazılım aracılığıyla belirlenmesini sağlayan bir sistem geliştirmektir. Günümüzde özellikle büyük şehirlerde araç sahipleri otoparklarda yer bulmakta zorlanmakta, bu da hem zaman kaybına hem de trafik yoğunluğuna yol açmaktadır.

### Kapsam
- **Veri Modelleri**: ParkAlani ve Otopark sınıfları
- **Simülasyon**: Gerçekçi otopark operasyonlarını simüle etme
- **Web API**: Flask ile REST API sağlanması
- **Görselleştirme**: Otopark doluluk durumunun online takibi

## 🔧 Öncül Gereksinimler

- Python 3.8+
- Flask 2.3+
- Temel Python bilgisi (sınıflar, listeler, sözlükler)

## 📁 Dosya Yapısı

```
Otopark_Projesi/
├── Otopark_Projesi.py      # Eski versiyon (başlangıç dosyası)
├── models.py               # Veri modelleri (ParkAlani, Otopark)
├── simulator.py            # Simülasyon sistemi
├── app.py                  # Flask Web API
├── requirements.txt        # Proje bağımlılıkları
└── README.md              # Bu dosya
```

## 🚀 Kurulum ve Başlangıç

### 1. Bağımlılıkları Yükle

```bash
pip install -r requirements.txt
```

### 2. Simülasyonu Test Et

```bash
python simulator.py
```

**Örnek Çıktı:**
```
✓ GİRİŞ: 34-ABC-1234 → Alan 5
✓ GİRİŞ: 06-XYZ-5678 → Alan 12
✓ ÇIKIS: 34-ABC-1234 ← Alan 5 (2.5 dk)
```

### 3. Web API'sini Başlat

```bash
python app.py
```

**Çıktı:**
```
Otopark Web API Başlatılıyor
Adres: http://127.0.0.1:5000
```

Tarayıcınızı açıp `http://127.0.0.1:5000` adresine gidin.

## 📚 API Endpoints

### 1. Otopark Durumunu Göster
**GET** `/api/durum`

Otoparkın genel durumunu döndürür.

**Örnek Cevap:**
```json
{
  "otopark_adi": "Çankırı Merkez Otopark",
  "toplam_kapasite": 30,
  "dolu_alan": 5,
  "bos_alan": 25,
  "doluluk_orani": "16.67%",
  "zamanstampa": "2025-02-28 10:30:45"
}
```

---

### 2. Otoparkta Bulunan Araçları Listele
**GET** `/api/araclar`

Otoparkta bulunan tüm araçları listeler.

**Örnek Cevap:**
```json
{
  "toplam": 3,
  "araclar": [
    {
      "plaka": "34-ABC-1234",
      "alan_id": 5,
      "giris_zamani": "2025-02-28 10:20:15"
    },
    {
      "plaka": "06-XYZ-5678",
      "alan_id": 12,
      "giris_zamani": "2025-02-28 10:25:30"
    }
  ]
}
```

---

### 3. Tüm Alan Durumlarını Göster
**GET** `/api/alanlar`

Tüm park alanlarının detaylı durumunu döndürür.

**Örnek Cevap:**
```json
{
  "otopark": "Çankırı Merkez Otopark",
  "toplam_kapasite": 30,
  "alanlar": {
    "1": {
      "alan_id": 1,
      "konum": "Alan-1",
      "durum": "boş",
      "arac_plakasi": null,
      "giris_zamani": null
    },
    "5": {
      "alan_id": 5,
      "konum": "Alan-5",
      "durum": "dolu",
      "arac_plakasi": "34-ABC-1234",
      "giris_zamani": "2025-02-28 10:20:15"
    }
  }
}
```

---

### 4. Araç Otoparka Entrada
**POST** `/api/arac/gir`

Araç otoparka girer.

**İstek Body:**
```json
{
  "plaka": "34-ABC-1234",
  "tercih_edilen_alan": 5
}
```

**Başarılı Cevap (200):**
```json
{
  "basarili": true,
  "plaka": "34-ABC-1234",
  "alan_id": 5,
  "mesaj": "Araç 34-ABC-1234 5. alana park edildi.",
  "otopark_durumu": {
    "otopark_adi": "Çankırı Merkez Otopark",
    "toplam_kapasite": 30,
    "dolu_alan": 6,
    "bos_alan": 24,
    "doluluk_orani": "20.00%",
    "zamanstampa": "2025-02-28 10:35:20"
  }
}
```

**Başarısız Cevap (400):**
```json
{
  "basarili": false,
  "mesaj": "Otopark dolu. Boş alan bulunamadı.",
  "otopark_durumu": { ... }
}
```

---

### 5. Araç Otoparktan Çıkması
**POST** `/api/arac/cik`

Araç otoparktan çıkar.

**İstek Body:**
```json
{
  "plaka": "34-ABC-1234"
}
```

**Başarılı Cevap (200):**
```json
{
  "basarili": true,
  "plaka": "34-ABC-1234",
  "alan_id": 5,
  "park_suresi_dakika": 15.5,
  "mesaj": "Araç 34-ABC-1234 otoparktan çıkarıldı. Park süresi: 15.50 dakika.",
  "otopark_durumu": {
    "otopark_adi": "Çankırı Merkez Otopark",
    "toplam_kapasite": 30,
    "dolu_alan": 5,
    "bos_alan": 25,
    "doluluk_orani": "16.67%",
    "zamanstampa": "2025-02-28 10:50:35"
  }
}
```

---

### 6. Belirli Bir Alanın Durumunu Göster
**GET** `/api/alanlar/<alan_id>`

Belirli bir alanın detaylı durumunu döndürür.

**Örnek:** `GET /api/alanlar/5`

**Cevap:**
```json
{
  "basarili": true,
  "alan": {
    "alan_id": 5,
    "konum": "Alan-5",
    "durum": "dolu",
    "arac_plakasi": "34-ABC-1234",
    "giris_zamani": "2025-02-28 10:20:15"
  }
}
```

---

### 7. İstatistikleri Göster
**GET** `/api/istatistikler`

Sistem istatistiklerini döndürür.

**Cevap:**
```json
{
  "otopark_adi": "Çankırı Merkez Otopark",
  "toplam_kapasite": 30,
  "dolu_alan_sayisi": 5,
  "bos_alan_sayisi": 25,
  "doluluk_orani_yuzde": 16.67,
  "otoparkta_arac_sayisi": 5,
  "sorgulama_zamani": "2025-02-28 10:55:00"
}
```

## 🧪 Kod Örnekleri

### Örnek 1: Temel Kullanım (Python)

```python
from models import Otopark

# Otopark oluştur
otopark = Otopark("Çankırı Merkez Otopark", 30)

# Araç ekle
basarili, alan_id, mesaj = otopark.arac_ekle("34-ABC-1234")
print(mesaj)  # Araç 34-ABC-1234 5. alana park edildi.

# Otopark durumunu göster
print(otopark.otopark_durumu())

# Araç çıkar
basarili, alan_id, sure, mesaj = otopark.arac_cikar("34-ABC-1234")
print(mesaj)  # Araç 34-ABC-1234 otoparktan çıkarıldı. Park süresi: 2.50 dakika.
```

### Örnek 2: Simülasyon (Python)

```python
from models import Otopark
from simulator import OtoparkSimulatoru

# Otopark ve simülatör oluştur
otopark = Otopark("Çankırı Merkez Otopark", 30)
simulatoru = OtoparkSimulatoru(otopark)

# 10 giriş, 3 çıkış simüle et
simulatoru.hizli_simulasyon(giris_sayisi=10, cikis_sayisi=3)
```

### Örnek 3: API ile Kullanım (cURL)

```bash
# Durum kontrol et
curl http://127.0.0.1:5000/api/durum

# Araç gir
curl -X POST http://127.0.0.1:5000/api/arac/gir \
  -H "Content-Type: application/json" \
  -d '{"plaka": "34-ABC-1234", "tercih_edilen_alan": 5}'

# Araç çıkar
curl -X POST http://127.0.0.1:5000/api/arac/cik \
  -H "Content-Type: application/json" \
  -d '{"plaka": "34-ABC-1234"}'

# Araçları listele
curl http://127.0.0.1:5000/api/araclar
```

## 📊 Sınıf Diyagramı

```
┌─────────────────────────┐
│      AlanDurumu(Enum)   │
├─────────────────────────┤
│ BOS                     │
│ DOLU                    │
│ BAKIMDA                 │
└─────────────────────────┘
           △
           │
           │
┌─────────────────────────┐
│     ParkAlani           │
├─────────────────────────┤
│ - alan_id               │
│ - konum                 │
│ - durum                 │
│ - arac_plakasi          │
│ - giris_zamani          │
├─────────────────────────┤
│ + arac_park_et()        │
│ + arac_cikar()          │
│ + bakima_al()           │
│ + durum_kontrol()       │
└─────────────────────────┘
           △
           │ contains
           │ many
┌─────────────────────────┐
│      Otopark            │
├─────────────────────────┤
│ - otopark_adi           │
│ - toplam_kapasite       │
│ - alanlar               │
│ - arac_gecmisi          │
├─────────────────────────┤
│ + arac_ekle()           │
│ + arac_cikar()          │
│ + bos_alan_sayisi()     │
│ + dolu_alan_sayisi()    │
│ + doluluk_orani()       │
│ + araclari_listele()    │
│ + otopark_durumu()      │
└─────────────────────────┘
           △
           │ uses
           │
┌─────────────────────────┐
│  OtoparkSimulatoru      │
├─────────────────────────┤
│ - otopark               │
│ - plakalar              │
│ - simülasyon_gecmisi    │
├─────────────────────────┤
│ + rastgele_giris_olay() │
│ + rastgele_cikis_olay() │
│ + hizli_simulasyon()    │
│ + rapor_yazdir()        │
└─────────────────────────┘
```

## 🎯 Görev Dağılımı (4 Kişi için)

| Görev | Kişi | Açıklama |
|-------|------|----------|
| **Planlama** | Proje Yöneticisi | Proje amacı, kapsam, gereksinim analizi |
| **Tasarım** | Tasarımcı | Veri yapıları, UML diyagramları, akış şemaları |
| **Back-End** | Backend Geliştirici | Python kodları, API, simülasyon |
| **Front-End & Sunum** | Frontend Geliştirici | Web arayüzü, dokümantasyon, demo |

## 📝 Kodlama Standartları

- **Isimlendirme**: snake_case (değişkenler), PascalCase (sınıflar)
- **Yorum**: Tüm fonksiyonlar için docstring kullanılmalı
- **Satır Uzunluğu**: Maksimum 100 karakter
- **Girintiler**: 4 boşluk

## 🐛 Hata Giderme

### Problem: "ModuleNotFoundError: No module named 'flask'"
**Çözüm:** `pip install -r requirements.txt` komutunu çalıştırın

### Problem: "Address already in use" hatası
**Çözüm:** Önceki Flask sunucusunu kapatın veya farklı bir port kullanın:
```python
app.run(port=5001)
```

### Problem: Araç ekleme başarısız
**Çözüm:** Otoparkın dolu olup olmadığını kontrol edin:
```python
print(otopark.bos_alan_sayisi())  # Kaç boş alan kaldığını göster
```

## 🔮 Gelecek Özellikler

- [ ] Veritabanı entegrasyonu (SQLite/PostgreSQL)
- [ ] Web arayüzü (HTML/CSS/JavaScript)
- [ ] Fatura sistemi (ücretlendirme)
- [ ] Gerçek zamanlı bildirimler (WebSocket)
- [ ] Mobil uygulama (iOS/Android)
- [ ] Yapay zeka ile araç tanıma

## 📄 Lisans

Bu proje eğitim amaçlı oluşturulmuştur.

## 👥 Yazarlar

- Proje Yöneticisi
- Backend Geliştirici
- Frontend Geliştirici
- Sistem Tasarımcısı

---

**Son Güncelleme:** Şubat 28, 2026
