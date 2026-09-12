# Fonksiyonel olmayan gereksinimler

Her NFR ölçülebilir bir ölçütle yazılır; ölçüm yöntemi test stratejisinde (06-test/01) tanımlıdır. "P95" = isteklerin %95'i.

| ID | Alan | Gereksinim | Ölçüt | Ölçüm |
|---|---|---|---|---|
| NFR-01 | Çevrimdışı | Personel akışı (liste açma, cevaplama, kanıt çekme, gönderme) bağlantısız çalışır | 72 saat çevrimdışı; senkte veri kaybı sıfır; kuyruk 500 kanıt | Uçak modu senaryosu TC-051…056; 100 tekrarlı çakışma testi |
| NFR-02 | Performans (mobil) | Personel akışı beklemesiz | Önbellekten liste açılışı < 1 sn; fotoğraf çekim → sonraki madde < 1,5 sn; gönderim onayı < 2 sn (çevrimiçi) | Düşük segment cihazda ölçüm (cihaz matrisi) |
| NFR-03 | Performans (web) | Izgara ve raporlar hızlı | Izgara (100 şube × 5 liste) ilk boyama < 2 sn; rapor sorguları P95 < 3 sn; PDF (tek çalıştırma) < 30 sn | k6 yük testi, 2.000 şube veri seti |
| NFR-04 | Ölçek | İlk 2 yıl büyümesi | 2.000 şube, 20.000 kullanıcı, günde 100.000 kanıt, 5 TB/yıl depolama; yatay ölçeklenebilir API ve iş kuyruğu | Yük testi; kapasite planı |
| NFR-05 | Kullanılabilirlik | Kapanış saatinde kesinti kabul edilemez | Aylık %99,5; planlı bakım 04:00–06:00; çevrimdışı mod kesintiyi örter | İzleme (uptime), aylık rapor |
| NFR-06 | Cihaz uyumluluğu | Düşük segment Android ve şube tabletleri | Android 9+ (API 28), iOS 15+; 2 GB RAM cihazda akıcı; uygulama boyutu < 40 MB; tablet yatay/dikey | Cihaz matrisi (06-test/04) |
| NFR-07 | Veri kullanımı | Mobil veriyle çalışan şubeler | Fotoğraf ≤ 300 KB, video ≤ 3 MB; günlük şube trafiği < 15 MB; senk yalnızca değişen veri | Ağ ölçümü |
| NFR-08 | Kanıt bütünlüğü | Zaman ve yer sonradan değiştirilemez | Sunucu zamanı esas; dosya hash'i cevaba bağlı; olay zinciri doğrulanabilir; damgalı kopya + ham dosya | ADR-0004; TC-100…103 |
| NFR-09 | Güvenlik | Kiracı yalıtımı ve erişim kontrolü | Her uç noktada rol × kapsam denetimi; imzalı süreli kanıt URL'leri (15 dk); yönetici 2FA; OWASP ASVS L1 / MASVS-L1; bağımlılık taraması CI'da; sızma testi GA öncesi | Güvenlik kontrol listesi; dış sızma testi |
| NFR-10 | KVKK | Türkiye'de barındırma; aydınlatma; silme | Veri TR bölgesinde (ADR-0003); aydınlatma sürümlü ve onaylı; silme/maskeleme ≤ 30 gün; biyometri yok; saklama politikası uygulanır | Uyum kontrol listesi (06-kvkk) |
| NFR-11 | Erişilebilirlik | Düşük okuryazarlık, gürültülü/ıslak ortam | Dokunma hedefi ≥ 44 px; ikon + kısa etiket; kontrast ≥ 4,5:1; tek elle akış; ekran okuyucu etiketleri; büyük yazı desteği | Tasarım incelemesi; erişilebilirlik tarayıcı |
| NFR-12 | Gözlemlenebilirlik | Destek yükünü düşürmek | Cihaz tarafı hata/senk günlükleri (son 7 gün) destek panelinden erişilebilir; bildirim teslimat izi; API hata oranı ve gecikme panoları; uyarı eşikleri | İzleme yığını (07-gelistirme/01) |
| NFR-13 | Yedekleme ve kurtarma | Kanıt kaybı = ürün kaybı | Günlük yedek; 35 gün nokta-zaman kurtarma; nesne depoda sürümleme; RPO 1 sa, RTO 4 sa; yılda 2 kurtarma tatbikatı | Tatbikat kaydı |
| NFR-14 | Zaman ve dil | Çok şubeli saat dilimi ve Türkçe | Tüm zamanlar UTC saklanır, şube diliminde gösterilir; Türkçe büyük/küçük harf (İ/ı) doğru işlenir; i18n hazır | Birim testleri (TC-032) |
| NFR-15 | Bakım ve dağıtım | Küçük ekip, sık sürüm | CI'da test ve tarama; mobil sürüm 2 haftada bir; backend günde birden çok dağıtım; geri alma < 15 dk; şema göçleri geriye uyumlu | CI/CD tanımı (07-gelistirme/02) |
| NFR-16 | Destek edilebilirlik | 1 destek uzmanı / 1.500 şube | Destek modu (maskeli kanıt), hazır tanı raporu, self-servis SSS; hedef ≤ 1 talep/şube/ay | Destek metrikleri |
