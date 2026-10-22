# Yetenek haritası

Kaynak: [v1 çekirdek kapsamı](06-v1-cekirdek-kapsam.md) (ADR-0008). Yetenek (CAP), kapsam satırlarını gruplar; her CAP use case'lere (UC) ve fonksiyonel gereksinimlere (FR) bağlanır. Sürüm: **v1** ilk sürüm · **v1.1** pilot sonrası · **v2** daha sonra. CAP numaraları korunur; ertelenen CAP'ler listede kalır.

| CAP | Yetenek | v1 içeriği | v1.1'e bırakılan | Sürüm | UC |
|---|---|---|---|---|---|
| CAP-01 | Hesap ve organizasyon | Çok kiracılı hesap; Marka › Bölge › Şube › İstasyon; Excel içe aktarma (şube, personel); pasifleştirme | Kimlik maskeleme ekranı (v1: destek betiği) | v1 | UC-01, UC-02 |
| CAP-02 | Kimlik ve yetki | 4 rol × kapsam; telefon + OTP; yönetici e-posta + şifre; kiosk cihaz kaydı, PIN, kilit; şube müdürünün PIN ataması (E-1) | 2FA; akıllı gruplar; Gözlemci rolü | v1 | UC-03, UC-04 |
| CAP-03 | Şablon tasarımı | Sürümlü editör (yayın hemen); 6 madde türü + talimat; zorunlu / fotoğraf zorunlu / kritik; sıcaklık aralığı; yüzde puan; 9 şablon kütüphanesi; yayın doğrulaması | Video/imza/barkod/tarih-saat; ağırlık ve eşik; tarihli yayın; 30 şablon | v1 | UC-05 |
| CAP-04 | Koşullu mantık | Tek sabit kural: başarısız cevapta fotoğraf + not; kritik → aksiyon | Kural editörü ve altı eylem | v1 sabit | UC-05, UC-08 |
| CAP-05 | Planlama ve pencereler | RRULE tekrar; pencere ve gece yarısı; tolerans; çalışma saatinden türetme; atama rol/kişi/herkes ("biri tamamlasın", ilk açan alır — E-2); üretim; kapalı gün; tek seferlik liste; sabit iki hatırlatma; günlük yeniden atama | "Herkes tamamlasın"; vardiya bazlı tekrar; hatırlatma ayarları | v1 | UC-06, UC-07, UC-19 |
| CAP-06 | Mobil yürütme ve kanıt | Bugün; madde tamamlama (tek kullanıcı, kaldığı yerden devam); kamera doğrudan, 1–3 fotoğraf, sıkıştırma, damga, hash; gönderim kilidi; açılışta dün gece özeti (E-3); erişilebilirlik | Ek kayıt; çoklu kullanıcı/madde kilidi; QR ile başlatma; video | v1 | UC-08, UC-09 |
| CAP-07 | Çevrimdışı çalışma | Aynen: önbellek, kuyruk, arka plan senk, zaman düzeltmesi, idempotency, kuyruk sınırları, senk ekranı | — | v1 | UC-09 |
| CAP-08 | Yapılamadı ve sorun bildirimi | Yapılamadı (sabit sebep seti, kritikte yok); sorun bildir (fotoğraf + not, sabit kategori) → şube müdürü → aksiyona çevir / kapat | Sebep/kategori setleri yönetimi; sebep raporu; yükseltme | v1 | UC-10, UC-11 |
| CAP-09 | Aksiyon ve eskalasyon | Aksiyon açık/kapalı, not, isteğe bağlı fotoğraf; otomatik oluşturma (kritik, yapılamadı, kaçırma), sabit vadeler; listeler; sabit eskalasyon kuralı; sabah özeti (E-5); kritik anında bildirim (E-6) | Durum makinesi, yorum dizisi, onaylı kapanış, merdiven editörü | v1 | UC-12, UC-13 |
| CAP-10 | Bildirimler | Push; SMS (OTP, kritik, push teslim olmazsa); sabit sessiz saat; teslimat izi; token yönetimi; kanal-bağımsız arayüz | Tercih ekranı | v1 | UC-07, UC-13 |
| CAP-11 | Duyuru ve onay | — | Tamamı | v1.1 | UC-14 |
| CAP-12 | Raporlama ve dışa aktarım | İstisna odaklı ızgara (E-4); çalıştırma detayı; basit kanıt galerisi; sıcaklık günlüğü; aylık tek sayfa (E-7); çalıştırma PDF'i ve dönem PDF'i (doğrulama kodlu, arka plan üretim); "Bölgem" mobil listesi | Sıralama, ısı haritası, sebep dağılımı, aksiyon raporu, kişi takibi, Excel, paylaşım bağlantısı | v1 | UC-15, UC-16 |
| CAP-13 | Denetim izi ve uyum | Ekle-yalnız hash zincirli olay günlüğü (arka plan); zincir doğrulama komutu (iç araç); güvenlik temel; biyometri yok; aydınlatma + konum izni; saklama 24 ay (arka plan); KVKK talepleri destek betiğiyle | Denetim izi ekranı; RFC 3161; KVKK talep ekranı; 2FA | v1 | UC-17 (arka plan), UC-18 (süreç) |
| CAP-14 | Yönetim paneli ve platform | 4 adımlı sihirbaz (tek plan); şube/personel/cihaz yönetimi; aktif şube sayacı; i18n hazırlığı | Ayarlar paneli; API/webhook | v1 | UC-01, UC-02 |
| CAP-15 | Şablon yardımcıları | — | Şube türü varyantı; AI taslak | v1.1 | UC-05 |
| CAP-16 | Vardiya ve istasyon kolaylıkları | Açılışta dün gece özeti (E-3, CAP-06'da) | Vardiya bazlı tekrar; QR | v1.1 | UC-06, UC-08 |
| CAP-17 | Gözden geçirme ve imza | — | Tamamı | v1.1 | UC-20 |
| CAP-18 | Planlı raporlar ve API | Sabah özeti (E-5, CAP-09'da) | Salt okunur API; webhook | v1.1 | UC-15 |
| CAP-19 | v2 adayları | — | SSO; formül/kaydırıcı; özel aksiyon tipleri; pano oluşturucu; PDKS/POS/İK | v2 | — |
| CAP-20 | Madde kütüphanesi ve işletme türü paketleri | Veri modeli alanları (boş); 9 şablon içeriği | Kütüphane maddesi (sürümlü, etiketli), editörde kütüphaneden ekle, hesap kütüphanesi, kaynak güncelleme bandı, işletme türü paketleri, hesap içi set uygulama ([ADR-0010](../adr/0010-madde-kutuphanesi-v1-1.md), [08-madde-kutuphanesi.md](08-madde-kutuphanesi.md)); v2: başka dikeyler, marka kütüphanesi (franchise) | v1.1 | UC-05, UC-01 |

## Sürüm dilimi

- **v1 (GA, 10. sprint):** CAP-01…CAP-10 (v1 içerikleri), CAP-12, CAP-13, CAP-14.
- **v1.1 (pilot geri bildirimiyle sıralanır):** CAP-20 (ilk epic, ADR-0010), CAP-11, CAP-15, CAP-17, CAP-18 ve yukarıdaki "v1.1'e bırakılan" sütunu. Aday sıra: madde kütüphanesi ve paketler → duyuru/onay → koşul editörü → herkes tamamlasın → aksiyon yorumları/onayı → raporlar → denetim izi ekranı + TSA → KVKK ekranı → 2FA → ayarlar → Excel/paylaşım → video/imza/barkod → QR → gruplar → varyant → AI.
- **v2:** CAP-19.

## Kapsam dışı (bilinçli)

Sohbet, mesai/PDKS, vardiya planı, eğitim/LMS, sensör/prob, varlık/iş emri, AI fotoğraf değerlendirme, WhatsApp kanalı, self-servis kayıt/ödeme, kişi skoru, franchise portalı — gerekçeleri 03-mvp-kapsam.html §5'te.
