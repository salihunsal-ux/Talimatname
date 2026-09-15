# Saha kiosk denemesi — gerçek tablet, gerçek kapanış

Açık karar #1'i ("ortak cihaz / kiosk modu v1'de kalır mı?") görüşmede sorarak değil, şubede **denenerek** kapatmak için. Blok 8 prototipi bir Android tablete kilit modunda kurulur; şube ziyaretinde (gözlem formu, 05) kapanış vardiyası boyunca personel listeyi bu tabletten tamamlar. Ürün değil, prototip: veri kaydetmez, kamera sahtedir — ölçülen şey cihazın ve alışkanlığın uyumu.

## Ne öğrenmek istiyoruz

| Soru | Ölçüt | Nasıl ölçülür |
|---|---|---|
| Personel ortak tableti kullanır mı? | Kapanışı yapan kişi listeyi **tablette 8 dk altında** bitirdi; "telefondan olsa" demedi | Kronometre + sohbet (form §3) |
| Mutfak ortamı dokunmatiğe izin veriyor mu? | Eldiven/ıslak el/yağ ile ≤ 2 yanlış dokunuş; ekran okunuyor | Gözlem sayımı; parlaklık %50'de deneme |
| Tablet nerede duracak? | Personel listeyi yaparken tablete ≥ 3 kez gidip geldi mi, yoksa yanında mı taşıdı? | Gözlem |
| Fotoğraf tabletle çekilir mi? | Personel tableti çöp alanına / kepenge götürdü mü; "telefonla çekeyim" dedi mi? | Gözlem (prototipte kamera sahte; hareketi izle) |
| Wi-Fi yeterli mi? | Bar, mutfak, depo, tuvalet önü: ≥ 2 çubuk | Telefonla test (form §1) |
| PIN akışı işliyor mu? | Adına dokun + 4 hane ≤ 15 sn; PIN'i hatırlıyor mu | Kronometre |
| Kilit ve devir | 2 dk kilitten sonra kaldığı yerden devam etti mi; ikinci kişi kendi adıyla girebildi mi | Gözlem |

**Karar kuralı (3 ziyaret):** ≥ 2 şubede personel listeyi tablette 8 dk altında bitirdi ve "telefon daha iyi" demedi → kiosk v1'de kalır (O-5). Aksi hâlde personel telefonu birincil, kiosk isteğe bağlı (v1'de yine var, ama sihirbazda "cihaz kaydı" zorunlu adım olmaz). Görüşmelerdeki `tablet_sube_orani` (%50 eşiği) ile birlikte yorumlanır; ikisi çelişirse saha kazanır.

## Donanım (kullanıcı alır)

| Parça | Öneri | Not |
|---|---|---|
| Tablet | Android 13+, 10–11", ≥ 4 GB RAM, 64 GB, Wi-Fi; arka kamera ≥ 8 MP; parlaklık ≥ 400 nit tercih (Galaxy Tab A9+ / Lenovo Tab M11 / Redmi Pad SE sınıfı) | 2026 fiyatı ≈ ₺6–10 bin (önceki "₺3–5 bin" tahminim iyimserdi). Pilotta şube başına aynı sınıf |
| Kılıf + stand | Darbeye dayanıklı, ayaklı; tezgâha yapışan tutucu veya duvar aparatı | Bar/kasa arkasına, göz hizasına |
| Ekran koruyucu | Mat (yağ ve parlama için) | Test: aynı ziyarette mat/parlak fark |
| Şarj | 2 m kablo + adaptör; tezgâhta priz | Gün boyu fişte |
| Yedek internet | Telefon hotspot | Şube Wi-Fi'ı personele kapalıysa |
| Temizlik | Alkollü mendil | Vardiya sonu ekran; hijyen sorusu için gözlem |

## Yazılım kurulumu (30 dk, ziyaretten önce)

1. **Prototipi tablete al.** İki yol:
   - A · Bağlantı: Blok 8 prototipinin canlı sayfasını paylaşım menüsünden bağlantıyla açın; tablette Chrome'da açın → menü → "Ana ekrana ekle" (tam ekran açılır). İnternet gerekir.
   - B · Dosya (çevrimdışı, önerilen): `docs/05-tasarim/05-prototip/blok8-prototip.html` dosyasını tabletin `Download` klasörüne kopyalayın (USB, e-posta veya Drive). Tek dosya, bağımlılık yok; yazı tipi yüklenmezse sistem yazı tipine düşer.
2. **Kiosk modu:** adresin sonuna `?kiosk=1` ekleyin (ör. `file:///sdcard/Download/blok8-prototip.html?kiosk=1`). Bu modda görüşmeci paneli gizlenir, ekran tam boy olur, 2 dakika dokunulmazsa kilit ekranına döner (kaldığı yerden devam eder).
3. **Kilitleme (uygulamadan çıkışı engelleme):** Ayarlar → Güvenlik → **Uygulama sabitleme** (ekran sabitleme) açın; Chrome'u sabitleyin. Daha sıkı istiyorsanız **Fully Kiosk Browser** (ücretsiz sürüm yeter): Start URL = yukarıdaki adres, "Kiosk Mode" açık, çıkış PIN'i belirleyin, ekran kapanmasın.
4. Parlaklık %50, otomatik döndürme kapalı (yatay), bildirimler kapalı, sesler kapalı.
5. Deneme: adına dokun → PIN 1234 → listeyi bir kez baştan sona yapın; 2 dk bekleyip kilidi görün.

## Ziyaret akışı (kapanış vardiyası, ~90 dk)

| Dakika | Ne | Kim |
|---|---|---|
| −30 | Tableti şube müdürüyle birlikte yerleştirin (bar/kasa/mutfak: **onlar seçsin**, sebebini not edin). Wi-Fi ölçümü 4 istasyonda | Görüşmeci + şube müdürü |
| −15 | Personele 2 dk anlatım: "Bu bir deneme, gerçek kayıt değil. Kapanışı normal yapın, her maddeyi tablette işaretleyin." Adlarını prototipteki 6 isimden birine eşleyin (gerçek ad girilmez) | Görüşmeci |
| 0 | Kapanış başlar; **müdahale etmeyin.** Kronometre: PIN girişi, ilk madde, son madde, "Gönder". Yanlış dokunuş, tablete gidiş-geliş, fotoğraf davranışı, soru sorma sayısı | Gözlemci |
| +? | 2 dk kilit yaşanırsa tepkiyi not edin (kızdı mı, doğal mı) | |
| Bitiş | Personel sohbeti 5 dk (form §3 + "telefonunuzda olsa?") · şube müdürü sohbeti 5 dk ("bu tablet burada bir ay kalsa?") | Görüşmeci |
| Sonra | Tablet ekranını temizleyin; not formunu 10 dk içinde doldurun | |

Ölçüm kaydı: prototip "Ne oldu?" ekranındaki olay izi saatleri kronometre yerine geçer (gönderim ekranının fotoğrafını çekin; kişi adı yok).

## Not dosyası

`gorusmeler/YYYY-MM-DD-zincir-kodu-kiosk.md` — `puanla.py` bu dosyaları görüşme tablosuna katmaz, ayrı sayar ve kararı özetler.

```
---
tur: kiosk
tarih: 2026-10-
zincir_kodu: ""
sube: ""
format: kafe            # kafe / hizli-servis / restoran
konum: bar              # bar / kasa / mutfak / ofis — tableti nereye koydular
wifi_min_cubuk: 2       # 4 istasyonun en düşüğü
pin_sn: 12              # adına dokun → PIN → liste açıldı
liste_dk: 7.5           # ilk madde → Gönder
yanlis_dokunus: 1
gidis_gelis: 2          # tablete kaç kez gitti
foto_davranisi: tasidi  # tasidi / telefon-istedi / atladi
kilit_yasandi: evet     # 2 dk kilit görüldü mü
kilit_tepki: dogal      # dogal / rahatsiz
telefon_tercihi: hayir  # "telefondan olsa daha iyi" dedi mi: evet / hayir / kararsiz
eldiven_islak: evet     # eldiven veya ıslak elle kullanıldı mı
ekran_okunur: evet
karar: kiosk            # kiosk / telefon / ikisi — gözlemcinin bu şube için kararı
---
## Gözlem (isim yok)
## Personel sözleri (alıntı)
## Şube müdürü: "bir ay kalsa?"
## Kötü sinyaller (en az 1)
## Kapsam etkisi (O-5, E-1, Y-3, sihirbaz adım 4)
```

## Riskler

- Tablet "denetim cihazı" gibi algılanır → anlatımda "gerçek kayıt değil" cümlesi; personel adı girilmez.
- Görüşmeci yardım etme refleksi → gözlemci sessiz; yalnızca sorulursa cevap.
- Tek şube, tek vardiya genellemesi → 3 şube (kafe, hızlı servis, restoran), ikisi İstanbul dışı olabilir.
- Prototip sınırları (kamera sahte, senk yok) sonucu bozar → yalnızca cihaz-alışkanlık soruları puanlanır; "uygulama yavaş/eksik" yorumları ayrı yazılır.
