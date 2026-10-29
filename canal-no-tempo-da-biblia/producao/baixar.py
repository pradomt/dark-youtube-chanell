import json, sys, urllib.request, os, time, re, glob
UA = {"User-Agent": "CanalDarkResearch/1.0 (contact: project owner) python-urllib"}
idx = {}
for f in glob.glob('/tmp/w/busca*.json'):
    for q, l in json.load(open(f)).items():
        for x in l: idx[x['title']] = x
man = json.load(open('img/creditos.json')) if os.path.exists('img/creditos.json') else {}
for line in open(sys.argv[1]):
    if not line.strip(): continue
    nome, sub = [s.strip() for s in line.split('=', 1)]
    cand = [x for t, x in idx.items() if sub in t]
    if not cand: print('NAO ACHEI', sub); continue
    x = cand[0]; dst = f'img/{nome}.jpg'
    if not os.path.exists(dst):
        for k in range(6):
            try:
                import subprocess, hashlib, urllib.parse as up
                fn = x['title'][5:].replace(' ', '_'); h = hashlib.md5(fn.encode()).hexdigest()
                w = 1920 if x['w'] >= 1920 else 1280 if x['w'] >= 1280 else 960
                ext = '.jpg' if fn.lower().endswith(('.tif', '.tiff')) else ''
                pre = 'lossy-page1-' if ext else ''
                u = f"https://upload.wikimedia.org/wikipedia/commons/thumb/{h[0]}/{h[:2]}/{up.quote(fn)}/{pre}{w}px-{up.quote(fn)}{ext}"
                r = subprocess.run(['curl', '-sf', '-A', 'CanalDarkResearch/1.0', '-o', dst, u]); assert r.returncode == 0, r.returncode; break
            except Exception as e: print('erro', e); time.sleep(8 * (k + 1))
        time.sleep(4)
    art = re.sub(r'\s+', ' ', x['artist']).strip()[:60]
    man[nome] = dict(arquivo=x['title'], autor=art, licenca=x['lic'], pagina=x['page'])
    print(nome, '|', art, '|', x['lic'])
json.dump(man, open('img/creditos.json', 'w'), ensure_ascii=False, indent=1)
