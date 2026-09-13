# ADR-0008 · v1 çekirdek: basit, ilk gün kullanılabilir, en önemli yetenekler

- Tarih: 2026-09-13 · Durum: Kabul edildi (kullanıcı onayı; K1–K21 ve E1–E7 tamamı)

## Bağlam
İlk kapsam (02-urun/03) 57 Must satırı, 140 Must gereksinim, 138 hikâye, 25 ekran ve 7 rol içeriyordu; iki geliştiriciye 12 sprint, tampon yok. Aktör gözüyle gözden geçirme (02-urun/05) bunun bir ilk sürüm değil 1.x yol haritası olduğunu gösterdi: personelin 6–8 dakikalık gece akışına sürtünme, şube müdürüne iş yükü, gece 03:30 SMS gibi gerçek hayata aykırı kurallar, kimsenin bakmayacağı raporlar.

## Karar
1. v1 yalnızca **çekirdek döngüyü** içerir: merkez listeyi ve planı kurar → personel kioskta/telefonda tamamlar ve fotoğrafla kanıtlar → sistem pencereyi izler, kaçırılanı ve kritik olanı bildirir → yönetici istisna odaklı ızgara, sabah özeti ve PDF ile görür.
2. **Sıra ilkesi:** bir özellik v1'e ancak "personel görmese liste tamamlanmaz mı / yönetici görmese kaçırılan iş görünmez mi / bu olmadan denetimde kanıt verilemez mi" sorularından birine "evet" alırsa girer.
3. Kesintiler K1–K21 ve eklemeler E1–E7 (02-urun/05 §3) aynen uygulanır; kaynak belge artık **02-urun/06-v1-cekirdek-kapsam.md**; 02-urun/03 tarihsel referanstır.
4. Roller v1'de dört: Yönetici (merkez), Bölge müdürü, Şube müdürü, Personel.
5. Parametreler v1'de sabittir (tolerans, vadeler, sessiz saat, saklama); ayar paneli v1.1.
6. Ertelenen her madde silinmez; "v1.1" (veya "v2") etiketiyle aynı belgelerde kalır ve pilot geri bildirimiyle sıralanır. ID'ler değişmez.

## Sonuçlar
- Kapsam ~34 Must satırı, ~80 v1 gereksinimi, 16 ekran, ~85 hikâye; GA 10. sprint, 2 sprint tampon.
- Hash zinciri ve saklama arka planda ilk günden çalışır; ekranları v1.1. KVKK talepleri v1'de destek süreciyle (betik), ekran v1.1.
- Duyuru modülü olmadığı için müşteri duyuru için WhatsApp'ı kullanmaya devam eder — bilinçli; ürünün v1 iddiası "liste + kanıt".
- Sabah özeti (07:00 push + e-posta) yönetici tarafının ana kanalıdır; gece SMS yalnızca kritik sıcaklık için.
