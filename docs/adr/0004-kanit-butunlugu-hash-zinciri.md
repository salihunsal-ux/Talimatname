# ADR-0004 · Kanıt bütünlüğü: sunucu zamanı, dosya hash'i, ekle-yalnız olay günlüğü

- Tarih: 2026-09-12 · Durum: Kabul edildi

## Bağlam
Ürünün değeri kanıtın sonradan değiştirilemezliğine dayanır ("fotoğrafı dün çekmiş" itirazı). Cihaz saati güvenilmez; personel galeriden eski fotoğraf yükleyebilir; yönetici kaydı düzeltmek isteyebilir.

## Karar
1. Zaman: her kayıt sunucu zamanıyla damgalanır; cihaz saati farkı ayrıca loglanır. Çevrimdışı kayıtlarda çekim anı = cihaz zamanı + senk anında hesaplanan sunucu farkı düzeltmesi (logda ham ve düzeltilmiş).
2. Kanıt: dosyanın SHA-256 özeti cevaba bağlanır; şablon "yalnızca kamera" derse galeri kapalı; fotoğrafa görünür damga (şube, tarih-saat, kullanıcı) sunucu tarafında basılır, ham dosya da saklanır.
3. Olay günlüğü: ekle-yalnız tablo; her olay `önceki_hash + olay_json` üzerinden zincirlenir; günlük kök özeti günde bir dış zaman damgası servisine yazılır (RFC 3161).
4. Düzeltme: gönderilmiş kayıt değiştirilemez; düzeltme yeni "ek" kaydıdır, eski görünür kalır.

## Sonuçlar
- Depolama artar (ham + damgalı); kabul edilebilir (fotoğraf ≤300 KB).
- Denetim PDF'i doğrulama kodu (hash) taşır; müşteri doğrulama sayfasında kontrol edebilir (v1.x).
