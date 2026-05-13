# Fatih'in Otopark Projesi - Detaylı Kod Açıklaması

## 📋 Genel Bakış

Bu proje, otoparkların doluluğunu gerçek zamanlı olarak takip edebilen ve web arayüzü ile görselleştiren bir Flask uygulamasıdır. Sistem XML formatındaki otopark verilerini okur, işler ve dinamik bir web sayfasında gösterir.

---

## 🛠️ Sistem Mimarisi

```
xmlParser.py (Ana Uygulama)
├── XML Dosyaları
├── Routes (URL yönlendirmeler)
└── Templates (HTML Sayfaları)
    ├── otoparklar.html (Ana sayfa)
    ├── home.html (Kat listesi)
    └── index.html (Detaylı kat görünümü)
```

---

## 📁 Dosya Yapısı ve İşlevleri

### 1. **xmlParser.py** (Ana Uygulama Dosyası)

**Açıklama:** Flask web uygulamasının ana dosyasıdır. XML verilerini işler, veritabanı gibi hareket eder ve web sayfalarına veri gönderir.

#### 1.1 İthalatlar (Import) - Satırlar 1-2
```python
import xml.etree.ElementTree as ET
from flask import Flask, render_template
```
- `ElementTree`: XML dosyalarını okuyup işlemek için kullanılır
- `Flask`: Web uygulaması oluşturmak için
- `render_template`: HTML şablonlarına Python verisi göndermek için

#### 1.2 Flask Uygulaması Başlatması - Satır 4
```python
app = Flask(__name__)
```
- Yeni bir Flask web uygulaması oluşturur
- `__name__` otomatik olarak app adını belirler

#### 1.3 `parsenode()` Fonksiyonu - Satırlar 6-12
```python
def parsenode(node):
    return {
        "tag": node.tag,           # XML etiketi (örn: "grid", "cell")
        "value": (node.text or "").strip(),    # Düğümün metni
        "attributes": node.attrib,  # Düğümün özellikleri
        "children": [parsenode(child) for child in node]  # Alt düğümler
    }
```
**Amaç:** XML düğümlerini Python sözlüğüne çevirir
**Örnek:**
```xml
<grid cols="5" rows="5">
    <cell col="1" row="1" status="free">A1</cell>
</grid>
```
Sonuç:
```python
{
    "tag": "grid",
    "value": "",
    "attributes": {"cols": "5", "rows": "5"},
    "children": [{...}, {...}]
}
```

#### 1.4 `get_cells()` Fonksiyonu - Satırlar 14-21
```python
def get_cells(node):
    cells = []
    if node["tag"] == "cell":
        cells.append(node)
    for child in node["children"]:
        cells.extend(get_cells(child))
    return cells
```
**Amaç:** Tüm `<cell>` düğümlerini bulur ve bir listeye dönüştürür (Özyinelemeli arama)
**İşlem:** 
- Eğer düğüm "cell" ise listeye ekle
- Tüm alt düğümleri kontrol et ve al
- Sonunda tüm hücrelerin listesini döndür

#### 1.5 `stat_calculation()` Fonksiyonu - Satırlar 23-31
```python
def stat_calculation(cells):
    """Hücrelerin istatistiklerini hesapla"""
    total_cells = len(cells)
    occupied = sum(1 for c in cells if c["attributes"].get("status") == "occupied")
    percentage_parking = (occupied / total_cells * 100) if total_cells > 0 else 0
    return {
        "total_cells": total_cells,
        "occupied": occupied,
        "percentage_parking": percentage_parking
    }
```
**Amaç:** Park doluluğu yüzdesini hesaplar
**Hesaplama:**
- Toplam hücre sayısı
- Dolu hücre sayısı (status="occupied" olan)
- Doluluğun yüzdesi = (dolu / toplam) × 100

#### 1.6 `get_floors()` Fonksiyonu - Satırlar 33-51
```python
def get_floors(root):
    floors = []
    for floor in root.findall("floor"):
        level = floor.attrib.get("level")
        grid_node = floor.find("grid")
        if grid_node is None:
            continue
        data = parsenode(grid_node)
        cells = get_cells(data)
        stats = stat_calculation(cells)
        
        floors.append({
            "level": level,
            "percentage_parking": stats["percentage_parking"],
            "total_cells": stats["total_cells"]
        })
    return floors
```
**Amaç:** Tüm katların bilgisini toplar
**Adımlar:**
1. XML'de tüm `<floor>` öğelerini bul
2. Her kat için:
   - Kat seviyesi (level) al
   - Grid verilerini parse et
   - Tüm hücreleri al
   - İstatistikleri hesapla
3. Katın bilgisini listeye ekle

#### 1.7 `get_otoparklar()` Fonksiyonu - Satırlar 53-88
```python
def get_otoparklar():
    otoparklar = [
        {"id": 1, "isim": "Ana Otopark", "dosya": "data1.xml"},
        {"id": 2, "isim": "Merkez", "dosya": "data2.xml"},
        {"id": 3, "isim": "AVM", "dosya": "data3.xml"},
    ]

    for otopark in otoparklar:
        dosya_yolu = f"example_otopark_data/{otopark['dosya']}"
        try:
            tree = ET.parse(dosya_yolu)
            root = tree.getroot()

            total_cells = 0
            occupied = 0

            for floor in root.findall("floor"):
                grid_node = floor.find("grid")
                if grid_node is None:
                    continue
                data = parsenode(grid_node)
                cells = get_cells(data)

                total_cells += len(cells)
                occupied += sum(1 for c in cells if c["attributes"].get("status") == "occupied")

            percentage = (occupied / total_cells * 100) if total_cells > 0 else 0
            otopark["doluluk"] = round(percentage, 2)

        except:
            otopark["doluluk"] = 0

    return otoparklar
```
**Amaç:** Tüm otoparkların doluluğunu hesapla
**Veritabanı:** 
- Üç otopark tanımlanır (data1.xml, data2.xml, data3.xml)
- Her otopark:
  - `id`: Benzersiz tanımlayıcı
  - `isim`: İnsan tarafından okunur ad
  - `dosya`: XML dosya adı
  - `doluluk`: Hesaplanan doluluğun yüzdesi

#### 1.8 Route: `/` - Satırlar 91-94 (Otopark Listesi)
```python
@app.route("/")
def otopark_listesi():
    otoparklar = get_otoparklar()
    return render_template("otoparklar.html", otoparklar=otoparklar)
```
**URL:** `http://127.0.0.1:5000/`
**İşlem:**
- Tüm otoparkları al
- HTML şablonuna veri gönder
- Tarayıcıda göster

#### 1.9 Route: `/otopark/<int:id>` - Satırlar 96-112 (Otopark Detayı)
```python
@app.route("/otopark/<int:id>")
def otopark_detay(id):
    otoparklar = get_otoparklar()
    otopark = next((o for o in otoparklar if o["id"] == id), None)
    
    dosya_yolu = f"example_otopark_data/{otopark['dosya']}"
    tree = ET.parse(dosya_yolu)
    root = tree.getroot()
    
    if not otopark:
        return "Otopark bulunamadı", 404

    floors_percentage_data = get_floors(root)
    return render_template("home.html", floors=floors_percentage_data, id=id)
```
**URL:** `http://127.0.0.1:5000/otopark/1`
**Adımlar:**
1. URL'den `id` değerini al (1, 2 veya 3)
2. Seçilen otopark bulunur
3. Otopark XML dosyası aç
4. Tüm katların bilgisini al
5. HTML şablonuna veri gönder

#### 1.10 Route: `/otopark/<int:id>/floor/<int:level>` - Satırlar 114-132 (Kat Detayı)
```python
@app.route("/otopark/<int:id>/floor/<int:level>")
def show_floor(id, level):
    otoparklar = get_otoparklar()
    otopark = next((o for o in otoparklar if o["id"] == id), None)

    if not otopark:
        return "Otopark bulunamadı", 404

    dosya_yolu = f"example_otopark_data/{otopark['dosya']}"
    tree = ET.parse(dosya_yolu)
    root = tree.getroot()

    floor = root.find(f"./floor[@level='{level}']")
    if floor is None:
        return "Bu kat yok", 404

    grid_node = floor.find("grid")
    data = parsenode(grid_node)
    cells = get_cells(data)
    stats = stat_calculation(cells)

    return render_template("index.html", node=data, cells=cells, level=level, stats=stats, otopark=otopark)
```
**URL:** `http://127.0.0.1:5000/otopark/1/floor/1`
**Adımlar:**
1. Otopark ve kat bilgisini al
2. XML'de belirtilen kattı bul
3. Kat verilerini parse et
4. Tüm park yerlerini ve istatistikleri al
5. Detaylı HTML sayfasına gönder

#### 1.11 Uygulama Başlatması - Satır 134
```python
if __name__ == "__main__":
    app.run(debug=False)
```
- Dosya doğrudan çalıştırıldığında uygulamayı başlat
- `debug=False`: Üretim modunda çalış

---

### 2. **templates/otoparklar.html** (Ana Sayfa)

**Amaç:** Tüm otoparkları liste halinde gösterir

```html
<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="{{url_for('static',filename='styles.css')}}">
    <title>Otopark Listesi</title>
</head>
<body>
    <h1>Otopark Listesi</h1>
    <ul>
        {% for otopark in otoparklar %}
            <li>
                <a href="/otopark/{{ otopark.id }}">
                    {{ otopark.isim }} - {{ otopark.doluluk }}%
                    <div class="progressbar">
                        <div class="progressbar_fill" style="width: {{ otopark.doluluk|default(0)|int}}%">
                        </div>
                    </div>
                </a>
            </li>
        {% endfor %}
    </ul>
</body>
</html>
```

**Açıklama:**
- Python veri döngüsü: `{% for otopark in otoparklar %}`
- Her otopark için link oluştur: `/otopark/{{ otopark.id }}`
- Doluluğu progress bar ile göster

---

### 3. **templates/home.html** (Otopark Katları)

**Amaç:** Seçilen otoparktaki tüm katları listeler

```html
<!DOCTYPE html>
<html>
    <head>
    <link rel="stylesheet" href="{{url_for('static',filename='styles.css')}}">
    </head>
    <body>
        <h1>Otopark Katları</h1>
        <div>
        <a href="/">Geri Don</a>
        </div>
        <ul>
        {% for floor in floors %}
            <li>
            <a href="/otopark/{{ id }}/floor/{{ floor.level }}">
                Kat {{ floor.level }}
            </a>
             - {{"%.2f"|format(floor.percentage_parking|float)}}% 
             <div class="progressbar">
                <div class="progressbar_fill" style="width: {{ floor.percentage_parking|default(0)|int}}%">
                </div>
             </div>
            </li>
        {% endfor %}
        </ul>
    </body>
</html>
```

**Önemli Filtreler:**
- `{{"%.2f"|format(...)}}`: Sayıyı 2 ondalak basamağa formatla
- `|float`: String'i float'a çevir
- `|int`: Float'ı integer'a çevir

---

### 4. **templates/index.html** (Kat Detayı - Park Yerleri)

**Amaç:** Bir kattaki tüm park yerlerini gösterir

```html
<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="{{url_for('static',filename='styles.css')}}">
</head>
<body>
    <h1>OTOPARK A - KAT {{level}}</h1>

    <div class="stats">
        <a href="/otopark/{{ otopark.id }}">Geri Don</a>
        <br>
        <a href="/">Otopark Listesi</a>
        <br>
        <p>Toplam Park Sayisi: {{stats.total_cells}}</p>
        <p>Park Dolulugu: {{stats.percentage_parking|round(2)}}%</p>
    </div>

    <div class="parkinglot" style="--cols:{{node.attributes.get('cols',5)|int}}; --rows:{{node.attributes.get('rows',5)|int}};">
        {% for cell in cells %}
            <div class="spot"
                style="grid-row: {{ cell.attributes.row }};
                    grid-column: {{ cell.attributes.col }};">
                
                {% if cell.attributes.status == "occupied" %}
                    <div class="car red"> {{cell.value}} </div>
                {% else %}
                    <div class="car green"> {{cell.value}} </div>
                {% endif %}
            </div>
        {% endfor %}
    </div>
</body>
</html>
```

**Açıklama:**
- CSS Grid layout kullanılır
- Her hücre (cell) görselleştirilir
- Dolu parklar kırmızı, boş parklar yeşil gösterilir
- `|round(2)`: Sayıyı 2 ondalaka basamağa yuvarla

---

### 5. **static/styles.css** (Stil Dosyası)

**Temel Stiller:**

```css
/* Sayfa Ayarları */
body {
    background-color: lightblue;    /* Arka plan rengi */
    font-family: "Segoe UI", Roboto, sans-serif;
    font-size: 20px;
    color: #253238;
}

/* Park Yerleri Grid */
.parkinglot {
    display: grid;
    grid-template-columns: repeat(var(--cols), 70px);
    grid-template-rows: repeat(var(--rows), 70px);
}

/* Park Yeri Hücresi */
.spot {
    width: 70px;
    height: 70px;
    display: flex;
    align-items: center;
    justify-content: center;
}

/* Araç Şekli */
.car {
    width: 90px;
    height: 70px;
    border: 2px solid black;
    display: flex;
    justify-content: center;
    align-items: center;
    color: white;
    font-size: 18px;
    clip-path: polygon(...);  /* Araba şekli */
}

/* Renk Kodları */
.red { background: red; }      /* Dolu park */
.green { background: green; }  /* Boş park */

/* Progress Bar */
.progressbar {
    width: 100px;
    height: 10px;
    background: green;
}

.progressbar_fill {
    height: 100%;
    background: red;
    width: 0%;  /* JavaScript tarafından değiştirilir */
}
```

---

### 6. **example_otopark_data/** (XML Veri Dosyaları)

**Yapı Örneği (data1.xml):**
```xml
<parking>
    <floor level="1">
        <grid cols="5" rows="5">
            <cell col="1" row="1" status="free">A1</cell>
            <cell col="2" row="1" status="occupied">A2</cell>
            ...
        </grid>
    </floor>
    <floor level="2">
        ...
    </floor>
</parking>
```

**XML Öğeleri:**
- `<parking>`: Kök öğe
- `<floor level="X">`: X. kat
- `<grid cols="Y" rows="Z">`: Y sütun, Z satır
- `<cell>`: Tek bir park yeri
  - `col`: Kolon numarası
  - `row`: Satır numarası
  - `status`: "free" (boş) veya "occupied" (dolu)
  - İçerik: Park yeri adı (A1, A2, vb.)

---

## 🚀 Çalıştırma Kılavuzu

### 1. Bağımlılıkları Kur
```bash
cd /home/good_vibes/Desktop/otopark-app
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

### 2. Uygulamayı Başlat
```bash
source venv/bin/activate
python3 xmlParser.py
```

### 3. Tarayıcıda Aç
- Ana sayfa: `http://127.0.0.1:5000/`
- Otopark detayı: `http://127.0.0.1:5000/otopark/1`
- Kat detayı: `http://127.0.0.1:5000/otopark/1/floor/1`

---

## 🔧 Yapılan Düzeltmeler

### Hata 1: CSS Yolu Yanlış
**Sorun:** `template.html` dosyasında CSS yolu `./css/styles.css` olarak yazılmıştı, oysa CSS dosyası `static/` klasöründedir.
```html
<!-- Yanlış -->
<link rel="stylesheet" href="{{ url_for('static', filename='./css/styles.css') }}">

<!-- Doğru -->
<link rel="stylesheet" href="{{ url_for('static', filename='styles.css') }}">
```

### Hata 2: `stat_calculation()` Fonksiyonu Eksik
**Sorun:** İstatistik hesaplaması başında eksik, sonunda yinelendi.
**Çözüm:** Fonksiyonu XML parser başına taşındı ve yineleneni silindi.

### Hata 3: Tekrarlanan Fonksiyon
**Sorun:** `stat_calculation()` fonksiyonu iki kez yazılmıştı.
**Çözüm:** Yinelenen sürüm silindi.

### Hata 4: `template.html` Kullanılmıyor
**Sorun:** `template.html` dosyası hiçbir yerde kullanılmıyordu.
**Durumu:** Silmeme karar verildi (ileride kullanılabilir).

---

## 📊 Veri Akışı Diyagramı

```
Kullanıcı Tarayıcısı
    ↓
Flask Route (otopark_listesi)
    ↓
get_otoparklar() → XML dosyaları oku
    ↓
otoparklar.html render et
    ↓
Otopark Listesi Göster

--- Kullanıcı /otopark/1 tıklar ---

Flask Route (otopark_detay)
    ↓
get_floors() → XML kat bilgisini al
    ↓
home.html render et
    ↓
Katlar Listesi Göster

--- Kullanıcı Katı tıklar ---

Flask Route (show_floor)
    ↓
Kat verilerini parse et
    ↓
index.html render et
    ↓
Park Yerleri Grid Göster
```

---

## 💡 Önemli Kavramlar

### 1. **Jinja2 Şablonları**
- `{{ değişken }}`: Değişkeni HTML'ye gömme
- `{% for ... %}...{% endfor %}`: Döngü
- `{% if ... %}...{% endif %}`: Koşul
- `|filter`: Veri filtreleme

### 2. **XML Parsing**
- `ET.parse()`: XML dosyasını aç
- `findall()`: Tüm eşleşen öğeleri bul
- `find()`: İlk eşleşen öğeyi bul
- `.attrib`: Öğenin özelliklerini al

### 3. **Flask Routing**
- `@app.route()`: URL yönlendirmesi
- `<int:id>`: URL parametresi
- `render_template()`: HTML şablonunu render et

---

## 🎯 Sistem Özellikleri

✅ **Çalışan Özellikler:**
- Tüm otoparkları listele
- Otopark katlarını listele
- Kat detaylarını göster
- Park yerlerini renkli grid olarak göster
- Doluluğu yüzde olarak hesapla
- Progress bar ile görselleştir

📈 **İyileştirme Fırsatları:**
- Veritabanına geçilmesi
- Gerçek zamanlı veri güncellenmesi
- Sayfa yenileme otomasyonu (AJAX)
- Mobil arayüz iyileştirmesi
- Hata yönetiminin geliştirilmesi

---

## 📝 Sonuç

Fatih'in kodu, otopark doluluğunu etkili bir şekilde takip eden ve kullanıcı dostu bir web arayüzü sunan iyi yapılandırılmış bir Flask uygulamasıdır. XML tabanlı veri depolaması ve modüler fonksiyon yapısı, kodun bakım ve genişletilmesi açısından iyidir.
