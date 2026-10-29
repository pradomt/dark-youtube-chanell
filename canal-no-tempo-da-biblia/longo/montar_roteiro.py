"""Monta o roteiro.json do vídeo longo a partir do plano visual (plano_*.py) e dos tempos da narração.
Uso: python montar_roteiro.py plano_x.py tempos.json narracao.mp3 saida.json
Plano: CAP = {secao: (numero, titulo, subtitulo)}; P = lista de dicts por parágrafo:
  s (seção), p (parágrafo), apoio, titulo (com *destaque*), cena (dict opcional: arquivo, etiqueta, rotulo, painel, f = frase onde entra),
  d = [(frase, texto)] para o diário. Frases são índices dentro do parágrafo; 'fim' em painel numero/lista usa frases também."""
import json, sys, runpy
plano = runpy.run_path(sys.argv[1]); T = json.load(open(sys.argv[2]))
par = {}
for e in T: par.setdefault((e['sec'], e['para']), []).append(e)
chaves = list(par)
def ini(s, p, f=0): fr = par[(s, p)]; return fr[min(f, len(fr) - 1)]['start']
def fim(s, p): return par[(s, p)][-1]['end']
R = {k: plano.get(k.upper(), d) for k, d in [('tema', 'papel'), ('marca', ''), ('acento', None), ('decoracao', 'biblia'), ('aviso', '')]}
R.update(audio=sys.argv[3], batidas=[], cenas=[], diario=[], capitulos=[])
CAP_DUR = 2.6
secs = []
for s, p in chaves:
    if s not in secs: secs.append(s)
for s in secs:
    if s in plano['CAP']:
        n, t, sub = plano['CAP'][s]; a = ini(s, 0)
        R['capitulos'].append(dict(n=n, t=t, s=sub, a=max(0.2, a - 0.3), b=a + CAP_DUR))
P = plano['P']
for i, x in enumerate(P):
    s, p = x['s'], x['p']; a = ini(s, p)
    if s in plano['CAP'] and p == 0: a = ini(s, 0) + CAP_DUR + 0.3
    nxt = P[i + 1] if i + 1 < len(P) else None
    b = (ini(nxt['s'], nxt['p']) - 0.15) if nxt else fim(s, p) + 1.5
    if nxt and nxt['s'] in plano['CAP'] and nxt['p'] == 0: b = ini(nxt['s'], 0) - 0.35
    pedacos = [w for w in x['titulo'].split('|')]
    R['batidas'].append(dict(b=round(b, 2), apoio=[round(a, 2), x.get('apoio', '')], titulo=[[round(a + .35 + .35 * k, 2), w.strip()] for k, w in enumerate(pedacos)]))
    for c in x.get('cenas', [x['cena']] if 'cena' in x else []):
        c = dict(c); f0 = c.pop('f', 0); ac = ini(s, p, f0)
        if s in plano['CAP'] and p == 0 and f0 == 0: ac = max(ac, ini(s, 0) + CAP_DUR)
        pn = c['painel']
        for it in pn.get('itens', []): it['t'] = round(max(ac, ini(s, p, it.pop('f', 0))) + 0.2 + it.pop('dt', 0), 2)
        if 'contaf' in pn: f0, f1 = pn.pop('contaf'); c0 = max(ac + .3, ini(s, p, f0)); pn['conta'] = [c0, c0 + f1]
        if pn['tipo'] == 'svg' and 'arquivo_svg' in pn:
            svg = open(pn.pop('arquivo_svg')).read()
            for k, f in pn.pop('passos_f', {}).items(): svg = svg.replace(f'data-t="{k}"', f'data-t="{round(ini(s, p, f), 2)}"')
            pn['svg'] = svg; pn['passos'] = True
        if pn['tipo'] == 'lista' and pn['itens'] and min(it['t'] for it in pn['itens']) > ac + 1.5:
            ac = min(it['t'] for it in pn['itens']) - 0.5   # lista entra junto do 1º item, sem cartão vazio
        c['a'] = round(ac, 2); R['cenas'].append(c)
    for f, txt in x.get('d', []): R['diario'].append([round(ini(s, p, f) + 0.3, 2), txt])
if plano.get('FIM_CARTAO'): R['cartaoB'] = plano['FIM_CARTAO'](ini)
json.dump(R, open(sys.argv[4], 'w'), ensure_ascii=False, indent=1)
print(len(R['batidas']), 'batidas,', len(R['cenas']), 'cenas,', len(R['capitulos']), 'capítulos')
