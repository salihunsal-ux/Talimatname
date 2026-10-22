# ADR-0014 · Kod deposu düzeni, katmanlar ve kodlama standartları

- Tarih: 2026-10-22 · Durum: Kabul edildi ([ADR-0002](0002-teknoloji-yigini.md) yığınını uygular; [02-repo-ve-ortam-kurulumu.md](../07-gelistirme/02-repo-ve-ortam-kurulumu.md)'nun beş ayrı depo planını tek depoya indirir)

## Bağlam

ADR-0002 yığını seçti (Flutter · React + TS · FastAPI · PostgreSQL), ADR-0012 barındırmayı ve taşınabilirlik şartını, ADR-0013 faz sırasını belirledi. Kodlama Faz A ile başlıyor; başlamadan önce üç şeyin yazılı olması gerekiyor: **deponun şekli, katmanların bağımlılık yönü ve "iyi kod" ölçütleri.** Aksi hâlde ilk iki hafta sonra geriye dönük düzeltilecek kararlar birikir.

Bu ürünün sıradan bir CRUD uygulamasından ayrıldığı dört nokta, standartları da belirliyor:

1. **Çok kiracılı ve kapsam denetimli** — veri sızıntısı ürünün sonu (TC-011 kiracı yalıtımı, TC-006/010 rol kapsamı).
2. **Kanıt ve olay izi değiştirilemez olmalı** — hash zinciri, sunucu damgası (ADR-0004).
3. **İki istemci aynı kuralı çalıştırıyor** — pencere, puan, durum ve sabit kural hem backend'de hem mobilde aynı sonucu vermek zorunda (ADR-0005).
4. **Çevrimdışı yazma var** — aynı kayıt birden çok kez, farklı sırayla gelebilir; idempotency bir ek değil, veri modelinin parçası.

## Karar

### 1 · Tek kod deposu (monorepo): `talimatname-kod`

```
talimatname-kod/
  api/     FastAPI, alan modeli, kural motoru, göçler, testler
  web/     React + TS yönetim paneli
  mobile/  Flutter (Faz B'de açılır)
  spec/    kural motoru JSON fikstürleri — iki istemcinin ortak testi
  infra/   compose, dağıtım, yedek betikleri, CI iş akışları
```

02-repo beş ayrı depo öngörmüştü; tek geliştiriciyle (ADR-0013) bu düzen **maliyet üretir**: API sözleşmesi değişince istemci sürümünü ayrı depoda güncellemek, fikstürü iki yere kopyalamak, iki CI'yı eşlemek. Tek depoda API + istemci + fikstür **tek commit**'te değişir. Klasörler bağımsız kaldığı için ayrışma gerekirse (ekip büyürse) `git subtree split` ile beş depoya bölünebilir; bu kapı açık tutulur.

**Ürün dokümantasyonu ayrı kalır** (`Talimatname` deposu): ürün dosyası olarak yayınlanıyor, kodla birlikte sürümlenmesi gerekmiyor.

### 2 · Katmanlar ve bağımlılık yönü

```
api/src/talimatname/
  api/        HTTP: yönlendiriciler, istek/yanıt şemaları (pydantic), hata haritası
  services/   kullanım senaryoları (uygulama katmanı); işlem sınırı burada
  domain/     SAF: varlıklar, değer nesneleri, kural motoru. I/O yok, import yok (stdlib + dateutil)
  infra/      SQLAlchemy modelleri, depolar (repository), nesne depolama, bildirim, saat
```

Bağımlılık **içe doğru**: `api → services → domain`, `infra → domain`. `domain` hiçbir katmanı import etmez; veritabanı, HTTP, dosya sistemi ve **gerçek saat** domain'e girmez — zaman ve kimlik parametre olarak geçirilir. Bu kural `ruff` ile değil gözle korunur; ihlali inceleme reddi sebebidir.

### 3 · Kural motoru saf fonksiyon + ortak fikstür

Pencere hesabı, puan, durum makinesi ve sabit kural **saf fonksiyonlardır**; girdileri JSON'dan okunabilir, çıktıları JSON'a yazılabilir. Fikstürler `spec/fikstur/*.json` altında; backend testleri ve (Faz B'de) Flutter testleri **aynı dosyaları** geçer. Bir kural değişikliği fikstür değişikliği olmadan birleştirilemez.

### 4 · Çok kiracılılık: PostgreSQL RLS

- Her kiracı tablosunda `tenant_id uuid not null`; satır düzeyi güvenlik politikası `tenant_id = current_setting('app.tenant_id')::uuid`.
- Uygulama rolü `BYPASSRLS` **almaz**; göçler ayrı rolle koşar.
- Her istek, işlem başında `SET LOCAL app.tenant_id` yapar; bunu tek bir bağımlılık (dependency) üstlenir, elle çağrı yoktur.
- Kapsam denetimi (bölge/şube) RLS'in **üstünde**, servis katmanında: her uç nokta rol × kapsam denetler ve olumsuz testi (403) vardır.
- Gerekçe: iki katmanlı savunma. Uygulama hatası kiracı sızıntısına dönüşmez.

### 5 · Idempotency ve çakışma

- İstemcide üretilen UUID yazma anahtarıdır: `PUT /api/v1/runs/{run_id}/answers/{answer_uuid}`. Aynı gövdeyle tekrar → 200 ve aynı kayıt; farklı gövdeyle tekrar → son yazan kazanır, ikisi de olay izine girer (FR-0705).
- Toplu senk uç noktası parça parça başarısız olabilir: yanıt her öğe için sonuç döner, tamamı için tek hata dönmez.
- Sunucu, istemcinin gönderdiği zamanı **kaydeder ama kullanmaz**; sıralama ve "zamanında mı" kararı sunucu saatiyle verilir (BR-13).

### 6 · Olay izi (`audit.emit()`)

Kullanıcı eylemi değiştiren her servis çağrısı, **aynı veritabanı işlemi içinde** olay yazar: `(tenant_id, actor, action, subject, payload, prev_hash, hash)`. Ekle-yalnız; `UPDATE`/`DELETE` izni yok. Hash zinciri ADR-0004'e göre. Olay yazılmadan iş kaydı yazılamaz (aynı işlem, ya ikisi ya hiçbiri).

### 7 · Zaman, dil ve adlandırma

- Veritabanında **UTC** (`timestamptz`); hesaplama şube saat diliminde; iş günü = pencere başlangıç tarihi (BR-01).
- **Kod İngilizce** (tanımlayıcılar, dosya adları, commit gövdesindeki teknik terimler); **kullanıcıya görünen metin Türkçe** ve i18n kaynak dosyasında (FR-1803).
- Türkçe alan terimleri ile İngilizce tanımlayıcılar arasındaki eşleme **tek yerde**: [09-kod-sozlugu.md](../07-gelistirme/09-kod-sozlugu.md). Sözlükte olmayan bir terim kodda icat edilmez; önce sözlüğe eklenir.

### 8 · Hata biçimi

Tüm hatalar RFC 9457 `application/problem+json`: `type` (makine kodu, ör. `urn:talimatname:pencere-kapali`), `title` (Türkçe kısa metin), `status`, `detail`, `instance`. İstemci **`type`'a göre** davranır, metne göre değil. Doğrulama hataları alan bazlı liste döner.

### 9 · Test piramidi

| Katman | Araç | Gereksinim |
|---|---|---|
| Alan/kural (saf) | pytest, `spec/fikstur` | Veritabanı gerekmez; **kural kodunda kapsama ≥ %90** |
| Servis/entegrasyon | pytest + gerçek PostgreSQL | RLS ve kapsam testleri burada (TC-006, 010, 011) |
| Sözleşme | Schemathesis (OpenAPI) | Her PR |
| Uçtan uca (web) | Playwright | Smoke her PR, tam gece |
| Kabul (TC) | yukarıdakilerin birleşimi | TC numarası testin adında geçer: `test_tc011_kiraci_yalitimi` |

Kabul testi numarasının test adında geçmesi zorunludur: izlenebilirlik zinciri (FR → TC → ST) koda kadar devam eder.

### 10 · Araçlar ve kapılar

- **api:** `ruff` (biçim + lint), `mypy --strict`, `pytest`; bağımlılıklar `pyproject.toml`, kilit dosyası depoda.
- **web:** `tsc --strict`, `eslint`, `prettier`, `vitest`, `playwright`; API istemcisi **OpenAPI'den üretilir** (elle yazılmaz), üretilmiş dosya depoda ve CI'da yeniden üretilip karşılaştırılır (sözleşme kayması derleme hatasıdır).
- **pre-commit:** ruff + mypy + hızlı pytest + eslint + prettier. Ürün dokümantasyon deposundaki dört kontrol (sayılar, js, üretim, taşma) kendi deposunda kalır.
- Yeni bağımlılık eklemek bir karardır: tek satırlık işi yapan paket eklenmez; eklenen paket PR açıklamasında gerekçelenir.

### 11 · Veritabanı ve göç

- SQLAlchemy 2.0 (tipli), Alembic göçleri; her göç **ileri ve geri** test edilir.
- Göçler geriye uyumlu: önce ekle, sonra yaz, sonra sil (üç adımlı sütun kaldırma).
- Doğal anahtar yok; `uuid` birincil anahtar (istemcide üretilebilmesi için).
- Tarihsel tablolar (cevap, kanıt, olay) **yalnızca ekleme**; düzeltme yeni satırdır.
- ADR-0012 taşınabilirlik şartı: sağlayıcıya özel uzantı kullanılmaz (`pgcrypto`, `uuid-ossp` yerine uygulama tarafı üretim).

### 12 · Yapılandırma ve sır

12-factor: tüm yapılandırma ortam değişkeniyle, `pydantic-settings` ile tiplenmiş, `.env.example` depoda, gerçek değer asla depoda. Uygulama, eksik ya da geçersiz ayarla **açılmaz** (başlangıçta doğrulama).

## Sonuçlar

- Beş depo planı tek depoya indi: 02-repo'nun depo tablosu güncellenir; CI tek iş akışı dosyasıyla başlar.
- `spec/fikstur` Faz A'da doldurulur ve Faz B'nin ilk günü Flutter tarafından **aynı dosyalarla** koşulur — ADR-0013'ün devir kapısını somutlaştırır.
- Kod sözlüğü (09) yeni bir belge olarak zincire girer; terim uyuşmazlığı artık inceleme konusu.
- Testlerin bir kısmı (servis/entegrasyon) **çalışan bir PostgreSQL ister**; yerel geliştirme ortamı kararı buna bağlıdır (ADR-0012 md.2: ücretsiz/AB olabilir, gerçek veri yok).

## Gözden geçirme tetikleyicileri

- Ekip üçüncü kişiye çıkarsa: monorepo'nun CI süresi ve inceleme trafiği ölçülür; gerekiyorsa `web/` ayrı depoya çıkar.
- RLS performansı ızgara sorgusunda (100 şube × 30 gün) eşiği aşarsa: politika yerine servis katmanı filtresi + ayrı okuma modeli tartışılır (NFR-03).
- Flutter fikstürleri geçmiyorsa: kural motorunun tek kaynak olma ilkesi (md.3) yeniden ele alınır — iki uygulama yerine sunucu tarafı hesap.
