# Hukuki metin taslakları

Durum: **taslak — avukat incelemesi gerekli.** Bu metinler hukuki görüş değildir; KVKK (6698) ve ilgili tebliğlere göre ürün gereksinimlerinden (06-kvkk-ve-guvenlik.md) türetilmiş çalışma taslaklarıdır. Avukat onayı olmadan pilotta kullanılmaz; onaylı sürüm ürün içine (FR-1312: indirilebilir belgeler; U-3: ilk girişte aydınlatma) ve LOI 7. maddesine bağlanır.

| Dosya | Ne | Kim imzalar / gösterir | Ne zaman gerekir |
|---|---|---|---|
| [01-aydinlatma-metni-personel.md](01-aydinlatma-metni-personel.md) | Zincirin (veri sorumlusu) personeline aydınlatma metni — tam metin + uygulama içi kısa katman + konum ve kiosk ekran metinleri | Zincir; uygulama ilk girişte gösterir, "okudum" zaman damgalı | Pilot kurulumundan önce (7. hafta); personel dosyası yüklenmeden |
| [02-veri-isleme-sozlesmesi.md](02-veri-isleme-sozlesmesi.md) | Talimatname (veri işleyen) ile zincir (veri sorumlusu) arasında veri işleme sözleşmesi + alt işleyen listesi eki | İki taraf; LOI 7. maddesinin bağlayıcı kısmını ayrıntılandırır | LOI imzasıyla birlikte veya pilot sözleşmesiyle (5–7. hafta) |

## Avukata sorulacaklar (taslakta işaretli yerler)

1. **Push bildirimleri ve yurt dışı aktarım (m.9):** FCM/APNs üzerinden geçen veri yalnızca cihaz belirteci ve kişisel içerik taşımayan kısa metin ("Kapanış listesi açıldı"). Bu, m.9 kapsamında "aktarım" sayılır mı; sayılırsa 2024 değişikliğindeki standart sözleşme yolu mu, yoksa istisna mı? Aydınlatma metninde nasıl ifade edilmeli?
2. **Hukuki sebep:** personel verisi için açık rıza yerine sözleşmenin ifası (m.5/2-c), hukuki yükümlülük (m.5/2-ç; gıda hijyeni kayıtları) ve meşru menfaat (m.5/2-f) dayanaklarını kullandık; konum (tek nokta) için meşru menfaat dengeleme testinin yazılı yapılması gerekir mi?
3. **Silme yerine maskeleme:** personel ayrılınca kimlik alanları maskelenip iş kaydı (cevap, zaman, şube) anonim kalıyor (BR-21/22, gıda kaydı bütünlüğü). "Anonim hâle getirme" olarak kabul edilebilir mi; hangi koşullarla?
4. **Kiosk (ortak cihaz) ve aydınlatma kanıtı:** aydınlatma onayı ortak tablette PIN geçişinde alınıyor; kişiye bağlı zaman damgalı log yeterli kanıt mı, ayrıca ıslak imza/İK dosyası gerekir mi?
5. **VERBİS:** Talimatname şirketi ve pilot zincirler için kayıt eşiği (çalışan sayısı / bilanço) değerlendirmesi.
6. **Saklama süresi:** kanıt dosyaları varsayılan 24 ay; iş kayıtları için iş hukuku/ticari defter süreleri (5–10 yıl) ile çelişki var mı? Zincir isterse 24 ayı uzatabilir; varsayılanın gerekçesi.
7. **Veri ihlali bildirim süresi:** veri işleyen → veri sorumlusu için taslakta 24 saat; Kurul'a 72 saat (Kurul 2019/10). Uygun mu?
8. **Sözleşme dili:** LOI ve veri işleme sözleşmesinin bağlayıcılık sınırı; cezai şart konulup konulmayacağı (taslakta yok).

## Ürünle bağ

- Uygulama ilk girişte kısa katmanı gösterir, tam metne bağlantı verir; onay `audit.emit()` ile sürüm numarasıyla loglanır (TC-012).
- Hesap yöneticisi tam metindeki zincir alanlarını (unvan, adres, başvuru kanalı) panelden doldurur; metin sürümlenir; değişince yeniden gösterilir (06-kvkk §Aydınlatma 5).
- Veri işleme sözleşmesi eki (alt işleyenler) ürün belgesi olarak yayınlanır; değişiklikte 30 gün önce bildirim.
