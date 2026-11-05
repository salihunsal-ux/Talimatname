# Çalıştırma ataması: tasarım ile uygulama arasındaki açık

- Tarih: 2026-11-05 · Durum: **karar verildi — A, Faz B'de** (5 Kasım 2026, kullanıcı onayı)
- İlgili: FR-0508, FR-0519, FR-0520, FR-0521, FR-1211, BR-16, BR-26,
  [veri modeli](04-veri-modeli.md), [ADR-0008](../adr/0008-v1-cekirdek.md)

## Soru

Plan kurulurken iş **şubeye mi** atanıyor, **kişiye mi**?

Bugünkü cevap: **şubeye**. Plan bir şube listesi taşıyor, her iş günü kapsamdaki
her şube için bir çalıştırma üretiliyor, çalıştırma kaydında şube var. Kişi bağı
planlama anında değil **çalışma anında** kuruluyor: listeyi ilk açan kilidi alıyor
(`run.locked_by`), diğerleri "X yapıyor" görüyor (FR-0521, BR-26).

Bu doğru tasarım. Vardiya her gün değişir, plan aylarca durur; planı kişiye
bağlamak her izinde, her ayrılmada planı bozardı. Sabit olan birim şube.

Planın bir de `assignment` alanı var (FR-0508) — `anyone` / `role` / `user`. Ama bu
çalıştırmanın **sahibini** değil, **bildirimin kime gideceğini** belirliyor
(`services/reminders.py · _alicilar`). Üç türde de çalıştırma şubenin kalıyor.

## Açık

Veri modeli bir `CALISTIRMA_ATAMA` varlığı tanımlıyor:

| Varlık | Alanlar | Kaynak |
|---|---|---|
| CALISTIRMA_ATAMA | `calistirma_id, kullanici_id?, rol?, istasyon_id?, tamamladi, gonderim_zamani?` | BR-16 |

**Uygulanan şemada bu tablo yok.** `run` tablosunda yalnızca `locked_by` var ve o
bir kilit, atama değil: kim çalışıyor onu söyler, kimin çalışması gerektiğini değil.

Buna bağlı iki v1 gereksinimi bugünkü şemayla karşılanamıyor:

- **FR-0519** — şube müdürü günün çalıştırmasında atananı değiştirebilir;
  "herkes tamamlasın" listelerinde kişi ekleyip çıkarabilir.
- **FR-0520** — atama değişikliği yeni atanana anında bildirilir, eskisinden
  kaldırılır, olay günlüğe yazılır.

FR-1211 bu yeteneği mobil yönetici görünümünde de bekliyor ("şube müdürü için
mobilde **de**"), yani tüketicisi hem panel hem telefon.

Ayrıca panelin plan formu atama alanını hiç göstermiyor: her planı
`kind: "anyone"` ile gönderiyor. Bu ikinci ve daha küçük bir eksik — FR-0508 planın
ataması, FR-0519 çalıştırmanınki; ikisi aynı şey değil.

## Seçenekler

| | Kurgu | Artısı | Eksisi |
|---|---|---|---|
| **A** | `CALISTIRMA_ATAMA` tablosunu tasarımda yazdığı gibi uygula | FR-0519/0520 v1'de karşılanır; v1.1'in "herkes tamamlasın" kuralı (BR-16) aynı tabloya oturur, iş iki kez yapılmaz; atama değişikliği denetim izine doğal olarak düşer | Göç, uç nokta, bildirim dalı ve iki ekran (pano çalıştırma detayı + SCR-M-10); tüketici ekranlar hazır olmadan değeri yok |
| **B** | FR-0519'u daralt: "atananı değiştir" yerine **"kilidi devret"**; tabloyu v1.1'e ertele | Mevcut modele oturuyor, göç gerekmiyor; şube müdürünün asıl ihtiyacı olan "yanlış kişi almış, al bundan" karşılanır | Gereksinimin söylediği şey değil; "herkes tamamlasın" geldiğinde tablo yine gerekir ve kilit mantığı ikinci kez elden geçer; atanmamış bir işe önceden kişi yazılamaz |
| **C** | Hiçbir şey yapma, açığı FR listesinde işaretle | Maliyet yok | FR-0519/0520 v1 etiketiyle duruyor ama yapılamıyor; "bitti tanımı" yanlış ölçülür |

## Karar

**A, Faz B'de** (5 Kasım 2026). `CALISTIRMA_ATAMA` tasarımda yazdığı gibi
uygulanacak; iş Faz B'nin kapsamında, ilk tüketici ekranla birlikte.
Gerekçe aşağıdaki tavsiyeyle aynı.

## Tavsiye (karara esas)

**A, ama Faz B'de** — tabloyu ilk tüketici ekranla birlikte yaz.

Gerekçe: FR-0519'un iki tüketicisi de henüz yok (panelin çalıştırma detayında atama
denetimi, SCR-M-10 yönetici mobil görünümü). Tabloyu bugün açmak, kullanıcısı olmayan
bir göç demek. Ama B'yi seçmek, v1.1 geldiğinde kilit mantığını ikinci kez açmak
demek — BR-16 zaten "herkes tamamlasın"ı aynı yapıya bağlıyor.

Bu arada yapılması gereken: FR-0519/0520'nin **Faz A'nın bitti tanımında olmadığını**
yazılı hale getirmek. Şu an v1 etiketiyle duruyorlar ve panel "bitti" sayılırken
ikisi de yapılmamış olacak.

## Yapılacaklar (A · Faz B)

1. Göç: `CALISTIRMA_ATAMA` (`calistirma_id, kullanici_id?, rol?, istasyon_id?,
   tamamladi, gonderim_zamani?`), kiracı yalıtımı ve RLS politikası dâhil.
2. Uç nokta: çalıştırmanın atananını değiştir (FR-0519); yetki şube müdürü ve üstü.
3. FR-0520: yeni atanana bildirim, eskisinden kaldırma,
   `audit.emit("calistirma.atama_degisti")`.
4. İki ekranda atama denetimi: panelin çalıştırma detayı ve SCR-M-10.
5. Kilit (`run.locked_by`) ile atamanın ilişkisi yazılır: atama "kim yapmalı",
   kilit "kim yapıyor" — biri diğerini ezmez.

Ayrıca karara bağlanacak (bu notun kapsamı dışında): planın `assignment` alanı
panelde neden görünmüyor — form eksik mi, yoksa v1'de bilerek gizli mi.
