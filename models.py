"""
Otopark Projesi - Veri Modelleri (Models)

Bu modül, otopark sistemi için temel sınıfları içerir:
- ParkAlani: Bir park alanını temsil eder
- Otopark: Otopark yönetimini sağlayan ana sınıf
"""

from datetime import datetime
from enum import Enum


class AlanDurumu(Enum):
    """Park alanının durumunu tanımlar"""
    BOS = "boş"
    DOLU = "dolu"
    BAKIMDA = "bakımda"


class ParkAlani:
    """Tek bir park alanını temsil eder"""

    def __init__(self, alan_id, konum=None):
        """
        Parametreler:
            alan_id (int): Park alanının benzersiz kimliği
            konum (str): Park alanının konumu/sıra numarası (isteğe bağlı)
        """
        self.alan_id = alan_id
        self.konum = konum or f"Alan-{alan_id}"
        self.durum = AlanDurumu.BOS
        self.arac_plakasi = None
        self.giris_zamani = None

    def arac_park_et(self, plaka):
        """Araç alan'a park eder"""
        if self.durum == AlanDurumu.BOS:
            self.arac_plakasi = plaka
            self.durum = AlanDurumu.DOLU
            self.giris_zamani = datetime.now()
            return True
        return False

    def arac_cikar(self):
        """Araç alanı terk eder"""
        if self.durum == AlanDurumu.DOLU:
            cikis_zamani = datetime.now()
            sure = (cikis_zamani - self.giris_zamani).total_seconds() / 60  # dakika cinsinden

            self.arac_plakasi = None
            self.durum = AlanDurumu.BOS
            self.giris_zamani = None
            return True, sure
        return False, None

    def bakima_al(self):
        """Alanı bakıma alır"""
        if self.durum == AlanDurumu.BOS:
            self.durum = AlanDurumu.BAKIMDA
            return True
        return False

    def bakimdan_cikar(self):
        """Alanı bakımdan çıkarır"""
        if self.durum == AlanDurumu.BAKIMDA:
            self.durum = AlanDurumu.BOS
            return True
        return False

    def durum_kontrol(self):
        """Alan durumunu sözlük olarak döndürür"""
        # Araç varsa park süresi (dakika) hesapla
        bekleme_suresi_dk = None
        if self.durum == AlanDurumu.DOLU and self.giris_zamani:
            bekleme_suresi_dk = (datetime.now() - self.giris_zamani).total_seconds() / 60

        return {
            "alan_id": self.alan_id,
            "konum": self.konum,
            "durum": self.durum.value,
            "arac_plakasi": self.arac_plakasi,
            "giris_zamani": self.giris_zamani.strftime("%Y-%m-%d %H:%M:%S") if self.giris_zamani else None,
            "bekleme_suresi_dakika": round(bekleme_suresi_dk, 2) if bekleme_suresi_dk else None
        }


class Otopark:
    """Otopark yönetim sistemi"""

    def __init__(self, otopark_adi, toplam_kapasite):
        """
        Parametreler:
            otopark_adi (str): Otoparkın adı
            toplam_kapasite (int): Toplam park alanı sayısı
        """
        self.otopark_adi = otopark_adi
        self.toplam_kapasite = toplam_kapasite
        self.alanlar = {}
        self.arac_gecmisi = []

        # Tüm park alanlarını oluştur
        for i in range(1, toplam_kapasite + 1):
            self.alanlar[i] = ParkAlani(i)

    def arac_ekle(self, plaka, tercih_edilen_alan=None):
        """
        Araç otoparka ekler

        Parametreler:
            plaka (str): Araç plakası
            tercih_edilen_alan (int): Tercihe bağlı alan ID (isteğe bağlı)

        Döndürür:
            (bool, int, str): (başarı, alan_id, mesaj)
        """
        # Tercih edilen alanı kontrol et
        if tercih_edilen_alan and tercih_edilen_alan in self.alanlar:
            alan = self.alanlar[tercih_edilen_alan]
            if alan.arac_park_et(plaka):
                self.arac_gecmisi.append({
                    "plaka": plaka,
                    "alan_id": tercih_edilen_alan,
                    "olay": "giris",
                    "zaman": datetime.now()
                })
                return True, tercih_edilen_alan, f"Araç {plaka} {tercih_edilen_alan}. alana başarıyla park edildi."

        # Boş alan bul
        for alan_id, alan in self.alanlar.items():
            if alan.arac_park_et(plaka):
                self.arac_gecmisi.append({
                    "plaka": plaka,
                    "alan_id": alan_id,
                    "olay": "giris",
                    "zaman": datetime.now()
                })
                return True, alan_id, f"Araç {plaka} {alan_id}. alana park edildi."

        return False, None, "Otopark dolu. Boş alan bulunamadı."

    def arac_cikar(self, plaka):
        """
        Araç otoparktan çıkarır

        Parametreler:
            plaka (str): Çıkarılacak araç plakası

        Döndürür:
            (bool, int, float, str): (başarı, alan_id, parktime_dakika, mesaj)
        """
        for alan_id, alan in self.alanlar.items():
            if alan.arac_plakasi == plaka:
                basarili, sure = alan.arac_cikar()
                if basarili:
                    self.arac_gecmisi.append({
                        "plaka": plaka,
                        "alan_id": alan_id,
                        "olay": "cikis",
                        "zaman": datetime.now()
                    })
                    return True, alan_id, sure, f"Araç {plaka} otoparktan çıkarıldı. Park süresi: {sure:.2f} dakika."

        return False, None, None, f"Araç {plaka} otoparkta bulunamadı."

    def bos_alan_sayisi(self):
        """Boş alan sayısını döndürür"""
        return sum(1 for alan in self.alanlar.values() if alan.durum == AlanDurumu.BOS)

    def dolu_alan_sayisi(self):
        """Dolu alan sayısını döndürür"""
        return sum(1 for alan in self.alanlar.values() if alan.durum == AlanDurumu.DOLU)

    def doluluk_orani(self):
        """Doluluk oranını yüzde olarak döndürür"""
        dolu = self.dolu_alan_sayisi()
        return (dolu / self.toplam_kapasite) * 100

    def otopark_durumu(self):
        """Otoparkın genel durumunu sözlük olarak döndürür"""
        return {
            "otopark_adi": self.otopark_adi,
            "toplam_kapasite": self.toplam_kapasite,
            "dolu_alan": self.dolu_alan_sayisi(),
            "bos_alan": self.bos_alan_sayisi(),
            "doluluk_orani": f"{self.doluluk_orani():.2f}%",
            "zamanstampa": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

    def alan_durumlari(self):
        """Tüm alanların detaylı durumunu döndürür"""
        return {alan_id: alan.durum_kontrol() for alan_id, alan in self.alanlar.items()}

    def araclari_listele(self):
        """Otoparkta bulunan araçları listeler"""
        araclar = []
        for alan_id, alan in self.alanlar.items():
            if alan.durum == AlanDurumu.DOLU:
                araclar.append({
                    "plaka": alan.arac_plakasi,
                    "alan_id": alan_id,
                    "giris_zamani": alan.giris_zamani.strftime("%Y-%m-%d %H:%M:%S")
                })
        return araclar