import sys, json, urllib.request, urllib.parse, os, re, time
UA = {"User-Agent": "CanalDarkResearch/1.0 (contact: project owner) python-urllib"}
def api(**p):
    p.update(format="json")
    for k in range(5):
        try:
            r = urllib.request.urlopen(urllib.request.Request("https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(p), headers=UA), timeout=30)
            return json.load(r)
        except Exception as e:
            print('erro', e, file=sys.stderr); time.sleep(10 * (k + 1))
    return {}
def search(q, n=8):
    d = api(action="query", generator="search", gsrsearch=q, gsrnamespace=6, gsrlimit=n,
            prop="imageinfo", iiprop="url|extmetadata|size", iiurlwidth=1600)
    out = []
    for p in sorted(d.get("query", {}).get("pages", {}).values(), key=lambda x: x.get("index", 0)):
        ii = p["imageinfo"][0]; m = ii.get("extmetadata", {})
        g = lambda k: re.sub("<[^>]+>", "", m.get(k, {}).get("value", ""))[:120]
        out.append(dict(title=p["title"], thumb=ii.get("thumburl"), w=ii["width"], h=ii["height"],
                        lic=g("LicenseShortName"), artist=g("Artist"), date=g("DateTimeOriginal"), page=ii.get("descriptionurl")))
    return out
if __name__ == "__main__":
    res = {}
    for q in sys.argv[2:]:
        res[q] = search(q); time.sleep(2.5)
    json.dump(res, open(sys.argv[1], "w"), ensure_ascii=False, indent=1)
