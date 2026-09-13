# v1 çekirdek — aktör gözüyle gözden geçirme

Tarih: 13 Eylül 2026. Amaç: hazırlanan kapsam, gereksinim, ekran ve sprint planını hazırlayanın değil **kullananın** gözüyle okumak; ilk sürümün basit, ilk gün kullanılabilir ve yalnızca en önemli yetenekleri içeren bir ürün olmasını sağlamak. Sonuç: bugünkü "MVP" bir ilk sürüm değil, bir **1.x yol haritası**; çekirdek bunun yaklaşık yarısı.

## 1. Sayılarla mevcut durum

| Ölçü | Bugün | Kim taşıyacak |
|---|---|---|
| Kapsam satırı (Must) | 57 | 2 geliştirici |
| Fonksiyonel gereksinim (Must) | 140 / 155 | |
| Kullanıcı hikâyesi | 138 (14'ü L) | 12 sprint ≈ 190 geliştirici günü; plan zaten "sıkı" notuyla yazıldı |
| Ekran | 25 (11 mobil, 14 web) | |
| Rol | 7 | Personel için 1 ekran, yönetici için 14 |
| Madde türü | 11 | Kapanış listesi için 5'i yeter |
| Aksiyon durumu | 5 (+ reddedildi) | Şube müdürü telefonda |
| Kabul testi | 112 | |

Fizibilite ve kapsam belgesi rakiplerden "iyi özellikleri" toplarken iyi bir **ikinci yıl** ürünü tarif etti. Rakiplerin (Mitti, Connecteam) 10+ yılda biriktirdiği özellik kümesine ilk sürümde yaklaşmak, ilk sürümün asıl işini — WhatsApp'ın yerine geçecek kadar basit olmak — tehlikeye atıyor.

## 2. Aktör aktör

### Emre — personel (ürünü her gece açan kişi; kayıp burada belirlenir)

**İlk hafta gerçekten ne yapıyor:** 22:00'de tablette adına dokunuyor, PIN giriyor, kapanış listesini açıyor, 12 maddeyi işaretliyor, 3 fotoğraf çekiyor, bir sıcaklık giriyor, bir şeyi yapamadıysa sebebini seçiyor, "Gönder"e basıyor. 6–8 dakika. Ertesi gün aynısı.

| Bugünkü kapsamda fazla olan | Neden fazla | v1 kararı |
|---|---|---|
| 11 madde türü (video, imza, barkod/QR, tarih-saat) | Kapanış, açılış, hijyen, soğuk zincir listelerinde kullanılmıyor; her tür ayrı bileşen, ayrı hata | 6 tür: onay, çoktan seçmeli, sayı+birim, sıcaklık, metin, fotoğraf (+ talimat metni). Diğerleri v1.1 |
| Madde başına 1–5 fotoğraf | Personel 1 fotoğraf çeker; 5'e izin vermek "doğru sayı kaç" sorusu doğurur | Varsayılan 1, en çok 3; fotoğraf zorunlu maddede kamera doğrudan açılır, çekince madde tamamlanır (2 dokunuş) |
| "Herkes tamamlasın" modu ve madde bazlı kilit | Kim hangi bölümü yapacak karmaşası; tabletin başında bir kişi var | v1'de yalnızca "biri tamamlasın"; listeyi ilk açan alır, diğerleri "Emre yapıyor" görür. Çoklu kullanıcı v1.1 |
| Gönderim sonrası "ek kayıt" ile düzeltme | Gönderilen kayıt değişmez fikrini bulandırır; personel neyi düzelteceğini bilmez | v1'de düzeltme yok: gönderdin, bitti. Hata varsa şube müdürü aksiyon notuyla açıklar |
| Duyuru onayı, imza | Bugün ekranında ilk gördüğü şey "onay bekleyen duyuru" olmamalı; liste olmalı | Duyuru modülü v1.1 |
| Koşullu mantıkla açılan ek sorular | Liste uzadıkça sürpriz sorular güven kırar | v1'de tek sabit kural: "Hayır / Uygun değil / aralık dışı" → fotoğraf + not; kritik ise aksiyon. Kural editörü v1.1 |

| Eksik olan | Neden önemli | v1 kararı |
|---|---|---|
| Telefonu olmayan / telefonunu getirmeyen personelin PIN'i | Kapsamda PIN "ilk girişte kullanıcı belirler" — kioskta OTP yok, telefonu yok: giremez | Şube müdürü kioskta personele PIN atar; personel ilk kullanımda değiştirebilir |
| Açılışta dün gecenin özeti | Sabahçı, gece ne yapılamadıysa onunla başlar ("deterjan yok") | Açılış listesinin başında "dün gece: 2 madde yapılamadı" bloğu — vardiya devri notunun yerine, sıfır ek iş |
| "Ben yaptım ama çekmedim" durumu | Fotoğraf zorunluysa çekmeden geçemez; aksi hâlde tik yeter | Şablonda madde başına "fotoğraf zorunlu" tek ayar; başka kanıt ayarı yok |

### Ayşe — şube müdürü (WhatsApp yükünü taşıyan; ürünü şubede yaşatan)

**Gerçek ihtiyacı:** bugün kim ne yapacak belli olsun; yapılmayan/yapılamayan sabah önüne düşsün; su kesintisi gibi durumlarda "bugün olmayacak" diyebilsin; fotoğrafa bakabilsin; personele PIN verebilsin.

| Fazla olan | v1 kararı |
|---|---|
| Aksiyon durum makinesi (açık → devam → kapatma bekliyor → kapalı / reddedildi), onaylı kapanış | Aksiyon = **açık / kapalı**; kapatırken not, isteğe bağlı fotoğraf. Onay akışı v1.1 |
| Aksiyon yorum dizisi, @bahsetme | Sohbet geri geliyor; Ayşe zaten WhatsApp'ta | v1'de tek "not" alanı (eklenir, silinmez). Yorum dizisi v1.1 |
| "Yapılamadı"yı şube müdürünün doğrulaması / reddetmesi | Ek iş; sebebi görmesi yeter | Yapılamadı → şube müdürüne bildirim + aksiyon; onay/ret yok |
| Sorun kategorileri, yükseltme akışı | | Sorun bildir = fotoğraf + not → şube müdürüne düşer; "aksiyona çevir" tek düğme. Kategori sabit 4, yükseltme v1.1 |
| Kişi düzeyi takip ekranı | Ayşe kimin ne yapmadığını çalıştırma detayından zaten görür | v1.1 |

| Eksik olan | v1 kararı |
|---|---|
| Atanmamış liste ne olur? | Varsayılan: şubedeki herkes görür, ilk açan alır. Rol/kişi ataması isteğe bağlı |
| Gece 03:30'da SMS | Kaçırılan kapanış için gece kimse aranmaz: şube müdürüne push (anında), bölge müdürüne **07:00 sabah özeti**. Yalnızca kritik sıcaklık aralık dışı anında (push; teslim olmazsa SMS) |
| Listeyi kendisi yapabilme | Şube müdürü de personel gibi tamamlayabilir (rol matrisi bunu içeriyor; ekranda görünür olmalı) |

### Murat — bölge müdürü (ürünün "her sabah" kullanıcısı)

**Gerçek ihtiyacı:** sabah 07:30'da 12 şubeden hangisi kaçırdı, hangisi başarısız, fotoğraflar; dokunup şubeyi dürtmek. Ziyarette şubenin son 7 gününü görmek.

| Fazla olan | v1 kararı |
|---|---|
| Özelleştirilebilir eskalasyon merdiveni, adım editörü | Sabit kural (yukarıda). Merdiven editörü v1.1 |
| Ayrı yönetici mobil uygulaması görünümü (özet ızgara, atama, gözden geçirme) | Mobilde tek "Bölgem" listesi: şube × dün gece durumu (renk + ikon), dokununca çalıştırma detayı (fotoğraflar). Atama ve raporlar web'de (telefonda da açılır, duyarlı tasarım) |
| Şube sıralaması, ısı haritaları, aksiyon raporu, sebep dağılımı | v1.1 — v1'de ızgara + detay + sıcaklık günlüğü yeter |
| Gözden geçirme / ikinci imza | v1.1 |

| Eksik olan | v1 kararı |
|---|---|
| **Sabah özeti** (07:00 push + e-posta): dün gece kaçıran, başarısız, yapılamayan, kritik | Kapsamda Should'du (R-8); v1'de **zorunlu** — yönetici tarafının ana kanalı |
| **İstisna görünümü** | 25 şube × 5 liste ızgarasında 22 yeşil hücre gürültü; varsayılan görünüm "sorunlu olanlar" + "her şey yolunda" durumu |

### Selin — operasyon müdürü (satın alan; ilk saatte ürünü kuran)

**Gerçek ihtiyacı:** şubeleri yükle, kütüphaneden kapanış listesini seç, saatleri onayla, personeli davet et, ertesi sabah ızgaraya bak; denetimde PDF ver.

| Fazla olan | v1 kararı |
|---|---|
| Şablon editörü: ağırlıklı puan, eşik, kritik kuralı, koşul editörü, tarihli yayın, şube türü varyantı, kural deneme | Editör = madde listesi + tür + 3 kutu (zorunlu · fotoğraf zorunlu · kritik) + sıcaklık aralığı. Puan = geçen madde yüzdesi (bilgi); "Başarısız" yalnızca kritik madde başarısızsa. Ağırlık/eşik/tarihli yayın v1.1 |
| 30 şablon | 30 vasat yerine **8 iyi** şablon: kapanış, açılış, saatlik tuvalet/hijyen, soğuk zincir, haftalık derin temizlik, yağ değişimi, kasa devri, teslimat kabul |
| Akıllı gruplar, 7 rol, kalite/hesap yöneticisi ayrımı | 4 rol: **Yönetici** (merkez: operasyon + kalite + hesap), **Bölge müdürü**, **Şube müdürü**, **Personel**. Gözlemci ve gruplar v1.1 |
| Sihirbaz 5 adım, ilk günde 3 şablon | İlk gün **tek plan**: kapanış. Diğerleri ikinci hafta; ürün "bir gece çalıştı" güvenini önce kurmalı |
| Hesap ayarları paneli (parametre tablosu), sessiz saatler, kanal tercihleri | v1'de parametreler sabit (tolerans 120 dk, kritik vade 4 sa, sessiz saat 23–07, saklama 24 ay); ayar ekranı v1.1 |
| Duyuru, onay, imza | v1.1 |
| Excel dışa aktarım, paylaşım bağlantısı, arka plan üretim | Çalıştırma PDF'i ve dönem PDF'i (sıcaklık günlüğü) v1; Excel ve paylaşım v1.1 |

| Eksik olan | v1 kararı |
|---|---|
| "Kanıtlara kim bakacak?" | 25 şube × 5 fotoğraf = gecede 125 fotoğraf; kimse bakmaz. Izgara istisna odaklı; detayda fotoğraflar; **rastgele örnekleme** ("bugün 5 rastgele kanıt") v1.1 fikri olarak not |
| Fiyatı savunacak tek rapor | "Bu ay: %91 zamanında, 12 kaçırma, 3 kritik" — sabah özetinin aylık hâli; v1'de tek sayfa |

### Deniz — kalite (denetim günü kullanıcısı)

Sıcaklık günlüğü + dönem PDF'i (zaman damgalı, doğrulama kodlu) v1'de kalır — ürünün "kanıt" iddiasının somut çıktısı. Denetim izi görüntüleyici, zincir doğrulama ekranı, RFC 3161 dış damga: **arka planda hash zinciri ilk günden çalışır**, ekranı ve dış damga v1.1. Gözden geçirme/imza v1.1.

### Cem — hesap yöneticisi (kurulum ve personel devri)

Excel'den şube ve personel yükleme, pasifleştirme, kiosk kaydı v1. KVKK dışa aktarma/silme **ekranı** v1.1 — v1'de talep gelirse destek ekibi betikle yapar (30 gün içinde; süreç belgelenir). Aydınlatma metni ürün içinde v1 (hukuki zorunluluk). Saklama silme işi arka planda sabit 24 ay. 2FA v1.1 (yönetici şifre politikası v1).

## 3. Kesinti ve sadeleştirme listesi

| # | Karar | Etkilenen | Neden |
|---|---|---|---|
| K1 | Madde türleri 11 → 6 (+ talimat) | Ş-2, FR-0303, SCR-M-05 | Personel akışı; yeme-içme listeleri |
| K2 | Koşullu mantık editörü → tek sabit kural | Ş-4, FR-0401…0404, SCR-W-05 | Sürpriz soru yok; editör karmaşıklığı |
| K3 | Puan: ağırlık/eşik yok; başarısız = kritik madde | Ş-3, Ş-5, FR-0306, BR-07 | Anlaşılır tek kural |
| K4 | "Herkes tamamlasın" ve madde bazlı kilit → v1.1 | P-3, Y-2, FR-0508, 0609, BR-16, BR-24 | Tek kişi, tek liste |
| K5 | Ek kayıt (düzeltme) → v1.1 | Y-6, FR-0608, BR-12 (kısmen) | Gönderilen değişmez |
| K6 | Aksiyon: açık/kapalı + not; yorum dizisi, onaylı kapanış, özel tipler → v1.1 | A-1, A-3, A-5, FR-0904…0906 | Şube müdürü yükü |
| K7 | Eskalasyon: sabit kural; merdiven editörü → v1.1; gece SMS yok | A-4, FR-0510, 0912, BR-11, BR-23 | Gerçek hayat: 03:30'da kimse aranmaz |
| K8 | Sabah özeti (07:00 push + e-posta) → v1 zorunlu | R-8, FR-1212 | Yöneticinin ana kanalı |
| K9 | Duyuru/onay/imza modülü → v1.1 | D-1…D-4, CAP-11, UC-14 | Çekirdek değil |
| K10 | Raporlar v1: istisna odaklı ızgara, çalıştırma detayı, kanıt galerisi (basit), sıcaklık günlüğü, aylık tek sayfa; sıralama/ısı haritası/sebep dağılımı/aksiyon raporu/kişi takibi → v1.1 | R-2…R-4, R-7, R-9 | Bakılmayacak rapor yapılmaz |
| K11 | Dışa aktarım v1: çalıştırma PDF + dönem PDF; Excel, paylaşım bağlantısı → v1.1 | R-6 | |
| K12 | Denetim izi ekranı, zincir doğrulama ekranı, RFC 3161 → v1.1 (zincir backend'de v1) | U-2, FR-1302…1304, UC-17 | |
| K13 | KVKK talep ekranı → v1.1 (destek süreci v1); aydınlatma v1; saklama sabit | U-3, U-4, FR-1309, 1310, UC-18 | |
| K14 | Roller 7 → 4; akıllı gruplar, Gözlemci → v1.1 | O-3, O-7, FR-0205, 0206 | Basit yetki, basit zihinsel model |
| K15 | Ayarlar paneli → v1.1 (parametreler sabit) | W-3, FR-1402 | |
| K16 | 2FA → v1.1 | O-4 (kısmen), FR-0202 | |
| K17 | Yönetici mobil görünümü → tek "Bölgem" listesi + duyarlı web | Y-12, FR-1211, SCR-M-10 | Flutter kapsamı yarıya iner |
| K18 | Şablon kütüphanesi 30 → 8 | Ş-6, FR-0311, ST-102 | Kalite > sayı |
| K19 | Sihirbaz: 4 adım, tek plan (kapanış) | W-1, FR-1401 | İlk gece güveni |
| K20 | Fotoğraf: varsayılan 1, en çok 3; kamera doğrudan açılır | Y-3, FR-0604 | 2 dokunuş |
| K21 | QR istasyon, vardiya devri notu (yerine açılışta dün gece özeti), AI taslak, şube varyantı, gözden geçirme, API/webhook: v1.1 | CAP-15…18 | Zaten Should; netleşti |

**Eklenenler (v1):** E1 şube müdürünün personele PIN ataması · E2 atanmamış liste = şubede herkes görür, ilk açan alır · E3 açılış listesinde "dün gece" özeti · E4 istisna odaklı ızgara ve "her şey yolunda" durumu · E5 sabah özeti · E6 kritik sıcaklıkta anında bildirim (push, teslim olmazsa SMS) · E7 aylık tek sayfa özet.

## 4. v1 çekirdek (öneri)

**Merkez kurar (web):** hesap + şubeler/istasyonlar (Excel) · personel (Excel/elle) ve 4 rol · kiosk cihaz kaydı (QR) · 8 hazır şablon, basit editör (6 madde türü; zorunlu / fotoğraf zorunlu / kritik; sıcaklık aralığı) · plan: tekrar (günlük/saatlik/haftalık), pencere (gece yarısı aşan), tolerans, atama (rol/kişi/şubedeki herkes), tek seferlik liste · sihirbaz (4 adım, tek plan).

**Personel yapar (mobil, kiosk-öncelikli):** OTP giriş veya kiosk PIN · Bugün · liste tamamlama (6 tür) · fotoğraf 2 dokunuş, damga, hash · "yapılamadı" + sebep · sorun bildir (fotoğraf + not) · çevrimdışı kuyruk ve senk · açılışta dün gece özeti.

**Sistem izler:** çalıştırma üretimi, pencere/durum motoru, kaçırıldı · kritik madde başarısız → aksiyon (açık/kapalı) · bildirim: push; OTP ve kritik için SMS · sabit eskalasyon: şube müdürü anında, bölge müdürü sabah özeti, kritik anında · olay günlüğü + hash zinciri (arka plan) · saklama 24 ay (arka plan).

**Yönetici görür:** istisna odaklı ızgara (web, telefonda da) · çalıştırma detayı + fotoğraflar · basit kanıt galerisi · sıcaklık günlüğü · sabah özeti (push + e-posta) · aylık tek sayfa · çalıştırma PDF ve dönem PDF (doğrulama kodlu) · mobilde "Bölgem" listesi · aksiyon listesi (açık/kapalı) · yapılmayacak işaretleme.

**Uyum:** aydınlatma metni + konum izni akışı · biyometri yok · KVKK talepleri destek süreciyle.

Kapsam dışı (v1.1'e): duyuru/onay, koşul editörü, ağırlıklı puan, herkes-tamamlasın, ek kayıt, aksiyon yorumları/onayı, eskalasyon editörü, akıllı gruplar, Gözlemci, ayarlar paneli, 2FA, denetim izi ekranı, TSA, KVKK ekranı, Excel/paylaşım, raporların geri kalanı, video/imza/barkod/tarih-saat, QR, AI taslak, varyant, gözden geçirme, API/webhook.

## 5. Etki tahmini

| Ölçü | Bugün | v1 çekirdek |
|---|---|---|
| Kapsam satırı (Must) | 57 | ~34 |
| FR (Must) | 140 | ~80 |
| Ekran | 25 | 16 (mobil 9, web 7) |
| Rol | 7 | 4 |
| Hikâye | 138 | ~85 |
| Sprint (GA) | 12 (tampon yok) | 10 (Alfa 5, Beta 7, GA 10) + 2 sprint pilot bulguları/v1.1 başlangıcı |
| Kabul testi | 112 | ~70 çekirdek (geri kalanı v1.1'de açılır) |

Zamanlama değişmiyor (6 ay), ama artık **tampon var** ve pilot bulgularına yer var; en riskli motor işleri (S3–S6) aynı kalıyor çünkü onlar çekirdek.

## 6. Sıra ilkesi (gelecek tartışmalar için)

Bir özellik v1'e ancak şu üç soruya "evet" alırsa girer: (1) Personel bunu görmese kapanış listesi yine tamamlanır mı? — hayırsa girer. (2) Yönetici bunu görmese kaçırılan iş görünmez mi? — evetse girer. (3) Bu olmadan denetimde kanıt verilemez mi? — evetse girer. Diğer her şey, ne kadar iyi olursa olsun, v1.1 listesine yazılır ve pilot geri bildirimiyle sıralanır.

## 7. Onay bekleyen kararlar

K1–K21 ve E1–E7 onaylanırsa: kapsam belgesi, yetenek haritası, FR (M/S bayrakları), use case'ler, ekran envanteri ve tel-çerçeveler, kabul testleri, backlog/sprint planı bu çekirdeğe göre yeniden çizilir (ID'ler korunur; ertelenenler "v1.1" etiketi alır, silinmez). Özellikle görüş istenenler: **K9** (duyuru modülünün ertelenmesi), **K12** (denetim izi ekranı ve dış zaman damgasının ertelenmesi — "kanıt" iddiası için hassas), **K17** (yönetici mobil görünümünün küçültülmesi), **K18** (8 şablon).
