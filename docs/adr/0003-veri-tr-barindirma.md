# ADR-0003 · Veri Türkiye'de barındırılır

- Tarih: 2026-09-12 · Durum: Kabul edildi (pilot BT şartlarına göre gözden geçirilir)

## Bağlam
Ürün çalışanların kişisel verisini (ad, telefon, fotoğraf, görev anı konumu) işler. KVKK'da yurt dışı aktarım, 2024 değişikliğiyle standart sözleşme yoluyla mümkün olsa da hedef müşterilerin (zincir BT/hukuk) beklentisi çoğunlukla "veri Türkiye'de".

## Karar
Üretim ortamı Türkiye'de yerel bulut sağlayıcıda; nesne depolama aynı sağlayıcıda. Pilot görüşmeleri "AB + standart sözleşme kabul edilir" derse ikinci bölge seçeneği açılır. Uygulama katmanı sağlayıcıdan bağımsız (Docker, S3 uyumlu API, yönetilen PostgreSQL yerine kendi örneği kabul edilebilir).

## Sonuçlar
- Maliyet farkı önemsiz; yönetilen servis çeşitliliği daha az — yedekleme ve izleme kendi sorumluluğumuz.
- Veri işleyen sıfatıyla müşteriyle veri işleme sözleşmesi şart.
