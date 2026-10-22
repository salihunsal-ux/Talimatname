# Kod sözlüğü: Türkçe alan terimi → İngilizce tanımlayıcı

[ADR-0014](../adr/0014-kod-duzeni-katmanlar-ve-standartlar.md) md.7'nin tek kaynağı. Kural: **kod İngilizce, kullanıcıya görünen metin Türkçe.** Sözlükte olmayan bir terim kodda icat edilmez; önce buraya eklenir (PR'da bir satır). Belgelerdeki Türkçe terim değişmez — eşleme burada yapılır.

## Organizasyon ve kimlik

| Türkçe | Kod | Not |
|---|---|---|
| Hesap / kiracı | `tenant` | Çok kiracılılığın birimi; her tabloda `tenant_id` |
| Marka | `brand` | Hesap içinde markalaşma (logo, renk) |
| Bölge | `region` | |
| Şube | `branch` | |
| İstasyon | `station` | Şube içi nokta (mutfak, bar, tuvalet) |
| Çalışma saatleri | `business_hours` | Haftanın gününe göre açılış/kapanış |
| Tatil / kapalı gün | `closed_day`, `holiday_calendar` | |
| Kullanıcı | `user` | |
| Rol: Yönetici · Bölge müdürü · Şube müdürü · Personel | `admin` · `region_manager` · `branch_manager` · `staff` | Tek `enum`; kodda Türkçe karşılığı yok |
| Kapsam | `scope` | `tenant` \| `region` \| `branch` |
| Davet | `invitation` | |
| Pasifleştirme | `deactivate` | Silme değil |
| Maskeleme | `mask` | KVKK; `masked_at` |
| Kiosk cihazı | `kiosk_device` | |
| PIN | `pin` | Hash'li; `pin_hash` |

## Şablon ve içerik

| Türkçe | Kod | Not |
|---|---|---|
| Şablon | `template` | |
| Şablon sürümü | `template_version` | Yayınlanan sürüm değişmez |
| Bölüm | `section` | |
| Madde | `item` | |
| Madde türü | `item_type` | `confirm` \| `choice` \| `number` \| `temperature` \| `text` \| `photo` \| `instruction` |
| Talimat maddesi | `instruction` | Puanlanmaz |
| Zorunlu | `required` | |
| Fotoğraf zorunlu | `photo_required` | |
| Kritik madde | `critical` | |
| Sıcaklık aralığı | `min_value` / `max_value` | Tür `temperature` ve `number` |
| Puan | `score` | Yüzde; `scored_item_count` |
| Kütüphane şablonu | `library_template` | Kopyala-düzenle kaynağı |

## Planlama ve çalıştırma

| Türkçe | Kod | Not |
|---|---|---|
| Plan | `plan` | Şablon sürümü + kapsam + tekrar + atama |
| Tekrar kuralı | `recurrence` | RFC 5545 RRULE metni |
| Çıpa (çalışma saatinden türetme) | `anchor` | `open`/`close` + dakika ofseti |
| Pencere | `window` | `window_start`, `window_end` |
| Tolerans | `tolerance` | `tolerance_end` |
| İş günü | `business_day` | Pencere başlangıç tarihi (BR-01) |
| Çalıştırma | `run` | Belirli şube + plan + iş günü |
| Çalıştırma kilidi | `run_lock` | İlk açan alır (FR-0521) |
| Atama | `assignment` | `role` \| `user` \| `anyone` |
| Durum | `status` | `scheduled` \| `in_progress` \| `submitted` \| `missed` \| `cancelled` |
| Sonuç | `result` | `passed` \| `failed` (gönderilmiş çalıştırmada) |
| Geç tamamlandı | `late` | Durum değil, bayrak: `submitted` + `late=true` |
| Yapılmayacak | `cancelled` | Şube müdürü işaretler, sebep zorunlu |
| Tek seferlik liste | `one_off` | Planın `recurrence`'ı yok |

## Yürütme, kanıt, aksiyon

| Türkçe | Kod | Not |
|---|---|---|
| Cevap | `answer` | İstemcide üretilen `uuid` = idempotency anahtarı |
| Kanıt | `evidence` | |
| Ham / damgalı kopya | `raw_object_key` / `stamped_object_key` | |
| Damga | `stamp` | Sunucu basar; şube · zaman · kullanıcı · cihaz |
| Dosya özeti | `sha256` | |
| Kanıt bayrağı | `evidence_flag` | `gallery` \| `off_site` \| `device_clock` \| `late_sync` |
| Yapılamadı | `not_done` | `reason`, `note`; kritik maddede yok |
| Sorun bildirimi | `issue` | Kategori: `safety` \| `hygiene` \| `equipment` \| `stock` \| `other` |
| Aksiyon | `action` | `open` \| `closed`; `due_at`, `priority` |
| Öncelik | `priority` | `critical` \| `high` \| `normal` |
| Eskalasyon | `escalation` | |
| Ölçüm | `measurement` | Sıcaklık ve sayı cevaplarının zaman serisi görünümü |
| Aralık dışı | `out_of_range` | |
| Belge | `document` | `valid_until`, `owner_user_id` |
| Belge takvimi | `document_calendar` | |

## Bildirim, senk, uyum

| Türkçe | Kod | Not |
|---|---|---|
| Bildirim | `notification` | Kanal-bağımsız arayüz |
| Kanal | `channel` | `push` \| `sms` \| `email` |
| Teslim izi | `delivery_trace` | |
| Sessiz saat | `quiet_hours` | |
| Sabah özeti | `morning_digest` | |
| Çevrimdışı kuyruk | `outbox` | Cihazdaki yazma kuyruğu |
| Eşitleme | `sync` | `/sync/manifest`, `/sync/batch` |
| Zaman düzeltmesi | `clock_skew` | Cihaz saati farkı; kaydedilir, kullanılmaz |
| Olay günlüğü | `audit_log` | Ekle-yalnız |
| Olay | `audit_event` | `actor`, `action`, `subject`, `prev_hash`, `hash` |
| Günlük kök | `daily_root` | |
| Aydınlatma metni | `privacy_notice` | Sürümlü, onay zaman damgalı |
| Saklama | `retention` | Sabit 24 ay (v1) |
| Doğrulama kodu | `verification_code` | PDF'lerde |
| Tohum verisi | `seed` | |
| Fikstür | `fixture` | `spec/fikstur/*.json` |

## Yazım kuralları

- Veritabanı: `snake_case`, tablo adları **tekil** (`run`, `answer`, `audit_event`), birincil anahtar `id uuid`.
- Python: `snake_case`, sınıflar `PascalCase`; enum değerleri yukarıdaki dizelerin aynısı (`"region_manager"`), int değil.
- TypeScript: `camelCase` değişken, `PascalCase` tip; API'den gelen alan adları **dönüştürülmez** (`snake_case` kalır, üretilmiş istemci ne diyorsa).
- Zaman alanları `*_at` (`submitted_at`), tarih alanları `*_date` / `business_day`, süre alanları `*_minutes`.
- Boole alanları olumlu ve sıfat: `is_critical` değil `critical`, `late`, `required`.
- Kabul testi adı: `test_tc0NN_kisa_ad` — izlenebilirlik koda kadar iner (ADR-0014 md.9).
