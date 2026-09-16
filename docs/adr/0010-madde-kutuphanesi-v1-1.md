# ADR-0010 · Madde kütüphanesi ve işletme türü paketleri: v1.1'in ilk epic'i

- Tarih: 2026-09-16 · Durum: Kabul edildi (kullanıcı önerisi, PO değerlendirmesi)

## Bağlam
Kullanıcı önerisi: farklı işletme türleri için hazır talimatlar (madde) ve sıralı talimat setleri; merkez kendi maddesini yazsın ya da hazır maddelerden set kursun, şablon olarak kaydetsin; hazır setleri aynen veya değiştirerek kullansın. v1'de kütüphane **şablon (set) düzeyinde**dir: 8 hazır şablon, kopyala-düzenle, madde ekle/çıkar, sürümleme (Ş-6, FR-0311). Maddeler şablonun içinde yaşar; şablonlar arası paylaşılmaz; işletme türü etiketi ve paket kavramı yoktur.

## Karar
1. **v1 değişmez.** Madde düzeyinde kütüphane sıra ilkesinin üç sorusuna da "hayır" alır (02-urun/05 §4); pilot 8 şablonla yürür.
2. **v1.1'in ilk epic'i "Madde kütüphanesi ve paketler"** (CAP-20, EP-13): hesaplar arası paylaşılan, etiketli, sürümlü **kütüphane maddeleri**; editörde "kütüphaneden madde ekle"; şablonun ve maddenin **kaynak takibi** (`kaynak_madde_id`, `kaynak_surum`) — zincir kopyayı değiştirse de bağ kalır, kütüphane maddesi güncellenince "uygula?" önerilir; **işletme türü paketleri** (kafe, hızlı servis, restoran, fırın-pastane) = sıralı şablon setleri; sihirbaz paketle başlar.
3. **İçerik yazılımdan önce.** 200–300 madde PO + kalite danışmanı tarafından, pilot şubelerin duvar listeleri ve gözlemlerden derlenerek yazılır; her madde alan, tür, önerilen ayar ve mevzuat notu taşır. Yazılım 1–2 sprint; içerik pilot boyunca birikir.
4. **v2:** başka dikeyler için paketler (perakende, eczane, spor salonu…) — her biri kendi saha doğrulamasıyla; **marka kütüphanesi** (franchise merkezi standart setini bayilere dağıtır, bayi yalnızca yerel alanları değiştirir) — Blok 6 franchise sinyaline göre öne alınabilir. Topluluk/pazaryeri düşünülmez.

## Sonuçlar
- Veri modeli v1'de geriye uyumlu hazırlanır: `MADDE.kaynak_madde_id?`, `MADDE.kaynak_surum?`, `SABLON.kutuphane_kaynak_id` (zaten var), `SABLON.isletme_turu?`. v1'de doldurulmaz.
- 8 şablon belgesi (02-urun/07) kütüphanenin tohumudur; maddeler oradan kütüphaneye taşınır.
- Personel tarafında hiçbir şey değişmez; kütüphane yalnızca merkezin editöründe görünür.
- Ayrıntı: [02-urun/08-madde-kutuphanesi.md](../02-urun/08-madde-kutuphanesi.md); FR-0313…0318; EP-13 (ST-147…151).
