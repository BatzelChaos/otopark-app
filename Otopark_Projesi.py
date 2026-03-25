"""
Otopark Projesi - Ana Dosya

Bu dosya, otopark sistemi için başlangıç noktasıdır.
Yeni modüler yapı (models.py, simulator.py, app.py) kullanılmaktadır.

Başlangıç sınıfı (eski versiyon) öğrenme amaçlı burada tutulmuştur.
Üretim ve gerçek uygulamalar için models.py kullanılacaktır.
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
    """
    Proje başlangıç noktası
    """
    
    print("\n" + "="*60)
    print("OTOPARK PROJESİ - ANA DOSYA")
    print("="*60)
    
    print("\n[SEÇENEK 1] Basit Otopark Sınıfı ile Test:")
    print("-" * 60)
    
    otopark_basit = OtoparkBasit(5)
    
    otopark_basit.arac_ekle("34-ABC-1234")
    otopark_basit.arac_ekle("06-XYZ-5678")
    otopark_basit.arac_ekle("35-DEF-9012")
    
    print(f"\nBoş kapasite: {otopark_basit.bos_kapasite()} alan")
    print(f"Doluluk oranı: {otopark_basit.doluluk_orani():.2f}%")
    
    otopark_basit.arac_cikar("34-ABC-1234")
    
    print("\n" + "="*60)
