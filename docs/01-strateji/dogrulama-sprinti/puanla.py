# -*- coding: utf-8 -*-
"""Görüşme notlarını (gorusmeler/*.md, YAML başlık bloğu) okur; rubrik toplamı, kapı sayaçları, örneklem dengesi,
isim testi ve van Westendorp fiyat analizini üretir → gorusmeler/00-ozet.md. Bağımlılık yok (saf Python).
Çalıştır: python puanla.py   (docs/01-strateji/dogrulama-sprinti içinden)"""
import os, re, glob, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
NOTES = os.path.join(HERE, "..", "gorusmeler")
OUT = os.path.join(NOTES, "00-ozet.md")

def parse_front(text):
    m = re.match(r'^---\s*\n(.*?)\n---', text, flags=re.S)
    if not m:
        return None
    d = {}
    for line in m.group(1).split("\n"):
        line = line.split("#", 1)[0].rstrip() if not line.strip().startswith("#") else ""
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        k = k.strip(); v = v.strip().strip('"').strip("'")
        if v.lower() in ("true", "false"):
            d[k] = v.lower() == "true"
        else:
            try:
                d[k] = float(v) if "." in v else int(v)
            except ValueError:
                d[k] = v
    return d

def load():
    rows = []
    for p in sorted(glob.glob(os.path.join(NOTES, "*.md"))):
        if os.path.basename(p).startswith("00-") or os.path.basename(p) == "README.md":
            continue
        d = parse_front(open(p, encoding="utf-8").read())
        if not d or d.get("ornek"):
            continue
        d["_dosya"] = os.path.basename(p)
        rows.append(d)
    return rows

def num(d, k):
    v = d.get(k, 0)
    return v if isinstance(v, (int, float)) else 0

def toplam(d):
    return sum(num(d, k) for k in ("p_aci", "p_liste", "p_cihaz", "p_yetki", "p_odeme", "p_taahhut")) + num(d, "p_engel")

def van_westendorp(rows):
    """Klasik PSM: her katılımcının 4 fiyatı; OPP = 'çok ucuz' ile 'çok pahalı' kesişimi, IPP = 'ucuz(uygun)' ile 'pahalı' kesişimi.
    Kümülatif dağılımlar kaba ızgarada hesaplanır; ≥ 5 cevap olmadan yorumlanmaz."""
    keys = ("fiyat_cok_ucuz", "fiyat_uygun", "fiyat_pahali", "fiyat_cok_pahali")
    data = [tuple(num(r, k) for k in keys) for r in rows if all(num(r, k) > 0 for k in keys)]
    if len(data) < 5:
        return None, len(data)
    lo = min(min(t) for t in data); hi = max(max(t) for t in data)
    grid = [lo + (hi - lo) * i / 400 for i in range(401)]
    n = len(data)
    def frac_le(idx, p): return sum(1 for t in data if t[idx] <= p) / n
    def frac_ge(idx, p): return sum(1 for t in data if t[idx] >= p) / n
    # "çok ucuz" ve "uygun": fiyat p'de bu fiyatı ucuz bulanların oranı = fiyatı >= p verenler (azalan);
    # "pahalı" ve "çok pahalı": fiyatı <= p verenler (artan)
    def cross(f_desc, f_asc):
        best = None
        for p in grid:
            diff = f_desc(p) - f_asc(p)
            if best is None or abs(diff) < best[0]:
                best = (abs(diff), p)
        return best[1]
    opp = cross(lambda p: frac_ge(0, p), lambda p: frac_le(3, p))   # çok ucuz × çok pahalı
    ipp = cross(lambda p: frac_ge(1, p), lambda p: frac_le(2, p))   # uygun × pahalı
    pmc = cross(lambda p: frac_ge(1, p), lambda p: frac_le(3, p))   # uygun × çok pahalı (alt sınır)
    pme = cross(lambda p: frac_ge(0, p), lambda p: frac_le(2, p))   # çok ucuz × pahalı (üst sınır)
    med = lambda i: sorted(t[i] for t in data)[len(data) // 2]
    return dict(n=n, opp=opp, ipp=ipp, pmc=min(pmc, pme), pme=max(pmc, pme),
                med=dict(zip(keys, (med(0), med(1), med(2), med(3))))), n

def main():
    rows = load()
    lines = [f"# Görüşme özeti ve kapı sayacı", "", f"Üretim: {datetime.date.today().isoformat()} · `puanla.py` · {len(rows)} görüşme notu (ornek=true olanlar hariç)", ""]
    # ---- tablo
    lines += ["| # | Tarih | Zincir | Şube | Kutu | Format | Model | Tür | Acı | Liste | Cihaz | Yetki | Ödeme | Taahhüt | Engel | Toplam /16 | K1 | LOI | İsim |",
              "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    k1 = 0; loi = 0; adaylar = []
    for i, r in enumerate(rows, 1):
        t = toplam(r)
        g1 = num(r, "p_liste") >= 2 and num(r, "p_aci") >= 2
        k1 += g1
        l = str(r.get("loi", "")).lower()
        loi += l in ("evet", "sartli", "şartlı")
        if t >= 11: adaylar.append((t, r.get("zincir", "")))
        lines.append(f"| {i} | {r.get('tarih','')} | {r.get('zincir','')} | {num(r,'sube_sayisi'):.0f} | {r.get('kutu','')} | {r.get('format','')} | {r.get('model','')} | {r.get('gorusme_turu','')} | "
                     f"{num(r,'p_aci'):.0f} | {num(r,'p_liste'):.0f} | {num(r,'p_cihaz'):.0f} | {num(r,'p_yetki'):.0f} | {num(r,'p_odeme'):.0f} | {num(r,'p_taahhut'):.0f} | {num(r,'p_engel'):.0f} | **{t:.0f}** | {'✓' if g1 else '–'} | {r.get('loi','')} | {r.get('isim_tercihi','')} |")
    merkez = [r for r in rows if str(r.get("gorusme_turu", "A")).upper() == "A"]
    lines += ["", "## Kapılar", "",
              f"- **K1** (liste ≥ 2 ve acı ≥ 2): **{k1} / {len(merkez)}** merkez görüşmesi — hedef ≥ 12/20 → {'GEÇTİ' if k1 >= 12 else 'henüz değil'}",
              f"- **K2** (LOI evet/şartlı): **{loi}** — hedef ≥ 5 → {'GEÇTİ' if loi >= 5 else 'henüz değil'}",
              f"- Pilot adayları (toplam ≥ 11): {', '.join(f'{z} ({t:.0f})' for t, z in sorted(adaylar, reverse=True)) or '—'}", ""]
    # ---- örneklem dengesi
    def cnt(key, val): return sum(1 for r in merkez if str(r.get(key, "")).lower() == val)
    lines += ["## Örneklem dengesi (merkez görüşmeleri)", "", "| Boyut | Gerçekleşen | Hedef |", "|---|---|---|",
              f"| Kutu A / B / C | {cnt('kutu','a')} / {cnt('kutu','b')} / {cnt('kutu','c')} | 6 / 9 / 5 |",
              f"| kafe / hızlı servis / restoran | {cnt('format','kafe')} / {cnt('format','hizli-servis')} / {cnt('format','restoran')} | 7 / 7 / 6 |",
              f"| kendi / karma / franchise | {cnt('model','kendi')} / {cnt('model','karma')} / {cnt('model','franchise')} | 8 / 8 / 4 |",
              f"| İstanbul dışı | {sum(1 for r in merkez if r.get('istanbul_disi'))} | ≥ 5 |", ""]
    # ---- isim testi
    isim = {}
    for r in rows:
        s = str(r.get("isim_tercihi", "")).strip().lower()
        if s: isim[s] = isim.get(s, 0) + 1
    lines += ["## İsim testi", "", "| Kart | Tercih |", "|---|---|"] + [f"| {k} | {v} |" for k, v in sorted(isim.items(), key=lambda x: -x[1])] + ([] if isim else ["| — | 0 |"]) + [""]
    # ---- fiyat
    vw, n = van_westendorp(rows)
    lines += ["## Fiyat hassasiyeti (van Westendorp, ₺/şube/ay)", ""]
    if vw:
        lines += [f"- Cevap sayısı: {vw['n']}",
                  f"- Kabul edilebilir aralık: **₺{vw['pmc']:.0f} – ₺{vw['pme']:.0f}**",
                  f"- Optimum fiyat noktası (OPP): **₺{vw['opp']:.0f}** · Kayıtsızlık noktası (IPP): **₺{vw['ipp']:.0f}**",
                  f"- Medyanlar: çok ucuz ₺{vw['med']['fiyat_cok_ucuz']:.0f} · uygun ₺{vw['med']['fiyat_uygun']:.0f} · pahalı ₺{vw['med']['fiyat_pahali']:.0f} · çok pahalı ₺{vw['med']['fiyat_cok_pahali']:.0f}",
                  f"- Fizibilite Baz varsayımı ₺730/şube/ay bu aralığın {'içinde' if vw['pmc'] <= 730 <= vw['pme'] else 'DIŞINDA'}."]
    else:
        lines += [f"- Henüz {n} tam cevap (≥ 5 gerekir)."]
    lines += ["", "## Kapsam kararlarına sinyaller", ""]
    def oran(key, val):
        m = [r for r in merkez if str(r.get(key, ""))]
        return (sum(1 for r in m if str(r.get(key, "")).lower() == val), len(m))
    tab = sum(num(r, "tablet_sube_orani") for r in merkez) / max(1, len([r for r in merkez if num(r, "tablet_sube_orani") > 0]))
    lines += [f"- Tablet: ortalama şube oranı {tab:.0%} (kiosk Must eşiği %50) · telefon serbest: {oran('telefon_serbest','evet')[0]}/{oran('telefon_serbest','evet')[1]}",
              f"- Barındırma şartı: TR sunucu {oran('barindirma_sarti','tr-sunucu')[0]} · on-premise {oran('barindirma_sarti','on-premise')[0]} · şart yok {oran('barindirma_sarti','yok')[0]} · sözleşme yeter {oran('barindirma_sarti','sozlesme-yeter')[0]}",
              f"- Fotoğraf/konum itirazı: var {oran('foto_konum_itirazi','var')[0]}/{oran('foto_konum_itirazi','var')[1]}",
              f"- Prob talebi: var {oran('prob_talebi','var')[0]}/{oran('prob_talebi','var')[1]}",
              f"- Franchise bayi görsün: evet {oran('franchise_bayi_gorsun','evet')[0]} · hayır {oran('franchise_bayi_gorsun','hayir')[0]}", ""]
    open(OUT, "w", encoding="utf-8").write("\n".join(lines))
    print(f"{len(rows)} not → {OUT}\nK1 {k1}/{len(merkez)} · K2 LOI {loi} · pilot adayı {len(adaylar)}")

if __name__ == "__main__":
    main()
