# İş kuralları

Kod ve testlerin tek referansı. Her kural tek cümle + kesin parametre. **v1'de parametreler sabittir** (ADR-0008); "(ayar)" işaretli olanlar v1.1'de hesap düzeyinde düzenlenebilir hâle gelir. Sürüm notu olmayan kurallar v1'de geçerlidir.

## Pencere, iş günü, durum

- **BR-01 · İş günü.** Bir çalıştırmanın iş günü = pencere başlangıç tarihi (şube saat diliminde). Gece yarısını aşan pencere (22:00–01:30) önceki güne aittir; raporlar ve ızgara iş gününe göre gruplar.
- **BR-02 · Tolerans.** Pencere bitişinden sonra `tolerans` (plan ayarı, 0–240 dk, varsayılan kapanış 120 / saatlik 0) içinde gönderilen çalıştırma "Geç tamamlandı" sayılır; zamanındalık raporunda ayrı gösterilir.
- **BR-03 · Kaçırıldı kesindir.** Tolerans bitiminde tamamlanmamış çalıştırma "Kaçırıldı" olur; sonradan cevap girilemez, düzenlenemez; yalnızca ek not eklenebilir (logda).
- **BR-04 · Yapılmayacak.** Yalnızca şube müdürü ve üstü, sebep (seçim + not) girerek "Yapılmayacak" işaretleyebilir; puanlamaya girmez, raporda ayrı sayılır, eskalasyonu durdurur; işaretleme olayı logda.
- **BR-16 · Tamamlama kuralı.** v1'de tek kural: "biri tamamlasın" — çalıştırmayı ilk açan kullanıcı alır (BR-26), ilk gönderim çalıştırmayı kapatır. "Herkes tamamlasın" (her atanan kendi bölümünü gönderir; eksik atananlar raporlanır) v1.1.
- **BR-17 · Kapalı gün.** Şube kapalı gün takviminde çalıştırma üretilmez; ızgara hücresi "kapalı"; hesap düzeyi resmî tatil takvimi devralınır, şube geçersiz kılabilir.
- **BR-18 · Sürüm bağı.** Çalıştırma, üretildiği andaki şablon sürümüne bağlanır; şablon değişince başlanmamış (Planlandı) çalıştırmalar yeni sürüme geçer, başlanmış olanlar eski sürümde biter.

## Madde, puan, kanıt

- **BR-05 · Gönderim kilidi.** Zorunlu maddelerin tamamı cevaplanmadan (cevap, "yapılamadı" veya koşulla atlanmış) gönderim yapılamaz.
- **BR-06 · Kritik madde.** Kritik işaretli bir madde başarısızsa (hayır/uygun değil/aralık dışı/yapılamadı) çalıştırma puandan bağımsız "Başarısız" işaretlenir ve kritik aksiyon açılır.
- **BR-07 · Puan.** v1: liste puanı = geçen madde sayısı / puanlanan madde sayısı × 100 (bilgi amaçlı; talimat maddeleri puanlanmaz). "Başarısız çalıştırma" yalnızca BR-06 (kritik madde) ile belirlenir. Ağırlıklı puan ve eşik v1.1.
- **BR-08 · Sıcaklık.** Kabul aralığı dışındaki ölçüm maddeyi başarısız yapar, fotoğraf ve not ister (koşul varsayılanı), kritik ise BR-06 uygulanır; aralık sınırları dahildir (0–4 °C: 4,0 geçer, 4,1 geçmez).
- **BR-09 · Yapılamadı.** Sebep seçimi zorunlu (v1 sabit set: malzeme yok, ekipman arızalı, zaman yetmedi, yetkim yok, diğer); "Diğer" → not ≥ 5 karakter zorunlu; kritik maddede "Yapılamadı" yoktur. Şube müdürü onay/ret vermez; bildirim ve aksiyon alır.
- **BR-12 · Kanıt değişmez.** Gönderilmiş cevap ve kanıt üzerine yazılmaz ve v1'de düzeltilemez; açıklama gerekiyorsa ilgili aksiyona not eklenir. "Ek kayıt" ile düzeltme v1.1. Silme yoktur (KVKK silme hariç, o da maskeleme/dosya silme + log).
- **BR-13 · Sunucu zamanı.** Tüm olaylarda sunucu zamanı esastır; çevrimdışı kayıtlarda çekim zamanı = cihaz zamanı + senk anında hesaplanan fark; ham cihaz zamanı ve fark saklanır; fark 10 dk'yı aşıyorsa kanıt "saat farkı" bayrağı alır.
- **BR-14 · Yalnızca kamera.** Şablon "yalnızca kamera" ise galeri/dosya seçimi sunulmaz; kanıt uygulama içi kameradan gelir; ayar kapalıysa galeri kanıtı "galeri" bayrağıyla işaretlenir.
- **BR-15 · Konum.** Konum yalnızca cevap anında tek nokta olarak alınır; izin yoksa "konum yok" bayrağı; şube konumuna uzaklık > 500 m ise "uzak" bayrağı; sürekli izleme yoktur.
- **BR-24 · Çakışma.** v1'de bir çalıştırmayı aynı anda tek kullanıcı doldurur (BR-26 kilidi); yine de aynı maddeye iki cevap gelirse (kilit süresi dolmuş, çevrimdışı) sunucu zamanına göre son yazan kazanır, önceki cevap "üzerine yazıldı" olayıyla logda kalır; kanıt dosyaları asla silinmez.

## Aksiyon ve eskalasyon

- **BR-10 · Otomatik aksiyon.** Tetik (v1): kritik madde başarısız (kritik), "yapılamadı" (orta), kaçırılan çalıştırma (yüksek). Varsayılan atanan: şube müdürü (şube için tanımlı değilse bölge müdürü). Vade = oluşturma + öncelik süresi: kritik 4 sa, yüksek 24 sa, orta 72 sa. Aynı kaynak için tek aksiyon. Durum yalnızca açık/kapalı; kapatırken not zorunlu.
- **BR-11 · Eskalasyon (v1, sabit).** Kaçırılan çalıştırma: şube müdürüne anında push; bölge müdürü ve yöneticiye 07:00 sabah özeti (BR-27). Kritik madde başarısız: şube ve bölge müdürüne anında push, 10 dk içinde teslim/okunma yoksa SMS. Gecikmiş aksiyon: sabah özetinde. Gece SMS yalnızca kritik. Özelleştirilebilir merdiven v1.1 (ayar).
- **BR-23 · Kanal.** Varsayılan kanal push; SMS yalnızca OTP ve push teslim edilemeyen kritik madde bildirimi için. Sessiz saatler sabit 23:00–07:00: yönetici push'ları sabah özetine ertelenir; kritik anında. Hatırlatmalar sabit: pencere açılışı ve bitişe 30 dk.

## Kimlik, cihaz, kişi

- **BR-19 · Kiosk.** 2 dk hareketsizlikte kilit (ayar 1–10 dk); 5 hatalı PIN → 1 dk blok; art arda 3 blok → şube müdürüne bildirim; her cevap PIN sahibine ve cihaz kimliğine yazılır.
- **BR-20 · Kişi skoru yok.** Puan, sıralama, karşılaştırma ve rozet yalnızca şube/bölge/liste düzeyinde hesaplanır; kişi düzeyinde yalnızca gecikme/eksik listesi (şube/bölge müdürüne görünür); personel kendi kaydını görür (ADR-0007).
- **BR-22 · Pasifleştirme.** Pasif kullanıcının kayıtları (cevap, kanıt, log) değişmeden kalır; kimlik alanları maskelenebilir; maskeleme geri alınamaz.

- **BR-26 · Çalıştırma kilidi.** Atanmamış çalıştırma şubedeki herkeste görünür; ilk açan kullanıcı alır (kilit 30 dk, etkinlikle yenilenir); diğerleri "X yapıyor" görür ve açamaz; kilit dolarsa veya sahibi bırakırsa serbest kalır; şube müdürü kilidi kaldırabilir; kilit olayları logda.
- **BR-27 · Sabah özeti.** Her gün 07:00 (şube saat dilimi; bölge için en erken şube), bölge müdürüne bölgesi, yöneticiye tüm hesap: önceki iş gününde kaçırılan ve başarısız çalıştırmalar, yapılamayan maddeler, gecikmiş aksiyonlar; push + e-posta; sorun yoksa "her şey yolunda".

## Uyum

- **BR-21 · Saklama.** Kanıt dosyaları saklama süresi (v1 sabit 24 ay; v1.1 ayar 6–60 ay) sonunda silinir; cevap değerleri ve olay günlüğü özeti kalır; silme işlemi logda ve aylık raporda.
- **BR-25 · Duyuru onayı (v1.1).** "Okudum ve anladım" onayı zaman damgalıdır; 48 sa (ayar) sonra onaylamayanlara otomatik hatırlatma; imza zorunlu duyuruda onay ancak imzayla tamamlanır; onay geri alınamaz.

## Parametre tablosu

v1'de tümü sabittir; "Aralık" sütunu v1.1'deki ayar sınırlarıdır.

| Parametre | v1 sabit değer | Aralık (v1.1) | Kural |
|---|---|---|---|
| Tolerans (kapanış / saatlik / haftalık) | 120 / 0 / 240 dk (plan bazında) | 0–240 | BR-02 |
| Puan eşiği | — (yalnızca kritik kuralı) | 50–100 | BR-06, BR-07 |
| Aksiyon vadeleri (kritik/yüksek/orta) | 4 sa / 24 sa / 72 sa | — | BR-10 |
| Sabah özeti saati | 07:00 | 05:00–10:00 | BR-27 |
| Kritik SMS gecikmesi | 10 dk | 5–30 dk | BR-11 |
| Sessiz saatler | 23:00–07:00 | — | BR-23 |
| Kiosk kilit süresi | 2 dk | 1–10 dk | BR-19 |
| Çalıştırma kilidi | 30 dk | 10–120 dk | BR-26 |
| Saklama süresi | 24 ay | 6–60 ay | BR-21 |
| Uzak konum eşiği | 500 m | 100–2.000 m | BR-15 |
| Saat farkı bayrağı eşiği | 10 dk | 1–60 dk | BR-13 |
| Fotoğraf / madde | 1 varsayılan, 3 en çok | 1–5 | FR-0604 |
