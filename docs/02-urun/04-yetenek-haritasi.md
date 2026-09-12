# Yetenek haritası (MVP)

Kaynak: [MVP kapsamı](03-mvp-kapsam.html) §4 (57 Must / 10 Should / 5 Could). Yetenek (CAP), kapsam satırlarını (O-1, Ş-2, P-3…) geliştirme ve test için gruplar; her CAP, use case'lere (UC) ve fonksiyonel gereksinimlere (FR) bağlanır. Öncelik: **M** = MVP zorunlu, **S** = süre izin verirse MVP, **C** = v1.x.

| CAP | Yetenek | Kapsam satırları | Ö | Kısa tanım | UC |
|---|---|---|---|---|---|
| CAP-01 | Hesap ve organizasyon | O-1, O-2, O-6, O-8 | M | Çok kiracılı hesap; Marka › Bölge › Şube › İstasyon hiyerarşisi; Excel'den toplu yükleme; işten ayrılma/maskeleme | UC-01, UC-02 |
| CAP-02 | Kimlik ve yetki | O-3, O-4, O-5, O-7 | M | Roller ve yetki matrisi; telefon + OTP; yönetici e-posta + 2FA; ortak cihaz (kiosk) PIN; akıllı gruplar | UC-03, UC-04 |
| CAP-03 | Şablon tasarımı | Ş-1, Ş-2, Ş-3, Ş-5, Ş-6 | M | Sürümlü şablon editörü; madde türleri (onay, çoktan seçmeli, sayı, sıcaklık, metin, fotoğraf, video, imza, barkod, tarih-saat, talimat); puanlama; 30 Türkçe şablon | UC-05 |
| CAP-04 | Koşullu mantık | Ş-4 | M | (madde, cevap) → ek soru / not iste / fotoğraf iste / aksiyon oluştur / bildir / atla | UC-05, UC-08 |
| CAP-05 | Planlama ve pencereler | P-1…P-7 | M | RRULE tekrar; açılış/kapanış pencereleri (gece yarısını aşan); atama (rol/kişi/grup/istasyon; biri/herkes); otomatik çalıştırma üretimi; tatil takvimi; tek seferlik liste; hatırlatma politikası | UC-06, UC-07 |
| CAP-06 | Mobil yürütme ve kanıt | Y-1, Y-2, Y-3, Y-6, Y-9 | M | Bugün ekranı; madde tamamlama; kamera-içi kanıt, damga, sıkıştırma; gönderim ve kilit; düşük okuryazarlık tasarımı | UC-08, UC-09 |
| CAP-07 | Çevrimdışı çalışma | Y-5 | M | Yerel önbellek ve kanıt kuyruğu; arka planda senk; çakışma kuralları; 72 saat | UC-09 |
| CAP-08 | Yapılamadı ve sorun bildirimi | Y-4, Y-7 | M | Sebep seti + not + fotoğraf; kritik maddede yasak; liste dışı sorun bildirimi | UC-10, UC-11 |
| CAP-09 | Aksiyon ve eskalasyon | A-1…A-6 | M | Aksiyon kaydı (atanan, vade, öncelik, durum); otomatik oluşturma; kapanış kanıtı; zamanlı eskalasyon merdiveni; yorum dizisi; filtreli listeler | UC-12, UC-13 |
| CAP-10 | Bildirimler | Y-8, P-7 | M | Push (FCM/APNs) öncelikli; SMS yedek (kritik/eskalasyon); rol bazlı tercihler; sessiz saatler; teslimat izi | UC-07, UC-13 |
| CAP-11 | Duyuru ve onay | D-1, D-2 | M | Hedefli duyuru; "okudum" onayı; hatırlatma; onay oranı | UC-14 |
| CAP-12 | Raporlama ve dışa aktarım | R-1…R-7, R-9 | M | Operasyon ızgarası; tamamlanma/zamanındalık; başarısız madde analizi; ölçüm günlüğü; kanıt galerisi; PDF/Excel; aksiyon raporu; kişi düzeyi gecikme/eksik (skor yok) | UC-15, UC-16 |
| CAP-13 | Denetim izi ve uyum | U-1…U-6 | M | Ekle-yalnız hash zincirli olay günlüğü; denetim izi görüntüleyici; KVKK aydınlatma, dışa aktarma/silme; saklama politikası; güvenlik; biyometri yok | UC-17, UC-18 |
| CAP-14 | Yönetim paneli ve platform | W-1, W-2, W-3, W-4 | M | Kurulum sihirbazı; şube/personel yönetimi; bildirim ve eskalasyon ayarları; aktif şube sayacı (manuel faturalama) | UC-01, UC-02 |
| CAP-15 | Şablon yardımcıları | Ş-7, Ş-8 | S | Şube türüne göre varyant; SOP/PDF'ten AI ile taslak şablon | UC-05 |
| CAP-16 | Vardiya ve istasyon kolaylıkları | P-8, Y-10, Y-11 | S | Vardiya bazlı tekrar; vardiya devri notu; QR ile istasyondan başlatma | UC-06, UC-08 |
| CAP-17 | Gözden geçirme ve imza | D-3, D-4, A-3 onaylı kapanış | S | Yönetici gözden geçirme notu; imzalı belge; duyuru → şablon bağlantısı | UC-14, UC-16 |
| CAP-18 | Planlı raporlar ve API | R-8, W-5, W-7 | S | Sabah/haftalık e-posta özeti; salt okunur REST + webhook; i18n hazırlığı | UC-15 |
| CAP-19 | v1.x adayları | O-9, Ş-9, A-7, R-10, W-6 | C | SSO/dizin senkronu; formül ve kaydırıcı; özel aksiyon tipleri; pano oluşturucu; PDKS/POS/İK bağlayıcıları | — |

## Sürüm dilimi

- **GA (6. ay):** CAP-01…CAP-14 tamamı.
- **GA'da süre kalırsa:** CAP-15…CAP-18 (Should) — sıralama: CAP-16 (QR, devir notu) → CAP-18 (sabah özeti) → CAP-15 → CAP-17.
- **v1.x:** CAP-19.

## Kapsam dışı (bilinçli)

Sohbet, mesai/PDKS, vardiya planı, eğitim/LMS, sensör/prob, varlık/iş emri, AI fotoğraf değerlendirme, WhatsApp kanalı, self-servis kayıt/ödeme, kişi skoru, franchise portalı — gerekçeleri MVP kapsamı §5'te.
