"""
Otopark Projesi - Ana Dosya

Bu dosya, otopark sistemi için başlangıç noktasıdır.
Yeni modüler yapı (models.py, simulator.py, app.py) kullanılmaktadır.

Başlangıç sınıfı (eski versiyon) eğitim amaçlı burada tutulmuştur.
Üretim ve gerçek uygulamalar için models.py kullanınız.
"""

class OtoparkBasit:
    """
    Basit otopark sınıfı (başlangıç versiyonu)

    Not: Bu sınıf eğitim amaçlı oluşturulmuştur.
    Gerçek uygulamalar için models.py dosyasında bulunan
    Otopark sınıfını kullanınız.
    """

    def __init__(self, kapasite):
        """
        Basit otopark nesnesi oluşturur

        Parametreler:
            kapasite (int): Toplam araç kapasitesi
        """
        self.kapasite = kapasite
        self.araclar = []

    def arac_ekle(self, arac):
        """Araç otoparka ekler"""
        if len(self.araclar) < self.kapasite:
            self.araclar.append(arac)
            print(f"✓ {arac} otoparka eklendi.")
        else:
            print(f"✗ {arac} eklenemedi - Otopark dolu!")

    def arac_cikar(self, arac):
        """Araç otoparktan çıkarır"""
        if arac in self.araclar:
            self.araclar.remove(arac)
            print(f"✓ {arac} otoparktan çıkarıldı.")
        else:
            print(f"✗ {arac} otoparkta bulunamadı.")

    def bos_kapasite(self):
        """Boş kapasite sayısını döndürür"""
        return self.kapasite - len(self.araclar)

    def doluluk_orani(self):
        """Doluluk oranını yüzde olarak döndürür"""
        return (len(self.araclar) / self.kapasite) * 100


if __name__ == "__main__":
    print("\n" + "="*60)
    print("OTOPARK PROJESİ - ANA DOSYA")
    print("="*60)

    # --- SEÇENEK 1: Basit Otopark ile Test ---
    print("\n[SEÇENEK 1] Basit Otopark Sınıfı ile Test:")
    print("-" * 60)

    otopark_basit = OtoparkBasit(5)

    otopark_basit.arac_ekle("34-ABC-1234")
    otopark_basit.arac_ekle("06-XYZ-5678")
    otopark_basit.arac_ekle("35-DEF-9012")

    print(f"\nBoş kapasite: {otopark_basit.bos_kapasite()} alan")
    print(f"Doluluk oranı: {otopark_basit.doluluk_orani():.2f}%")

    otopark_basit.arac_cikar("34-ABC-1234")

    # --- SEÇENEK 2: Yeni Modüler Yapı ile Test ---
    print("\n\n[SEÇENEK 2] Yeni Modüler Yapı ile Test:")
    print("-" * 60)

    try:
        from models import Otopark, ParkAlani
        from simulator import OtoparkSimulatoru

        otopark = Otopark("Çankırı Merkez Otopark", 10)

        print("\nAraçlar ekleniyor:")
        basarili1, alan1, mesaj1 = otopark.arac_ekle("34-ABC-1234")
        print(f"  {mesaj1}")

        basarili2, alan2, mesaj2 = otopark.arac_ekle("06-XYZ-5678")
        print(f"  {mesaj2}")

        basarili3, alan3, mesaj3 = otopark.arac_ekle("35-DEF-9012")
        print(f"  {mesaj3}")

        durumu = otopark.otopark_durumu()
        print(f"\nOtopark Durumu:")
        print(f"  Adı: {durumu['otopark_adi']}")
        print(f"  Toplam kapasite: {durumu['toplam_kapasite']}")
        print(f"  Dolu alanlar: {durumu['dolu_alan']}")
        print(f"  Boş alanlar: {durumu['bos_alan']}")
        print(f"  Doluluk oranı: {durumu['doluluk_orani']}")

        print(f"\nAraç çıkışı:")
        basarili, alan_id, sure, mesaj = otopark.arac_cikar("34-ABC-1234")
        print(f"  {mesaj}")

        araclar = otopark.araclari_listele()
        print(f"\nOtoparkta kalan araçlar: {len(araclar)} araç")
        for arac in araclar:
            print(f"  - {arac['plaka']} (Alan {arac['alan_id']})")

        print("\n" + "-"*60)
        print("✓ Modüler yapı başarıyla çalıştı!")
        print("-"*60)

    except ImportError:
        print("\n⚠️  Hata: models.py dosyası bulunamadı!")
        print("models.py, simulator.py ve app.py dosyalarının")
        print("Otopark_Projesi.py ile aynı klasörde olduğundan emin olun.")

    print("\n" + "="*60)
    print("SONRAKI ADIMLAR:")
    print("="*60)
    print("1. Simülasyonu çalıştırın:")
    print("   python simulator.py")
    print("\n2. Web API'sini başlatın:")
    print("   python app.py")
    print("\n3. Tarayıcıda açın:")
    print("   http://127.0.0.1:5000")
    print("="*60 + "\n")