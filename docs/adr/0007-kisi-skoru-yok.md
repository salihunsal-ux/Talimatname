# ADR-0007 · Kişi bazlı performans skoru yok

- Tarih: 2026-09-12 · Durum: Kabul edildi (kullanıcı onayı)

## Bağlam
Jolt gibi rakipler personel "hesap verebilirlik" puanını satış argümanı yapıyor. Türkiye'de KVKK (işleme amacı, ölçülülük) ve iş barışı açısından hassas; ürünün personel tarafında "gözetim" değil "kanıt" olarak algılanması benimsemenin ön koşulu.

## Karar
Puan ve sıralama yalnızca şube/bölge/liste düzeyinde. Kişi düzeyinde yalnızca şube/bölge müdürüne görünen "gecikme ve eksik" listesi ve açık aksiyonlar; puan, sıralama, karşılaştırma, rozet, gamification yok. Personel kendi kaydını görür.

## Sonuçlar
- Raporlama modülünde R-9 "kişi düzeyi takip (skor yok)" olarak tanımlı; veri modelinde kişi skoru alanı yok.
- Aydınlatma metni "performans değerlendirme" amacını içermez.
