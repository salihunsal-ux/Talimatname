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

## Sprint 0 kontrol listesi (2 hafta)

- [ ] Depolar açıldı, dal koruması, CODEOWNERS, PR şablonu (DoD kontrol listesi)
- [ ] `talimatname-api`: iskelet (FastAPI, Alembic, pytest), `audit.emit()` altyapısı, RLS politikası, OpenAPI yayını
- [ ] `talimatname-mobile`: iskelet (Riverpod, Drift, üretilmiş istemci, tema token'ları 05-tasarim/04)
- [ ] `talimatname-web`: iskelet (Vite, yönlendirme, tema token'ları, üretilmiş istemci, oturum)
- [ ] `talimatname-infra`: dev compose, sahte servisler, CI iş akışları, staging ortamı (TR bölgesi), izleme temel
- [ ] Tohum betiği v0 (hesap, 3 şube, 5 kullanıcı, 1 şablon, 1 plan) — tam set Sprint 3'e kadar
- [ ] Kural motoru spesifikasyon fikstürleri (puan, pencere/durum, koşullu mantık) — backend ve mobil ortak
- [ ] Sağlayıcı seçimleri (nesne depo, SMS, TSA) ve test hesapları
- [ ] Tasarım token'ları kodda (Flutter ThemeData, CSS değişkenleri)
- [ ] Hata takibi ve backlog aracı (GitHub Projects) — 03-backlog hikâyeleri yüklü

## Erişim ve güvenlik

- Prod erişimi yalnızca 2 kişi; MFA zorunlu; üretim veritabanına doğrudan erişim yok (bastion + denetimli oturum).
- Yedekler ayrı hesapta; geri yükleme tatbikatı aylık (NFR-13).
- Bağımlılık güncellemeleri haftalık (Dependabot); kritik CVE 48 saat.
