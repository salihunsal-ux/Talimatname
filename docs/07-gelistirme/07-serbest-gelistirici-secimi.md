# Serbest geliştirici ilanı ve seçim süreci (ADR-0009, seçenek A)

> **ADR-0013 (22 Ekim):** iki pozisyon **sırayla** aranır. Önce **panel/arka uç** geliştiricisi (Faz A, hemen); mobil geliştirici ilanı Faz A'nın 3.–4. haftasında çıkar, başlangıcı 6.–8. hafta. Aşağıdaki iki rol tanımı ve süreç geçerli; yalnızca eşzamanlılık ve takvim değişti — **ilan metni yayından önce tek pozisyona göre güncellenmeli**.

Hedef takvim (1 Ekim 2026'da yeniden kuruldu): ilan **2 Ekim** → başvuru 9 Ekim → görüşme ve mini görev 10–15 Ekim → sözleşme 16 Ekim → **Sprint 0 başlangıcı 19 Ekim** → Sprint 1 2 Kasım. Aday bulunmazsa bir hafta kaydırılır; Kasım'a sarkarsa pilot ölçümü Mart'a gider ve tampon tükenir (05-sprint0 §1).

Gönderilebilir ilan metni: [ilan/serbest-gelistirici-ilani.html](ilan/serbest-gelistirici-ilani.html) (PDF'i de aynı klasörde). Depo özel olduğu için adaylar bu belgeyi değil ilanı görür; belgeye erişim sözleşmeyle.

## 1. İki rol

| | Backend / web | Mobil |
|---|---|---|
| Yapacağı | FastAPI + PostgreSQL (RLS, Alembic, Redis kuyruk), OpenAPI, RRULE pencere motoru, bildirim servisi, PDF üretimi; Sprint 5'ten sonra React paneli (yarı zaman) | Flutter (Riverpod, Drift), çevrimdışı kuyruk + idempotent senk, kamera → damga → hash, kiosk modu, düşük segment Android performansı |
| Zorunlu | Python 3.11+, FastAPI veya eşdeğeri, PostgreSQL (göç, indeks, RLS fikri), test yazma alışkanlığı, Docker; en az bir üretimde çalışan API | Flutter 3.x ile mağazada en az bir uygulama; yerel veritabanı ve senk deneyimi; kamera/dosya eklentileri; iOS + Android derleme |
| Artı | React + TypeScript; zaman dilimi/takvim işleri; KVKK farkındalığı; TR bulut/SMS sağlayıcı deneyimi | Kiosk/ortak cihaz, arka plan işleri (WorkManager/BGTask), Patrol/entegrasyon testi, tasarım token'larıyla çalışma |
| Süre | Tam zamanlı, Sprint 0–10 (~22 hafta) + 2 sprint tampon seçeneği | Aynı |
| Kapı | Sprint 2 sonu devam/dur (K1); 2 hafta bildirim | Aynı |

## 2. İlan metni (kısa; tam sürüm ilan/ klasöründe)

> **Talimatname — iki serbest geliştirici arıyoruz (Flutter · Python/FastAPI)**
> Çok şubeli yeme-içme zincirleri için şube talimat listelerini kanıtlı hâle getiren bir ürün geliştiriyoruz: personel listeyi tabletten tamamlar, fotoğraf ve sıcaklıkla kanıtlar; merkez her sabah istisnaları görür. Kapsam, gereksinimler (175 FR), ekranlar, 128 kabul testi ve 10 sprintlik backlog hazır; tıklanabilir prototipler ve ürünü tek oturumda anlatan 10 sayfalık özellik föyü var. Sizden beklediğimiz: 2 haftalık sprintlerle, küçük ama sağlam bir ilk sürümü Şubat 2027'de yayına almak.
> **Backend/web:** FastAPI, PostgreSQL (RLS), Redis, OpenAPI; sonra React paneli. **Mobil:** Flutter, çevrimdışı öncelikli, kamera, kiosk.
> Tam zamanlı, uzaktan, ~22 hafta; sprint bazlı ücret; 3 saatlik ücretli mini görevle seçim. Başvuru: [e-posta] — CV/portföy + 3 satır: neden bu ürün, en zor çevrimdışı/zaman dilimi problemi, müsaitlik tarihi.

Yayın kanalları: LinkedIn (kişisel + ilan), Türkiye Flutter ve Python toplulukları (Discord/Telegram grupları, Kommunity etkinlik ağı), Kariyer.net/Kolay İK serbest ilanı, tanıdık tavsiyesi (en iyi kanal — mesaj şablonu §6), gerekirse Upwork/Toptal (İngilizce, daha pahalı).

## 3. Seçim adımları

| Adım | Süre | Elek |
|---|---|---|
| 1 · Başvuru eleme | 10 dk/aday | Zorunlu şartlar; mağazada/üretimde çalışan iş; "3 satır" cevabının somutluğu |
| 2 · Görüşme (45 dk, çevrimiçi) | 6–8 aday | §4 soruları; prototipi ekranda gösterip "burada ne kırılır?" sorusu |
| 3 · Ücretli mini görev (3 saat, ₺[3–5 bin], 48 saat teslim) | 3–4 aday | §5; teslim: depo bağlantısı + 10 dk açıklama görüşmesi |
| 4 · Referans + teklif | 2 aday | 1 referans araması; sözleşme başlıkları §7 |

Her adayda iki kişi puanlar (kurucu + teknik danışman/tanıdık bir kıdemli geliştirici); rubrik §5.

## 4. Görüşme soruları (45 dk)

**Ortak (15 dk)**
1. Prototipte kapanış listesini gösterin: "Personel 23:20'de aralık dışı sıcaklık girdi, Wi-Fi yok. Bu kayıt sunucuya nasıl, ne zaman, hangi zamanla ulaşır?" — beklenen: cihaz UUID, kuyruk, sunucu zamanı düzeltmesi, idempotency.
2. "Gönderilmiş kayıt değiştirilemez" ilkesini nasıl uygularsınız; düzeltme nasıl olur? — beklenen: ek kayıt, olay günlüğü, hash zinciri fikri.
3. KVKK: kanıt fotoğrafı ve konum verisi için ne yapar, ne yapmazsınız? — beklenen: asgari veri, logda maskeleme, TR barındırma, biyometri yok.
4. Son projede en çok ne kaydı; nasıl fark ettiniz? Sprint ritmi ve PR incelemesiyle çalıştınız mı?
5. Müsaitlik, günlük ritim (10:00 15 dk), tarife.

**Backend/web (15 dk)**
6. 22:00–01:30 penceresi, tolerans 120 dk, Europe/Istanbul: hangi iş gününe yazılır, "kaçırıldı" ne zaman tetiklenir, kural değişince başlanmış çalıştırmalara ne olur? (RRULE + pencere, ADR-0005)
7. Çok kiracılı veritabanında hesap izolasyonunu nasıl kurarsınız? RLS mi uygulama katmanı mı, neden? Yatay yetki ihlali testini nasıl yazarsınız?
8. "Push gitti, 10 dk içinde okunmadıysa SMS" — Redis/gecikmeli iş tasarımı; sessiz saat istisnası.
9. Alembic göçünde geri alma; RLS politikası göçte nasıl yönetilir?
10. React: büyük bir ızgarayı (25 şube × 30 gün) nasıl çizersiniz; ne zaman sanallaştırırsınız?

**Mobil (15 dk)**
6. Drift/SQLite kuyruğu: uygulama öldürülünce, cihaz yeniden başlayınca, 500 kayıt birikince ne olur? Senk sırası, çakışma, kısmi başarı.
7. Kamera: galeriyi nasıl kapatırsınız; ≤ 300 KB sıkıştırma ve SHA-256'yı düşük segment cihazda 3 saniyenin altına nasıl indirirsiniz?
8. Kiosk: 2 dk hareketsizlik kilidi, PIN geçişi, kullanıcı değişince yerel veri ayrımı.
9. Riverpod ile durum yönetimi: liste ekranında 15 madde, üçü sıcaklık; yeniden çizim maliyeti.
10. iOS arka plan senk sınırları; kullanıcıya "senk bekliyor" nasıl gösterilir?

## 5. Mini görevler (3 saat, ücretli) ve rubrik

**Backend — pencere motoru.** Verilen: 6 fikstür (JSON): günlük 22:00–01:30 tolerans 120 (Europe/Istanbul); her 2 saat 10–22; haftalık Pazartesi 14:00–17:00 tolerans 240; kapalı gün; Europe/Berlin yaz saati geçiş gecesi; 7 gün ileri üretimde tekillik. İstenen: `pencere(kural, saat_dilimi, tarih) → (başlangıç, bitiş, tolerans_sonu, iş_günü)` + `durum(pencere, gönderim_zamanı) → zamanında | geç | kaçırıldı`, pytest ile 6 fikstür geçer, README'de 5 satır tasarım notu. `python-dateutil` serbest.

**Mobil — çevrimdışı kuyruk + kamera.** Verilen: 5 maddelik liste (JSON), sahte uç nokta (`PUT /answers/{uuid}` — 200 döner, tekrarında da 200; verilen küçük Python sunucusu veya httpbin). İstenen: Flutter uygulaması; maddeleri uçak modunda işaretle → yerel kuyruk (UUID); "Senkle" → idempotent gönderim, bekleyen sayısı ekranda; uygulama öldürülüp açılınca kuyruk durur; bir madde için kamera açılır, çekilen fotoğrafa "şube · tarih-saat" yazısı basılır ve SHA-256 hesaplanır. Tasarım önemsiz.

| Ölçüt | Ağırlık | 0 | 2 | 4 |
|---|---|---|---|---|
| Doğruluk (fikstürler / kuyruk davranışı) | 35 | çoğu yanlış | küçük hatalar | tamamı doğru, kenar durumları düşünülmüş |
| Test | 20 | yok | var, yüzeysel | anlamlı, kenar durumlu |
| Kod okunabilirliği ve yapı | 20 | tek dosya karmaşa | makul | modüler, adlandırma iyi |
| Açıklama görüşmesi (10 dk) | 15 | kararları açıklayamıyor | açıklıyor | takasları ve alternatifleri biliyor |
| Süre disiplini (3 saat, 48 saat teslim) | 10 | aşım, gecikme | küçük aşım | zamanında, kapsamı sınırlamış |

Eşik: 16/20 ağırlıklı ortalama. Mini görev kodu ürüne alınmaz; ücret teslimle ödenir, adayın olur.

## 6. Mesaj şablonları

**Tanıdığa (LinkedIn/WhatsApp):** "Merhaba [ad], küçük bir ürün için iki serbest geliştirici arıyorum: Flutter ve Python/FastAPI, ~5 ay tam zamanlı, uzaktan, Ekim başı. Kapsam ve backlog hazır. Aklına gelen biri varsa iki satırla tanıştırır mısın? İlan: [bağlantı]."

**Adaya (görüşme daveti):** "Merhaba [ad], başvurunuz için teşekkürler. 45 dakikalık görüşme için [2 seçenek]. Görüşmede prototip üzerinden konuşacağız; hazırlık gerekmiyor."

**Mini görev gönderimi:** "Ekte 3 saatlik görev ve fikstürler; ücret ₺[…] teslimle ödenir. Teslim: [tarih], depo bağlantısı yeterli. Sonra 10 dakikalık açıklama görüşmesi yapacağız."

**Ret:** "Teşekkürler; bu tur başka bir adayla ilerliyoruz. Mini görev ücretiniz [tarih] ödenecek. İzin verirseniz ilerideki işler için iletişimde kalalım."

## 7. Sözleşme başlıkları (avukat şablona döker)

- Konu: Sprint 0 + Sprint 1–10 (2 haftalık sprintler); kapsam 03-backlog; değişiklik PO ile sprint planlamasında.
- Süre ve çalışma: tam zamanlı, uzaktan; günlük 15 dk, sprint törenleri; 22 hafta + 2 sprint tampon seçeneği.
- Ücret: sprint başına sabit ücret; ödeme sprint gözden geçirmesindeki kabulle; mini görev ayrı.
- **Devam/dur kapısı:** Sprint 2 sonu; şirket 2 hafta bildirimle sonlandırabilir, o güne kadarki iş ödenir. Her iki taraf için 2 hafta bildirim.
- Fikri mülkiyet: tüm kod, belge ve çıktılar teslimle şirkete devredilir (mali haklar; FSEK); açık kaynak bağımlılıklar lisans listesiyle.
- Gizlilik ve KVKK: NDA; müşteri verisine erişim yalnızca test/sahte veriyle; üretim verisine erişim yok (destek modu maskeli); veri işleyen personeli taahhüdü (hukuki/02 Ek-3).
- Araçlar ve hesaplar: şirketin GitHub organizasyonu, backlog aracı; kişisel hesapta kod tutulmaz.
- Kalite: DoD (04-tanimlar); S11–12 tamponunda hata düzeltme dahil; sonrası saatlik bakım tarifesi.
- Uyuşmazlık, damga vergisi, fatura düzeni: avukat/mali müşavir.

## 8. Kurucunun hazırlık listesi (Sprint 0'dan önce)

- [ ] GitHub organizasyonu (`talimatname`), 5 depo boş açılmış, dal koruması; geliştiriciler davet edilecek
- [ ] GitHub Projects panosu; S0–S2 hikâyeleri yüklü (03-backlog)
- [ ] Sözleşme + NDA imzalı (§7); mini görev ücretleri ödenmiş
- [ ] Sağlayıcı hesapları: TR bulut (deneme), SMS sağlayıcı (test), Firebase projesi, Apple Developer ve Google Play hesapları (şirket adına), e-posta gönderim (SMTP/servis)
- [ ] Alan adı (staging için de gerekli: `staging.talimatname.app`) — 03-isim-ve-marka bekleyen iş
- [ ] Tasarım token'ları ve marka dosyaları erişimi (05-tasarim/04, marka/)
- [ ] İlk gün paketi e-postası (06-ilk-gun-paketi §Gönderim) ve takvim davetleri (günlük 15 dk, planlama, gözden geçirme)
