# ADR-0006 · WhatsApp entegrasyonu MVP dışı

- Tarih: 2026-09-12 · Durum: Kabul edildi

## Bağlam
Bildirimlerin WhatsApp Business API üzerinden gitmesi benimseme engelini düşürebilirdi (TR yardımcı mesaj ≈0,0014 $). Ancak BSP entegrasyonu, şablon onayları ve kanıt bütünlüğü (WhatsApp'tan yükleme) kapsamı büyütüyor.

## Karar
MVP'de WhatsApp yok. Bildirim katmanı kanal-bağımsız yazılır (push öncelikli, kritik olaylarda SMS yedek); WhatsApp v1.x'te kanal olarak eklenebilir. Benimseme riski ortak cihaz (kiosk) modu ve yerinde onboarding ile karşılanır.

## Sonuçlar
- Bildirim servisi arayüzü: `kanal`, `alıcı`, `olay`, `içerik`, `teslimat izi` — WhatsApp eklenince yalnızca yeni kanal uygulaması.
