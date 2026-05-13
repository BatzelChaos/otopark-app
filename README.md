# 🅿️ Otopark Yönetim Sistemi

Otoparkların doluluğunu gerçek zamanlı olarak takip edebilen, web arayüzü ile görselleştiren Flask tabanlı otopark yönetim sistemi.

## 📌 Proje Özeti

Bu sistem, otoparkların:
- Park yerlerinin durumunu (dolu/boş) takip eder
- Kat bazlı doluluk yüzdesini hesaplar  
- Web arayüzü ile görselleştirir
- Kolay navigasyon sağlar

## 🎯 Özellikler

✅ Tüm otoparkları listeleme  
✅ Otopark katlarını görüntüleme  
✅ Kat detaylarını 2D grid olarak gösterme  
✅ Park yerlerini renkli olarak kategorileme (Dolu: Kırmızı, Boş: Yeşil)  
✅ Doluluk yüzdesini otomatik hesaplama  
✅ Progress bar gösterimi  

## 🛠️ Kullanılan Teknolojiler

| Teknoloji | Versiyon |
|-----------|----------|
| Python | 3.12.3 |
| Flask | 2.3.2 |
| HTML5 | - |
| CSS3 | - |
| XML | - |

## 📦 Bağımlılıklar

```
Flask==2.3.2
Werkzeug==2.3.6
```

## 🚀 Hızlı Başlangıç

### 1️⃣ Sanal Ortamı Oluştur

```bash
cd /home/good_vibes/Desktop/otopark-app
python3 -m venv venv
source venv/bin/activate
```

### 2️⃣ Bağımlılıkları Yükle

```bash
pip3 install -r requirements.txt
```

### 3️⃣ Uygulamayı Başlat

```bash
python3 xmlParser.py
```

**Çıktı:**
```
 * Serving Flask app 'xmlParser'
 * Debug mode: off
 * Running on http://127.0.0.1:5000
```

### 4️⃣ Tarayıcıda Aç

- **Ana Sayfa:** http://127.0.0.1:5000/
- **Otopark 1:** http://127.0.0.1:5000/otopark/1
- **Otopark 1, Kat 1:** http://127.0.0.1:5000/otopark/1/floor/1

## 📁 Dosya Yapısı

```
otopark-app/
├── xmlParser.py                     # Ana Flask uygulaması
├── templates/
│   ├── otoparklar.html             # Otopark listesi sayfası
│   ├── home.html                   # Kat listesi sayfası
│   └── index.html                  # Kat detayları sayfası
├── static/
│   └── styles.css                  # CSS stilleri
├── example_otopark_data/
│   ├── data1.xml                   # Ana Otopark verileri
│   ├── data2.xml                   # Merkez Otopark verileri
│   └── data3.xml                   # AVM Otopark verileri
├── requirements.txt                # Bağımlılıklar
├── README.md                       # Bu dosya
├── KOD_ACIKLAMASI.md              # Detaylı kod açıklaması
└── SONUC_RAPORU.md                # Proje sonuç raporu
```

## 🗂️ Veri Yapısı (XML Format)

### Örnek XML Dosyası

```xml
<parking>
    <floor level="1">
        <grid cols="5" rows="5">
            <cell col="1" row="1" status="free">A1</cell>
            <cell col="2" row="1" status="occupied">A2</cell>
            <cell col="3" row="1" status="free">A3</cell>
            <!-- ... -->
        </grid>
    </floor>
    <floor level="2">
        <!-- ... -->
    </floor>
</parking>
```

### XML Parametreleri

| Parametre | Açıklama | Örnek |
|-----------|----------|-------|
| `level` | Kat numarası | 1, 2, 3 |
| `cols` | Kolon sayısı | 5 |
| `rows` | Satır sayısı | 5 |
| `col` | Hücrenin kolon pozisyonu | 1-5 |
| `row` | Hücrenin satır pozisyonu | 1-5 |
| `status` | Park durumu | "free" / "occupied" |

## 🌐 Web Arayüzü

### Sayfalar

#### 1. Ana Sayfa (http://127.0.0.1:5000/)
- Tüm otoparkları liste halinde gösterir
- Her otopark için doluluğu yüzde ve progress bar ile gösterir
- Otoparka tıklayarak detaylara gitme imkânı

#### 2. Otopark Detayları (http://127.0.0.1:5000/otopark/1)
- Seçilen otoparktaki tüm katları gösterir
- Her katın doluluğunu yüzde ile gösterir
- Katların ortalamasını progress bar ile gösterir

#### 3. Kat Detayları (http://127.0.0.1:5000/otopark/1/floor/1)
- Seçilen katın park yerlerini 2D grid olarak gösterir
- Dolu parkları kırmızı, boş parkları yeşil renkle gösterir
- Park yeri adlarını (A1, A2, vb.) gösterir
- Kat istatistiklerini gösterir

## 🎨 Renkler ve Gösterim

| Durum | Renk | Anlamı |
|-------|------|--------|
| Boş Park | 🟢 Yeşil | Park yeri kullanılabilir |
| Dolu Park | 🔴 Kırmızı | Park yeri meşgul |
| Progress Bar Dolgu | 🔴 Kırmızı | Dolu alan oranı |
| Progress Bar Arka | 🟢 Yeşil | Boş alan oranı |

## 💻 Kod Yapısı

### Ana Modüller

#### `xmlParser.py`

**Fonksiyonlar:**
- `parsenode(node)`: XML düğümünü sözlüğe çevir
- `get_cells(node)`: Tüm park yerlerini bul
- `stat_calculation(cells)`: Doluluk yüzdesini hesapla
- `get_floors(root)`: Tüm katların bilgisini topla
- `get_otoparklar()`: Tüm otoparkların bilgisini al

**Routes (URL Yolları):**
- `GET /`: Otopark listesi
- `GET /otopark/<id>`: Otopark katları
- `GET /otopark/<id>/floor/<level>`: Kat detayları

### Şablonlar (Templates)

- `otoparklar.html`: Jinja2 döngüsü ile dinamik liste
- `home.html`: Kat listesi ve progress bar gösterimi
- `index.html`: CSS Grid kullanarak 2D park düzeni

### Stil (CSS)

- `styles.css`: Responsive tasarım ve grid layout

## 🔍 Veri İşlem Akışı

```
1. Kullanıcı Ana Sayfa'ya Gider
   ↓
2. get_otoparklar() tüm XML dosyaları okur
   ↓
3. Her otopark için doluluğu hesaplar
   ↓
4. otoparklar.html'de gösterir
   ↓
5. Kullanıcı Otopark'a Tıklar
   ↓
6. get_floors() seçilen otopark verilerini okur
   ↓
7. Her kat için istatistik hesaplar
   ↓
8. home.html'de katları gösterir
   ↓
9. Kullanıcı Kat'a Tıklar
   ↓
10. show_floor() kat verilerini işler
    ↓
11. index.html'de 2D grid gösterir
```

## 🧪 Test Sonuçları

| Test | Durum |
|------|-------|
| XML Parsing | ✅ Başarılı |
| Flask Başlatma | ✅ Başarılı |
| Ana Sayfa | ✅ Çalışıyor |
| Otopark Detayları | ✅ Çalışıyor |
| Kat Detayları | ✅ Çalışıyor |
| CSS Stili | ✅ Uygulanıyor |

## ⚙️ Sistem Gereksinimleri

- **İşletim Sistemi:** Linux, Windows, macOS
- **Python Versiyonu:** 3.8+
- **Bellek:** Minimum 256MB
- **Disk Alanı:** 50MB

## 🐛 Hata Ayıklama

### Sorun: "Flask import bulunamadı"
```bash
# Sanal ortamı etkinleştir
source venv/bin/activate
# Yeniden kur
pip3 install -r requirements.txt
```

### Sorun: "XML dosyası bulunamadı"
- `example_otopark_data/` klasörünün bulunduğunu kontrol et
- XML dosyalarının adlarını kontrol et

### Sorun: "Port 5000 kullanımda"
```bash
# Farklı portta çalıştır
python3 -c "from xmlParser import app; app.run(port=5001)"
```

## 📚 Belgeleme

Detaylı kod açıklaması için: [KOD_ACIKLAMASI.md](KOD_ACIKLAMASI.md)  
Proje sonuç raporu için: [SONUC_RAPORU.md](SONUC_RAPORU.md)

## 🎓 Eğitim Amaçlı Kullanım

Bu proje aşağıdaki konuların öğrenilmesi için uygundur:
- Flask web framework'ü
- XML parsing
- HTML/CSS/Jinja2 şablonları
- RESTful API tasarımı
- Python OOP

## 📈 Gelecek İyileştirmeler

- [ ] Veritabanı entegrasyonu
- [ ] Gerçek zamanlı güncellemeler (WebSocket)
- [ ] Kullanıcı kimlik doğrulaması
- [ ] İstatistiksel raporlar
- [ ] Mobil uygulaması
- [ ] Docker containerization

## 👥 Grup Üyeleri

- **Erenalp Demir** - Rapor Lideri, Grup Yöneticisi
- **Fatih Kerem Arslan** - Geliştirici
- **Kadir Umut Akbaş** - Grup Üyesi

## 📄 Lisans

Bu proje Yazılım Mühendisliği dönem ödevi olarak geliştirilmiştir.

## 📞 Destek ve İletişim

Sorular veya öneriler için lütfen proje repositorısine issue açınız.

---

**Son Güncelleme:** 13 Mayıs 2026  
**Versiyon:** 1.0 (Nihai)  
**Durum:** ✅ Üretim Hazır
