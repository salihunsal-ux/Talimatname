# İş kuralları

Kod ve testlerin tek referansı. Her kural tek cümle + kesin parametre; parametreler hesap düzeyinde düzenlenebiliyorsa "(ayar)" yazılır ve varsayılan verilir.

## Pencere, iş günü, durum

- **BR-01 · İş günü.** Bir çalıştırmanın iş günü = pencere başlangıç tarihi (şube saat diliminde). Gece yarısını aşan pencere (22:00–01:30) önceki güne aittir; raporlar ve ızgara iş gününe göre gruplar.
- **BR-02 · Tolerans.** Pencere bitişinden sonra `tolerans` (plan ayarı, 0–240 dk, varsayılan kapanış 120 / saatlik 0) içinde gönderilen çalıştırma "Geç tamamlandı" sayılır; zamanındalık raporunda ayrı gösterilir.
- **BR-03 · Kaçırıldı kesindir.** Tolerans bitiminde tamamlanmamış çalıştırma "Kaçırıldı" olur; sonradan cevap girilemez, düzenlenemez; yalnızca ek not eklenebilir (logda).
- **BR-04 · Yapılmayacak.** Yalnızca şube müdürü ve üstü, sebep (seçim + not) girerek "Yapılmayacak" işaretleyebilir; puanlamaya girmez, raporda ayrı sayılır, eskalasyonu durdurur; işaretleme olayı logda.
- **BR-16 · Tamamlama kuralı.** "Biri tamamlasın": ilk gönderim çalıştırmayı kapatır. "Herkes tamamlasın": her atanan kendi bölümünü gönderir; çalıştırma, tüm atananlar gönderince tamamlanır; tolerans sonunda eksik atananlar "eksik" olarak raporlanır (kişi puanı değil).
- **BR-17 · Kapalı gün.** Şube kapalı gün takviminde çalıştırma üretilmez; ızgara hücresi "kapalı"; hesap düzeyi resmî tatil takvimi devralınır, şube geçersiz kılabilir.
- **BR-18 · Sürüm bağı.** Çalıştırma, üretildiği andaki şablon sürümüne bağlanır; şablon değişince başlanmamış (Planlandı) çalıştırmalar yeni sürüme geçer, başlanmış olanlar eski sürümde biter.

## Madde, puan, kanıt

- **BR-05 · Gönderim kilidi.** Zorunlu maddelerin tamamı cevaplanmadan (cevap, "yapılamadı" veya koşulla atlanmış) gönderim yapılamaz.
- **BR-06 · Kritik madde.** Kritik işaretli bir madde başarısızsa (hayır/uygun değil/aralık dışı/yapılamadı) çalıştırma puandan bağımsız "Başarısız" işaretlenir ve kritik aksiyon açılır.
- **BR-07 · Puan.** Liste puanı = Σ(geçen madde ağırlığı) / Σ(puanlanan madde ağırlığı) × 100; talimat maddeleri ve koşulla atlanan maddeler puanlanmaz; eşik (şablon ayarı, varsayılan %90) altı "Başarısız".
- **BR-08 · Sıcaklık.** Kabul aralığı dışındaki ölçüm maddeyi başarısız yapar, fotoğraf ve not ister (koşul varsayılanı), kritik ise BR-06 uygulanır; aralık sınırları dahildir (0–4 °C: 4,0 geçer, 4,1 geçmez).
- **BR-09 · Yapılamadı.** Sebep seçimi zorunlu; "Diğer" → not ≥ 5 karakter zorunlu; kritik maddede veya şablon kapatmışsa "Yapılamadı" yoktur.
- **BR-12 · Kanıt değişmez.** Gönderilmiş cevap ve kanıt üzerine yazılmaz; düzeltme yeni "ek" kayıttır; eski görünür kalır; silme yoktur (KVKK silme hariç, o da maskeleme/dosya silme + log).
- **BR-13 · Sunucu zamanı.** Tüm olaylarda sunucu zamanı esastır; çevrimdışı kayıtlarda çekim zamanı = cihaz zamanı + senk anında hesaplanan fark; ham cihaz zamanı ve fark saklanır; fark 10 dk'yı aşıyorsa kanıt "saat farkı" bayrağı alır.
- **BR-14 · Yalnızca kamera.** Şablon "yalnızca kamera" ise galeri/dosya seçimi sunulmaz; kanıt uygulama içi kameradan gelir; ayar kapalıysa galeri kanıtı "galeri" bayrağıyla işaretlenir.
- **BR-15 · Konum.** Konum yalnızca cevap anında tek nokta olarak alınır; izin yoksa "konum yok" bayrağı; şube konumuna uzaklık > 500 m ise "uzak" bayrağı; sürekli izleme yoktur.
- **BR-24 · Çakışma.** Aynı maddeye iki cihazdan cevap gelirse sunucu zamanına göre son yazan kazanır; önceki cevap "üzerine yazıldı" olayıyla logda kalır; kanıt dosyaları asla silinmez.

## Aksiyon ve eskalasyon

- **BR-10 · Otomatik aksiyon.** Tetik: koşullu mantık "aksiyon oluştur", aralık dışı ölçüm, "yapılamadı", kaçırılan çalıştırma. Varsayılan atanan: şube müdürü (şube için tanımlı değilse bölge müdürü). Vade = oluşturma + öncelik süresi: kritik 4 sa, yüksek 24 sa, orta 72 sa, düşük 7 gün (ayar). Aynı kaynak için tek aksiyon.
- **BR-11 · Eskalasyon merdiveni (varsayılan).** Kaçırılan çalıştırma: 0. adım şube müdürü (push); +2 sa bölge müdürü (push, kritik listede + SMS); +24 sa operasyon müdürü (push + e-posta). Gecikmiş aksiyon: vade + 0 atanana; +4 sa bir üst rol; +24 sa merkez. Plan/şablon bazında özelleştirilebilir (ayar).
- **BR-23 · Kanal.** Varsayılan kanal push; SMS yalnızca OTP, kritik liste hatırlatmaları, eskalasyon adımları ve push teslim edilemeyen kritik olaylar için. Sessiz saatler (ayar, varsayılan 23:00–07:00) yönetici bildirimlerine uygulanır; kritik ve eskalasyon hariç.

## Kimlik, cihaz, kişi

- **BR-19 · Kiosk.** 2 dk hareketsizlikte kilit (ayar 1–10 dk); 5 hatalı PIN → 1 dk blok; art arda 3 blok → şube müdürüne bildirim; her cevap PIN sahibine ve cihaz kimliğine yazılır.
- **BR-20 · Kişi skoru yok.** Puan, sıralama, karşılaştırma ve rozet yalnızca şube/bölge/liste düzeyinde hesaplanır; kişi düzeyinde yalnızca gecikme/eksik listesi (şube/bölge müdürüne görünür); personel kendi kaydını görür (ADR-0007).
- **BR-22 · Pasifleştirme.** Pasif kullanıcının kayıtları (cevap, kanıt, log) değişmeden kalır; kimlik alanları maskelenebilir; maskeleme geri alınamaz.

## Uyum

- **BR-21 · Saklama.** Kanıt dosyaları hesap saklama süresi (ayar, varsayılan 24 ay, 6–60 ay) sonunda silinir; cevap değerleri ve olay günlüğü özeti kalır; silme işlemi logda ve aylık raporda.
- **BR-25 · Duyuru onayı.** "Okudum ve anladım" onayı zaman damgalıdır; 48 sa (ayar) sonra onaylamayanlara otomatik hatırlatma; imza zorunlu duyuruda onay ancak imzayla tamamlanır; onay geri alınamaz.

## Parametre tablosu (hesap ayarları)

| Parametre | Varsayılan | Aralık | Kural |
|---|---|---|---|
| Tolerans (kapanış / saatlik / haftalık) | 120 / 0 / 240 dk | 0–240 | BR-02 |
| Puan eşiği | %90 | 50–100 | BR-07 |
| Aksiyon vadeleri (kritik/yüksek/orta/düşük) | 4 sa / 24 sa / 72 sa / 7 gün | — | BR-10 |
| Eskalasyon gecikmeleri | +2 sa, +24 sa | 15 dk – 72 sa | BR-11 |
| Sessiz saatler | 23:00–07:00 | — | BR-23 |
| Kiosk kilit süresi | 2 dk | 1–10 dk | BR-19 |
| Saklama süresi | 24 ay | 6–60 ay | BR-21 |
| Duyuru hatırlatma | 48 sa | 12–168 sa | BR-25 |
| Uzak konum eşiği | 500 m | 100–2.000 m | BR-15 |
| Saat farkı bayrağı eşiği | 10 dk | 1–60 dk | BR-13 |
