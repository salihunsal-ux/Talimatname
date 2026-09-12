# ADR-0005 · Tekrar kuralları RRULE (RFC 5545) + pencere kavramı

- Tarih: 2026-09-12 · Durum: Kabul edildi

## Bağlam
Listeler günlük (birden çok saat), saatlik, haftalık, aylık tekrar eder; kapanış penceresi gece yarısını aşar (22:00–01:30); tatil/kapalı günler vardır; şubeler farklı çalışma saatleriyle çalışır.

## Karar
- Tekrar tanımı standart **RRULE** dizesiyle saklanır (kütüphane desteği, öngörülebilirlik); şube saat diliminde değerlendirilir.
- Her tekrar bir **pencere** üretir: `baslangic`, `bitis`, `tolerans` (geç gönderim süresi). Gece yarısını aşan pencere açılış gününe yazılır (iş günü = pencere başlangıç tarihi).
- Çalıştırmalar 7 gün ileriye önceden üretilir (arka plan işi); kural değişince gelecekteki üretilmemiş/başlanmamış çalıştırmalar yeniden hesaplanır, başlanmış olanlar korunur.
- Şube kapalı gün takvimi çalıştırma üretimini bastırır; rapora "kapalı" düşer.

## Sonuçlar
- Vardiya bazlı tekrar (P-8) şube "vardiya saatleri" tanımıyla RRULE'a çevrilir; PDKS entegrasyonu sonra.
- Yaz saati geçişleri test senaryosu olarak zorunlu (TC).
