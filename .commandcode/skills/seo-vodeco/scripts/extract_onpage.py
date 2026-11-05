#!/usr/bin/env python3
"""Ekstrak data on-page dari sebuah URL (library standar saja).
Pemakaian: python3 extract_onpage.py <url> [keyword]
"""
import sys, json, re, urllib.request, urllib.parse
from html.parser import HTMLParser

class P(HTMLParser):
    def __init__(s):
        super().__init__(convert_charrefs=True)
        s.title = ""; s.meta = {}; s.canonical = ""; s.headings = []
        s.images = []; s.links = []; s.text = []; s.jsonld = []
        s._tag = None; s._buf = []; s._skip = 0; s._a = None; s._ld = False
        s.breadcrumb = False
    def handle_starttag(s, t, a):
        a = dict(a)
        if t in ("script", "style", "noscript"):
            s._skip += 1
            if t == "script" and a.get("type") == "application/ld+json": s._ld = True; s._buf = []
        if t == "title": s._tag = "title"; s._buf = []
        elif t == "meta":
            k = a.get("name") or a.get("property")
            if k: s.meta[k.lower()] = a.get("content", "")
        elif t == "link" and a.get("rel") == "canonical": s.canonical = a.get("href", "")
        elif re.fullmatch(r"h[1-6]", t): s._tag = t; s._buf = []
        elif t == "img":
            s.images.append({"src": a.get("src") or a.get("data-src", ""), "alt": a.get("alt"), "title": a.get("title")})
        elif t == "a":
            s._a = {"href": a.get("href", ""), "rel": a.get("rel", ""), "target": a.get("target", ""), "text": ""}
            s.links.append(s._a)
        cls = (a.get("class") or "") + " " + (a.get("id") or "")
        if "breadcrumb" in cls.lower(): s.breadcrumb = True
    def handle_endtag(s, t):
        if t in ("script", "style", "noscript"):
            if s._ld: s.jsonld.append("".join(s._buf)); s._ld = False
            s._skip = max(0, s._skip - 1)
        if t == "title" and s._tag == "title": s.title = "".join(s._buf).strip(); s._tag = None
        elif s._tag == t and re.fullmatch(r"h[1-6]", t):
            s.headings.append({"level": t, "text": " ".join("".join(s._buf).split())}); s._tag = None
        if t == "a": s._a = None
    def handle_data(s, d):
        if s._ld: s._buf.append(d); return
        if s._skip: return
        if s._tag: s._buf.append(d)
        if s._tag == "title": return
        if s._a is not None: s._a["text"] += d
        s.text.append(d)

def main():
    if len(sys.argv) < 2: sys.exit(__doc__)
    url = sys.argv[1]; kw = sys.argv[2].lower() if len(sys.argv) > 2 else None
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; seo-vodeco/1.0)"})
    with urllib.request.urlopen(req, timeout=30) as r:
        html = r.read().decode(r.headers.get_content_charset() or "utf-8", "replace")
    p = P(); p.feed(html)
    host = urllib.parse.urlparse(url).netloc.lower().removeprefix("www.")
    internal, external = [], []
    for l in p.links:
        href = urllib.parse.urljoin(url, l["href"])
        if not href.startswith("http"): continue
        h = urllib.parse.urlparse(href).netloc.lower().removeprefix("www.")
        (internal if h == host else external).append({**l, "href": href})
    words = " ".join(" ".join(p.text).split()).split(" ")
    first100 = " ".join(words[:100])
    path = urllib.parse.urlparse(url).path
    out = {
        "url": url, "slug": path.rstrip("/").split("/")[-1],
        "title": p.title, "title_length": len(p.title),
        "meta_description": p.meta.get("description", ""), "meta_description_length": len(p.meta.get("description", "")),
        "canonical": p.canonical, "headings": p.headings,
        "h1_count": sum(1 for h in p.headings if h["level"] == "h1"),
        "word_count": len(words), "first_100_words": first100,
        "images": p.images, "images_without_alt": sum(1 for i in p.images if not i["alt"]),
        "internal_links": internal, "external_links": external,
        "breadcrumb_detected": p.breadcrumb or any("BreadcrumbList" in j for j in p.jsonld),
    }
    if kw:
        low = " ".join(words).lower()
        out["keyword"] = {"in_first_100_words": kw in first100.lower(), "in_title": kw in p.title.lower(),
            "title_starts_with": p.title.lower().startswith(kw), "in_slug": kw.replace(" ", "-") in path.lower(),
            "in_meta": kw in p.meta.get("description", "").lower(),
            "count": low.count(kw), "density_pct": round(low.count(kw) * len(kw.split()) / max(1, len(words)) * 100, 2),
            "in_headings": [h["level"] for h in p.headings if kw in h["text"].lower()]}
    print(json.dumps(out, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
