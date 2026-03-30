"""
Otopark Projesi - Veri Simülatörü (Simulator)

Bu modül, otopark sistemini test etmek için örnek veriler ve simülasyonlar oluşturur.
Rastgele araç giriş-çıkışlarını simüle eder ve sistem performansını test eder.
"""

import random
import time
from datetime import datetime, timedelta
from models import Otopark


class OtoparkSimulatoru:
    """Otopark sistemini simüle eden sınıf"""

    def __init__(self, otopark):
        """
        Parametreler:
            otopark (Otopark): Simüle edilecek otopark nesnesi
        """
        self.otopark = otopark
        self.plakalar = self._plaka_listesi_olustur()
        self.simülasyon_gecmisi = []

    @staticmethod
    def _plaka_listesi_olustur(adet=50):
        """Rastgele plaka listesi oluşturur"""
        plakalar = []
        for i in range(adet):
            # Türk plaka formatı: 34-ABC-1234
            sil = random.randint(1, 81)  # İl kodu
            harf = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=3))
            sayi = random.randint(1000, 9999)
            plaka = f"{sil:02d}-{harf}-{sayi}"
            plakalar.append(plaka)
        return plakalar

    def rastgele_giris_olay(self):
        """Rastgele bir araç giriş olayı simüle eder"""
        plaka = random.choice(self.plakalar)
        basarili, alan_id, mesaj = self.otopark.arac_ekle(plaka)

        event = {
            "zaman": datetime.now(),
            "olay_tipi": "giris",
            "plaka": plaka,
            "basarili": basarili,
            "alan_id": alan_id,
            "mesaj": mesaj
        }
        self.simülasyon_gecmisi.append(event)
        return event

    def rastgele_cikis_olay(self):
        """Rastgele bir araç çıkış olayı simüle eder"""
        araclar = self.otopark.araclari_listele()
        if not araclar:
            return None

        arac = random.choice(araclar)
        plaka = arac["plaka"]
        basarili, alan_id, park_suresi, mesaj = self.otopark.arac_cikar(plaka)

        event = {
            "zaman": datetime.now(),
            "olay_tipi": "cikis",
            "plaka": plaka,
            "basarili": basarili,
            "alan_id": alan_id,
            "park_suresi_dakika": park_suresi,
            "mesaj": mesaj
        }
        self.simülasyon_gecmisi.append(event)
        return event

    def calisma_saati_simülasyonu(self, dakika=10, giris_olasılığı=0.6, cikis_olasılığı=0.3):
        """
        Belirli bir süre otopark operasyonlarını simüle eder

        Parametreler:
            dakika (int): Simülasyon süresi (dakika)
            giris_olasılığı (float): Her saniyede giriş olayı olasılığı (0-1)
            cikis_olasılığı (float): Her saniyede çıkış olayı olasılığı (0-1)
        """
        print(f"\n{'='*60}")
        print(f"Simülasyon Başlıyor: {dakika} dakika boyunca")
        print(f"{'='*60}\n")

        baslangic = datetime.now()
        while (datetime.now() - baslangic).total_seconds() < dakika * 60:
            # Giriş olayı
            if random.random() < giris_olasılığı:
                olay = self.rastgele_giris_olay()
                if olay["basarili"]:
                    print(f"✓ GİRİŞ: {olay['plaka']} → Alan {olay['alan_id']}")
                else:
                    print(f"✗ GİRİŞ BAŞARISIZ: {olay['plaka']} (Otopark dolu)")

            # Çıkış olayı
            if random.random() < cikis_olasılığı:
                olay = self.rastgele_cikis_olay()
                if olay and olay["basarili"]:
                    print(f"✓ ÇIKIS: {olay['plaka']} ← Alan {olay['alan_id']} ({olay['park_suresi_dakika']:.1f} dk)")

            # Sistem durumunu yazdır (her 3 saniyede bir)
            durumu = self.otopark.otopark_durumu()
            print(f"   [{durumu['dolu_alan']}/{durumu['toplam_kapasite']} dolu - {durumu['doluluk_orani']}]", end="\r")

            time.sleep(1)

        print("\n\n" + "="*60)
        print("Simülasyon Tamamlandı")
        print("="*60)
        self.rapor_yazdir()

    def hizli_simulasyon(self, giris_sayisi=10, cikis_sayisi=3):
        """Hızlı bir simülasyon çalıştırır (gecikmesiz)"""
        print(f"\n{'='*60}")
        print(f"Hızlı Simülasyon: {giris_sayisi} giriş, {cikis_sayisi} çıkış")
        print(f"{'='*60}\n")

        # Giriş olayları
        for i in range(giris_sayisi):
            olay = self.rastgele_giris_olay()
            if olay["basarili"]:
                print(f"✓ {i+1}. GİRİŞ: {olay['plaka']} → Alan {olay['alan_id']}")
            else:
                print(f"✗ {i+1}. GİRİŞ BAŞARISIZ: {olay['plaka']}")

        print()

        # Çıkış olayları
        for i in range(cikis_sayisi):
            olay = self.rastgele_cikis_olay()
            if olay and olay["basarili"]:
                print(f"✓ {i+1}. ÇIKIS: {olay['plaka']} ← Alan {olay['alan_id']} ({olay['park_suresi_dakika']:.1f} dk)")

        print()
        self.rapor_yazdir()

    def rapor_yazdir(self):
        """Simülasyon raporunu yazdırır"""
        durumu = self.otopark.otopark_durumu()
        print(f"\nOtopark: {durumu['otopark_adi']}")
        print(f"Kapasite: {durumu['dolu_alan']}/{durumu['toplam_kapasite']}")
        print(f"Doluluk Oranı: {durumu['doluluk_orani']}")
        print(f"Otoparkta Araçlar: {len(self.otopark.araclari_listele())}")

        if self.simülasyon_gecmisi:
            giris_olaylari = [o for o in self.simülasyon_gecmisi if o['olay_tipi'] == 'giris']
            cikis_olaylari = [o for o in self.simülasyon_gecmisi if o['olay_tipi'] == 'cikis']

            basarili_giriş = sum(1 for o in giris_olaylari if o['basarili'])
            basarili_cikis = sum(1 for o in cikis_olaylari if o['basarili'])

            print(f"\nİstatistikler:")
            print(f"  Toplam Giriş Denemesi: {len(giris_olaylari)}")
            print(f"  Başarılı Giriş: {basarili_giriş}")
            print(f"  Toplam Çıkış Denemesi: {len(cikis_olaylari)}")
            print(f"  Başarılı Çıkış: {basarili_cikis}")

    def kullanıcı_belirtilen_test(self, islemler):
        """
        Kullanıcı tarafından belirtilen işlemleri test eder

        Parametreler:
            islemler (list): [{"olay": "giris", "plaka": "34-ABC-1234"}, ...]
        """
        print(f"\n{'='*60}")
        print(f"Belirtilen İşlemler Test Ediliyor")
        print(f"{'='*60}\n")

        for islem in islemler:
            if islem.get("olay") == "giris":
                plaka = islem.get("plaka")
                basarili, alan_id, mesaj = self.otopark.arac_ekle(plaka)
                print(f"{'✓' if basarili else '✗'} {mesaj}")

            elif islem.get("olay") == "cikis":
                plaka = islem.get("plaka")
                basarili, alan_id, sure, mesaj = self.otopark.arac_cikar(plaka)
                print(f"{'✓' if basarili else '✗'} {mesaj}")

        print()
        self.rapor_yazdir()


def main():
    """Test fonksiyonu"""
    # Otopark oluştur
    otopark = Otopark("Cankiri Merkez Otopark", 20)

    # Simülatörü oluştur
    simulatoru = OtoparkSimulatoru(otopark)

    # Hızlı test çalıştır
    simulatoru.hizli_simulasyon(giris_sayisi=15, cikis_sayisi=5)


if __name__ == "__main__":
    main()