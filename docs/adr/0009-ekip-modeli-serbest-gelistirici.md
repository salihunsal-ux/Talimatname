# ADR-0009 · Ekip modeli: iki serbest geliştirici + yarı zamanlı tasarımcı (seçenek A)

- Tarih: 2026-09-16 · Durum: Kabul edildi (kullanıcı kararı)

## Bağlam
Sprint 0 doğrulama sprintinin 2–3. haftasında başlamazsa pilot ölçümü (K3) Ocak'tan Mart 2027'ye kayar (07-gelistirme/05 §1). Üç seçenek değerlendirildi: A iki serbest geliştirici, B yazılım evi (sabit kapsam), C teknik kurucu ortak. Kapsam pilot geri bildirimiyle değişeceği (v1.1 sırası) ve K1 geçmezse durabilmek gerektiği için B elenmişti; C en iyi uzun vade ama 4–8 hafta arama süresi takvimi bozuyor.

## Karar
1. **Seçenek A:** bir Flutter (mobil) ve bir Python/FastAPI + React (backend/web) serbest geliştirici, tam zamanlı; yarı zamanlı tasarımcı Sprint 3'ten itibaren; QA Sprint 6'dan itibaren yarı zamanlı (03-backlog ekip notu).
2. **Devam/dur kapısı:** Sprint 2 sonunda K1 raporuyla. K1 geçmezse sözleşmeler 2 hafta bildirimle biter; o güne kadarki iş ödenir; iskelet ve spike çıktıları şirkette kalır.
3. **Seçim:** 07-gelistirme/07 sürecine göre — ilan, 45 dk görüşme, 3 saatlik ücretli mini görev (spike türevi), rubrik. Hedef (1 Ekim'de yeniden kuruldu; önceki: ilan 17 Eylül, başlangıç 5 Ekim — gerçekleşmedi): ilan 2 Ekim, seçim 15 Ekim, Sprint 0 başlangıcı **19 Ekim**.
4. **Sözleşme:** sprint bazlı ücret, sprint kabulüyle ödeme; fikri mülkiyet devri, gizlilik ve KVKK taahhüdü; kod şirketin GitHub organizasyonunda.
5. C seçeneği kapanmadı: teknik ortak arayışı paralel sürer; bulunursa Sprint 3'ten sonra ekip yeniden kurulur (serbest geliştiriciler devam edebilir).

## Sonuçlar
- Koordinasyon kurucuda (PO); günlük 15 dk, 2 haftalık sprint, 06-ilk-gun-paketi ritmi.
- Bilgi kişide kalma riski: ADR'ler, spesifikasyon fikstürleri ve PR incelemeleri zorunlu (DoD); her sprint sonunda mimari notu.
- Takvim (yeniden kurulan): Sprint 1 2 Kasım, Alfa (S6) 22 Ocak 2027, Beta (S8) 19 Şubat, GA (S10) 19 Mart — pilot ölçümü Şubat; fizibilitedeki 6. ay lansmanına iki hafta mesafe, tampon S11–S12 duruyor.
