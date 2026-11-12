# ADR-0013 · Faz sırası: önce yönetim paneli, mobil ikinci geliştiriciyle

- Tarih: 2026-10-22 · Durum: Kabul edildi ([ADR-0009](0009-ekip-modeli-serbest-gelistirici.md)'un "iki geliştirici aynı anda başlar" varsayımını değiştirir; ekip modelini —iki serbest geliştirici— değiştirmez)

## Bağlam

ADR-0009 ekip modelini seçmişti: iki serbest geliştirici (1 mobil, 1 backend/web), Sprint 0'da birlikte başlar. Üç yeni bilgi bu varsayımı geçersiz kıldı.

**1 · Saha durumu.** 22 Ekim itibarıyla ilan yayınlanmadı, görüşme notu yok, işe alım yok, Sprint 0 başlamadı; K1 kapısı (≥ 12/20 görüşme) ölçülemedi. İki kişi aramak, bir kişi aramaktan hem yavaş hem —K1 sinyali gelmeden— daha pahalı.

**2 · İş asimetrik.** Backlog gözden geçirmesinde (commit `b9994a9`) hikâyeleri hatlara böldük:

| Hat | Hikâye | Gün |
|---|---|---|
| A · panel + arka uç | 82 | 244 |
| B · mobil | 25 | 74 |
| A+B · ortak | 11 | 40 |

Ortağı yarı yarıya saydığımızda **A ≈ 264 gün, B ≈ 94 gün**: panel ve arka uç, mobilin **2,8 katı**. "1 mobil + 1 backend/web" dengesi işin şekline uymuyor.

**3 · Bağımlılık yönü tek taraflı.** Zincir, şube, personel, şablon ve plan panelden kurulur; mobil, panelin ürettiği veriyi tüketir. Panel olmadan mobilde gösterilecek tek bir çalıştırma yoktur. Tersi doğru değil: panel mobil olmadan kurulabilir, tohum ve sentetik veriyle gösterilebilir.

Buna karşı duran tek gerçek: **planın en riskli iki deneyi mobildir** (Spike A çevrimdışı kuyruk + idempotent senk, Spike C kamera → damga → SHA-256). "Mobili sona bırakmak" bu riski projenin sonuna taşır; takvimi öldüren klasik hata budur.

## Seçenekler

| | Kurgu | Artısı | Eksisi |
|---|---|---|---|
| A · Özgün plan | İki geliştirici Sprint 0'da birlikte başlar | En kısa takvim (paralellik) | İki işe alım, tam maliyet, K1 ölçülmeden; S1'de mobil kapasite boşta (mobil ekranlar S2 API'lerini bekliyor) |
| B · Tamamen sıralı | Panel bitince mobil başlar | Tek işe alım, en düşük nakit | Paralellik tamamen kaybedilir; mobil ~5. ayda başlar, Alfa 11.–12. ay; iki riskli spike sona kalır |
| **C · Kademeli (seçilen)** | Panel tek kişiyle başlar, mobil geliştirici 6.–8. haftada katılır | Tek işe alımla başlar, ilk iki ay yarı maliyet; riskli spike'lar 2. ayda koşar | Paralel plandan ~4–6 hafta geride; ikinci kişi bulunamazsa Faz B gecikir |

## Karar

1. **Faz A hemen, tek geliştiriciyle (backend/web).** Kapsam: backend çekirdek (hesap/kiracı, RLS, `audit.emit()`, hiyerarşi, OTP, 4 rol), panel (giriş, şubeler, personel, şablon editörü, plan editörü, pano), plan ve çalıştırma motoru, **Spike B** (RRULE pencere) ve **Spike D** (bildirim → SMS), tohum ve sentetik veri. Sprint 0 tek kişilik olur.
2. **Mobil geliştirici Faz A'nın 6.–8. haftasında katılır** — panelin bitmesi beklenmez. Mobilin ilk 3–4 haftalık işi (spike'lar, kabuk, madde bileşenleri) motoru beklemez.
3. **Faz B'nin ilk iki haftası yalnızca Spike A ve Spike C'dir** (stub API ile). Ekran yok. Gerekçe: riskin erken keşfi.

   *12 Kasım 2026 eki.* Spike A'nın **sunucuya bakan yarısı** Faz A içinde, Flutter'sız koşuldu: bkz. [Sprint 0 ve teknik spike](../07-gelistirme/05-sprint0-ve-teknik-spike.md) §4. Gerekçe: senk sözleşmesinin birim testleri vardı ama onu hiçbir istemci çalıştırmamıştı; sözleşme kusuru Flutter'da keşfedilse mobil geliştiricinin haftalarına mal olurdu. Faz B'de kalan kısım istemci tarafı (arka plan senki, uygulama öldürülüp açılınca kuyruğun sürmesi, kamera yolu).
4. **Mobil başlamadan önce üç API sözleşmesi yazılı ve testlidir** (Faz A'nın bitti tanımına eklendi): idempotent cevap yazma (cihaz UUID'siyle), kanıt yükleme akışı (ön imzalı URL → tamamlama → damga + SHA-256), senk uç noktalarının taslağı (`/sync/manifest`, `/sync/batch`). Yazılmazsa API panelin çevrimiçi istek-cevap şekline oturur ve Faz B onu söker.

   *7 Kasım 2026 eki.* Bu liste iki şeyi atlamıştı; ikisi de bağımsız test turunda çıktı ve Faz B başlamadan kapatılmalı:

   - **Oturum yenileme.** Dördüncü sözleşme olmalıydı; bkz. [oturum süresi açığı](../04-gereksinimler/08-oturum-suresi-acigi.md). **Kapandı (11 Kasım 2026):** yenileme belirteci eklendi — web 12 saat, mobil 30 gün; döndürülmüş belirteç yeniden kullanılırsa zincirin tamamı iptal edilir.
   - **Pencere açılış saati.** Senk manifestine `writable_from` eklendi (geriye uyumlu): cihaz, penceresi açılmamış listeyi önceden indirip gösterebilir ama doldurmaya davet etmemeli — sunucu `pencere-acilmadi` ile reddeder (BR-02a). Mobil geliştirici bu alanı okumalı; okumazsa kullanıcıyı doldurulamayacak bir listeye sokar ve çevrimdışı kuyruk toptan reddedilir.
5. **Sprint 0'ın mobil maddeleri Faz B'nin 1. haftasına taşındı:** Flutter iskeleti, Flutter tema token'ları, tel-çerçeve iki ekran, Spike A, Spike C. Sprint 0'da mobil tarafta yalnızca boş depo ve dal koruması vardır.
6. **Mobil kuyruğu bitince mobil geliştirici web hattına geçer** (≈ Faz B'nin 10. sprinti). Hatlar arasındaki 2,8 katlık fark böyle kapanır.
7. **Pilot, Alfa ve K3 mobil olmadan yapılamaz.** Pilot zincirlere tarih verilirken Faz B'nin başlangıcından en az 10 hafta sayılır; bu tarih **ikinci geliştiricinin bulunma tarihine** bağlıdır, Faz A'nın hızına değil.

## Sonuçlar

- **Takvim:** darboğaz A hattıdır — iki kişiyle mobil ~5. ayda, panel ~14. ayda biter. Kademeli başlangıç bu tabloyu kötüleştirmez; paralel plandan farkı ikinci kişinin 6–8 hafta sonra gelmesidir (≈ 4–6 hafta).
- **Maliyet:** ilk ~2 ay tek kişi. ADR-0009'un iki kişilik aylık tahmini ₺250–400 bin; Faz A'nın ilk iki ayı bunun yarısı.
- **Ekip şekli:** kapasite kaldıracı olarak üçüncü geliştirici seçilirse **web geliştiricisi** olmalıdır, mobil değil (asimetri). Bu, kapasite notundaki 1. seçeneği netleştirir; kaldıraç kararı hâlâ açıktır ve K1'e bağlıdır.
- **Devam/dur kapısı:** K1 geçmezse harcanan, iki kişilik iki sprint değil **tek kişilik iki ay** olur.
- **İlan güncellenmeli:** [ilan/](../07-gelistirme/ilan/serbest-gelistirici-ilani.html) iki pozisyon ve "19 Ekim başlangıç" anlatıyor; ikisi de geçersiz. İlan yayınlanmadığı için maliyeti yoktur, ama yayından önce tek pozisyona (backend/web) çevrilmesi gerekir; mobil ilanı Faz A'nın 3.–4. haftasında çıkar.
- Sprint tabloları bağımlılık sırasını koruduğu için yerinde kaldı; hat bilgisi [backlog](../07-gelistirme/03-backlog-ve-sprint-plani.md)'daki **Faz** kolonundadır.

## Gözden geçirme tetikleyicileri

- **Mobil geliştirici 8. haftaya kadar bulunamazsa:** Faz B gecikir, Alfa ve pilot kayar; kapsam kaldıracı (PDF/aylık özet, belge takvimi, kiosk) devreye girer.
- **Spike A ya da C geçmezse:** ADR-0002/0004'e uygulama notu; çevrimdışı modeli "yalnızca çevrimiçi gönder, çevrimdışı taslak" seçeneğine daralır (05-sprint0 §4).
- **K1 ≥ 12/20 gelirse:** üçüncü (web) geliştirici kararı ve takvim kaldıracı yeniden tartılır.
- **Pilot, mobil hazır olmadan sözleşme isterse:** panelin tek başına satılabileceği varsayımı test edilmiş olur — bu, ürün konumlanmasını (kanıtlı görev listesi) değiştirecek bir sinyaldir, ADR gerektirir.
