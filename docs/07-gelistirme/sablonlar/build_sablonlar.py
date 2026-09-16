# -*- coding: utf-8 -*-
"""Kurulum sihirbazının içe aktarma şablonları: subeler.xlsx ve personel.xlsx (FR-0105/0106, W-1 adım 1 ve 4).
Çalıştır: python build_sablonlar.py  (formül yok; openpyxl yeter)"""
import os
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.comments import Comment

HERE = os.path.dirname(os.path.abspath(__file__))
F = "Arial"
HEAD = Font(name=F, bold=True, color="FFFFFF", size=10)
HEADFILL = PatternFill("solid", fgColor="1F6F5B")
BODY = Font(name=F, size=10)
EX = Font(name=F, size=10, italic=True, color="4B5560")
INFILL = PatternFill("solid", fgColor="FFFFCC")  # doldurulacak alan
THIN = Side(style="thin", color="D6D9D2")
BORDER = Border(top=THIN, bottom=THIN, left=THIN, right=THIN)
GUNLER = '"—,Pazartesi,Salı,Çarşamba,Perşembe,Cuma,Cumartesi,Pazar"'

def sheet_with_headers(ws, headers, widths, required):
    for i, h in enumerate(headers, 1):
        c = ws.cell(row=1, column=i, value=h + (" *" if h in required else ""))
        c.font = HEAD; c.fill = HEADFILL; c.alignment = Alignment(vertical="center", wrap_text=True); c.border = BORDER
        ws.column_dimensions[c.column_letter].width = widths[i - 1]
    ws.row_dimensions[1].height = 30
    ws.freeze_panes = "A2"
    for r in range(2, 202):
        for i in range(1, len(headers) + 1):
            cell = ws.cell(row=r, column=i); cell.font = BODY; cell.border = BORDER; cell.fill = INFILL

def legend(ws, title, lines):
    ws.column_dimensions["A"].width = 110
    ws["A1"] = title; ws["A1"].font = Font(name=F, bold=True, size=12)
    for i, l in enumerate(lines, 3):
        ws.cell(row=i, column=1, value=l).font = BODY
        ws.cell(row=i, column=1).alignment = Alignment(wrap_text=True, vertical="top")

# ------------------------------------------------------------------ subeler.xlsx
wb = Workbook(); ws = wb.active; ws.title = "Şubeler"
headers = ["Şube adı", "Bölge", "Açılış saati", "Kapanış saati", "Kapalı gün", "Saat dilimi", "İlçe / il", "Şube müdürü adı", "Şube müdürü telefonu", "Not"]
sheet_with_headers(ws, headers, [22, 14, 13, 13, 13, 18, 18, 20, 20, 30], {"Şube adı", "Bölge", "Açılış saati", "Kapanış saati"})
ex = [["Kadıköy", "Anadolu", "08:00", "23:00", "—", "Europe/Istanbul", "Kadıköy / İstanbul", "Ayşe Kaya", "+90 5xx xxx xx xx", "örnek satır — silin"],
      ["Bornova", "Ege", "09:00", "23:00", "Pazar", "Europe/Istanbul", "Bornova / İzmir", "", "", "kapalı gün örneği"]]
for r, row in enumerate(ex, 2):
    for c, v in enumerate(row, 1):
        cell = ws.cell(row=r, column=c, value=v); cell.font = EX
ws["A1"].comment = Comment("Zorunlu. Aynı hesapta benzersiz olmalı; panelde ve bildirimlerde görünür.", "Talimatname")
ws["B1"].comment = Comment("Zorunlu. Bölge müdürü ataması bu ada göre yapılır; yeni ad yeni bölge açar.", "Talimatname")
ws["C1"].comment = Comment("Zorunlu, SS:DD. Açılış listesi penceresi bu saatten türetilir (açılıştan 45 dk önce → +30 dk).", "Talimatname")
ws["D1"].comment = Comment("Zorunlu, SS:DD; 24:00 gece yarısı. Kapanış penceresi kapanıştan 60 dk önce başlar, +90 dk sonra biter; gece yarısını aşan pencere aynı iş gününe yazılır.", "Talimatname")
ws["E1"].comment = Comment("Haftalık sabit kapalı gün; boş veya — ise yok. Tatiller panelden takvime eklenir.", "Talimatname")
ws["F1"].comment = Comment("Boşsa Europe/Istanbul.", "Talimatname")
dv_gun = DataValidation(type="list", formula1=GUNLER, allow_blank=True); ws.add_data_validation(dv_gun); dv_gun.add("E2:E201")
dv_saat = DataValidation(type="time", allow_blank=True, showErrorMessage=True, errorTitle="Saat", error="SS:DD biçiminde girin (ör. 08:00)")
ws.add_data_validation(dv_saat); dv_saat.add("C2:D201")
info = wb.create_sheet("Açıklama")
legend(info, "subeler.xlsx — kurulum sihirbazı adım 1 (şubeler)", [
    "Sarı hücreler doldurulur; 1. satır değiştirilmez. * işaretli sütunlar zorunludur. 2–3. satırlardaki örnekler silinir.",
    "Bir satır = bir şube. Bölge adı yeni ise bölge kendiliğinden açılır; bölge müdürleri personel dosyasında bu ada bağlanır.",
    "Saatler SS:DD (24 saat). Kapanış 24:00 yazılabilir; 00:30 gibi gece yarısını aşan kapanışta 24:30 yazın (sistem aynı iş gününe sayar).",
    "Kapalı gün: haftalık sabit kapalı gün; o gün çalıştırma üretilmez, panoda 'kapalı' görünür. Bayram ve tatiller panelden eklenir.",
    "Doğrulama (FR-0106): hatalı satırlar satır bazında raporlanır; hatalı satır oranı %20'yi geçerse hiçbir kayıt oluşmaz (TC-003). Şube adı tekrarları hata sayılır.",
    "Yeniden yükleme: aynı şube adı varsa satır güncellenir, silinmez; kaldırma panelden yapılır (kayıtlar korunur).",
    "İstasyonlar (bar, mutfak, kasa, tuvalet) v1'de isteğe bağlıdır; şablonda yoktur, panelden eklenir.",
    "Bu dosyada kişisel veri yalnızca şube müdürü adı/telefonu olabilir; e-posta ile göndermeyin, panelden yükleyin.",
])
wb.save(os.path.join(HERE, "subeler.xlsx")); print("subeler.xlsx")

# ------------------------------------------------------------------ personel.xlsx
wb = Workbook(); ws = wb.active; ws.title = "Personel"
headers = ["Ad Soyad", "Telefon", "Şube", "Rol", "Bölge (bölge müdürü için)", "E-posta (yönetici / bölge müdürü)", "Telefonu yok — PIN ile giriş", "Not"]
sheet_with_headers(ws, headers, [24, 20, 18, 16, 22, 30, 22, 30], {"Ad Soyad", "Şube", "Rol"})
ex = [["Emre Tekin", "+90 5xx xxx xx xx", "Kadıköy", "Personel", "", "", "Hayır", "örnek satır — silin"],
      ["Ayşe Kaya", "+90 5xx xxx xx xx", "Kadıköy", "Şube müdürü", "", "", "Hayır", ""],
      ["Deniz Öz", "", "Kadıköy", "Personel", "", "", "Evet", "telefonu yok: şube müdürü kioskta PIN atar"],
      ["Murat Demir", "+90 5xx xxx xx xx", "", "Bölge müdürü", "Anadolu", "murat@zincir.com", "Hayır", "şube boş, bölge dolu"]]
for r, row in enumerate(ex, 2):
    for c, v in enumerate(row, 1):
        cell = ws.cell(row=r, column=c, value=v); cell.font = EX
ws["B1"].comment = Comment("+90 ile, boşluklu veya boşluksuz. Personel ve şube müdürü için davet SMS'i buraya gider; boşsa 'Telefonu yok' Evet olmalı.", "Talimatname")
ws["C1"].comment = Comment("subeler.xlsx'teki şube adıyla birebir aynı. Bölge müdürü ve yönetici için boş bırakılır.", "Talimatname")
ws["D1"].comment = Comment("v1'de dört rol: Personel, Şube müdürü, Bölge müdürü, Yönetici. Yetki = rol × kapsam (şube / bölge / hesap).", "Talimatname")
ws["G1"].comment = Comment("Evet ise davet SMS'i gitmez; şube müdürü kioskta başlangıç PIN'i atar (E-1), personel ilk girişte değiştirir.", "Talimatname")
dv_rol = DataValidation(type="list", formula1='"Personel,Şube müdürü,Bölge müdürü,Yönetici"', allow_blank=False); ws.add_data_validation(dv_rol); dv_rol.add("D2:D501")
dv_eh = DataValidation(type="list", formula1='"Hayır,Evet"', allow_blank=True); ws.add_data_validation(dv_eh); dv_eh.add("G2:G501")
info = wb.create_sheet("Açıklama")
legend(info, "personel.xlsx — kurulum sihirbazı adım 4 (personel ve roller)", [
    "Sarı hücreler doldurulur; 1. satır değiştirilmez. * işaretli sütunlar zorunludur. 2–5. satırlardaki örnekler silinir.",
    "Bir satır = bir kişi. Şube adı, subeler.xlsx ile birebir aynı yazılır (büyük/küçük harf ve Türkçe karakter dahil).",
    "Roller (v1): Personel (şube), Şube müdürü (şube; her şubede en az bir), Bölge müdürü (bölge; şube boş, bölge dolu), Yönetici (hesap; e-posta zorunlu).",
    "Telefon zorunlu değildir: 'Telefonu yok' Evet ise kişi yalnızca şube tabletinden PIN ile girer; PIN'i şube müdürü atar.",
    "Yayınlanınca telefonu olanlara davet SMS'i gider (OTP ile giriş); yöneticilere e-posta. Davetler 7 gün geçerlidir, panelden yenilenir.",
    "Doğrulama: hatalı satırlar (bilinmeyen şube, geçersiz telefon, boş rol) satır bazında raporlanır; %20 üstü hata dosyayı reddeder (TC-003 kuralı).",
    "İşten ayrılanlar bu dosyadan silinmez; panelden pasifleştirilir (kayıtları ve kanıtları korunur, FR-0208).",
    "KVKK: bu dosya kişisel veri içerir. Aydınlatma metni personele yayından önce iletilir; dosya e-posta/WhatsApp ile paylaşılmaz, yalnızca panelden yüklenir; yükleme sonrası yerel kopya silinir.",
])
wb.save(os.path.join(HERE, "personel.xlsx")); print("personel.xlsx")
