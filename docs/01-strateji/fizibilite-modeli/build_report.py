# -*- coding: utf-8 -*-
"""results.json -> index.html (fizibilite raporu). Çalıştır: python model.py && python build_report.py"""
import json, html

R = json.load(open("results.json", encoding="utf-8"))
FX = R["usdtry"]
S = R["scenarios"]
ORDER = ["Kötümser", "Yalın", "Baz", "İyimser"]
COLOR = {"Kötümser": "s1", "Yalın": "s2", "Baz": "s3", "İyimser": "s4"}

# ------------------------------------------------------------------ biçimleyiciler (Türkçe)
def tr(x, d=0):
    s = f"{x:,.{d}f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")

def usd_m(x, d=2):  return f"{tr(x/1e6, d)} M$"
def usd_k(x):       return f"{tr(x/1e3)} bin $"
def tl_m(x, d=1):   return f"₺{tr(x*FX/1e6, d)} M"
def tl_k(x):        return f"₺{tr(x*FX/1e3)} bin"
def pct(x, d=0):    return f"%{tr(x*100, d)}"
def n(x, d=0):      return tr(x, d)
def month_str(m):   return "60 ay içinde yok" if m is None else f"{m}. ay"
def irr_str(x):     return "—" if x is None else pct(x)

# ------------------------------------------------------------------ SVG çizgi grafiği
def line_chart(cid, title, ylabel, series, yfmt, unit_div=1e3, y0=None):
    W, H = 760, 340
    L, Rm, T, B = 64, 96, 28, 40
    pw, ph = W - L - Rm, H - T - B
    allv = [v for _, vals in series for v in vals]
    ymin = min(0, min(allv)) if y0 is None else y0
    ymax = max(allv)
    # güzel adım
    span = ymax - ymin
    raw = span / 5
    mag = 10 ** (len(str(int(raw))) - 1)
    step = next(s for s in (1, 2, 2.5, 5, 10) if raw <= s * mag) * mag
    ylo = (ymin // step) * step
    yhi = -((-ymax) // step) * step
    if yhi == ymax: yhi += step
    def X(m): return L + pw * (m / 60)
    def Y(v): return T + ph * (1 - (v - ylo) / (yhi - ylo))
    g = [f'<svg class="chart" id="{cid}" viewBox="0 0 {W} {H}" role="img" aria-label="{html.escape(title)}">']
    g.append(f'<text class="ct" x="{L}" y="16">{html.escape(title)}</text>')
    # y grid
    v = ylo
    while v <= yhi + 1e-9:
        y = Y(v)
        cls = "ax0" if abs(v) < 1e-9 else "grid"
        g.append(f'<line class="{cls}" x1="{L}" x2="{L+pw}" y1="{y:.1f}" y2="{y:.1f}"/>')
        g.append(f'<text class="tick" x="{L-8}" y="{y+4:.1f}" text-anchor="end">{yfmt(v)}</text>')
        v += step
    g.append(f'<text class="tick" x="{L-8}" y="{T-8}" text-anchor="end">{html.escape(ylabel)}</text>')
    # x ticks (yıllar)
    for yr in range(0, 6):
        x = X(yr * 12)
        g.append(f'<line class="grid" x1="{x:.1f}" x2="{x:.1f}" y1="{T+ph}" y2="{T+ph+5}"/>')
        lab = "Başlangıç" if yr == 0 else f"Y{yr}"
        g.append(f'<text class="tick" x="{x:.1f}" y="{T+ph+20}" text-anchor="middle">{lab}</text>')
    # çizgiler
    ends = []
    for name, vals in series:
        pts = " ".join(f"{X(i+1):.1f},{Y(v):.1f}" for i, v in enumerate(vals))
        g.append(f'<polyline class="ln {COLOR[name]}" points="{pts}"/>')
        ends.append((Y(vals[-1]), name, vals[-1]))
    # uç etiketleri (çakışma önle)
    ends.sort()
    placed = []
    for y, name, val in ends:
        yy = y
        for p in placed:
            if abs(yy - p) < 14: yy = p + 14
        placed.append(yy)
        g.append(f'<circle class="dot {COLOR[name]}" cx="{X(60):.1f}" cy="{y:.1f}" r="4"/>')
        g.append(f'<text class="lbl" x="{X(60)+8:.1f}" y="{yy+4:.1f}">{html.escape(name)} <tspan class="lblv">{yfmt(val)}</tspan></text>')
    # hover katmanı
    data = json.dumps([[nm, [round(v, 1) for v in vals]] for nm, vals in series], ensure_ascii=False)
    g.append(f'<line class="xh" id="{cid}-xh" x1="0" x2="0" y1="{T}" y2="{T+ph}" style="display:none"/>')
    g.append(f'<rect class="hit" x="{L}" y="{T}" width="{pw}" height="{ph}" fill="transparent" '
             f'data-l="{L}" data-pw="{pw}" data-series=\'{html.escape(data, quote=True)}\' data-unit="{unit_div}"/>')
    g.append("</svg>")
    return "\n".join(g)

def kfmt(v):  # bin $
    return f"{tr(v/1e3)}"

arr_series = [(k, [r["arr"] for r in S[k]["rows"]]) for k in ORDER]
cum_series = [(k, [r["cum"] for r in S[k]["rows"]]) for k in ORDER]
chart_arr = line_chart("c-arr", "Yıllık yinelenen gelir (ARR), bin $", "bin $", arr_series, kfmt)
chart_cum = line_chart("c-cum", "Kümülatif nakit (sermaye ihtiyacı), bin $", "bin $", cum_series, kfmt)

# ------------------------------------------------------------------ tablolar
def scen_table():
    h = ['<div class="tw"><table class="data"><thead><tr><th>Senaryo</th><th>Lansman</th><th>Y5 lokasyon</th>'
         '<th>Y5 gelir</th><th>Y5 ARR</th><th>Başabaş</th><th>Tepe sermaye</th><th>24. ay ARR</th>'
         '<th>Çıkış (ARR×kat)</th><th>MOIC</th><th>IRR</th></tr></thead><tbody>']
    for k in ORDER:
        r = S[k]; y5 = r["years"][-1]
        h.append(f'<tr><td><span class="sw {COLOR[k]}"></span>{k}</td><td>{r["params"]["launch"]}. ay</td>'
                 f'<td>{n(y5["locs_end"])}</td><td>{usd_k(y5["rev"])}</td><td>{usd_k(y5["arr_end"])}</td>'
                 f'<td>{month_str(r["be_month"])}</td><td>{usd_k(-r["peak_need"])}<br><span class="sub">{tl_m(-r["peak_need"])}</span></td>'
                 f'<td>{usd_k(r["arr_m24"])}</td><td>{usd_m(r["exit_val"])}<br><span class="sub">×{n(r["params"]["exit_multiple"],1)}</span></td>'
                 f'<td>{n(r["moic"],1)}×</td><td>{irr_str(r["irr_annual"])}</td></tr>')
    h.append("</tbody></table></div>")
    return "\n".join(h)

def year_table(k):
    r = S[k]
    h = [f'<div class="tw"><table class="data"><thead><tr><th>{k}</th>' + "".join(f"<th>Y{y}</th>" for y in range(1, 6)) + "</tr></thead><tbody>"]
    rows = [("Lokasyon (yıl sonu)", "locs_end", n), ("— zincir", "chain_end", n), ("— tekil", "single_end", n),
            ("Gelir", "rev", usd_k), ("Satılan hizmet maliyeti", "cogs", usd_k), ("Faaliyet gideri (CAC dahil)", "opex", usd_k),
            ("— CAC harcaması", "cac", usd_k), ("EBITDA", "ebitda", usd_k), ("ARR (yıl sonu)", "arr_end", usd_k),
            ("Kümülatif nakit", "cum_end", usd_k)]
    for lab, key, f in rows:
        cls = ' class="tot"' if key in ("ebitda", "cum_end") else ""
        h.append(f"<tr{cls}><td>{lab}</td>" + "".join(f"<td>{f(y[key])}</td>" for y in r["years"]) + "</tr>")
    h.append("</tbody></table></div>")
    return "\n".join(h)

def unit_table():
    h = ['<div class="tw"><table class="data"><thead><tr><th>Birim ekonomi (olgun dönem)</th>']
    for k in ORDER: h.append(f"<th>{k}</th>")
    h.append("</tr></thead><tbody>")
    rows = [
        ("Zincir ARPU ($/lokasyon/ay)", lambda r: f'{n(r["params"]["chain_arpu"],1)} $ <span class="sub">(₺{n(r["params"]["chain_arpu"]*FX)})</span>'),
        ("Zincir aylık kayıp (churn)", lambda r: pct(r["params"]["chain_churn"], 1)),
        ("Zincir brüt marj", lambda r: pct(r["unit"]["gm_chain"])),
        ("Zincir LTV / lokasyon", lambda r: f'{n(r["unit"]["ltv_chain"])} $'),
        ("Zincir CAC / lokasyon", lambda r: f'{n(r["params"]["cac_chain"])} $'),
        ("Zincir LTV/CAC", lambda r: f'{n(r["unit"]["ltv_cac_chain"],1)}×'),
        ("Zincir CAC geri ödeme", lambda r: f'{n(r["unit"]["payback_chain"],1)} ay'),
        ("Tekil ARPU ($/hesap/ay)", lambda r: f'{n(r["params"]["single_arpu"],1)} $ <span class="sub">(₺{n(r["params"]["single_arpu"]*FX)})</span>'),
        ("Tekil aylık kayıp", lambda r: pct(r["params"]["single_churn"], 1)),
        ("Tekil LTV/CAC", lambda r: f'{n(r["unit"]["ltv_cac_single"],1)}×'),
        ("Tekil CAC geri ödeme", lambda r: f'{n(r["unit"]["payback_single"],1)} ay'),
    ]
    for lab, f in rows:
        h.append(f"<tr><td>{lab}</td>" + "".join(f"<td>{f(S[k])}</td>" for k in ORDER) + "</tr>")
    h.append("</tbody></table></div>")
    return "\n".join(h)

def sens_table(grid, rowlab, collab, cellkey, cellfmt, caption):
    vals = [c[cellkey] for row in grid for c in row if c[cellkey] is not None]
    lo, hi = min(vals), max(vals)
    h = [f'<div class="tw"><table class="data heat"><caption>{caption}</caption><thead><tr><th>{rowlab} ↓ / {collab} →</th>']
    for c in grid[0]: h.append(f"<th>{c['_col']}</th>")
    h.append("</tr></thead><tbody>")
    for row in grid:
        h.append(f"<tr><td>{row[0]['_row']}</td>")
        for c in row:
            v = c[cellkey]
            t = 0 if v is None or hi == lo else (v - lo) / (hi - lo)
            base = " base" if c.get("_base") else ""
            h.append(f'<td class="hc{base}" style="--t:{t:.2f}">{cellfmt(v)}</td>')
        h.append("</tr>")
    h.append("</tbody></table></div>")
    return "\n".join(h)

sens1 = R["sens"]
for row in sens1:
    for c in row:
        c["_row"] = f"{n(c['arpu'],1)} $"; c["_col"] = pct(c["churn"], 1)
        c["_base"] = (c["arpu"] == 15 and abs(c["churn"] - 0.018) < 1e-9)
sens2 = R["sens2"]
for row in sens2:
    for c in row:
        c["_row"] = f"×{n(c['mult'],2)}"; c["_col"] = f"{n(c['arpu'],1)} $"
        c["_base"] = (c["arpu"] == 15 and c["mult"] == 1.0)
sens_arr = sens_table(sens1, "Zincir ARPU", "aylık churn", "arr5", lambda v: usd_k(v), "Baz senaryo — Y5 ARR")
sens_irr = sens_table(sens2, "Müşteri edinme hızı", "zincir ARPU", "irr",
                      lambda v: irr_str(v), "Baz senaryo — IRR (çıkış ×4 ARR varsayımıyla)")

def tam_table():
    t = R["tam"]
    h = ['<div class="tw"><table class="data"><thead><tr><th>Segment (Türkiye)</th><th>Lokasyon</th><th>SAM payı</th>'
         '<th>Hedef ARPU</th><th>TAM / yıl</th><th>SAM / yıl</th></tr></thead><tbody>']
    for r in t["rows"]:
        h.append(f'<tr><td>{r["seg"]}</td><td>{n(r["n"])}</td><td>{pct(r["share"])}</td><td>{n(r["arpu"])} $</td>'
                 f'<td>{usd_m(r["tam"])}</td><td>{usd_m(r["sam"])}</td></tr>')
    h.append(f'<tr class="tot"><td>Toplam</td><td>{n(t["tam_n"])}</td><td>{pct(t["sam_n"]/t["tam_n"])}</td><td>—</td>'
             f'<td>{usd_m(t["tam_usd"],1)}<br><span class="sub">{tl_m(t["tam_usd"],0)}</span></td>'
             f'<td>{usd_m(t["sam_usd"],1)}<br><span class="sub">{tl_m(t["sam_usd"],0)}</span></td></tr>')
    h.append("</tbody></table></div>")
    return "\n".join(h)

def ev_table():
    h = ['<div class="tw"><table class="data"><thead><tr><th>Senaryo</th><th>Sonuç</th><th>Olasılık A</th><th>Olasılık B</th></tr></thead><tbody>']
    a = {p["scen"]: p for p in R["ev"]["a"]["parts"]}; b = {p["scen"]: p for p in R["ev"]["b"]["parts"]}
    for k in ORDER:
        res = a[k]["profit"]
        lab = "24. ayda kapatma, kayıp" if k == "Kötümser" else "çıkış − yatırılan sermaye"
        h.append(f'<tr><td><span class="sw {COLOR[k]}"></span>{k}</td><td>{usd_m(res)} <span class="sub">({lab})</span></td>'
                 f'<td>{pct(a[k]["p"])}</td><td>{pct(b[k]["p"])}</td></tr>')
    h.append(f'<tr class="tot"><td>Beklenen kâr</td><td></td><td>{usd_m(R["ev"]["a"]["ev"])}</td><td>{usd_m(R["ev"]["b"]["ev"])}</td></tr>')
    h.append("</tbody></table></div>")
    return "\n".join(h)

def dcf_table():
    h = ['<div class="tw"><table class="data"><thead><tr><th>Çıkış yoksa (Y6–Y10 nakit akışı DCF)</th>']
    for k in ORDER: h.append(f"<th>{k}</th>")
    h.append("</tr></thead><tbody>")
    h.append("<tr><td>Y10 ARR (büyüme %25→%5)</td>" + "".join(f'<td>{usd_m(R["dcf"][k]["0.2"]["arr10"])}</td>' for k in ORDER) + "</tr>")
    h.append("<tr><td>Bugünkü değer, iskonto %20</td>" + "".join(f'<td>{usd_m(R["dcf"][k]["0.2"]["pv_t0"])}</td>' for k in ORDER) + "</tr>")
    h.append("<tr><td>Bugünkü değer, iskonto %30</td>" + "".join(f'<td>{usd_m(R["dcf"][k]["0.3"]["pv_t0"])}</td>' for k in ORDER) + "</tr>")
    h.append("<tr class=\"tot\"><td>Yatırılan sermaye (tepe)</td>" + "".join(f'<td>{usd_m(-S[k]["peak_need"])}</td>' for k in ORDER) + "</tr>")
    h.append("</tbody></table></div>")
    return "\n".join(h)

C = R["costs"]
SPRINT = 6500  # 90 günlük doğrulama sprinti, $ (1 geliştirici 2 ay + prototip + seyahat)
B = S["Baz"]; Yl = S["Yalın"]; Op = S["İyimser"]; Ko = S["Kötümser"]
T = R["tam"]

# ------------------------------------------------------------------ CSS
CSS = r"""
<title>Talimatname Fizibilitesi</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400&family=IBM+Plex+Sans:wght@400;500;600&display=swap">
<style>
:root{
  --bg:#f4f6f4; --sf:#ffffff; --sf2:#eef2ef; --ink:#151c22; --ink2:#46525c; --mut:#77838c; --line:#d6ddd9; --line2:#e7ece9;
  --acc:#0e6b6b; --accs:#dcecea; --acct:#0a5252; --stamp:#b8412f; --stamps:#f6e3df; --good:#1f7a3d; --goods:#e0f0e4; --warn:#9a6300; --warns:#f7ead0;
  --s1:#eb6834; --s2:#4a3aa7; --s3:#1baf7a; --s4:#2a78d6; --heat:14,107,107;
  --fd:"Bricolage Grotesque","Trebuchet MS",Arial,sans-serif; --fb:"Source Serif 4",Georgia,"Times New Roman",serif; --fu:"IBM Plex Sans","Segoe UI",Arial,sans-serif;
}
@media (prefers-color-scheme: dark){ :root:not([data-theme="light"]){
  --bg:#0f1315; --sf:#161b1e; --sf2:#1d2427; --ink:#e7ece9; --ink2:#b3bdb8; --mut:#7f8b87; --line:#2b3438; --line2:#222a2e;
  --acc:#3fb3ad; --accs:#15302f; --acct:#7fd4cf; --stamp:#e46f5a; --stamps:#3a201b; --good:#5fc47f; --goods:#16301f; --warn:#e2a93f; --warns:#33290f;
  --s1:#d95926; --s2:#9085e9; --s3:#199e70; --s4:#3987e5; --heat:63,179,173;
}}
:root[data-theme="dark"]{
  --bg:#0f1315; --sf:#161b1e; --sf2:#1d2427; --ink:#e7ece9; --ink2:#b3bdb8; --mut:#7f8b87; --line:#2b3438; --line2:#222a2e;
  --acc:#3fb3ad; --accs:#15302f; --acct:#7fd4cf; --stamp:#e46f5a; --stamps:#3a201b; --good:#5fc47f; --goods:#16301f; --warn:#e2a93f; --warns:#33290f;
  --s1:#d95926; --s2:#9085e9; --s3:#199e70; --s4:#3987e5; --heat:63,179,173;
}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--fb);font-size:17px;line-height:1.6;-webkit-font-smoothing:antialiased}
a{color:var(--acct);text-decoration-thickness:1px;text-underline-offset:2px}
a:focus-visible,button:focus-visible{outline:2px solid var(--acc);outline-offset:2px}
.wrap{max-width:1180px;margin:0 auto;padding:0 20px 80px}
header.top{border-bottom:1px solid var(--line);padding:40px 0 28px;margin-bottom:12px}
.eyebrow{font-family:var(--fu);font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:var(--mut);font-weight:600}
h1{font-family:var(--fd);font-weight:700;font-size:clamp(34px,5vw,58px);line-height:1.02;letter-spacing:-.01em;margin:10px 0 14px;text-wrap:balance;max-width:20ch}
.lede{font-size:20px;line-height:1.5;max-width:62ch;color:var(--ink2);margin:0 0 18px}
.meta{font-family:var(--fu);font-size:13px;color:var(--mut);display:flex;flex-wrap:wrap;gap:6px 22px}
.layout{display:grid;grid-template-columns:1fr;gap:0 40px}
@media (min-width:1080px){.layout{grid-template-columns:220px minmax(0,1fr)}}
nav.toc{display:none}
@media (min-width:1080px){nav.toc{display:block;position:sticky;top:20px;align-self:start;padding-top:28px}}
nav.toc ol{list-style:none;margin:0;padding:0;font-family:var(--fu);font-size:13px;line-height:1.35}
nav.toc li{padding:5px 0;border-left:2px solid var(--line2);padding-left:12px}
nav.toc li a{color:var(--ink2);text-decoration:none}
nav.toc li a:hover{color:var(--acct)}
nav.toc .v{display:inline-block;width:14px;color:var(--mut);font-weight:600}
main{min-width:0}
section.item{padding:34px 0 8px;border-top:1px solid var(--line)}
section.item:first-of-type{border-top:0}
.ih{display:flex;align-items:flex-start;gap:14px;margin-bottom:12px}
.box{flex:none;width:30px;height:30px;border:2px solid var(--ink);border-radius:4px;display:grid;place-items:center;font-family:var(--fu);font-weight:700;font-size:16px;margin-top:6px}
.box.ok{border-color:var(--good);color:var(--good);background:var(--goods)}
.box.cond{border-color:var(--warn);color:var(--warn);background:var(--warns)}
.box.no{border-color:var(--stamp);color:var(--stamp);background:var(--stamps)}
.box.info{border-color:var(--line);color:var(--mut)}
h2{font-family:var(--fd);font-weight:700;font-size:30px;line-height:1.1;margin:0;letter-spacing:-.01em;text-wrap:balance}
.verdict{font-family:var(--fu);font-size:12px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;padding:3px 9px;border-radius:3px;display:inline-block;margin-top:8px}
.verdict.ok{background:var(--goods);color:var(--good)} .verdict.cond{background:var(--warns);color:var(--warn)} .verdict.no{background:var(--stamps);color:var(--stamp)} .verdict.info{background:var(--sf2);color:var(--ink2)}
h3{font-family:var(--fd);font-weight:700;font-size:20px;margin:28px 0 8px;letter-spacing:-.005em}
p,ul,ol{max-width:68ch}
p{margin:0 0 14px}
ul,ol{padding-left:22px;margin:0 0 14px}
li{margin-bottom:5px}
strong{font-weight:600}
.note{font-family:var(--fu);font-size:14px;color:var(--ink2);background:var(--sf2);border-left:3px solid var(--acc);padding:10px 14px;margin:14px 0 18px;max-width:80ch}
.note.warn{border-left-color:var(--warn)}
.note.stamp{border-left-color:var(--stamp)}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:1px;background:var(--line);border:1px solid var(--line);margin:18px 0 8px;max-width:980px}
.kpi{background:var(--sf);padding:14px 16px}
.kpi .l{font-family:var(--fu);font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:var(--mut);font-weight:600}
.kpi .v{font-family:var(--fd);font-weight:700;font-size:26px;line-height:1.1;margin-top:6px;font-variant-numeric:tabular-nums}
.kpi .s{font-family:var(--fu);font-size:12px;color:var(--ink2);margin-top:4px}
.decision{border:2px solid var(--stamp);border-radius:6px;padding:18px 22px;margin:18px 0 10px;max-width:980px;background:var(--sf);position:relative}
.decision .st{position:absolute;top:-13px;left:18px;background:var(--sf);padding:0 8px;font-family:var(--fu);font-weight:700;font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--stamp)}
.decision h3{margin:4px 0 8px;font-size:24px}
.decision p{max-width:80ch}
.grid2{display:grid;grid-template-columns:1fr;gap:18px;max-width:980px}
@media (min-width:820px){.grid2{grid-template-columns:1fr 1fr}}
.tw{overflow-x:auto;margin:12px 0 20px;max-width:980px}
table.data{border-collapse:collapse;width:100%;font-family:var(--fu);font-size:13.5px;font-variant-numeric:tabular-nums;background:var(--sf)}
table.data caption{text-align:left;font-weight:600;font-size:13px;color:var(--ink2);padding:0 0 8px;letter-spacing:.02em}
table.data th{font-weight:600;text-align:left;font-size:12px;letter-spacing:.04em;text-transform:uppercase;color:var(--mut);border-bottom:1.5px solid var(--ink);padding:8px 10px;white-space:nowrap}
table.data td{border-bottom:1px solid var(--line2);padding:8px 10px;vertical-align:top}
table.data td:first-child{color:var(--ink);font-weight:500}
table.data tr.tot td{font-weight:600;border-top:1.5px solid var(--ink);border-bottom:0}
table.data .sub{color:var(--mut);font-size:12px;font-weight:400}
table.data.wide td{white-space:normal;min-width:140px}
table.data.wide td:first-child{min-width:150px}
.sw{display:inline-block;width:10px;height:10px;border-radius:2px;margin-right:8px;vertical-align:-1px}
.s1{color:var(--s1);background:var(--s1)} .s2{color:var(--s2);background:var(--s2)} .s3{color:var(--s3);background:var(--s3)} .s4{color:var(--s4);background:var(--s4)}
table.data.heat td.hc{background:rgba(var(--heat),calc(var(--t)*.55));text-align:right}
table.data.heat td.hc.base{outline:2px solid var(--ink);outline-offset:-2px;font-weight:700}
figure{margin:18px 0 22px;max-width:980px}
figcaption{font-family:var(--fu);font-size:13px;color:var(--ink2);margin-top:6px;max-width:80ch}
svg.chart{width:100%;height:auto;display:block;background:var(--sf);border:1px solid var(--line);font-family:var(--fu)}
svg.chart .ct{font-size:13px;font-weight:600;fill:var(--ink)}
svg.chart .tick{font-size:11px;fill:var(--mut)}
svg.chart .grid{stroke:var(--line2);stroke-width:1}
svg.chart .ax0{stroke:var(--line);stroke-width:1.5}
svg.chart .ln{fill:none;stroke-width:2.2;stroke-linejoin:round;stroke-linecap:round}
svg.chart .ln.s1{stroke:var(--s1)} svg.chart .ln.s2{stroke:var(--s2)} svg.chart .ln.s3{stroke:var(--s3)} svg.chart .ln.s4{stroke:var(--s4)}
svg.chart .dot{stroke:var(--sf);stroke-width:2}
svg.chart .dot.s1{fill:var(--s1)} svg.chart .dot.s2{fill:var(--s2)} svg.chart .dot.s3{fill:var(--s3)} svg.chart .dot.s4{fill:var(--s4)}
svg.chart .lbl{font-size:11.5px;font-weight:600;fill:var(--ink)}
svg.chart .lblv{font-weight:400;fill:var(--ink2)}
svg.chart .xh{stroke:var(--ink2);stroke-width:1;stroke-dasharray:3 3}
.tip{position:fixed;pointer-events:none;background:var(--ink);color:var(--bg);font-family:var(--fu);font-size:12px;padding:8px 10px;border-radius:4px;display:none;z-index:9;line-height:1.5;white-space:nowrap}
.tip b{font-weight:600}
.tag{font-family:var(--fu);font-size:11px;font-weight:600;letter-spacing:.06em;text-transform:uppercase;padding:2px 7px;border-radius:3px;background:var(--sf2);color:var(--ink2);white-space:nowrap}
.tag.hi{background:var(--stamps);color:var(--stamp)} .tag.md{background:var(--warns);color:var(--warn)} .tag.lo{background:var(--goods);color:var(--good)}
.src{font-family:var(--fu);font-size:13.5px;line-height:1.5}
.src li{margin-bottom:4px}
.src{max-width:90ch}
sup a{text-decoration:none;font-family:var(--fu);font-size:11px;color:var(--acct)}
.arch{font-family:var(--fu);font-size:13px;background:var(--sf2);padding:12px 14px;overflow-x:auto;white-space:pre;line-height:1.45;max-width:980px;border:1px solid var(--line2)}
@media (prefers-reduced-motion:no-preference){ nav.toc li a{transition:color .15s} }
</style>
"""

# ------------------------------------------------------------------ içerik
def item(idn, status, title, verdict, body):
    glyph = {"ok": "✓", "cond": "!", "no": "✗", "info": "i"}[status]
    return (f'<section class="item" id="{idn}"><div class="ih"><div class="box {status}">{glyph}</div><div>'
            f'<h2>{title}</h2><span class="verdict {status}">{verdict}</span></div></div>{body}</section>')

tocs = [("karar", "Karar özeti", "!"), ("urun", "Ürün ve değer önerisi", "✓"), ("pazar", "Pazar", "!"),
        ("rekabet", "Rekabet", "✓"), ("teknik", "Teknik fizibilite", "✓"), ("operasyon", "Operasyonel fizibilite", "!"),
        ("hukuk", "Hukuki / KVKK", "✓"), ("finans", "Finansal fizibilite", "!"), ("risk", "Riskler", "i"),
        ("plan", "Doğrulama planı", "i"), ("kaynak", "Kaynaklar ve sınırlar", "i")]
toc_html = '<nav class="toc" aria-label="İçindekiler"><ol>' + "".join(
    f'<li><span class="v">{g}</span><a href="#{i}">{t}</a></li>' for i, t, g in tocs) + "</ol></nav>"

y5b = B["years"][-1]; y5y = Yl["years"][-1]; y5o = Op["years"][-1]; y5k = Ko["years"][-1]

karar = f"""
<div class="decision"><span class="st">Karar</span>
<h3>Koşullu GO — yalın başla, 24. ayda kapı koy</h3>
<p>Ürün teknik ve hukuki olarak yapılabilir; sorun <em>yapılabilirlik</em> değil, <em>Türkiye pazarının küçüklüğü ve WhatsApp'ın bedava olması</em>. Lokasyon bazlı hesapla Türkiye'de erişilebilir pazar (SAM) yılda yaklaşık <strong>{usd_m(T["sam_usd"],1)}</strong> ({tl_m(T["sam_usd"],0)}); bu, tek başına "büyük çıkış" üretecek bir pazar değil, ama <strong>{usd_k(-Yl["peak_need"])}–{usd_k(-B["peak_need"])}</strong> ({tl_m(-Yl["peak_need"],0)}–{tl_m(-B["peak_need"],0)}) sermayeyle 5 yılda <strong>{usd_k(y5y["arr_end"])}–{usd_k(y5b["arr_end"])} ARR</strong>'ye ulaşan, kârlılığa yeni geçmiş bir şirket kurulabilir. Getiri; (1) makul bir çıkış çarpanına veya (2) 3. yıldan itibaren yurt dışına açılmaya bağlı. Bunlar olmadan, %30 iskontoyla bugünkü değer yatırılan sermayenin altında kalıyor.</p>
<p><strong>Öneri:</strong> 90 günlük, en fazla {tl_k(SPRINT)} maliyetli bir doğrulama sprinti (20 zincir görüşmesi, 3–5 tasarım ortağı, ücretli pilot) → geçerse Yalın senaryoyla lansman → 24. ayda net kapı: ARR ≥ {usd_k(Yl["arr_m24"])} ve zincir aylık kaybı ≤ %2 ise ölçekle (Baz), değilse kapat. Bu kapıya kadar azami kayıp ≈ <strong>{usd_k(-Ko["cum_m24"])}</strong> ({tl_m(-Ko["cum_m24"],0)}).</p>
</div>
<div class="kpis">
<div class="kpi"><div class="l">Türkiye SAM</div><div class="v">{usd_m(T["sam_usd"],1)}</div><div class="s">{n(T["sam_n"])} lokasyon · yıllık</div></div>
<div class="kpi"><div class="l">Tepe sermaye (Yalın / Baz)</div><div class="v">{usd_k(-Yl["peak_need"])} / {usd_k(-B["peak_need"])}</div><div class="s">{tl_m(-Yl["peak_need"],0)} / {tl_m(-B["peak_need"],0)}</div></div>
<div class="kpi"><div class="l">Başabaş (Yalın / Baz)</div><div class="v">{Yl["be_month"]}. / {B["be_month"]}. ay</div><div class="s">İyimser: {Op["be_month"]}. ay</div></div>
<div class="kpi"><div class="l">Y5 ARR (Baz)</div><div class="v">{usd_m(y5b["arr_end"])}</div><div class="s">{n(y5b["locs_end"])} lokasyon · SAM'ın {pct(y5b["locs_end"]/T["sam_n"],1)}'i</div></div>
<div class="kpi"><div class="l">Beklenen kâr (A / B)</div><div class="v">{usd_m(R["ev"]["a"]["ev"],1)} / {usd_m(R["ev"]["b"]["ev"],1)}</div><div class="s">çıkış çarpanına bağlı, bkz. §8</div></div>
</div>
<p class="note">Rakamlar sabit dolarla (TL enflasyonundan arındırılmış) ve 12 Eylül 2026 kuru <strong>1 $ = ₺{n(FX,1)}</strong> ile verilmiştir. Model ve varsayımlar <code>talimat-fizibilite/model.py</code> içinde; her tablo bu dosyadan üretildi.</p>
"""

urun = f"""
<p>Çalışma adı <strong>"Talimatname"</strong> (12 Eylül 2026; önceki çalışma adları Talimat ve yap lütfen; kesin isim pilot görüşmelerindeki isim testi sonrası). Yönetici, tekrar eden (saatlik, açılış, kapanış, haftalık) talimat listeleri hazırlar; sahadaki kişi mobil uygulamadan maddeleri tamamlar, <strong>fotoğraf/video/konum/zaman damgalı kanıt</strong> yükler, yapamadığını sebebiyle işaretler. Her adım değiştirilemez şekilde loglanır. Hedef: bugün WhatsApp gruplarında "yapıldı abi 👍" ile yürüyen işlerin kanıtlı, raporlanabilir ve denetlenebilir hâle gelmesi.</p>
<h3>WhatsApp neden yetmiyor — ve neden yine de zor rakip</h3>
<div class="tw"><table class="data wide"><thead><tr><th>İhtiyaç</th><th>WhatsApp grubu</th><th>Talimatname</th></tr></thead><tbody>
<tr><td>Tekrarlı iş planı</td><td>Her gün yöneticinin elle yazması gerekir; unutulur</td><td>Takvim kuralı (her gün 22:30 kapanış; pazartesi genel temizlik) otomatik açılır</td></tr>
<tr><td>Kanıt</td><td>Fotoğraf gelir ama hangi maddeye ait, ne zaman çekildi, arşivde bulunur mu — hayır</td><td>Madde bazında, zaman ve konum damgalı, aranabilir arşiv</td></tr>
<tr><td>Yapılmayan işler</td><td>Sessizlik = belirsizlik</td><td>"Yapılamadı + sebep" zorunlu; eksik maddeler yöneticiye düşer</td></tr>
<tr><td>Raporlama</td><td>Yok</td><td>Şube × liste × kişi tamamlanma oranı, gecikme, tekrar eden sorunlar</td></tr>
<tr><td>Denetim / uyuşmazlık</td><td>Ekran görüntüsü</td><td>Değiştirilemez log; iş hukuku ve gıda güvenliği denetimlerinde kanıt</td></tr>
<tr><td>Kurulum ve alışkanlık</td><td><strong>Sıfır — herkesin telefonunda var</strong></td><td>Uygulama indirtmek ve alışkanlık kurmak gerekir — <strong>en büyük engel</strong></td></tr>
</tbody></table></div>
<p>Değer önerisi gerçek: gıda güvenliği, franchise standardı, tesis yönetimi gibi alanlarda "kanıt" bir lüks değil zorunluluk. Ama ürün, bedava ve evrensel bir aracın yerine geçmeye çalışıyor; bu yüzden <strong>satış argümanı "WhatsApp'ı bırakın" değil, "WhatsApp'ta kaybolan işleri görünür kılın" olmalı</strong>. Bildirimlerin WhatsApp Business API üzerinden gitmesi (Türkiye'de yardımcı mesaj tarifesi mesaj başına ≈0,0014 $<sup><a href="#k-wa">[WA]</a></sup>) alışkanlık engelini düşürür: çalışan bildirimi WhatsApp'ta görür, tek dokunuşla uygulamada tamamlar.</p>
<h3>Temel özellik seti (MVP)</h3>
<ul>
<li>Liste şablonları ve tekrar kuralları (RRULE: saatli, açılış/kapanış, haftalık, aylık; vardiya ve şube bazlı)</li>
<li>Madde türleri: onay kutusu, fotoğraf zorunlu, sayısal (sıcaklık, kasa sayımı), imza, çoktan seçmeli</li>
<li>Kanıt: kamera-içi çekim (galeriden yükleme kapatılabilir), zaman/konum damgası, sıkıştırma, çevrimdışı kuyruk</li>
<li>"Yapılamadı" akışı: sebep seçimi + not; otomatik eskalasyon (şube müdürü → bölge → merkez)</li>
<li>Roller: merkez, bölge, şube, personel; kişi/grup atama</li>
<li>Rapor ekranı: tamamlanma, gecikme, sorun ısı haritası; PDF/Excel dışa aktarım</li>
<li>Değiştirilemez günlük (hash zinciri), KVKK aydınlatma akışı, veri saklama süreleri</li>
</ul>
"""

pazar = f"""
<h3>Küresel sinyal: kategori var, para akıyor</h3>
<p>Ürünün girdiği kategori ("frontline / deskless operations", dijital kontrol listesi) küresel ölçekte kanıtlanmış: SafetyCulture 2024'te <strong>1,7 milyar $</strong> değerlemeyle 350 M$ topladı; Connecteam 800 M$ değerlemeyle 120 M$ Seri C aldı<sup><a href="#k-fund">[F]</a></sup>. Kategori büyüklüğü tanıma göre 6,8 mlr $ (2025) → 12,3 mlr $ (2030, YBBO %12,6) ya da 8,1 mlr $ → 40 mlr $ (2034, YBBO %18,5)<sup><a href="#k-mkt">[M]</a></sup>. Drake Star'ın Ağustos 2026 raporuna göre frontline teknolojisinde çeyreklik M&A hacmi 14 mlr $'a çıktı<sup><a href="#k-mkt">[M]</a></sup>. Yani ürün fikri doğru; soru, Türkiye'de kaç para ettiği.</p>
<h3>Türkiye: lokasyon bazlı TAM / SAM</h3>
<p>Fiyatlama lokasyon başına olacağı için pazar da lokasyonla ölçülmeli. Kaynaklı sayılar: UFRAD'a göre 1.500+ franchise veren marka, <strong>80.000+ franchise noktası</strong><sup><a href="#k-tr">[T]</a></sup>; organize gıda perakendesi 2024 sonu <strong>55.737 mağaza</strong> (ilk 10 zincir 2025'te 51.916; ilk 3 — BİM, A101, Şok — ≈40.000 ve kendi sistemleri var)<sup><a href="#k-tr">[T]</a></sup>; kayıtlı yeme-içme işyeri <strong>158.725</strong> (2025)<sup><a href="#k-tr">[T]</a></sup>; akaryakıt istasyonu ≈12.500–13.200<sup><a href="#k-tr">[T]</a></sup>; spor salonu 6.000+<sup><a href="#k-tr">[T]</a></sup>. Otel/konaklama ve tesis-hizmet sahaları için resmi tek sayı bulamadım; <em>tahmin</em> olarak işaretlendi.</p>
{tam_table()}
<p class="note warn">SAM payları yargısal: örneğin bağımsız yeme-içmenin yalnızca %25'i (sahibinin başında durmadığı, ≥3 personelli işletmeler) erişilebilir sayıldı. ARPU'lar Türkiye'ye uyarlanmış ($9–15/lokasyon/ay; ABD'de Jolt 80–100 $, Xenia 30–200 $)<sup><a href="#k-comp">[R]</a></sup>. Eczaneler (≈25–26 bin) tek şubeli ve düşük uyumlu olduğu için dışarıda bırakıldı.</p>
<h3>Ne kadarı alınabilir (SOM)?</h3>
<p>Baz senaryo 5. yıl sonunda <strong>{n(y5b["locs_end"])} lokasyon</strong>a ulaşıyor; bu SAM'ın {pct(y5b["locs_end"]/T["sam_n"],1)}'i, TAM'ın {pct(y5b["locs_end"]/T["tam_n"],1)}'i. Kıyas: Türkiye'nin en bilinen İK SaaS'ı Kolay İK, 149 kişilik ekiple 2024'te ≈5,7 M$ gelire ulaşmış durumda<sup><a href="#k-tr-saas">[S]</a></sup> — yani Türkiye'de tek ülkeyle 5 yılda 1–2 M$ ARR "iyi", 4 M$+ "istisnai" sonuçtur. Türkiye pazarı, ürünü <strong>kanıtlamak</strong> için yeterli, <strong>büyütmek</strong> için değil.</p>
"""

rekabet = f"""
<p>Rekabet üç katmanda: küresel oyuncular (Türkçe yerelleştirme ve TL fiyat yok, satış ekibi yok), yerel yeni girişimler ve POS/İK yazılımlarının eklenti modülleri, bir de asıl rakip olan <strong>ücretsiz WhatsApp</strong>.</p>
<div class="tw"><table class="data wide"><thead><tr><th>Oyuncu</th><th>Konum</th><th>Fiyat (kaynaklı)</th><th>Türkiye'de zayıf noktası</th></tr></thead><tbody>
<tr><td>SafetyCulture (iAuditor)</td><td>Küresel lider, denetim + kontrol listesi</td><td>10 kullanıcıya kadar ücretsiz; Premium 24 $/kullanıcı/ay (yıllık), 29 $ aylık<sup><a href="#k-comp">[R]</a></sup></td><td>Kullanıcı başı fiyat Türkiye'de pahalı; ücretsiz katman küçük işletmeyi kapar ama zincir için yetersiz; Türkçe şablon kütüphanesi var, satış/destek yok</td></tr>
<tr><td>Connecteam</td><td>Saha ekipleri "hepsi bir arada"</td><td>Operasyon hub'ı Basic 29 $/ay (ilk 30 kullanıcı), Advanced 49 $, Expert 99 $; ek kullanıcı 0,5–3 $; 10 kullanıcıya kadar ücretsiz<sup><a href="#k-comp">[R]</a></sup></td><td>Çok geniş, karmaşık; Türkçe pazarlama yok; küçük ekipler için fiyat/performansı güçlü — <strong>en tehlikeli küresel rakip</strong></td></tr>
<tr><td>Jolt</td><td>Restoran operasyonu, ABD</td><td>≈80–100 $/lokasyon/ay; tam paket 207–296 $/ay + 500–600 $ kurulum<sup><a href="#k-comp">[R]</a></sup></td><td>Türkiye'de yok; fiyat 5–8 kat yüksek</td></tr>
<tr><td>Xenia</td><td>Çok şubeli operasyon, AI</td><td>Lokasyon başı özel fiyat; tek lokasyon ≈200 $, 500+ lokasyonda ≈30 $<sup><a href="#k-comp">[R]</a></sup></td><td>Türkiye'de yok</td></tr>
<tr><td>GoAudits / Bindy</td><td>Denetim odaklı</td><td>GoAudits 10–30 $/kullanıcı/ay; Bindy 129 $/ay'dan (10 denetim)<sup><a href="#k-comp">[R]</a></sup></td><td>Denetim odaklı, günlük görev akışı zayıf</td></tr>
<tr><td><strong>CheckMaster</strong> (İstanbul)</td><td>Doğrudan yerel rakip: şube, açılış/kapanış kontrol listesi, fotoğraf kanıtı, vardiya, eğitim</td><td>Sitede 249 ve 499 "/yıl" planlar; birim (şirket mi şube mi, $ mı ₺ mi) belirsiz<sup><a href="#k-comp">[R]</a></sup></td><td>App Store'da Haziran 2025'te çıktı, henüz yeterli değerlendirme yok; referans müşteri listelenmemiş. Fikir doğrulanmış ama pazar hâlâ boş — <strong>ilk hareket avantajı kaçmamış</strong></td></tr>
<tr><td>POS/franchise modülleri (YemekPOS, Menulux, Netpus, Aybil)</td><td>Merkez–şube yönetimi eklentisi</td><td>Paket içinde</td><td>Kontrol listesi ikincil özellik; kanıt/log derinliği yok; ama mevcut müşteriye "bedava" gelir — kanal ortağı da olabilir</td></tr>
<tr><td>PDKS uygulamaları (Patron PDKS, Paydoss, Shiftbox)</td><td>Mesai/konum takibi</td><td>Personel başı</td><td>Görev/kanıt yok; komşu kategori, entegrasyon fırsatı</td></tr>
<tr><td><strong>WhatsApp</strong></td><td>Fiili standart</td><td>0 ₺</td><td>Kanıt, log, tekrar, rapor yok — ama alışkanlık ve sıfır sürtünme</td></tr>
</tbody></table></div>
<h3>Konumlanma boşluğu</h3>
<ul>
<li><strong>Zincir + kanıt + Türkçe + TL + saha satışı</strong> kombinasyonu bugün kimsede tam yok. Küreseller ilk üçü, yereller son ikisini karşılıyor.</li>
<li>Fiyat çıpası düşük: CheckMaster'ın yıllık 249–499'luk planları ve Paraşüt'ün ₺940+KDV/ay ön muhasebe paketi<sup><a href="#k-tr-saas">[S]</a></sup> KOBİ'nin "yazılım" için ödemeye alıştığı bandı gösteriyor. Zincir başına ₺15–40 bin/ay'lık sözleşmeler (25–50 lokasyon) mümkün, tek şube için ₺300–500/ay tavan.</li>
<li>Savunma hattı ürün değil dağıtım: franchise verenlerle (marka merkezi) anlaşıp bayilere standart olarak indirtmek. Bir marka = onlarca lokasyon, tek satış görüşmesi.</li>
</ul>
"""

teknik = f"""
<p>Teknik olarak orta zorlukta, iyi bilinen bir problem. Riskli kısımlar kanıt bütünlüğü, çevrimdışı senkronizasyon ve tekrar kurallarının saat dilimi/vardiya karmaşası; hiçbiri araştırma gerektirmiyor.</p>
<div class="arch">Mobil (Flutter, iOS+Android)  ──►  API (Python/FastAPI veya Node)  ──►  PostgreSQL (görev, log, RRULE)
   • kamera-içi çekim, EXIF+GPS+sunucu zamanı           • nesne depolama (S3 uyumlu; fotoğraf/video, WORM politikası)
   • çevrimdışı kuyruk (SQLite) → senk                   • bildirim: push + WhatsApp Business API + SMS yedek
Web yönetim paneli (React)  ──►  şablon editörü, atama, raporlar, dışa aktarım, denetim izi görüntüleyici
Bütünlük: her olay hash-zincirli günlükte; günlük kökü günde bir kez zaman damgası servisine yazılır</div>
<h3>MVP kapsamı, süre ve ekip</h3>
<ul>
<li><strong>Süre:</strong> 5–6 ay (Yalın senaryoda 7. ay lansman). Kapsam: yukarıdaki MVP listesi; entegrasyonlar (PDKS, POS, HRIS) sonraya.</li>
<li><strong>Ekip:</strong> 2 geliştirici (1 mobil, 1 backend/web; modelde {n(C["DEV_COST"])} $ ≈ ₺{n(C["DEV_COST"]*FX/1e3)} bin/ay yüklü maliyet) + ürün sahibi kurucu + yarı zamanlı tasarımcı. Piyasa: Flutter geliştirici ortalama ₺67,2 bin, kıdemli çapraz-platform ≈₺117,5 bin net<sup><a href="#k-dev">[D]</a></sup>; yüklü işveren maliyeti net'in ~1,4–1,5 katı.</li>
<li><strong>MVP maliyeti:</strong> 6 ay × (2 geliştirici + kurucu + genel gider) ≈ <strong>{usd_k(6*(2*C["DEV_COST"]+C["FOUNDER_COST"]+C["GA_FIXED"][0]+C["CLOUD_FIXED"]))}</strong> ({tl_m(6*(2*C["DEV_COST"]+C["FOUNDER_COST"]+C["GA_FIXED"][0]+C["CLOUD_FIXED"]),1)}). AI destekli geliştirme bu süreyi kısaltabilir; modelde varsayılmadı (yukarı yönlü ihtiyat).</li>
<li><strong>İşletme maliyeti:</strong> depolama+işlem ≈{n(C["HOST_PER_LOC"],1)} $/lokasyon/ay (lokasyon başına günde ~20 fotoğraf × 300 KB → yılda ~2 GB), bildirim ≈{n(C["NOTIF_PER_LOC"],1)} $, destek payı ≈{n(C["SUPPORT_PER_LOC"],1)} $ → brüt marj zincirde {pct(B["unit"]["gm_chain"])}.</li>
</ul>
<h3>Yapım–satın alma ve platform kararları</h3>
<ul>
<li>SafetyCulture/Connecteam'in ücretsiz katmanı üstüne "Türkçe katman" kurmak (bayilik) mümkün ama marj ve veri sahipliği kaybolur; önerilmez.</li>
<li>Barındırma: KVKK yurt dışı aktarım kuralları (bkz. §6) nedeniyle Türkiye'de sunucu (yerel bulut) veya standart sözleşme ile AB bölgesi. Maliyet farkı önemsiz.</li>
<li>Kanıt bütünlüğü: galeriden yükleme kapalı, kamera-içi çekim, cihaz saati yerine sunucu saati, hash zinciri — "fotoğrafı dün çekmiş" itirazını kapatır.</li>
</ul>
"""

operasyon = f"""
<p>Asıl operasyonel yük yazılımda değil <strong>benimsetmede</strong>: her müşteride onlarca personelin uygulamayı indirmesi, ilk hafta alışkanlık kurulması, şablonların işletmeye uyarlanması. Bu, ürün değil müşteri-başarısı işidir ve maliyeti modele "CAC" ve "destek" olarak girildi.</p>
<ul>
<li><strong>Onboarding:</strong> sektör şablon kütüphanesi (restoran açılış/kapanış, market raf/soğuk zincir, spor salonu temizlik, akaryakıt vardiya devri) ilk günde değer üretmeli. Her zincir için 1–2 günlük kurulum hizmeti; ücretli olabilir (Jolt 500–600 $ alıyor).</li>
<li><strong>Destek:</strong> personel tarafı basit tutulmalı (3 ekran); sorunların çoğu "bildirim gelmiyor / fotoğraf yüklenmiyor" olacak. 1 destek kişisi / ~1.500 lokasyon varsayıldı.</li>
<li><strong>Satış döngüsü:</strong> zincir merkeziyle 4–8 hafta, pilot 1 ay; tekil işletmeler için self-servis (kart, 14 gün deneme). Satış ekibi Yalın'da PMF sonrası (2. yıl) devreye giriyor.</li>
<li><strong>Kayıp (churn) kontrolü:</strong> lokasyon başına haftalık tamamlanma oranı düşünce müşteri başarısı araması — kullanım düşüşü iptalin 1–2 ay öncüsüdür.</li>
<li><strong>Mevsimsellik:</strong> turizm/yeme-içme yaz yoğun; sözleşmeleri yıllık ve peşin yapmak (indirimle) hem nakit hem kaybı düzeltir.</li>
</ul>
"""

hukuk = f"""
<p>Ürün çalışanların kişisel verisini (ad, fotoğraf, konum, çalışma saatleri) işler; bu KVKK kapsamında yapılabilir ama tasarım kararlarıyla şekillenmeli.</p>
<ul>
<li><strong>Aydınlatma ve hukuki sebep:</strong> işveren, çalışanın verisini "meşru menfaat / sözleşmenin ifası" temelinde işleyebilir; aydınlatma metni somut olmalı ("konum yalnızca görev tamamlama anında, işyeri sınırında"). Kurul'un 2020/404 kararı aydınlatmasız işlemeyi cezalandırdı<sup><a href="#k-kvkk">[K]</a></sup>. Ürün, müşteriye hazır aydınlatma şablonu ve uygulama-içi onay akışı sağlamalı.</li>
<li><strong>Biyometri yasağı:</strong> Kurul'un 29.04.2026 tarihli 2026/921 sayılı ilke kararı mesai takibinde biyometrik veriyi kısıtladı<sup><a href="#k-kvkk">[K]</a></sup>. Ürün <strong>yüz tanıma/parmak izi kullanmamalı</strong>; kanıt fotoğrafı işi gösterir, kişiyi değil. Bu, bir rakip özelliği değil, uyum avantajı.</li>
<li><strong>Konum:</strong> sürekli takip değil, madde tamamlanırken tek seferlik damga; kapatılabilir; işyeri dışında toplanmaz.</li>
<li><strong>Yurt dışı aktarım:</strong> veriler Türkiye'de tutulursa sorun yok; yurt dışı bulut için 2024 değişikliğiyle gelen standart sözleşme yolu kullanılabilir. Veri işleyen sıfatıyla müşteriyle veri işleme sözleşmesi şart.</li>
<li><strong>İş hukuku:</strong> loglar disiplin süreçlerinde delil olur; bu müşteri için değer, çalışan için hassasiyet. Saklama süresi ve silme politikası (örn. 2 yıl) ürün ayarı olmalı.</li>
<li><strong>Diğer:</strong> KVKK VERBİS kaydı (çalışan sayısı eşiğine göre), uygulama mağazası gizlilik etiketleri, e-fatura/e-arşiv abonelik faturalaması. Hiçbiri engelleyici değil.</li>
</ul>
"""

finans = f"""
<p>Model 60 aylık; dört senaryo aynı maliyet yapısını, farklı büyüme/fiyat/kayıp varsayımlarını kullanıyor. <strong>Yalın</strong> senaryo kurucunun kendi kaynağıyla, satış ekibini ürün-pazar uyumu (PMF) sonrasına bırakarak ilerlediği yol; <strong>Baz</strong> dış sermayeyle daha hızlı ekip kurma; <strong>İyimser</strong> 3. yıldan itibaren yurt dışı (MENA/Doğu Avrupa) satışını içeriyor ve Türkiye SAM'ıyla sınırlı değil; <strong>Kötümser</strong> düşük fiyat + yüksek kayıp + geç lansman.</p>
<h3>Varsayımlar</h3>
<div class="tw"><table class="data wide"><thead><tr><th>Kalem</th><th>Değer</th><th>Dayanak</th></tr></thead><tbody>
<tr><td>Zincir ARPU</td><td>{n(Ko["params"]["chain_arpu"])}–{n(Op["params"]["chain_arpu"])} $/lokasyon/ay (Baz {n(B["params"]["chain_arpu"])} $ ≈ ₺{n(B["params"]["chain_arpu"]*FX)})</td><td>ABD fiyatlarının ~%15–25'i (Jolt 80–100 $, Xenia 30–200 $, SafetyCulture 24 $/kullanıcı); Paraşüt ₺940/ay çıpası</td></tr>
<tr><td>Tekil ARPU</td><td>{n(Ko["params"]["single_arpu"])}–{n(Op["params"]["single_arpu"])} $/ay (Baz {n(B["params"]["single_arpu"])} $ ≈ ₺{n(B["params"]["single_arpu"]*FX)})</td><td>Tek şube tavanı ₺300–500/ay</td></tr>
<tr><td>Aylık kayıp (churn)</td><td>Zincir {pct(Op["params"]["chain_churn"],1)}–{pct(Ko["params"]["chain_churn"],1)}, tekil {pct(Op["params"]["single_churn"],1)}–{pct(Ko["params"]["single_churn"],1)}</td><td>KOBİ SaaS %3–7/ay; yıllık sözleşmeli zincirlerde çok daha düşük<sup><a href="#k-saas">[B]</a></sup></td></tr>
<tr><td>CAC (maaş hariç)</td><td>Zincir {n(Op["params"]["cac_chain"])}–{n(Ko["params"]["cac_chain"])} $/lokasyon, tekil {n(Op["params"]["cac_single"])}–{n(Ko["params"]["cac_single"])} $</td><td>B2B CPL ₺200–1.500; 25 lokasyonluk zincir başına ≈2.750 $ (demo, pilot, kurulum, seyahat, prim); satış maaşları ayrıca</td></tr>
<tr><td>Ekip (yüklü maliyet)</td><td>Geliştirici {n(C["DEV_COST"])} $/ay, satış-CS {n(C["SALES_COST"])} $/ay, kurucu {n(C["FOUNDER_COST"])} $/ay</td><td>2026 maaş verisi × 1,4–1,5 işveren yükü<sup><a href="#k-dev">[D]</a></sup></td></tr>
<tr><td>Ekip büyüklüğü Y1→Y5</td><td>Yalın: gel. {"/".join(str(x) for x in Yl["params"]["dev_fte"])}, satış {"/".join(str(x) for x in Yl["params"]["sales_fte"])} · Baz: gel. {"/".join(str(x) for x in B["params"]["dev_fte"])}, satış {"/".join(str(x) for x in B["params"]["sales_fte"])}</td><td>Kolay İK ölçeği (149 kişi, 5,7 M$) referans</td></tr>
<tr><td>Satılan hizmet maliyeti</td><td>{n(C["HOST_PER_LOC"]+C["NOTIF_PER_LOC"]+C["SUPPORT_PER_LOC"],1)} $/lokasyon/ay + ödeme %{n(C["PAYMENT_FEE"]*100)} + sabit {n(C["CLOUD_FIXED"])} $/ay</td><td>Depolama, WhatsApp/SMS, destek FTE payı</td></tr>
<tr><td>Genel gider</td><td>{n(C["GA_FIXED"][0])} → {n(C["GA_FIXED"][4])} $/ay</td><td>Muhasebe, hukuk, ofis, araçlar</td></tr>
<tr><td>Çıkış çarpanı (Y5 ARR ×)</td><td>{n(Ko["params"]["exit_multiple"],1)} / {n(Yl["params"]["exit_multiple"],1)} / {n(B["params"]["exit_multiple"],1)} / {n(Op["params"]["exit_multiple"],1)}</td><td>Küresel KOBİ SaaS 4–6×; Türkiye iskontosu; Paraşüt→Mikro, Insider→Bluecore (2026) emsalleri tutar açıklamıyor<sup><a href="#k-tr-saas">[S]</a></sup></td></tr>
</tbody></table></div>
<h3>Senaryo özeti</h3>
{scen_table()}
<figure>{chart_arr}<figcaption>Yıl sonu ARR. İyimser eğri 3. yıldan itibaren yurt dışı satışı içerir; diğer üçü yalnızca Türkiye. Grafiğin üstüne gelince ay bazında değerler görünür.</figcaption></figure>
<figure>{chart_cum}<figcaption>Kümülatif nakit: en düşük nokta gereken toplam sermaye. Kötümser senaryo 5 yıl ısrar edildiğinde {usd_m(-Ko["peak_need"])} kaybettirir; 24. ayda kapatılırsa kayıp {usd_k(-Ko["cum_m24"])} ile sınırlı kalır.</figcaption></figure>
<h3>Yıllık tablolar</h3>
<div class="grid2">{year_table("Yalın")}{year_table("Baz")}</div>
<div class="grid2">{year_table("Kötümser")}{year_table("İyimser")}</div>
<h3>Birim ekonomi</h3>
{unit_table()}
<p>Zincir segmenti sağlıklı (LTV/CAC {n(B["unit"]["ltv_cac_chain"],1)}×, geri ödeme {n(B["unit"]["payback_chain"],1)} ay Baz'da); <strong>tekil işletme segmenti ancak self-servis ve düşük CAC ile ayakta duruyor</strong> (Kötümser'de LTV/CAC {n(Ko["unit"]["ltv_cac_single"],1)}×). Sonuç: satış eforu zincirlere, tekil işletmelere yalnızca ürün-güdümlü büyüme.</p>
<h3>Müşteri tarafında geri dönüş (fiyatı savunmak için)</h3>
<p>25 lokasyonlu bir yeme-içme zinciri Baz fiyatla ayda 25 × ₺{n(B["params"]["chain_arpu"]*FX)} = <strong>₺{n(25*B["params"]["chain_arpu"]*FX)}</strong> öder. Karşılığı: her şube müdürünün WhatsApp'ta iş kovalamaya harcadığı ~6 saat/ay (25 × 6 × ₺250 ≈ ₺37.500), bölge müdürünün şube ziyaret sayısının yarıya inmesi, bir gıda güvenliği/denetim cezasından kaçınma (tek seferde on binlerce ₺). Yalnızca zaman tasarrufu bile 2× geri dönüş — fiyat argümanı savunulabilir; itiraz fiyatta değil <em>alışkanlıkta</em> olacak.</p>
<h3>Duyarlılık</h3>
{sens_arr}
{sens_irr}
<p>ARR'nin fiyata duyarlılığı kayba duyarlılığından büyük; IRR ise en çok <strong>müşteri edinme hızına</strong> bağlı. Edinme hızı Baz'ın yarısına düşerse (ilk satır) IRR tek haneye iner — bu yüzden 24. ay kapısı edinme hızını ölçmeli.</p>
<h3>Çıkış olmazsa değer</h3>
{dcf_table()}
<p>Çıkış olmadan, şirketi 10 yıl işletip nakit akışını iskonto edince Baz senaryo bugünkü değeri %20 iskontoyla yatırılan sermayeye yakın, %30'da altında. Yani <strong>Türkiye-içi "nakit ineği" tezi tek başına zayıf</strong>; getiri tezi ya çıkış ya da yurt dışı ölçek.</p>
<h3>Beklenen değer (olasılık ağırlıklı)</h3>
{ev_table()}
<p>A ve B iki farklı önsel: A "iyi yürütülen" (%50 başarısızlık), B "sert" (%65 başarısızlık, İyimser %3). İkisinde de beklenen kâr pozitif; ama dağılım aşırı sağa çarpık — sonuçların çoğu kayıp, değer birkaç iyi sonuçta. Bu, kişisel sermayeyle girilecekse <strong>kayıp bütçesini baştan sınırlamayı</strong> (24. ay kapısı) gerektirir; portföy mantığıyla (birkaç girişimden biri) daha rahattır.</p>
"""

risk = f"""
<div class="tw"><table class="data wide"><thead><tr><th>Risk</th><th>Olasılık</th><th>Etki</th><th>Azaltma</th></tr></thead><tbody>
<tr><td>Personel uygulamayı kullanmıyor; yönetici WhatsApp'a geri dönüyor</td><td><span class="tag hi">Yüksek</span></td><td><span class="tag hi">Yüksek</span></td><td>WhatsApp API ile bildirim; 3 ekranlık personel arayüzü; ilk 2 hafta yerinde kurulum; kullanım düşüşünde otomatik uyarı</td></tr>
<tr><td>Düşük ödeme isteği; fiyat ₺500/lokasyon altına iniyor</td><td><span class="tag md">Orta</span></td><td><span class="tag hi">Yüksek</span></td><td>Zincir odaklı satış; yıllık peşin; ROI hesaplayıcı; tekil segmentte self-servis</td></tr>
<tr><td>Connecteam/SafetyCulture Türkçe + TL ile gelir</td><td><span class="tag md">Orta</span></td><td><span class="tag md">Orta</span></td><td>Yerel dağıtım (franchise merkezleri, POS ortaklıkları), yerel uyum (KVKK, e-fatura), hızlı destek</td></tr>
<tr><td>CheckMaster veya benzeri yerel oyuncu önce ölçeklenir</td><td><span class="tag md">Orta</span></td><td><span class="tag md">Orta</span></td><td>Pazar boş ve büyük; ilk 20 zincirle referans üstünlüğü; ürün değil dağıtım hızına yatırım</td></tr>
<tr><td>Yapay zekâ ile herkesin iç araç yazabilmesi kategoriyi metalaştırır</td><td><span class="tag md">Orta</span></td><td><span class="tag md">Orta</span></td><td>Değer, yazılımda değil şablon kütüphanesi, uyum paketi, denetim izi ve destek hizmetinde konumlanmalı</td></tr>
<tr><td>Zincir satış döngüsü uzar, CAC ikiye katlanır</td><td><span class="tag md">Orta</span></td><td><span class="tag md">Orta</span></td><td>Ücretli pilot (₺'li LOI) şartı; 8 haftayı geçen fırsatları kapatma disiplini</td></tr>
<tr><td>KVKK şikâyeti / çalışan tepkisi (gözetim algısı)</td><td><span class="tag lo">Düşük</span></td><td><span class="tag md">Orta</span></td><td>Biyometri yok, sürekli konum yok, şeffaf aydınlatma; "işi kanıtla, kişiyi izleme" ilkesi</td></tr>
<tr><td>TL/USD ve enflasyon: TL fiyat erir, dolar maliyet artar</td><td><span class="tag hi">Yüksek</span></td><td><span class="tag md">Orta</span></td><td>Fiyatları döviz endeksli veya çeyreklik güncellenir tutmak; sözleşmelerde artış maddesi</td></tr>
<tr><td>Kurucu tek başına; teknik ve satış aynı kişide</td><td><span class="tag md">Orta</span></td><td><span class="tag hi">Yüksek</span></td><td>Satış-operasyon ortak (perakende/yeme-içme geçmişli) — lansmandan önce</td></tr>
</tbody></table></div>
"""

plan = f"""
<p>Fizibilitenin en belirsiz üç girdisi (ödeme isteği, benimseme, edinme hızı) masa başında değil sahada doğrulanır. Öneri, harcamadan önce 90 gün:</p>
<ol>
<li><strong>Hafta 1–4 — Sorun görüşmeleri:</strong> 20 zincir (5–100 lokasyon; yeme-içme, market, spor salonu, tesis yönetimi) operasyon müdürüyle görüşme. Ölçüt: en az 12'si bugün WhatsApp'la yürüttüğü "kanıt gerektiren" en az 3 tekrarlı listeyi sayabiliyor ve mevcut çözümüyle ilgili somut acı anlatıyor.</li>
<li><strong>Hafta 3–8 — Tıklanabilir prototip + fiyat testi:</strong> Figma prototipi ile ₺{n(B["params"]["chain_arpu"]*FX)}/lokasyon/ay teklif. Ölçüt: 20'den en az 5 zincir ücretli pilot niyet mektubu (LOI) imzalıyor.</li>
<li><strong>Hafta 6–12 — "Çelik iplik" pilot:</strong> tek liste türü (kapanış), 3 tasarım-ortağı zincirde 15–30 lokasyon; WhatsApp bildirim + fotoğraf kanıtı. Ölçüt: 4. haftada lokasyon başına tamamlanma ≥ %80, yönetici haftada ≥ 3 kez rapor açıyor, en az 2 zincir yıllık sözleşmeye geçiyor.</li>
</ol>
<p class="note">Sprint maliyeti ≈ {tl_k(SPRINT)} ({usd_k(SPRINT)}; 1 geliştirici 2 ay + prototip + seyahat). Üç ölçütten ikisi tutmazsa proje burada biter; kayıp bir yazılım şirketinin bir aylık maaş bordrosu kadar.</p>
<h3>Sonraki kapılar</h3>
<ul>
<li><strong>6. ay (lansman):</strong> 3 ödeyen zincir, ≥ 100 lokasyon canlı.</li>
<li><strong>12. ay:</strong> en az 8 ödeyen zincir; gelir hedefi yerine <em>kayıp</em> ölçülür: zincir aylık kaybı ≤ %2,5, tekil ≤ %6; lokasyon başına haftalık tamamlanma ≥ %75.</li>
<li><strong>24. ay (büyüt/kapat kapısı):</strong> ARR ≥ {usd_k(Yl["arr_m24"])} ({tl_m(Yl["arr_m24"],1)}), zincir kaybı ≤ %2, CAC geri ödeme ≤ 12 ay → satış ekibi ve mümkünse dış sermaye ile Baz senaryoya geçiş; ilk yurt dışı pilot (Türkçe konuşulan / Körfez / Balkanlar'daki Türk zincirleri).</li>
<li><strong>36. ay:</strong> yurt dışı gelir payı ≥ %15 değilse "Türkiye'de kârlı niş" moduna geç (ekip sabit, EBITDA ≥ %20 hedefi), çıkış tezini franchise-yazılım/POS oyuncularına stratejik satış olarak kur.</li>
</ul>
"""

kaynak = f"""
<h3>Doğrulanamayan / tahmini kalemler</h3>
<ul>
<li>Otel/konaklama ve tesis-hizmet sahası lokasyon sayıları (tahmin; ±%50).</li>
<li>CheckMaster fiyatının birimi (şirket mi şube mi; $ mı ₺ mi) sitede net değil.</li>
<li>Kolay İK'nın güncel fiyatı yayınlanmıyor; TL ödeme isteği çıpası olarak Paraşüt kullanıldı.</li>
<li>Türkiye'de işletmelerin WhatsApp'ı iş takibinde kullanma oranına dair güvenilir istatistik bulunamadı; varsayım niteliksel.</li>
<li>Çıkış çarpanları: Türkiye'de bu ölçekte SaaS satışlarının bedelleri açıklanmıyor; küresel bantlardan iskonto uygulandı.</li>
<li>Model kurumlar vergisini, işletme sermayesini ve kur riskini içermiyor; sabit dolarla çalışır.</li>
</ul>
<h3>Kaynaklar</h3>
<ol class="src">
<li id="k-comp"><strong>[R] Rakip fiyatları:</strong> <a href="https://www.educate-me.co/blog/safetyculture-pricing">SafetyCulture fiyat rehberi</a>, <a href="https://www.xpay.sh/saas-pricing/safetyculture/">xpay SafetyCulture</a>; <a href="https://connecteam.com/pricing/">Connecteam pricing</a>, <a href="https://www.actitime.com/software-collections/connecteam-pricing">actiTIME – Connecteam hub modeli</a>; <a href="https://softwarefinder.com/resources/how-much-does-jolt-cost">Jolt maliyeti</a>, <a href="https://restauranttools.ai/tools/jolt">RestaurantTools – Jolt</a>; <a href="https://www.xenia.team/pricing">Xenia pricing</a>, <a href="https://operandio.com/xenia-app-cost/">Operandio – Xenia maliyeti</a>; <a href="https://goaudits.com/pricing/">GoAudits</a>, <a href="https://www.capterra.com/p/191777/GoAudits/pricing/">Capterra – GoAudits</a>; <a href="https://checkmaster.app/">CheckMaster</a>, <a href="https://apps.apple.com/tr/app/checkmaster/id6746339344?l=tr">CheckMaster App Store</a>; <a href="https://www.yemekpos.com/franchise-yonetim-yazilimi/">YemekPOS franchise</a>, <a href="https://www.menulux.com/restoran-yonetimi/web-portal/merkezi-yonetim">Menulux</a>, <a href="https://www.patronpdks.com/">Patron PDKS</a>.</li>
<li id="k-fund"><strong>[F] Finansman/değerleme:</strong> <a href="https://tracxn.com/d/companies/safetyculture/__b4zb84DDkwf7agQNXkBm2h8RPLNMOb5CC7E2h1QWnsc/funding-and-investors">Tracxn – SafetyCulture</a>, <a href="https://pitchbook.com/profiles/company/60535-18">PitchBook – SafetyCulture</a>; <a href="https://www.businesswire.com/news/home/20210503005296/en">Connecteam Seri C (BusinessWire)</a>, <a href="https://tracxn.com/d/companies/connecteam/__kxUHdDO-KYV5AYYQUalaQ4iO97HkUuKUoAHhUmHKRUI/funding-and-investors">Tracxn – Connecteam</a>.</li>
<li id="k-mkt"><strong>[M] Pazar büyüklüğü:</strong> <a href="https://www.guideflow.com/blog/frontline-worker-software">Guideflow – frontline software 2026</a>; <a href="https://growthmarketreports.com/report/frontline-worker-platform-market">Growth Market Reports – frontline platform</a>; <a href="https://www.researchandmarkets.com/reports/6260957/frontline-worker-technology-market-share">Research&Markets – frontline technology</a>; <a href="https://www.drakestar.com/news/drake-star-frontline-technology-report-august-2026">Drake Star Ağustos 2026 raporu</a>.</li>
<li id="k-tr"><strong>[T] Türkiye pazar sayıları:</strong> <a href="https://www.loginoffice.com.tr/turkiyede-franchise-almak/">Login Office – franchise rehberi (UFRAD verisi)</a>, <a href="https://www.ekonomim.com/ekonomi/franchiseda-islem-hacmi-50-milyar-dolara-ulasti-haberi-675905">Ekonomim – franchise hacmi</a>; <a href="https://www.marketingturkiye.com.tr/haberler/perakende-buyumeye-devam-ediyor-2024te-3-bin-478-yeni-market-acildi/">Marketing Türkiye – 55.737 market</a>, <a href="https://www.gazetebirlik.com/ekonomi/turkiyedeki-market-zincirlerinin-sube-sayisi-55-bini-asti/274498">Yeni Birlik – zincir şube sayıları</a>; <a href="https://www.milligazete.com.tr/turkiyede-kayitli-yeme-icme-is-yeri-sayisi-2010-yilinda-62-bin-iken-2025te-159-bine-cikti">Milli Gazete – 158.725 yeme-içme işyeri</a>, <a href="https://www.ipsos.com/tr-tr/restoran-ve-kafelerin-sayisi-artti">Ipsos</a>; <a href="https://petrolpiyasasi.com/tum-dagitim-sirketlerinin-2025-yili-toplam-istasyon-sayisi-fark-kayip-kazanc/">Petrol Piyasası – istasyon sayısı</a>, <a href="https://www.otoraf.com/akaryakit-istasyonlari-bp-opet-petrol-ofisi-shell-ve-total.html">Otoraf</a>; <a href="https://www.karo360.com/turkiyede-spor-merkezlerinin-sayisinda-hizli-artis-saglikli-yasama-dogru-adim/">Karo – spor salonu sayısı</a>; <a href="https://www.researchgate.net/profile/Mehmet-Atasever-3/publication/343987376_Turkiye_Serbest_Eczane_Sektor_Analizi/links/5f4ca1a2458515a88b95c919/Tuerkiye-Serbest-Eczane-Sektoer-Analizi.pdf">TEB – eczane sektör analizi</a>; <a href="https://www.dunya.com/ekonomi/tuik-acikladi-girisim-sayisi-ve-istihdamda-en-yuksek-pay-hizmet-sektorunde-haberi-791437">Dünya – TÜİK 2024 sanayi ve hizmet istatistikleri</a>.</li>
<li id="k-tr-saas"><strong>[S] Türkiye SaaS emsalleri:</strong> <a href="https://getlatka.com/companies/kolay-k">Latka – Kolay İK geliri</a>; <a href="https://www.parasut.com/on-muhasebe-fiyatlari">Paraşüt fiyatları</a>; <a href="https://tracxn.com/d/companies/parasut/___UwRXC2mDybt7qemB8X3MNUQvsKND3-UaTuA5pOT_4Y">Tracxn – Paraşüt</a>; <a href="https://pitchbook.com/profiles/company/166459-51">PitchBook – Insider</a>; <a href="https://www.scalexventures.com/content/turkish-startup-and-vc-ecosystem-at-a-glance">ScaleX – Türkiye ekosistemi</a>.</li>
<li id="k-dev"><strong>[D] Maaşlar:</strong> <a href="https://www.eleman.net/meslek/flutter-developer/maas">Eleman.net – Flutter maaşları 2026</a>; <a href="https://code2work.co/blog/yazilimci-maaslari-2026-turkiye">Code2Work – yazılımcı maaşları 2026</a>.</li>
<li id="k-saas"><strong>[B] SaaS kıyas ölçütleri:</strong> <a href="https://www.venasolutions.com/blog/saas-churn-rate">Vena – churn benchmarks</a>; <a href="https://www.stackmatix.com/blog/payback-period-saas-benchmarks">Stackmatix – CAC payback</a>; <a href="https://optif.ai/learn/questions/b2b-saas-churn-rate-benchmark/">Optifai – churn by segment</a>; <a href="https://abdullahcalis.com/blog/dijital-pazarlama-butcesi-2026">Abdullah Çalış – B2B CPL Türkiye</a>.</li>
<li id="k-wa"><strong>[WA] WhatsApp Business API:</strong> <a href="https://whautomate.com/whatsapp-business-api-pricing">Whautomate – ülke tarifeleri 2026</a>; <a href="https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing">Meta – WhatsApp pricing</a>.</li>
<li id="k-kvkk"><strong>[K] KVKK:</strong> <a href="https://www.kvkk.gov.tr/Icerik/8762/mesai-takibi-amaciyla-biyometrik-veri-islenmesi-hakkinda-kisisel-verileri-koruma-kurulunun-29-04-2026-tarihli-ve-2026-921-sayili-ilke-karari-iliskin-kamuoyu-duyurusu">Kurul 2026/921 ilke kararı</a>; <a href="https://www.kvkk.gov.tr/Icerik/6913/2020-404">Kurul 2020/404 kararı</a>; <a href="https://www.sinaneroglu.av.tr/isyerinde-izleme-sistemlerinin-hukuka-uygunlugu-kvkk-2026-921-ilke-karari-sonrasi-durum/">İşyerinde izleme – 2026/921 sonrası</a>.</li>
<li><strong>Kur:</strong> <a href="https://www.bloomberght.com/doviz/dolar">BloombergHT USD/TRY, 12 Eylül 2026</a>.</li>
</ol>
"""

JS = r"""
<div class="tip" id="tip"></div>
<script>
(function(){
  var tip=document.getElementById('tip');
  var fmt=function(v){return v.toLocaleString('tr-TR',{maximumFractionDigits:0});};
  document.querySelectorAll('svg.chart').forEach(function(svg){
    var hit=svg.querySelector('rect.hit'); if(!hit) return;
    var series=JSON.parse(hit.getAttribute('data-series'));
    var L=+hit.getAttribute('data-l'), pw=+hit.getAttribute('data-pw');
    var xh=svg.querySelector('line.xh');
    var pt=svg.createSVGPoint();
    function move(e){
      pt.x=e.clientX; pt.y=e.clientY;
      var p=pt.matrixTransform(svg.getScreenCTM().inverse());
      var m=Math.max(1,Math.min(60,Math.round((p.x-L)/pw*60)));
      var x=L+pw*(m/60);
      xh.setAttribute('x1',x); xh.setAttribute('x2',x); xh.style.display='';
      var y=Math.floor((m-1)/12)+1, mm=((m-1)%12)+1;
      var h='<b>'+m+'. ay</b> (Y'+y+' · '+mm+'. ay)<br>';
      series.forEach(function(s){ h+=s[0]+': <b>'+fmt(s[1][m-1]/1000)+' bin $</b><br>'; });
      tip.innerHTML=h; tip.style.display='block';
      var tx=e.clientX+14, ty=e.clientY+14;
      if(tx+tip.offsetWidth>window.innerWidth-8) tx=e.clientX-tip.offsetWidth-14;
      if(ty+tip.offsetHeight>window.innerHeight-8) ty=e.clientY-tip.offsetHeight-14;
      tip.style.left=tx+'px'; tip.style.top=ty+'px';
    }
    hit.addEventListener('mousemove',move);
    hit.addEventListener('mouseleave',function(){tip.style.display='none'; xh.style.display='none';});
  });
})();
</script>
"""

HTML = f"""{CSS}
<div class="wrap">
<header class="top">
<div class="eyebrow">Fizibilite çalışması · İş analizi · Eylül 2026</div>
<h1>Talimatname: kanıtlı görev listesi ürünü</h1>
<p class="lede">WhatsApp gruplarında yürüyen açılış, kapanış ve haftalık talimatların; fotoğraf kanıtlı, loglu ve tekrarlı bir mobil ürüne taşınması. Pazar, rekabet, teknik, operasyonel, hukuki ve finansal yapılabilirlik; 60 aylık model, dört senaryo.</p>
<div class="meta"><span>Hazırlayan: iş analisti rolünde Claude</span><span>Sabit $; 1 $ = ₺{n(FX,1)}</span><span>Kaynaklı rakamlar §11'de</span></div>
</header>
<div class="layout">
{toc_html}
<main>
{item("karar", "cond", "Karar özeti", "Koşullu GO", karar)}
{item("urun", "ok", "Ürün ve değer önerisi", "Geçerli — dağıtım problemi", urun)}
{item("pazar", "cond", "Pazar", "Kategori kanıtlı, Türkiye küçük", pazar)}
{item("rekabet", "ok", "Rekabet", "Boşluk var, kapanıyor", rekabet)}
{item("teknik", "ok", "Teknik fizibilite", "Yapılabilir, 5–6 ay", teknik)}
{item("operasyon", "cond", "Operasyonel fizibilite", "Benimsetme ana yük", operasyon)}
{item("hukuk", "ok", "Hukuki / KVKK", "Uyumlu tasarımla mümkün", hukuk)}
{item("finans", "cond", "Finansal fizibilite", "Getiri çıkışa/yurt dışına bağlı", finans)}
{item("risk", "info", "Riskler ve azaltma", "9 başlık", risk)}
{item("plan", "info", "Doğrulama planı ve kapılar", f"90 gün, {tl_k(SPRINT)}", plan)}
{item("kaynak", "info", "Kaynaklar ve sınırlar", "Neyi doğrulayamadım", kaynak)}
</main>
</div>
</div>
{JS}
"""

open("index.html", "w", encoding="utf-8").write(HTML)
print("index.html yazıldı,", len(HTML.encode("utf-8")) // 1024, "KB")
