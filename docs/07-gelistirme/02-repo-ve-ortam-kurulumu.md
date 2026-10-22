# Repo ve ortam kurulumu

## Depolar

| Depo | İçerik | Ana araçlar |
|---|---|---|
| `Talimatname` (bu depo) | Ürün dokümantasyonu, ADR, tasarım kaynakları | Markdown, HTML |
| `talimatname-api` | FastAPI backend, zamanlayıcı ve işçiler, Alembic göçleri, OpenAPI, tohum betiği, API testleri | Python 3.12, uv/poetry, pytest, ruff, mypy |
| `talimatname-mobile` | Flutter uygulaması (iOS/Android), üretilmiş API istemcisi, kural motoru, cihaz testleri | Flutter 3.x, Riverpod, Drift, Patrol |
| `talimatname-web` | React yönetim paneli, üretilmiş API istemcisi, Playwright testleri | Vite, TypeScript, TanStack, Playwright |
| `talimatname-infra` | Docker compose (dev/test), dağıtım tanımları, izleme yapılandırması, yedekleme betikleri | Docker, Terraform/Ansible (VM), GitHub Actions |
| `talimatname-spec` (isteğe bağlı, başlangıçta api içinde) | Kural motoru spesifikasyon fikstürleri (JSON): backend ve mobil aynı testleri geçer | JSON |

OpenAPI sözleşmesi `talimatname-api` içinde üretilir ve sürüm etiketiyle yayınlanır; mobil ve web istemcileri CI'da bu sözleşmeden üretilir (sürüm uyumsuzluğu derleme hatasıdır).

## Dallanma ve sürüm

- `main` korumalı; her iş `feat/ST-123-kisa-ad` dalında; PR + en az 1 inceleme + CI yeşil; squash merge.
- Sürüm etiketleri: `api-v1.4.0`, `mobile-v1.4.0` (semver); backend sürekli dağıtım (main → staging otomatik, prod onaylı); mobil 2 haftalık sürüm treni.
- Commit mesajı: Türkçe, `ST-123: …` öneki; hikâye numarası olmayan değişiklik yalnızca `chore:` / `fix:`.

## CI (GitHub Actions)

| Depo | Her PR | Gece | Etiket |
|---|---|---|---|
| api | ruff, mypy, pytest (birim + entegrasyon docker servisleriyle), Schemathesis sözleşme, bağımlılık taraması, Alembic göç kontrolü (ileri/geri) | Yük testi (k6, staging) | Konteyner imajı imzalı yayın |
| mobile | analyze, format, birim + widget testleri, kural spesifikasyon fikstürleri, derleme (Android APK, iOS simülatör) | Patrol E2E (Firebase Test Lab: düşük Android + tablet) | Mağaza dağıtımı (TestFlight / Play internal) |
| web | eslint, tsc, Vitest, Playwright (smoke) | Playwright tam E2E (staging) | Statik dağıtım |
| infra | terraform plan/validate | Yedek geri yükleme tatbikatı (aylık) | Dağıtım |

## Geliştirici ortamı (dev)

`talimatname-infra/dev/docker-compose.yml`: PostgreSQL 16, Redis 7, MinIO, sahte SMS/push/TSA servisleri, MailHog. `make dev` → servisler + göçler + tohum (Kahve Durağı) + API 8000. Mobil: `.env` ile API adresi (emülatör 10.0.2.2). Web: `VITE_API_URL`.

## Ortam değişkenleri (api, özet)

| Değişken | Örnek | Not |
|---|---|---|
| `DATABASE_URL` | postgresql://… | RLS için uygulama rolü; göç için ayrı rol |
| `REDIS_URL` | redis://… | |
| `OBJECT_STORE_ENDPOINT/BUCKET/KEY/SECRET` | … | Sürümleme açık; yaşam döngüsü kuralı yok (saklama uygulama tarafından) |
| `JWT_PRIVATE_KEY` / `JWT_PUBLIC_KEY` | RS256 | Kasadan |
| `SMS_PROVIDER`, `SMS_API_KEY` | … | Sahte: `fake` |
| `PUSH_FCM_CREDENTIALS`, `PUSH_APNS_*` | … | |
| `TSA_URL` | … | Sahte: yerel |
| `TIME_TRAVEL_ENABLED` | false | Yalnızca staging; prod'da derleme zamanında kapalı |
| `RETENTION_JOB_ENABLED` | true | |
| `LOG_LEVEL`, `SENTRY_DSN`, `OTEL_EXPORTER_*` | … | |

Gizli anahtarlar depoda yok; `.env.example` var; kasa (sağlayıcı KMS veya Vault).

Ortamlar arasındaki fark **yalnızca bu tablodur**: sağlayıcı değişmek, `DATABASE_URL`, `REDIS_URL` ve `OBJECT_STORE_*` değerlerinin değişmesi demektir — kod değişmez. [ADR-0012](../adr/0012-barindirma-saglayici-ve-ortamlar.md) md.4'ün taşınabilirlik şartı budur ve ortam değişikliğinin bir haftalık iş kalması buna bağlıdır. Sağlayıcıya özel SDK, kuyruk ya da kimlik servisi eklenmez; eklenmesi ADR değişikliği gerektirir.

## Sprint 0 kontrol listesi (2 hafta)

Takvim, ekip kararı ve teknik spike'lar: [05-sprint0-ve-teknik-spike.md](05-sprint0-ve-teknik-spike.md). Ortam ve sağlayıcı maddeleri [ADR-0012](../adr/0012-barindirma-saglayici-ve-ortamlar.md)'ye göre yazılmıştır: **üretim Türkiye'de**; geliştirme, CI ve staging ücretsiz ya da AB altyapıda olabilir — tek şart **gerçek kişisel veri olmaması**.

- [ ] Depolar açıldı, dal koruması, CODEOWNERS, PR şablonu (DoD kontrol listesi)
- [ ] `talimatname-api`: iskelet (FastAPI, Alembic, pytest), `audit.emit()` altyapısı, RLS politikası, OpenAPI yayını
- [ ] ~~`talimatname-mobile`: iskelet~~ → **Faz B'nin 1. haftası** (ADR-0013); Sprint 0'da yalnızca boş depo ve dal koruması açılır
- [ ] `talimatname-web`: iskelet (Vite, yönlendirme, tema token'ları, üretilmiş istemci, oturum)
- [ ] `talimatname-infra`: dev compose, sahte servisler, CI iş akışları, izleme temel
- [ ] **Staging ayakta — ücretsiz ya da AB altyapı yeterli**, içinde yalnızca tohum/fikstür verisi var (ADR-0012 md.2); `staging.talimatname.app` bağlı
- [ ] **Taşınabilirlik kontrolü** (ADR-0012 md.4): standart PostgreSQL 16, S3 uyumlu nesne depolama, Redis; sağlayıcıya özel hizmet (özel kuyruk/kimlik/fonksiyon) yok; dev ile staging aynı compose ve imajdan kalkıyor, aradaki tek fark ortam değişkeni
- [ ] **Üretim TR sağlayıcı kısa listesi**: 2–3 aday, ölçüt tablosuyla (KVKK/DPA belgeleri → yedek ve kurtarma → destek süresi → fiyat). Karar Sprint 2 sonuna kadar, **gerçek veri girmeden önce**
- [ ] **Yedek ve geri yükleme**: günlük otomatik veritabanı yedeği + nesne depoda sürümleme açık; geri yükleme betiği yazıldı ve Sprint 0'da **iki kez** (haftada bir) boş ortama koşturulup süresi ölçüldü — RTO 4 sa hedefi (NFR-13)
- [ ] **Gerçek veri yasağı denetlenebilir**: üretim dışı ortamlara gerçek kişisel veri kopyalanmaz; tohum betiği dışında veri yükleme yolu yok (06-test/03), üretim yedeğinden staging'e geri yükleme kapalı
- [ ] Tohum betiği v0 (hesap, 3 şube, 5 kullanıcı, 1 şablon, 1 plan) — tam set Sprint 3'e kadar
- [ ] Kural motoru spesifikasyon fikstürleri (puan, pencere/durum, koşullu mantık) — backend ve mobil ortak
- [ ] Sağlayıcı test hesapları: SMS (test), push (FCM/APNs), TSA (yerel sahte), nesne depolama (dev MinIO + staging kovası)
- [ ] Tasarım token'ları kodda (Flutter ThemeData, CSS değişkenleri)
- [ ] Hata takibi ve backlog aracı (GitHub Projects) — 03-backlog hikâyeleri yüklü

## Erişim ve güvenlik

- Prod erişimi yalnızca 2 kişi; MFA zorunlu; üretim veritabanına doğrudan erişim yok (bastion + denetimli oturum).
- Yedekler ayrı hesapta (mümkünse ayrı sağlayıcıda); geri yükleme tatbikatı **Sprint 0'da haftalık** (betiğin gerçekten çalıştığını görmek için iki koşu), sonrasında CI gece işiyle aylık otomatik, yılda 2 kez kayda geçen tam tatbikat — NFR-13'ün istediği budur.
- Üretim gizli anahtarları yalnızca Türkiye'deki üretim ortamının kasasında; staging ve CI ayrı anahtar setiyle çalışır, üretim anahtarı ücretsiz/AB ortama hiç inmez (ADR-0012).
- Bağımlılık güncellemeleri haftalık (Dependabot); kritik CVE 48 saat.
