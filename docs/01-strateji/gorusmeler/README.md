# Görüşme notları

Pilot keşif görüşmelerinin notları buraya, görüşme başına bir dosya. Kişisel veri (görüşülen kişinin adı, telefonu) bu depoya yazılmaz; yalnızca unvan ve zincir adı.

- Merkez/şube görüşmesi: `YYYY-MM-DD-zincir-kodu.md` — şablon: `../dogrulama-sprinti/03-gorusme-not-sablonu.md` (başlık bloğu makine tarafından okunur; alan adlarını değiştirmeyin). Örnek doldurulmuş not: `ornek-gorusme.md` (`ornek: true`, puanlamaya girmez).
- Şube ziyareti: `YYYY-MM-DD-zincir-kodu-gozlem.md` — şablon: `../dogrulama-sprinti/05-gozlem-formu.md`.
- Haftalık rapor: `rapor-hafta-NN.md` — şablon: `../dogrulama-sprinti/06-haftalik-rapor-sablonu.md`.
- Özet ve kapı sayacı: `00-ozet.md` — elle düzenlenmez; `python ../dogrulama-sprinti/puanla.py` üretir (rubrik toplamı, K1/K2 sayacı, örneklem dengesi, isim testi, van Westendorp fiyat analizi, kapsam sinyalleri).

Akış: görüşme biter → 10 dk içinde not → `puanla.py` → commit.
