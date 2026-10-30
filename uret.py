"""UYSA Yemek Hizmetleri tanıtım mikro sitesi — Argon metinlerinden statik HTML (GitHub Pages). 29 Eki 2026, tmux6."""
import re, pathlib, markdown, html, json

KOK = pathlib.Path(__file__).parent
src = pathlib.Path(r"F:\claude\tmp\isci\mikrosite.gemini.md").read_text(encoding="utf-8")
bl = re.split(r"^## ", src, flags=re.M)[1:]
sayfalar = []
for b in bl:
    sat = b.strip().splitlines()
    ad = sat[0].strip()
    meta = {k: next((l.split(":", 1)[1].strip() for l in sat if l.startswith(k + ":")), "") for k in ("slug", "baslik", "ozet")}
    govde = "\n".join(l for l in sat[1:] if not l.startswith(("slug:", "baslik:", "ozet:"))).strip()
    sayfalar.append({"ad": ad, "govde": markdown.markdown(govde, extensions=["tables"]), **meta})

SITE = "https://uysalfaruk19.github.io/uysa-yemek-hizmetleri"
CSS = (":root{--ink:#14213d;--acc:#c0392b;--muted:#5c6773;--line:#e5e9ef;--soft:#f6f8fa}*{box-sizing:border-box}"
       "body{margin:0;font-family:Inter,system-ui,Segoe UI,Arial,sans-serif;color:var(--ink);line-height:1.65;font-size:17px;background:#fff}"
       "header{background:var(--ink);color:#fff}header .w{max-width:960px;margin:0 auto;padding:14px 20px;display:flex;gap:16px;align-items:center;justify-content:space-between;flex-wrap:wrap}"
       "header a{color:#dfe6ee;text-decoration:none;font-size:15px}header .m{font-weight:700;font-size:18px;color:#fff}nav{display:flex;gap:14px;flex-wrap:wrap}"
       "main{max-width:960px;margin:0 auto;padding:28px 20px 48px}h1{font-size:clamp(26px,4vw,38px);line-height:1.2;margin:0 0 10px}h2{font-size:22px;margin:30px 0 8px}"
       ".giris{color:var(--muted);font-size:18px;margin:0 0 20px}a{color:var(--acc)}footer{border-top:1px solid var(--line);background:var(--soft);padding:22px 20px;font-size:14px;color:var(--muted)}"
       "footer .w{max-width:960px;margin:0 auto}table{border-collapse:collapse;width:100%}td,th{border:1px solid var(--line);padding:8px;text-align:left}"
       ".kart{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px;margin:18px 0}.kart a{display:block;padding:14px;border:1px solid var(--line);border-radius:10px;text-decoration:none;color:var(--ink);background:#fff}.kart a strong{display:block;margin-bottom:4px;color:var(--acc)}")
nav = "".join(f'<a href="{SITE}/{p["slug"]}/">{html.escape(p["ad"])}</a>' for p in sayfalar[1:])
org = {"@context": "https://schema.org", "@type": "Organization", "name": "UYSA Yemek Hizmetleri", "alternateName": "UYSA Yemek",
       "url": "https://uysayemek.com.tr/", "telephone": "+90 262 744 81 19", "email": "info@uysayemek.com.tr",
       "address": {"@type": "PostalAddress", "streetAddress": "Şekerpınar Mah. Muhsin Yazıcıoğlu Cd. No:15", "addressLocality": "Çayırova", "addressRegion": "Kocaeli", "postalCode": "41420", "addressCountry": "TR"},
       "areaServed": ["Gebze", "Çayırova", "Dilovası", "Darıca", "Kocaeli"],
       "sameAs": ["https://uysayemek.com.tr/", "https://yemekhaneci.com.tr/", "https://www.instagram.com/uysayemek/", "https://uysayemek.blogspot.com/", "https://uysa-yemek-gebze.blogspot.com/", "https://uysa-yemek-kocaeli.blogspot.com/", "https://uysa-yemek-catering.blogspot.com/", "https://uysa-yemek-hizmetleri.blogspot.com/", "https://uysa-yemek.blogspot.com/", "https://uysa-yemek-tarifleri.blogspot.com/", "https://uysa-yemekhane.blogspot.com/", "https://uysa-tabldot.blogspot.com/", "https://sites.google.com/view/uysa-yemek-hizmetleri", "https://www.youtube.com/watch?v=RNWZN-WmlNU", "https://gist.github.com/uysalfaruk19/184b567bdd9c786d9f261e1cecf628fd", "https://docs.google.com/document/d/e/2PACX-1vQEiJuTKoeYeBl9iSCh6rvtO55EWTuI8OpqsdOVRnXpFfa1rQXwdVNJjhee27DllbTMJGz1sGAO6ZZB/pub"]}
yazilan = []
for i, p in enumerate(sayfalar):
    yol = KOK / "index.html" if i == 0 else KOK / p["slug"] / "index.html"
    yol.parent.mkdir(parents=True, exist_ok=True)
    kartlar = ('<div class="kart">' + "".join(f'<a href="{SITE}/{q["slug"]}/"><strong>{html.escape(q["ad"])}</strong>{html.escape(q["ozet"][:110])}</a>' for q in sayfalar[1:]) + "</div>") if i == 0 else ""
    canon = f"{SITE}/" if i == 0 else f"{SITE}/{p['slug']}/"
    h1 = "UYSA Yemek Hizmetleri" if i == 0 else p["ad"]
    yol.write_text(
        f'<!doctype html><html lang="tr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
        f'<title>{html.escape(p["baslik"])}</title><meta name="description" content="{html.escape(p["ozet"])}"><link rel="canonical" href="{canon}">'
        f'<style>{CSS}</style><script type="application/ld+json">{json.dumps(org, ensure_ascii=False)}</script></head><body>'
        f'<header><div class="w"><a class="m" href="{SITE}/">UYSA Yemek Hizmetleri</a><nav>{nav}</nav></div></header>'
        f'<main><h1>{html.escape(h1)}</h1><p class="giris">{html.escape(p["ozet"])}</p>{p["govde"]}{kartlar}</main>'
        f'<footer><div class="w">UYSA Yemek Hizmetleri · Şekerpınar Mah. Muhsin Yazıcıoğlu Cd. No:15, Çayırova / Kocaeli · 0262 744 81 19 · '
        f'<a href="https://uysayemek.com.tr/">uysayemek.com.tr</a> · <a href="https://yemekhaneci.com.tr/">yemekhaneci.com.tr</a> · '
        f'<a href="https://uysayemek.blogspot.com/">Blog</a> · <a href="https://uysa-yemek-gebze.blogspot.com/">Gebze Blog</a> · <a href="https://uysa-yemek-kocaeli.blogspot.com/">Kocaeli Blog</a> · <a href="https://uysa-yemek-catering.blogspot.com/">Catering Blog</a> · <a href="https://uysa-yemek-hizmetleri.blogspot.com/">UYSA Yemek Hizmetleri Blog</a> · <a href="https://uysa-yemek.blogspot.com/">UYSA Yemek Gıda Güvenliği Blog</a> · <a href="https://uysa-tabldot.blogspot.com/">UYSA Tabldot Blog</a> · <a href="https://uysa-yemekhane.blogspot.com/">UYSA Yemekhane Blog</a> · <a href="https://uysa-yemek-tarifleri.blogspot.com/">UYSA Yemek Tarifleri Blog</a> · <a href="https://www.youtube.com/watch?v=RNWZN-WmlNU">Tanıtım Videosu</a> · <a href="https://www.instagram.com/uysayemek/">Instagram</a></div></footer></body></html>',
        encoding="utf-8")
    yazilan.append(str(yol.relative_to(KOK)).replace("\\", "/"))
urls = [f"{SITE}/"] + [f"{SITE}/{p['slug']}/" for p in sayfalar[1:]]
(KOK / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"  <url><loc>{u}</loc><lastmod>2026-10-29</lastmod></url>\n" for u in urls) + "</urlset>\n", encoding="utf-8")
(KOK / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n", encoding="utf-8")
(KOK / ".nojekyll").write_text("", encoding="utf-8")
(KOK / "README.md").write_text((KOK / "readme_sablon.md").read_text(encoding="utf-8"), encoding="utf-8")  # zengin README github.com sayfası olarak da aranır
(KOK / "dosyalar.txt").write_text("\n".join(yazilan + ["sitemap.xml", "robots.txt", ".nojekyll", "README.md"]) + "\n", encoding="utf-8")
print(len(sayfalar), "sayfa;", ", ".join(yazilan))
