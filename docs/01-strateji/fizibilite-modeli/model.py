"""
Talimat / kanıtlı görev-listesi SaaS — 5 yıllık aylık finansal fizibilite modeli.
Para birimi: sabit USD (TL enflasyonundan arındırmak için); TL karşılığı 48,6 kuru ile.
Çalıştır: python model.py  -> results.json + konsol özeti
"""
import json, math

USDTRY = 48.6
MONTHS = 60

# ---------------------------------------------------------------- senaryolar
SCEN = {
    "Kötümser": dict(
        launch=8,                       # MVP çıkış ayı
        chain_adds=[60, 350, 850, 1400, 2000],    # yıllık brüt yeni zincir lokasyonu
        single_adds=[30, 200, 450, 700, 900],     # yıllık brüt yeni tekil hesap
        chain_churn=0.025, single_churn=0.06,     # aylık
        chain_arpu=11.0, single_arpu=6.0,         # $/lokasyon/ay
        cac_chain=140.0, cac_single=60.0,         # $/brüt ekleme
        dev_fte=[3, 3, 4, 4, 5], sales_fte=[1, 2, 3, 4, 4],
        exit_multiple=2.5,
    ),
    "Yalın": dict(                       # kendi kaynağıyla, satış ekibi PMF sonrası
        launch=7,
        chain_adds=[80, 450, 1000, 1700, 2500],
        single_adds=[40, 250, 550, 850, 1100],
        chain_churn=0.018, single_churn=0.05,
        chain_arpu=15.0, single_arpu=9.0,
        cac_chain=90.0, cac_single=30.0,          # kurucu satışı + PLG, düşük CAC
        dev_fte=[2, 2, 3, 3, 4], sales_fte=[0, 1, 2, 3, 4],
        exit_multiple=4.0,
    ),
    "Baz": dict(
        launch=6,
        chain_adds=[120, 700, 1700, 2900, 4200],
        single_adds=[60, 400, 900, 1400, 1800],
        chain_churn=0.018, single_churn=0.05,
        chain_arpu=15.0, single_arpu=9.0,
        cac_chain=110.0, cac_single=50.0,
        dev_fte=[3, 4, 5, 6, 7], sales_fte=[1, 2, 4, 6, 8],
        exit_multiple=4.0,
    ),
    "İyimser": dict(
        launch=5,
        chain_adds=[200, 1300, 3200, 6000, 9000],  # Y3+ yurt dışı pilotlar dahil
        single_adds=[100, 600, 1400, 2200, 3000],
        chain_churn=0.012, single_churn=0.04,
        chain_arpu=19.0, single_arpu=12.0,
        cac_chain=100.0, cac_single=40.0,
        dev_fte=[3, 5, 7, 9, 12], sales_fte=[1, 3, 6, 9, 13],
        exit_multiple=6.0,
    ),
}

# ortak maliyet varsayımları ($/ay, yüklü işveren maliyeti)
DEV_COST = 2600      # ≈ ₺126k/ay yüklü (orta+kıdemli karışımı)
SALES_COST = 2200    # ≈ ₺107k/ay yüklü (satış / müşteri başarısı)
FOUNDER_COST = 2000  # kurucu-PM mütevazı maaş
GA_FIXED = [2500, 3500, 5000, 6500, 8000]   # muhasebe, hukuk, ofis, araçlar
CLOUD_FIXED = 600
HOST_PER_LOC = 0.6   # depolama+işlem $/lokasyon/ay (fotoğraf kanıtları dahil)
NOTIF_PER_LOC = 0.3  # WhatsApp/SMS/push bildirim $/lokasyon/ay
SUPPORT_PER_LOC = 1.2  # destek FTE payı $/lokasyon/ay (1 FTE / 1500 lokasyon)
PAYMENT_FEE = 0.03
MKT_FIXED = 800      # içerik/SEO sabit


def year_of(m):  # m: 1..60
    return (m - 1) // 12


def ramp(total_year, launch, m):
    """Yıllık brüt eklemeyi aylara dağıt: lansman öncesi 0; ilk yıl lansman sonrası aylara eşit."""
    y = year_of(m)
    if m < launch:
        return 0.0
    if y == 0:
        active = 12 - launch + 1
        return total_year / active
    return total_year / 12.0


def run(name, p):
    chain = single = 0.0
    rows = []
    cum_cash = 0.0
    peak_need = 0.0
    be_month = None
    for m in range(1, MONTHS + 1):
        y = year_of(m)
        a_c = ramp(p["chain_adds"][y], p["launch"], m)
        a_s = ramp(p["single_adds"][y], p["launch"], m)
        chain = chain * (1 - p["chain_churn"]) + a_c
        single = single * (1 - p["single_churn"]) + a_s
        locs = chain + single
        rev = chain * p["chain_arpu"] + single * p["single_arpu"]
        cogs = locs * (HOST_PER_LOC + NOTIF_PER_LOC + SUPPORT_PER_LOC) + rev * PAYMENT_FEE + CLOUD_FIXED
        gp = rev - cogs
        cac = a_c * p["cac_chain"] + a_s * p["cac_single"]
        mkt = MKT_FIXED if m >= p["launch"] - 2 else 0
        sales_hc = p["sales_fte"][y] if m >= p["launch"] - 1 else 0
        opex = (p["dev_fte"][y] * DEV_COST + FOUNDER_COST + sales_hc * SALES_COST
                + GA_FIXED[y] + cac + mkt)
        ebitda = gp - opex
        cum_cash += ebitda
        peak_need = min(peak_need, cum_cash)
        if be_month is None and ebitda > 0 and m > p["launch"]:
            be_month = m
        rows.append(dict(m=m, chain=chain, single=single, locs=locs, mrr=rev, arr=rev * 12,
                         cogs=cogs, gp=gp, cac=cac, opex=opex, ebitda=ebitda, cum=cum_cash,
                         adds_c=a_c, adds_s=a_s))
    # yıllık özet
    years = []
    for y in range(5):
        seg = rows[y * 12:(y + 1) * 12]
        years.append(dict(
            year=y + 1,
            rev=sum(r["mrr"] for r in seg),
            cogs=sum(r["cogs"] for r in seg),
            opex=sum(r["opex"] for r in seg),
            cac=sum(r["cac"] for r in seg),
            ebitda=sum(r["ebitda"] for r in seg),
            arr_end=seg[-1]["arr"],
            locs_end=seg[-1]["locs"],
            chain_end=seg[-1]["chain"],
            single_end=seg[-1]["single"],
            cum_end=seg[-1]["cum"],
        ))
    # birim ekonomi (olgun dönem)
    gm = 1 - (HOST_PER_LOC + NOTIF_PER_LOC + SUPPORT_PER_LOC) / p["chain_arpu"] - PAYMENT_FEE
    gm_s = 1 - (HOST_PER_LOC + NOTIF_PER_LOC + SUPPORT_PER_LOC) / p["single_arpu"] - PAYMENT_FEE
    ltv_c = p["chain_arpu"] * gm / p["chain_churn"]
    ltv_s = p["single_arpu"] * gm_s / p["single_churn"]
    unit = dict(
        gm_chain=gm, gm_single=gm_s,
        ltv_chain=ltv_c, ltv_single=ltv_s,
        ltv_cac_chain=ltv_c / p["cac_chain"], ltv_cac_single=ltv_s / p["cac_single"],
        payback_chain=p["cac_chain"] / (p["chain_arpu"] * gm),
        payback_single=p["cac_single"] / (p["single_arpu"] * gm_s),
        life_chain=1 / p["chain_churn"], life_single=1 / p["single_churn"],
    )
    # çıkış değeri & getiri: sermaye ihtiyacı = tepe kümülatif açık; çıkış = ARR_Y5 × çarpan
    exit_val = years[-1]["arr_end"] * p["exit_multiple"]
    # aylık nakit akışları: açıklar sermaye enjeksiyonu (negatif), fazlalar +; 60. ayda çıkış
    cfs = [r["ebitda"] for r in rows]
    cfs[-1] += exit_val
    irr = irr_monthly(cfs)
    invested = -peak_need
    moic = (exit_val + max(0.0, rows[-1]["cum"] - peak_need)) / invested if invested > 0 else float("inf")
    return dict(name=name, params=p, rows=rows, years=years, unit=unit,
                be_month=be_month, peak_need=peak_need, exit_val=exit_val,
                irr_annual=irr, moic=moic, cum_m24=rows[23]["cum"], arr_m24=rows[23]["arr"],
                locs_m24=rows[23]["locs"])


def npv(rate_m, cfs):
    return sum(cf / (1 + rate_m) ** (i + 1) for i, cf in enumerate(cfs))


def irr_monthly(cfs):
    lo, hi = -0.99 / 12, 2.0
    if npv(lo, cfs) * npv(hi, cfs) > 0:
        return None
    for _ in range(200):
        mid = (lo + hi) / 2
        if npv(lo, cfs) * npv(mid, cfs) <= 0:
            hi = mid
        else:
            lo = mid
    return (1 + (lo + hi) / 2) ** 12 - 1


def sensitivity(base):
    """Baz senaryoda ARR(Y5) ve tepe sermaye ihtiyacının ARPU × churn ızgarası."""
    grid = []
    for arpu in [10, 12.5, 15, 17.5, 20]:
        row = []
        for churn in [0.010, 0.015, 0.018, 0.025, 0.035]:
            p = dict(base); p["chain_arpu"] = arpu; p["chain_churn"] = churn
            r = run("s", p)
            row.append(dict(arpu=arpu, churn=churn, arr5=r["years"][-1]["arr_end"],
                            peak=r["peak_need"], be=r["be_month"], irr=r["irr_annual"]))
        grid.append(row)
    # ekleme çarpanı × ARPU -> IRR
    grid2 = []
    for mult in [0.5, 0.75, 1.0, 1.25, 1.5]:
        row = []
        for arpu in [10, 12.5, 15, 17.5, 20]:
            p = dict(base); p["chain_arpu"] = arpu
            p["chain_adds"] = [a * mult for a in base["chain_adds"]]
            p["single_adds"] = [a * mult for a in base["single_adds"]]
            r = run("s", p)
            row.append(dict(mult=mult, arpu=arpu, arr5=r["years"][-1]["arr_end"],
                            peak=r["peak_need"], irr=r["irr_annual"], moic=r["moic"]))
        grid2.append(row)
    return grid, grid2


def no_exit_dcf(arr5, rate):
    """Çıkış olmadan Y6-Y10 nakit akışı DCF'i (Y5 sonu itibarıyla ve t0'a indirgenmiş).
    Büyüme 25→5%, EBITDA marjı 10→30%, vergi %25, capex/işletme sermayesi ihmal, terminal büyüme %3."""
    growth = [0.25, 0.20, 0.15, 0.10, 0.05]
    margin = [0.10, 0.20, 0.25, 0.30, 0.30]
    arr = arr5; pv5 = 0.0; fcf = 0.0
    for i in range(5):
        arr *= 1 + growth[i]
        fcf = arr * margin[i] * 0.75
        pv5 += fcf / (1 + rate) ** (i + 1)
    tv = fcf * 1.03 / (rate - 0.03)
    pv5 += tv / (1 + rate) ** 5
    return dict(pv_y5=pv5, pv_t0=pv5 / (1 + rate) ** 5, arr10=arr)


def expected_value(res, probs):
    """Kötümser: 24. ayda kapatma (kayıp = küm. açık); diğerleri: çıkış − tepe sermaye."""
    ev = 0.0; parts = []
    for k, pr in probs.items():
        r = res[k]
        if k == "Kötümser":
            profit = r["cum_m24"]
        else:
            profit = r["exit_val"] + max(0.0, r["rows"][-1]["cum"] - r["peak_need"]) - (-r["peak_need"])
        ev += pr * profit
        parts.append(dict(scen=k, p=pr, profit=profit))
    return dict(ev=ev, parts=parts)


def tam():
    """Türkiye lokasyon-bazlı TAM/SAM (kaynaklar raporda)."""
    segs = [
        # ad, lokasyon sayısı, SAM'a giren pay, hedef ARPU $/ay
        ("Franchise / zincir noktaları (UFRAD 80k+)", 80000, 0.60, 15),
        ("Yerel market zincirleri (55,7k − ilk 3 ≈ 40k)", 16000, 0.50, 12),
        ("Bağımsız yeme-içme (159k kayıtlı; sahibi başta olmayan, ≥3 personel)", 60000, 0.25, 9),
        ("Akaryakıt istasyonları (~13k)", 13000, 0.40, 12),
        ("Spor salonları (6k+)", 6000, 0.50, 12),
        ("Oteller / konaklama tesisleri", 15000, 0.30, 15),
        ("Tesis yönetimi / temizlik / güvenlik hizmet sahaları", 20000, 0.50, 12),
        ("Klinik, diş, güzellik, oto-yıkama, kuru temizleme vb. çok-şubeli hizmet", 15000, 0.40, 12),
    ]
    out = []
    tam_v = sam_v = tam_n = sam_n = 0
    for name, n, share, arpu in segs:
        t = n * arpu * 12; s = n * share * arpu * 12
        tam_v += t; sam_v += s; tam_n += n; sam_n += n * share
        out.append(dict(seg=name, n=n, share=share, arpu=arpu, tam=t, sam=s))
    return dict(rows=out, tam_usd=tam_v, sam_usd=sam_v, tam_n=tam_n, sam_n=sam_n)


if __name__ == "__main__":
    res = {k: run(k, v) for k, v in SCEN.items()}
    sens, sens2 = sensitivity(SCEN["Baz"])
    t = tam()
    dcf = {k: {str(r): no_exit_dcf(v["years"][-1]["arr_end"], r) for r in (0.20, 0.30)} for k, v in res.items()}
    ev_a = expected_value(res, {"Kötümser": 0.50, "Yalın": 0.25, "Baz": 0.18, "İyimser": 0.07})
    ev_b = expected_value(res, {"Kötümser": 0.65, "Yalın": 0.20, "Baz": 0.12, "İyimser": 0.03})
    out = dict(usdtry=USDTRY, scenarios=res, sens=sens, sens2=sens2, tam=t, dcf=dcf, ev=dict(a=ev_a, b=ev_b),
               costs=dict(DEV_COST=DEV_COST, SALES_COST=SALES_COST, FOUNDER_COST=FOUNDER_COST, GA_FIXED=GA_FIXED,
                          CLOUD_FIXED=CLOUD_FIXED, HOST_PER_LOC=HOST_PER_LOC, NOTIF_PER_LOC=NOTIF_PER_LOC,
                          SUPPORT_PER_LOC=SUPPORT_PER_LOC, PAYMENT_FEE=PAYMENT_FEE, MKT_FIXED=MKT_FIXED))
    for k, v in dcf.items():
        print(f"DCF çıkışsız {k}: r=20% PV(t0) ${v['0.2']['pv_t0']/1e6:.2f}M | r=30% PV(t0) ${v['0.3']['pv_t0']/1e6:.2f}M | ARR Y10 ${v['0.2']['arr10']/1e6:.2f}M")
    print(f"EV(a) ${ev_a['ev']/1e6:.2f}M  " + ", ".join(f"{p['scen']} {p['p']:.0%}: ${p['profit']/1e6:.2f}M" for p in ev_a['parts']))
    print(f"EV(b) ${ev_b['ev']/1e6:.2f}M  " + ", ".join(f"{p['scen']} {p['p']:.0%}: ${p['profit']/1e6:.2f}M" for p in ev_b['parts']))
    with open("results.json", "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)

    print(f"TAM: {t['tam_n']:,.0f} lokasyon, ${t['tam_usd']/1e6:.1f}M/yıl (₺{t['tam_usd']*USDTRY/1e9:.2f} mlr) | "
          f"SAM: {t['sam_n']:,.0f} lokasyon, ${t['sam_usd']/1e6:.1f}M/yıl")
    for k, r in res.items():
        print(f"\n=== {k} ===  lansman ay {r['params']['launch']}  başabaş ay {r['be_month']}  "
              f"tepe sermaye ${-r['peak_need']/1e3:.0f}k (₺{-r['peak_need']*USDTRY/1e6:.1f}M)  "
              f"çıkış ${r['exit_val']/1e6:.2f}M  MOIC {r['moic']:.1f}x  IRR {r['irr_annual']*100 if r['irr_annual'] else float('nan'):.0f}%  | ay-24: küm ${r['cum_m24']/1e3:.0f}k, ARR ${r['arr_m24']/1e3:.0f}k, lok {r['locs_m24']:.0f}")
        for y in r["years"]:
            print(f"  Y{y['year']}: lok {y['locs_end']:6,.0f} (zincir {y['chain_end']:6,.0f}) | gelir ${y['rev']/1e3:7.0f}k | "
                  f"ARR-son ${y['arr_end']/1e3:7.0f}k | EBITDA ${y['ebitda']/1e3:7.0f}k | küm ${y['cum_end']/1e3:7.0f}k")
        u = r["unit"]
        print(f"  birim: zincir GM {u['gm_chain']*100:.0f}% LTV ${u['ltv_chain']:.0f} LTV/CAC {u['ltv_cac_chain']:.1f} payback {u['payback_chain']:.1f} ay | "
              f"tekil GM {u['gm_single']*100:.0f}% LTV ${u['ltv_single']:.0f} LTV/CAC {u['ltv_cac_single']:.1f} payback {u['payback_single']:.1f} ay")
    print("\nDuyarlılık (Baz) ARR Y5 $k — satır ARPU, sütun churn:")
    print("        " + "  ".join(f"{c['churn']*100:5.1f}%" for c in sens[0]))
    for row in sens:
        print(f"${row[0]['arpu']:5.1f}  " + "  ".join(f"{c['arr5']/1e3:6.0f}" for c in row))
    print("\nDuyarlılık (Baz) IRR — satır ekleme çarpanı, sütun ARPU:")
    print("        " + "  ".join(f"${c['arpu']:5.1f}" for c in sens2[0]))
    for row in sens2:
        print(f"x{row[0]['mult']:4.2f}  " + "  ".join(f"{(c['irr']*100 if c['irr'] is not None else float('nan')):6.0f}" for c in row))
