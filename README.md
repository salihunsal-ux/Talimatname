# Talimatname

Talimatname, çok şubeli yeme-içme zincirlerinin şubelere verdiği tekrarlı talimatları (açılış, kapanış, hijyen, soğuk zincir, haftalık temizlik) WhatsApp gruplarından çıkarıp **kanıtlı, loglu ve raporlanabilir** hâle getiren bir mobil + web üründür. Personel listeyi telefondan veya şube tabletinden tamamlar, fotoğraf/ölçüm kanıtı yükler, yapamadığını sebebiyle bildirir; merkez her sabah hangi şubede neyin yapılıp yapılmadığını kanıtıyla görür.

Bu depo ürünün **iş analizi ve ürün sahipliği** dokümantasyonunu taşır: strateji, kapsam, analiz, gereksinimler, ekran tasarımları, test hazırlığı ve geliştirme hazırlığı. Kod ayrı depolarda tutulacaktır (bkz. `docs/07-gelistirme/02-repo-ve-ortam-kurulumu.md`).

## Depo haritası

- [Ürün dosyası](index.html) — tek sayfa: ürün özeti, tüm belgeler okunabilir, açık konular; canlı sürüm https://claude.ai/code/artifact/bb2f5c58-4b72-4fc5-80c9-0baef13cd2b4 · belgeler değişince `python build_index.py` (bağımlılık: `pip install markdown`).
- [Ürün merkezi](docs/00-urun-merkezi.md) — buradan başla: ürün özeti, karar haritası, belge navigasyonu, durum.
- [Çalışma planı](docs/00-calisma-plani.md) — BA/PO çalışma fazları, teslimatlar, durum.
- [01 Strateji](docs/01-strateji) — fizibilite raporu ve modeli, pilot görüşme rehberi, isim ve marka çalışması.
- [02 Ürün](docs/02-urun) — vizyon ve konumlanma, personalar, MVP kapsamı, yetenek haritası.
- [03 Analiz](docs/03-analiz) — aktörler, kullanım senaryoları (use case) kataloğu ve detayları, uçtan uca senaryolar.
- [04 Gereksinimler](docs/04-gereksinimler) — fonksiyonel ve fonksiyonel olmayan gereksinimler, iş kuralları, veri modeli, API taslağı, KVKK ve güvenlik.
- [05 Tasarım](docs/05-tasarim) — ekran envanteri ve navigasyon, mobil ve web tel-çerçeveler, tasarım sistemi, marka dosyaları.
- [06 Test](docs/06-test) — test stratejisi, kabul test senaryoları, test verisi ve ortam, cihaz matrisi, pilot UAT planı.
- [07 Geliştirme](docs/07-gelistirme) — kodlama hazırlık indeksi, teknik mimari, repo ve ortam kurulumu, backlog ve sprint planı, DoR/DoD.
- [ADR](docs/adr) — ürün ve mimari karar kayıtları.

## Güncel ürün kararları

- Çalışma adı: **Talimatname** (12 Eylül 2026; kesin isim pilot görüşmelerindeki isim testinden sonra — kartlar: yap lütfen, tamamlist, tembihle)
- İlk pazar: Türkiye · ilk dikey: yeme-içme zincirleri · ilk müşteri: 5–100 şubeli zincir merkezi
- İlk sürüm: **v1 çekirdek** (ADR-0008) — 6 madde türü, sabit kural, 4 rol, sabit eskalasyon + sabah özeti, istisna odaklı ızgara; GA 10. sprint + 2 sprint tampon; duyuru, koşul editörü, raporların çoğu v1.1; WhatsApp entegrasyonu MVP dışı (push + SMS yedek)
- Kişi bazlı performans skoru yok; skor şube düzeyinde
- Fizibilite kararı: Koşullu GO — 90 günlük doğrulama sprinti (20 görüşme → 5 LOI → 3 pilot), 24. ayda büyüt/kapat kapısı

## Bu depoda nasıl çalışılır

1. `docs/00-urun-merkezi.md` ile başla.
2. Strateji belgeleri yalnızca pazar, konumlanma veya hedef kitle varsayımı değişince güncellenir.
3. Kapsam, akış veya veri modeli değişince gereksinim belgeleri ve izlenebilirlik tabloları birlikte güncellenir (ID'ler kalıcıdır; silinen madde "İptal" olarak işaretlenir, numarası yeniden kullanılmaz).
4. Her anlamlı karar `docs/adr` altına yazılır.
5. Her iş paketi bittiğinde commit atılır ve uzak depoya gönderilir.

## Hızlı başlangıç (geliştirici)

`docs/07-gelistirme/00-kodlama-hazirlik-indeksi.md` — kodlamaya başlamadan önce okunacak belgelerin sıralı listesi ve hazırlık kontrol listesi.

## Sayılar tek kaynaktan

Gereksinim, test, ekran, iş kuralı, hikâye ve belge sayfası sayıları elle yazılmaz: **`sayilar.py`** bunları belgelerden ve üretilmiş HTML'den sayar. Üreticiler (`build_index.py`, broşür, tanıtım, özellik föyü, ilan) bu modülü içe aktarır; markdown içindeki elle yazılmış sayılar tek komutla tazelenir.

```bash
python sayilar.py            # sayıları yazdırır
python sayilar.py --kontrol  # markdown'daki bayat sayıları listeler (bayat varsa çıkış kodu 1)
python sayilar.py --guncelle # bayat sayıları düzeltir
```

**Commit öncesi kanca.** `.githooks/pre-commit`, her commit'te `sayilar.py --kontrol` çalıştırır; bayat sayı varsa commit durur ve düzeltme komutunu yazar. Depoyu yeni klonlayan bir kez şunu çalıştırır (kanca ayarı sürümlenmez):

```bash
git config core.hooksPath .githooks
```

Acil durumda `SAYILAR_ATLA=1 git commit …` ya da `git commit --no-verify` ile atlanır.

Kapsam değiştiren bir işten sonra sıra: ilgili belgeyi güncelle → (broşür/föy/tanıtım/ilan değiştiyse) o üreticiyi çalıştır → `python sayilar.py --guncelle` → `python build_index.py`. Yeni bir sayı metne girecekse `sayilar.py` içindeki `_kurallar()` listesine bir desen eklemek yeterli; aksi hâlde sayı ilk kapsam değişikliğinde bayatlar.
