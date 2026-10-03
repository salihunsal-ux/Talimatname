# ADR-0011 · Kayıt dışı satış: üretim–satış mutabakatı dört kademede; kamera en son

- Tarih: 2026-10-03 · Durum: Kabul edildi (yön kararı; L0 v1'de mevcut araçlarla, L1 v1.1 adayı, L2–L3 v2 — hepsi saha sinyaline bağlı)

## Bağlam
Kullanıcı gerçek bir ihtiyaç tanımladı: bazı işletmelerde sipariş geçilmeden ürün üretiliyor, para elden alınıyor ve sisteme hiç girmiyor. İlk soru "kamera ürünü sayabilir mi, elden para alındığını görebilir mi?" biçimindeydi. İnceleme sonucu: **para alma hareketini tanımak teknik olarak kırılgan ve hukuken en riskli yol**; kayıt dışı satışın imzası tek bir eşitsizliktir — *üretilen > satılan*. Dolayısıyla problem bir gözetim problemi değil, **bağımsız bir üretim sayacı** ve bir mutabakat problemidir.

Yurt dışında olgun kategori POS verisi ile kamerayı eşleştiren "exception-based reporting"tir (çekmece açılışı, iptal, iade olaylarının videoyla eşleştirilmesi); kamera tek başına değil, POS kaydının yanında anlam taşır.

## Karar
1. **Ürün çıktısı suçlama değil, sayıdır:** "üretilen − satılan − açıklanan fire = **açıklanamayan fark**". Kimlik tespiti, kişi skoru ve biyometri yok (ADR-0007, KVKK 2026/921). Sistem fark ve zaman aralığı verir; inceleme zincirin kendi kaydı ve kendi İK süreciyle yapılır.
2. **Dört kademe, bu sırayla:**
   - **L0 — Sayım listesi.** Kapanışta "üretilen adet" ve "fire/iade/personel yemeği" maddeleri; POS adediyle elle karşılaştırma. **v1'de mevcut madde türleriyle bugün kurulabilir**, yeni geliştirme gerekmez.
   - **L1 — Tüketim mutabakatı (donanımsız).** Otomatik hesap, eşik, aksiyon ve sebep seti; haftalık kör malzeme sayımı (hamur, kutu, ambalaj) ikinci bağımsız kaynak. **v1.1 adayı** (büyüme listesi A14).
   - **L2 — Kamera ile üretim sayımı.** Fırın ağzı/tezgâh kamerası; adet ve ürün tipi. **v2** (A15).
   - **L3 — POS olay eşleştirme.** Çekmece açılışı / tezgâh etkileşimi ↔ fiş kaydı (±30 sn). **v2**, POS entegrasyonuna bağlı (A8, A16).
3. **Açıklama akışı zorunlu.** Fark tek başına yayınlanmaz; sebep seti (fire/hatalı üretim · personel yemeği · ikram · iade · POS'a geç giriş · sayım hatası · açıklanamıyor) ve kapanış notu olmadan aksiyon kapanmaz. "Açıklanamıyor" cevabı bölge müdürüne yükselir.
4. **Beyan tek kaynak sayılmaz.** Sayımı yapan kişi işin içinde olabilir; L1'in kör malzeme sayımı ve (varsa) L2 bu yüzden gereklidir. L0 tek başına zayıf sinyaldir ve belgede öyle anlatılır.
5. **Sıra kuralı:** L2/L3'e ancak L0–L1 bir zincirde çalışmış ve fark gerçekten ölçülmüşse geçilir. Kameradan başlanmaz.
6. **Doğrulama kapısı:** A14 ancak 20 görüşmenin **≥ 5'i somut fark tutarı** söylerse yol haritasına girer (not alanları `uretim_satis_kontrolu`, `uretim_satis_farki_tl`; sayaç `puanla.py`). L2 için ayrıca bir vardiyalık gerçek görüntüyle ölçüm spike'ı: hedef **gün sonu sayımı POS satışıyla ±%3**.

## Sonuçlar
- Senaryo: [S-11](../03-analiz/04-senaryolar.md); TC'ler L1 kabulünden sonra yazılır.
- Konumlanma riski: ürünün benimseme hikâyesi "kanıt personeli de korur". Gözetim algısı bunu zedeleyebilir; bu yüzden modül **şube ve vardiya düzeyinde** raporlar, duyurulur (aydınlatma metnine ek madde), caydırıcılık açıkça amaç olarak yazılır.
- Hukuk: işyeri kamerası ölçülülük, veri minimizasyonu, aydınlatma ve yasak alan (tuvalet, dinlenme, soyunma) kurallarına tabidir; L2/L3 öncesi hukuk görüşü ve aydınlatma metni güncellemesi şarttır. Biyometri hiçbir kademede yok.
- Satış dinamiği: kayıt dışı satış görünürlüğü bazı alıcılar için cazip, bazıları için tehdittir (kendi kayıt dışılığı). Görüşmede soru "kayıt dışı" diye değil, **kayıp ve fark** diye sorulur.
- Fizibilite: L1 Pro kademesinin fiyat farkını savunur; L2 donanım + abonelik kalemi getirir. Baz senaryoya girmedi; 24. ay kapısında değerlendirilir.
