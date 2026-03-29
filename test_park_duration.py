"""
Basit Test: ParkAlani.durum_kontrol() - Bekleme Süresi
Bu script, yeni bekleme_suresi_dakika alanının çalışıp çalışmadığını gösterir.
"""

from models import Otopark
import time

# Otopark oluştur
otopark = Otopark("Test Otopark", 5)

# Araç ekle
basarili, alan_id, mesaj = otopark.arac_ekle("34-ABC-1234")
print(f"✓ {mesaj}\n")

# 1. Alan detayı (hemen sonra - 0 saniye)
alan = otopark.alanlar[alan_id]
detay = alan.durum_kontrol()
print("Alan Durumu (araç az önce park edildi):")
print(f"  Plaka: {detay['arac_plakasi']}")
print(f"  Durum: {detay['durum']}")
print(f"  Giriş: {detay['giris_zamani']}")
print(f"  Bekleme Süresi: {detay['bekleme_suresi_dakika']} dakika\n")

# 2 saniye bekle, sonra tekrar kontrol et
print("2 saniye bekleniyor...\n")
time.sleep(2)

detay = alan.durum_kontrol()
print("Alan Durumu (2 saniye sonra):")
print(f"  Plaka: {detay['arac_plakasi']}")
print(f"  Durum: {detay['durum']}")
print(f"  Bekleme Süresi: {detay['bekleme_suresi_dakika']} dakika")
print(f"  (≈ {detay['bekleme_suresi_dakika'] * 60:.0f} saniye)\n")

# Araç çıkar
basarili, alan_id, sure, mesaj = otopark.arac_cikar("34-ABC-1234")
print(f"✓ {mesaj}\n")

# 3. Alan detayı (araç çıktıktan sonra)
detay = alan.durum_kontrol()
print("Alan Durumu (araç çıktıktan sonra):")
print(f"  Plaka: {detay['arac_plakasi']}")
print(f"  Durum: {detay['durum']}")
print(f"  Bekleme Süresi: {detay['bekleme_suresi_dakika']} dakika")