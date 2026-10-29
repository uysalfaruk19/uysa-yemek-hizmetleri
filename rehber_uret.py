"""Mikro siteye rehber sayfası ekle: python rehber_uret.py <kaynak.md> — uret.py şablonuyla aynı görünüm. 29 Eki 2026, tmux6."""
import re, sys, pathlib, html, json, markdown

KOK = pathlib.Path(__file__).parent
SITE = "https://uysalfaruk19.github.io/uysa-yemek-hizmetleri"
BUGUN = "2026-10-29"
src = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
ornek = (KOK / "index.html").read_text(encoding="utf-8")
CSS = re.search(r"<style>(.*?)</style>", ornek, re.S).group(1)
NAV = re.search(r"<nav>(.*?)</nav>", ornek, re.S).group(1)
FOOT = re.search(r"<footer>(.*?)</footer>", ornek, re.S).group(1)

sayfalar = []
for b in re.split(r"^## ", src, flags=re.M)[1:]:
    sat = b.strip().splitlines()
    ad = sat[0].strip()
    meta = {k: next((l.split(":", 1)[1].strip() for l in sat if l.startswith(k + ":")), "") for k in ("slug", "baslik", "ozet")}
    govde = "\n".join(l for l in sat[1:] if not l.startswith(("slug:", "baslik:", "ozet:"))).strip()
    govde = re.sub(r"(?m)^(.*?)(https://uysayemek\.com\.tr\S*)\s*$", r'\1<a href="\2">\2</a>', govde)
    sayfalar.append({"ad": ad, "govde": markdown.markdown(govde, extensions=["tables"]), **meta})

yazilan, urls = [], []
for p in sayfalar:
    url = f"{SITE}/rehber/{p['slug']}/"
    ld = {"@context": "https://schema.org", "@type": "Article", "headline": p["baslik"], "description": p["ozet"], "inLanguage": "tr-TR",
          "datePublished": BUGUN, "dateModified": BUGUN, "mainEntityOfPage": url,
          "author": {"@type": "Organization", "name": "UYSA Yemek Hizmetleri", "url": "https://uysayemek.com.tr/"},
          "publisher": {"@type": "Organization", "name": "UYSA Yemek Hizmetleri", "url": "https://uysayemek.com.tr/"}}
    yol = KOK / "rehber" / p["slug"] / "index.html"
    yol.parent.mkdir(parents=True, exist_ok=True)
    yol.write_text(
        f'<!doctype html><html lang="tr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
        f'<title>{html.escape(p["baslik"])}</title><meta name="description" content="{html.escape(p["ozet"])}"><link rel="canonical" href="{url}">'
        f'<style>{CSS}</style><script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script></head><body>'
        f'<header><div class="w"><a class="m" href="{SITE}/">UYSA Yemek Hizmetleri</a><nav>{NAV}</nav></div></header>'
        f'<main><p class="giris"><a href="{SITE}/rehber/">Rehber</a> · {BUGUN}</p><h1>{html.escape(p["ad"])}</h1><p class="giris">{html.escape(p["ozet"])}</p>{p["govde"]}</main>'
        f'<footer>{FOOT}</footer></body></html>', encoding="utf-8")
    yazilan.append(f"rehber/{p['slug']}/index.html"); urls.append(url)

# rehber dizini: yeni kartları kart ızgarasının başına ekle
ix = KOK / "rehber" / "index.html"; s = ix.read_text(encoding="utf-8")
kartlar = "".join(f'<a href="{SITE}/rehber/{p["slug"]}/"><strong>{html.escape(p["ad"])}</strong>{html.escape(p["ozet"][:110])}</a>' for p in sayfalar)
s = s.replace('<div class="kart">', '<div class="kart">' + kartlar, 1)
ix.write_text(s, encoding="utf-8")
# sitemap
sm = KOK / "sitemap.xml"; t = sm.read_text(encoding="utf-8")
t = t.replace("</urlset>", "".join(f"  <url><loc>{u}</loc><lastmod>{BUGUN}</lastmod></url>\n" for u in urls if u not in t) + "</urlset>")
sm.write_text(t, encoding="utf-8")
(KOK / "dosyalar3.txt").write_text("\n".join(yazilan + ["rehber/index.html", "sitemap.xml"]) + "\n", encoding="utf-8")
pathlib.Path(r"F:\claude\tmp\uysa-itibar\kayit\yeni-url-ms2.txt").write_text("\n".join(urls) + "\n", encoding="utf-8")
print(len(sayfalar), "sayfa;", "; ".join(p["slug"] for p in sayfalar))
