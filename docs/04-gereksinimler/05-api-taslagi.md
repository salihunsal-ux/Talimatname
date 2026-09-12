# API taslağı

REST + JSON, OpenAPI 3.1 sözleşmesi geliştirme deposunda üretilir (`openapi.yaml`); mobil ve web istemcileri sözleşmeden üretilir. Bu belge kaynak/uç nokta taslağı ve sözleşme ilkeleridir; alan düzeyi ayrıntı OpenAPI'de.

## İlkeler

- Taban: `https://api.<alan>/v1`. Kimlik: `Authorization: Bearer <JWT>` (erişim 15 dk, yenileme belirteci mobilde 30 gün / web 12 sa). Her belirteç `hesap_id`, `kullanici_id`, roller ve kapsamları taşır; sunucu her uç noktada kapsam denetler (FR-0205).
- Kiosk: cihaz belirteci (`X-Device-Token`) + PIN geçişiyle alınan kısa ömürlü kullanıcı belirteci.
- Idempotency: yazma uç noktalarında `Idempotency-Key` (istemci UUID); cevap/kanıt kimlikleri istemci üretimli.
- Sayfalama: imleç tabanlı (`?cursor=&limit=`), varsayılan 50, en çok 200. Sıralama alanı belirtilir.
- Hatalar: RFC 9457 problem details (`type`, `title`, `status`, `detail`, `errors[]`); iş kuralı ihlali `422` + `code` (örn. `BR-05`).
- Zaman: ISO 8601 UTC; şube saat dilimi yanıtta ayrı alan.
- Sürüm: yol sürümü (`/v1`); alan ekleme geriye uyumlu; kaldırma yeni sürümde.
- Hız sınırı: kullanıcı başına 600 istek/dk; OTP 3/15 dk; PDF 10/saat.

## Kaynaklar ve uç noktalar

### Kimlik
| Yöntem | Yol | Amaç |
|---|---|---|
| POST | /auth/otp/request | Telefon → OTP SMS |
| POST | /auth/otp/verify | OTP → belirteç çifti (ilk girişte aydınlatma durumu) |
| POST | /auth/login | E-posta + şifre (+ TOTP) |
| POST | /auth/refresh · /auth/logout | Yenileme / sonlandırma |
| POST | /devices/register · /devices/{id}/kiosk | Cihaz kaydı (push token), kiosk QR eşleme |
| POST | /kiosk/switch | PIN ile kullanıcı geçişi → kısa ömürlü belirteç |
| POST | /me/consent · GET /me | Aydınlatma onayı, profil |

### Organizasyon ve kullanıcılar
| Yöntem | Yol | Amaç |
|---|---|---|
| GET/POST/PATCH | /regions, /sites, /sites/{id}/stations | Hiyerarşi |
| POST | /imports/sites · /imports/users | Excel yükleme (asenkron iş, doğrulama raporu) |
| GET/POST/PATCH | /users, /users/{id}/roles, /users/{id}/deactivate, /users/{id}/mask | Personel, rol, pasifleştirme, maskeleme |
| GET/POST/PATCH | /groups | Akıllı gruplar (kural + üyelik önizleme) |
| GET/PATCH | /account/settings · /account/calendar | Hesap ayarları, tatil takvimi |

### Şablon ve plan
| Yöntem | Yol | Amaç |
|---|---|---|
| GET/POST | /templates · /templates/{id}/versions | Şablonlar ve sürümler |
| PATCH | /template-versions/{id} (taslak) · POST …/publish · POST …/validate | Düzenleme, yayın, doğrulama |
| GET/POST | /library/templates · POST /library/templates/{id}/copy | Kütüphane |
| POST | /template-versions/{id}/rules/test | Kural deneme (Should) |
| GET/POST/PATCH | /plans · GET /plans/{id}/preview?days=7 | Plan ve önizleme |
| POST | /plans/oneoff | Tek seferlik liste |

### Çalıştırma ve cevaplar (mobil ana yol)
| Yöntem | Yol | Amaç |
|---|---|---|
| GET | /runs?site=&from=&to= · GET /runs/today | Bugün / dönem çalıştırmaları (önbellek için ETag) |
| GET | /runs/{id} | Detay (maddeler, cevaplar, kanıt küçük resimleri) |
| PATCH | /runs/{id}/assignments | Günlük yeniden atama (FR-0519) |
| PUT | /runs/{id}/answers/{answerId} | Madde cevabı (idempotent; çevrimdışı kuyruk buradan boşalır) |
| POST | /runs/{id}/submit | Gönderim → puan/durum (BR-05…07) |
| POST | /runs/{id}/wont-do | Yapılmayacak (BR-04) |
| POST | /runs/{id}/addenda | Ek kayıt (BR-12) |
| POST | /evidence/upload-url · POST /evidence/{id}/complete | Ön imzalı yükleme URL'si; yükleme tamamlandı (hash doğrulama, damgalama işi) |
| GET | /evidence/{id}?variant=stamped|raw | İmzalı, 15 dk süreli indirme URL'si |
| POST | /sync/batch | Çevrimdışı kuyruk toplu senk (cevaplar + kanıt meta; zaman farkı hesabı) |
| GET | /sync/manifest?since= | Delta senk (değişen çalıştırma/şablon/sebep seti) |

### Sorun, aksiyon, eskalasyon
| Yöntem | Yol | Amaç |
|---|---|---|
| POST/GET | /issues | Sorun bildir/listele |
| POST | /issues/{id}/convert · /issues/{id}/escalate · /issues/{id}/close | Aksiyona çevir, yükselt, kapat |
| GET/POST/PATCH | /actions · /actions/{id}/transition · /actions/{id}/comments | Aksiyonlar, durum geçişi, yorumlar |
| GET | /escalations?source= | Eskalasyon adımları (destek/denetim) |

### Duyuru ve bildirim
| Yöntem | Yol | Amaç |
|---|---|---|
| GET/POST | /announcements · POST /announcements/{id}/ack · POST …/remind | Duyuru, onay, hatırlatma |
| GET/PATCH | /me/notification-preferences | Tercihler |
| GET | /notifications?user= | Teslimat izi (destek/yönetici) |

### Rapor ve dışa aktarım
| Yöntem | Yol | Amaç |
|---|---|---|
| GET | /reports/grid?date=&region= | Operasyon ızgarası |
| GET | /reports/completion · /reports/failed-items · /reports/reasons · /reports/measurements · /reports/actions | Raporlar (filtre: şube, bölge, şablon, dönem) |
| GET | /reports/person-followup?site= | Kişi düzeyi gecikme/eksik (yetki: şube/bölge müdürü; BR-20) |
| GET | /evidence?site=&station=&item=&from=&to= | Kanıt galerisi |
| POST | /exports/run-pdf · /exports/period-pdf · /exports/excel | Asenkron üretim; `GET /exports/{id}` durum + indirme |
| POST | /exports/{id}/share | Süreli paylaşım bağlantısı |

### Denetim izi ve uyum
| Yöntem | Yol | Amaç |
|---|---|---|
| GET | /audit?object=&from=&to= · GET /audit/verify?from=&to= | Olay izi, zincir doğrulama |
| GET | /audit/roots?date= | Günlük kök ve RFC 3161 damgası |
| POST/GET | /privacy/requests · /privacy/requests/{id} | KVKK dışa aktarma / silme talepleri |
| GET/PATCH | /account/retention | Saklama politikası |

### Salt okunur API ve webhook (Should)
| Yöntem | Yol | Amaç |
|---|---|---|
| GET | /public/v1/runs · /answers · /actions · /measurements | Hesap API anahtarıyla, salt okunur, imleç sayfalı |
| POST/GET | /webhooks | Olay abonelikleri: run.missed, item.critical_failed, action.overdue (HMAC imzalı) |

## Çevrimdışı senk sözleşmesi (özet)

1. İstemci `GET /sync/manifest?since=<son_senk>` ile değişen kayıtları alır (çalıştırmalar 48 sa ileri, şablon sürümleri, sebep/yanıt setleri, duyurular).
2. Yerel kuyruktaki cevaplar `POST /sync/batch` ile gönderilir: her öğe `{id, run_id, item_id, value, device_time, device_now}`; sunucu `zaman_farki = server_now − device_now` hesaplar, `sunucu_zamani = device_time + zaman_farki`.
3. Kanıtlar için `POST /evidence/upload-url` → doğrudan nesne depoya PUT → `POST /evidence/{id}/complete` (sha256 gönderilir; sunucu doğrular, damgalama işini kuyruğa atar).
4. Yanıt her öğe için `accepted | conflict(overwritten) | rejected(code)`; `conflict` bilgilendirir, istemci yeniden denemez.
5. Tüm adımlar idempotent; aynı `id` ikinci kez gelirse `accepted` döner, kayıt değişmez.

## Olay türleri (webhook ve bildirim ortak sözlüğü)

`run.opened`, `run.reminder`, `run.window_closed`, `run.completed`, `run.late`, `run.missed`, `run.failed`, `run.wont_do`, `item.critical_failed`, `item.out_of_range`, `item.could_not_do`, `issue.reported`, `action.created`, `action.assigned`, `action.due_soon`, `action.overdue`, `action.closed`, `escalation.step`, `announcement.published`, `announcement.reminder`, `privacy.request`.
