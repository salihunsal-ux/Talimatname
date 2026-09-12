# ADR-0002 · Mobil Flutter, web React, backend Python/FastAPI, PostgreSQL

- Tarih: 2026-09-12 · Durum: Kabul edildi

## Bağlam
Personel uygulaması iOS ve Android'de düşük segment cihazlarda, çevrimdışı öncelikli çalışmalı; yönetim paneli web; ekip küçük (2 geliştirici). Tek kod tabanıyla iki platform ve yerel kamera/dosya erişimi gerekiyor.

## Karar
- Mobil: **Flutter** (tek kod tabanı, düşük segment Android performansı, kamera/dosya erişimi, SQLite ile çevrimdışı kuyruk).
- Web paneli: **React + TypeScript** (şablon editörü ve panolar için olgun bileşen ekosistemi).
- Backend: **Python 3.12 + FastAPI**, **PostgreSQL 16**, nesne depolama **S3 uyumlu** (yerel bulut sağlayıcı), kuyruk **Redis** (bildirim, PDF üretimi, senk işleri).
- Bildirim: FCM/APNs push; SMS yerel sağlayıcı (yedek kanal).

## Sonuçlar
- İki geliştiriciyle üç yüzey; paylaşılan tipler için OpenAPI'den istemci üretimi zorunlu.
- Flutter web hedeflenmez; yönetici mobil görünümü Flutter uygulaması içinde ayrı rol ekranlarıdır.
