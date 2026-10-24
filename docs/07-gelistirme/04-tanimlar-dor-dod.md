# Tanımlar: Hazır (DoR), Bitti (DoD), çalışma kuralları

## Hazır tanımı (Definition of Ready) — bir hikâye sprint'e girmeden önce

- [ ] Hikâye kullanıcı bakışıyla yazılmış; hangi persona/aktör için olduğu belli
- [ ] En az bir FR ve ilgili BR'ler bağlanmış; ilgili UC adımı belirtilmiş
- [ ] Kabul kriteri = bağlı TC'ler + hikâye kartındaki ek kriterler (ölçülebilir)
- [ ] Ekran varsa SCR referansı; tasarımcı onayı (tel-çerçeve yeterli, hi-fi F8'den sonra)
- [ ] API değişikliği varsa OpenAPI taslağı PR'da
- [ ] Bağımlılıklar (başka hikâye, sağlayıcı hesabı, veri) listelenmiş ve çözülmüş
- [ ] Boyut verilmiş (S/M/L); L bölünmüş
- [ ] Test verisi ihtiyacı belirtilmiş (tohum/fikstür)

## Bitti tanımı (Definition of Done) — hikâye kapanmadan önce

- [ ] Kod incelendi (≥ 1 onay), CI yeşil (lint, tip, birim, sözleşme, entegrasyon)
- [ ] Birim testleri yazıldı; kural motoru değişikliğinde spesifikasyon fikstürleri güncellendi (backend ve mobil aynı fikstürü geçer)
- [ ] Bağlı TC'ler otomasyona alındı veya elle koşulup kaydedildi (test raporu bağlantısı)
- [ ] Olay günlüğü: yeni kullanıcı eylemleri `audit.emit()` ile loglanıyor
- [ ] Yetki: yeni uç noktada rol × kapsam denetimi ve olumsuz test (403) var
- [ ] Çevrimdışı etki değerlendirildi (mobil hikâyelerinde): kuyruk/senk davranışı belgelendi
- [ ] Erişilebilirlik: dokunma hedefi, etiket, kontrast (mobil/web ekran hikâyelerinde)
- [ ] OpenAPI güncellendi; istemciler yeniden üretildi; göç geriye uyumlu
- [ ] Gözlemlenebilirlik: yeni arka plan işi için metrik/uyarı; hata durumları loglanıyor
- [ ] Dokümantasyon: bu depoda ilgili FR/BR/ekran/ADR güncellendi (kapsam değiştiyse)
- [ ] Staging'e dağıtıldı ve PO tarafından kabul edildi

## Faz A'nın bitti tanımı (mobil başlamadan önce — ADR-0013)

Hikâye bazlı DoD'un üstüne, **Faz B'ye devir** için üç sözleşme:

- [x] **Cevap yazma idempotent:** cihazda üretilen UUID anahtarıyla `PUT`, tekrar gönderimde aynı kayıt; OpenAPI'de yazılı ve sözleşme testi var (ST-030, FR-0602/0607) — *24 Ekim 2026*
- [x] **Kanıt yükleme akışı:** ön imzalı URL → tamamlama → sunucu damgası + SHA-256 doğrulaması; ham ve damgalı dosya ayrı (ST-039/040, FR-0606, ADR-0004) — *24 Ekim 2026. Damgalama turlu işçi: görünür damga (şube · tarih-saat · kullanıcı) ve 320 px küçük resim ayrı kopyalar, ham dosya dokunulmaz. Sunucuda Türkçe harfleri çizebilen yazı tipi yoksa damga basılmaz (uyarı yazılır, küçük resim üretilir) — üretim imajında yazı tipi gerekiyor.*
- [x] **Senk uç noktaları:** `/sync/manifest`, `/sync/batch` ve cihaz saati düzeltmesi OpenAPI'de tanımlı **ve uygulandı** (taslaktan ileri gidildi: kısmi başarı, idempotans ve saat düzeltmesi testli; ST-054, FR-0701/0703/0704/0707) — *24 Ekim 2026*

Gerekçe: bu üçü yazılmazsa API panelin çevrimiçi istek-cevap şekline oturur ve mobil geldiğinde arka ucun bir kısmı yeniden yazılır.

## Hikâye kartı şablonu

```
ST-xxx · [Persona] olarak … istiyorum, böylece …
Epic: EP-xx · CAP-xx · Sprint: Sx · Boyut: M
FR: FR-xxxx, … · BR: BR-xx · UC: UC-xx (adım n) · SCR: SCR-M-xx
Kabul: TC-xxx, TC-xxx + ek kriterler:
  - …
Notlar / açık sorular:
  - …
```

## Törenler (2 haftalık sprint)

| Tören | Süre | Kim | Amaç |
|---|---|---|---|
| Planlama | 2 sa | Ekip + PO | DoR geçen hikâyeler, kapasite, sprint hedefi |
| Günlük | 10 dk | Ekip | Engeller; PO haftada 3 gün katılır |
| Backlog bakımı | 1 sa / hafta | PO + 1 geliştirici | Sonraki sprint hikâyelerini DoR'a getirmek |
| Gösterim | 45 dk | Ekip + PO (+ pilot temsilcisi Beta'dan sonra) | Staging'de çalışan yazılım; PO kabulü |
| Retrospektif | 45 dk | Ekip | 1–2 somut iyileştirme |
| Saha günü | Ayda 1 | Tüm ekip | Pilot şubede kapanış vardiyası gözlemi — geliştirici sahayı görür |

## Kalite kapıları

- **Her PR:** CI yeşil; kapsama düşüşü yok (kural kodunda ≥ %90).
- **Her sprint:** S1/S2 hata sıfır; performans ölçümü (S4'ten itibaren) eşik altı; kabul testi geçiş oranı raporu.
- **Alfa/Beta/GA:** 06-test/01 giriş/çıkış ölçütleri.

## Değişiklik yönetimi

- Kapsam değişikliği (yeni FR / FR iptali): PO kararı + belge güncellemesi + ADR (mimari/ürün etkisi varsa). Sprint içinde kapsam değişmez; acil durumlar (S1) hariç.
- Saha bulguları (pilot, görüşme): önce `01-strateji/gorusmeler/` notu, sonra ilgili belge, sonra backlog.
- Sürüm notları: her mobil sürümde kullanıcıya dönük Türkçe notlar; API değişiklikleri `CHANGELOG`.

## Ekip iletişimi

- Tek backlog aracı (GitHub Projects); tartışmalar hikâye kartında; kararlar ADR'de.
- Destek kanalı (pilot) ile geliştirme kanalı ayrı; PO köprü.
- Haftalık PO özeti: metrikler, riskler, sonraki hafta — bu depoda `docs/00-calisma-plani.md` durum tablosuna işlenir.
