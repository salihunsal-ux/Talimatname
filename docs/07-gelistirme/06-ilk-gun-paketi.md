# Geliştirici ilk gün paketi

Ekip modeli: iki serbest geliştirici (ADR-0009, seçenek A); seçim süreci [07-serbest-gelistirici-secimi.md](07-serbest-gelistirici-secimi.md). Bu belge sözleşme imzalanan iki geliştiriciye Sprint 0'ın ilk günü (hedef **19 Ekim 2026**; takvim 05-sprint0 §1) gönderilir (backend/web ve mobil için ortak; rol notları işaretli). Amaç: ilk gün sonunda ortam ayakta, ürün anlaşılmış, ilk hafta işi belli. Bu belge yeni bir şey anlatmaz; doğru sırayla doğru belgeye götürür.

## Hoş geldin: 5 cümlede ürün

Talimatname, çok şubeli yeme-içme zincirlerinin şubelere verdiği tekrarlı talimatları (açılış, kapanış, hijyen, soğuk zincir) WhatsApp gruplarından çıkarıp kanıtlı ve raporlanabilir hâle getirir. Personel listeyi şube tabletinden veya telefondan tamamlar, fotoğraf ve ölçümle kanıtlar, yapamadığını sebebiyle bildirir. Sistem pencereyi izler, kaçırılanı ve kritik olanı bildirir; yönetici her sabah istisna odaklı bir ızgara, sabah özeti ve doğrulama kodlu PDF ile görür. İlk sürüm bilerek küçük: 4 rol, 6 madde türü, tek sabit kural, sabit eskalasyon (ADR-0008). Kişi puanı yok, WhatsApp yok, biyometri yok.

Ürünü 10 dakikada görmek için: [Blok 8 prototipi](../05-tasarim/05-prototip/blok8-prototip.html) (personel + şube müdürü), [yönetici web prototipi](../05-tasarim/05-prototip/yonetici-web-prototip.html), [örnek çalıştırma PDF'i](../05-tasarim/06-kanit-raporu/01-calistirma-raporu.html). Üçü aynı Kadıköy senaryosunu anlatır.

## Gün 0 — kurucunun hazırlığı (paket gönderilmeden önce)

- [ ] GitHub organizasyonu `talimatname`: `Talimatname` (bu depo, okuma), `talimatname-api`, `talimatname-mobile`, `talimatname-web`, `talimatname-infra` (boş, dal koruması açık); iki geliştirici davet edilmiş
- [ ] GitHub Projects panosu: S0 kontrol listesi + S1–S2 hikâyeleri (03-backlog) kart olarak yüklü
- [ ] Sözleşme + NDA + KVKK taahhüdü imzalı (07 §7); mini görev ücretleri ödenmiş
- [ ] Sağlayıcı hesapları: staging için ücretsiz ya da AB altyapı hesabı (ADR-0012 — gerçek veri yok), SMS sağlayıcı test hesabı, Firebase projesi, Apple Developer ve Google Play (şirket adına — başvuru günler sürer, erken başlayın), e-posta gönderim servisi. **Üretim TR sağlayıcısı Sprint 0'da seçilmez**, kısa listesi çıkarılır (karar Sprint 2 sonu)
- [ ] Alan adı alınmış (`talimatname.app` → `staging.talimatname.app`) — 03-isim-ve-marka bekleyen iş
- [ ] Takvim davetleri: her gün 10:00 15 dk; **19 Ekim** 11:00 Sprint 0 açılışı (1 saat); **30 Ekim** Sprint 0 gözden geçirme
- [ ] Bu paketi e-postayla gönder (aşağıdaki şablon) — cuma, ilk günden önce

## Gönderim e-postası (şablon)

> Konu: Talimatname — ilk gün paketi (19 Ekim)
>
> Merhaba [ad], Pazartesi başlıyoruz. Ekte/aşağıda ilk gün paketi var; okuma sırası ve ortam kurulumu orada. GitHub organizasyonuna davetiniz gitti; `Talimatname` deposu ürün belgeleridir, `docs/07-gelistirme/06-ilk-gun-paketi.md` ile başlayın. Sizin spike'ınız: [Backend: B ve D · Mobil: A ve C] — `docs/07-gelistirme/05-sprint0-ve-teknik-spike.md` §4. Pazartesi 11:00'de 1 saatlik açılışta ürünü prototipler üzerinden anlatacağım; 10:00 günlükleri Salı başlar. Sorular için bana yazın; 24 saat içinde dönerim. — [kurucu]

## 1. gün

| Saat | Ne | Nerede |
|---|---|---|
| 1 | Hesaplar: GitHub organizasyonu ([org adı]), backlog aracı (GitHub Projects), staging sağlayıcı konsolu (yalnızca backend), sahte servis anahtarları yok — hepsi `.env.example` | Kurucu davet eder |
| 2–3 | Okuma: [kodlama hazırlık indeksi](00-kodlama-hazirlik-indeksi.md) 1–5 (ürün merkezi, vizyon, v1 kapsamı, senaryolar, iş kuralları) — en önemlisi **iş kuralları**: pencere, tolerans, puan, eskalasyon, kanıt | ~2 saat |
| 4–5 | Ortam: `talimatname-infra/dev` → `make dev` (PostgreSQL, Redis, MinIO, sahte SMS/push/TSA, MailHog) · API 8000'de · tohum v0 · mobil: Flutter 3.x, emülatör, `.env` API adresi · web: `VITE_API_URL` | [02-repo-ve-ortam-kurulumu.md](02-repo-ve-ortam-kurulumu.md) |
| 6 | Kahve Durağı test zincirini tanı: 25 şube, 3 bölge, kullanıcılar, şablonlar | [06-test/03](../06-test/03-test-verisi-ve-ortam.md) |
| 7 | Kurucuyla 30 dk: soruların; Sprint 0 takvimi ve senin spike'ın | [05-sprint0-ve-teknik-spike.md](05-sprint0-ve-teknik-spike.md) §3–4 |

Gün sonu ölçütü: `make dev` çalışıyor, OpenAPI açılıyor, mobil emülatörde iskelet ekran, kendi spike'ının kabul ölçütünü kendi cümlelerinle söyleyebiliyorsun.

## 1. hafta

| Rol | Gün 2–5 |
|---|---|
| Backend / web | Depo iskeleti (FastAPI, Alembic, pytest, ruff, mypy), `audit.emit()` ve RLS iskeleti, OpenAPI yayını → **Spike B** (RRULE pencere motoru, 2 gün) → **Spike D** (push → SMS teslim izi, 1,5 gün) |
| Mobil | Depo iskeleti (Riverpod, Drift, üretilmiş istemci), tasarım token'ları `ThemeData` → **Spike A** (çevrimdışı kuyruk + idempotent senk, 3 gün) → **Spike C** (kamera → damga → SHA-256, 2 gün) |
| Ortak | Kural spesifikasyon fikstürleri formatı (JSON; pencere/durum, puan, sabit kural) — iki taraf aynı dosyaları geçer |

Spike'ların her biri için brief [05 §4](05-sprint0-ve-teknik-spike.md)'te: soru → deney → kabul ölçütü → çıktı. "Geçmedi" geçerli sonuçtur; ADR notuna yazılır.

## Çalışma kuralları (kısa)

- Dal: `feat/ST-123-kisa-ad`; PR + 1 inceleme + CI yeşil; squash. Commit Türkçe, `ST-123: …`. [02-repo](02-repo-ve-ortam-kurulumu.md)
- Hikâye "hazır" ve "bitti" tanımları: [04-tanimlar-dor-dod.md](04-tanimlar-dor-dod.md). Bitti = testler (birim + ilgili TC) + `audit.emit()` + OpenAPI güncel + demo edilebilir.
- Zaman UTC saklanır, şube saat diliminde değerlendirilir; iş günü = pencere başlangıç tarihi (BR-01). Cihaz saati güvenilmez (BR-13).
- Kanıt iki kopya (ham + damgalı), gönderilmiş kayıt değişmez, düzeltme "ek" kayıttır (ADR-0004). Silme yok; durum/maskeleme (BR-21/22).
- Kişisel veri: kanıt içeriği loglara ve hata izlemeye düşmez; destek erişimi maskeli. [06-kvkk](../04-gereksinimler/06-kvkk-ve-guvenlik.md)
- v1'de olmayanı yapma: duyuru, koşul editörü, ağırlıklı puan, herkes-tamamlasın, ek kayıt, aksiyon yorum/onay, eskalasyon editörü, gruplar, ayarlar paneli, 2FA, denetim izi ekranı, TSA, KVKK ekranı, Excel/paylaşım, raporların çoğu, video/imza/barkod, QR — tam liste [02-urun/06](../02-urun/06-v1-cekirdek-kapsam.md). Bir hikâye bunlardan birine kayıyorsa PO'ya sor.

## Ritim

- Her gün 10:00, 15 dk: dün / bugün / engel (yazılı da olur).
- Sprint 2 hafta; planlama Pazartesi 1 saat, gözden geçirme + demo Cuma 1 saat, geriye bakış 30 dk.
- PO = kurucu; ürün soruları için tek muhatap. Cevap 24 saat içinde gelmezse hikâyeyi "bloke" işaretle, sıradakine geç.
- Pilot geri bildirimi Sprint 5'ten itibaren backlog'a girer; öncelik PO'da.

## İlk hafta cevaplanacak sorular (sağlayıcı ve araç seçimleri)

| Soru | Karar veren | Ne zaman |
|---|---|---|
| Staging altyapısı: ücretsiz/AB yeterli (ADR-0012), tek şart gerçek veri olmaması | Backend + PO | Gün 7 |
| Üretim TR sağlayıcı **kısa listesi** (yönetilen PostgreSQL var mı, S3 uyumlu depo, DPA belgesi, yedek) | Backend + PO | Kısa liste gün 7; karar Sprint 2 sonu |
| SMS sağlayıcı (OTP + kritik bildirim; teslim raporu API'si şart) | Backend | Gün 7 |
| Push: FCM/APNs kurulumu; içerik asgari (KVKK) | Mobil | Spike D ile |
| Hata izleme / performans (Sentry vb.; kişisel veri maskeleme) | Backend | Gün 9 |
| Mağaza hesapları (Google Play, App Store) — kurucu adına | PO | Sprint 1 |

## Sık takılınanlar

- **Kural motoru nerede?** v1'de kural sabittir (FR-0405); backend ve mobil aynı JSON fikstürleri geçer; editör v1.1'de bunun üstüne gelir.
- **Gece yarısı:** 22:00–01:30 penceresi açılış gününe yazılır; tolerans 120 dk → 03:30 "kaçırıldı"; Spike B'nin ilk fikstürü budur.
- **Çevrimdışı:** cevaplar ve kanıtlar UUID ile kuyrukta; `PUT /answers/{uuid}` idempotent; senk 2 dk; 500 kanıt sınırı. Spike A.
- **Bildirim:** push → 10 dk teslim yoksa SMS (yalnızca kritik); sessiz saat 23:00–07:00 (kritik hariç). Spike D.
- **Neyi kim görür:** rol × kapsam matrisi [06-kvkk](../04-gereksinimler/06-kvkk-ve-guvenlik.md); yatay yetki testi zorunlu (TC-010/011).
