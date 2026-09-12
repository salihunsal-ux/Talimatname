import re, base64, urllib.request, json, sys
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
FAMS = {
 "baloo": "Baloo+2:wght@800",
 "bricolage": "Bricolage+Grotesque:opsz,wght@12..96,700",
 "caveat": "Caveat:wght@700",
 "barlow": "Barlow+Semi+Condensed:wght@700",
 "outfit": "Outfit:wght@700",
 "jakarta": "Plus+Jakarta+Sans:wght@800",
 "archivo": "Archivo+Narrow:wght@700",
}
out = {}
for key, fam in FAMS.items():
    css_url = f"https://fonts.googleapis.com/css2?family={fam}&display=swap"
    req = urllib.request.Request(css_url, headers={"User-Agent": UA})
    css = urllib.request.urlopen(req, timeout=30).read().decode()
    family = re.search(r"font-family: '([^']+)'", css).group(1)
    blocks = re.findall(r"/\* (latin-ext|latin) \*/\s*@font-face \{(.*?)\}", css, flags=re.S)
    faces = []
    for subset, body in blocks:
        url = re.search(r"url\((https://fonts\.gstatic\.com/[^)]+\.woff2)\)", body).group(1)
        rng = re.search(r"unicode-range: ([^;]+);", body).group(1)
        weight = re.search(r"font-weight: ([^;]+);", body).group(1)
        data = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=30).read()
        b64 = base64.b64encode(data).decode()
        faces.append(f"@font-face{{font-family:'{family}';font-style:normal;font-weight:{weight};font-display:block;src:url(data:font/woff2;base64,{b64}) format('woff2');unicode-range:{rng};}}")
        print(f"{key}: {family} {subset} {len(data)//1024} KB weight {weight}")
    out[key] = {"family": family, "css": "".join(faces)}
json.dump(out, open("fonts/fonts.json", "w", encoding="utf-8"))
print("toplam", sum(len(v["css"]) for v in out.values())//1024, "KB css")
