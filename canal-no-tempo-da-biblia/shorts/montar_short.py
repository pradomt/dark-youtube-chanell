"""Monta o roteiro.json de um Short (template palco único) a partir de uma especificação por frase e do tempos.json.
Uso: python montar_short.py spec.py tempos.json narracao.mp3 saida.json"""
import json, sys, runpy
S = runpy.run_path(sys.argv[1]); T = json.load(open(sys.argv[2]))
ini = lambda f: T[min(f, len(T) - 1)]['start']
ch = ini(S['CHAMADA'])
R = dict(tema=S.get('TEMA', 'papel'), marca=S['MARCA'], audio=sys.argv[3], decoracao='biblia', acento=S.get('ACENTO'), aviso=S.get('AVISO', ''), batidas=[])
B = S['B']
for i, (f, apoio, tit) in enumerate(B):
    a = ini(f); b = ini(B[i + 1][0]) - 0.05 if i + 1 < len(B) else 99
    pcs = tit.split('|'); dur = (T[f]['end'] - a)
    R['batidas'].append(dict(b=round(b, 2), apoio=[round(max(0.3, a - .1), 2), apoio],
        titulo=[[round(max(0.5, a + .15 + k * min(.55, dur / (len(pcs) + 1))), 2), w.strip()] for k, w in enumerate(pcs)]))
C = S['CARTAO']
tl = lambda lst: [[round(ini(f) - .1 if f else 0, 2), x] for f, x in lst]
pa = []
for p in C['paineis']:
    p = dict(p); fa, fb = p.pop('fa'), p.pop('fb', None)
    p['a'] = round(max(0.7, ini(fa) - .2), 2) if fa else 0; p['b'] = round(ini(fb) - .1, 2) if fb is not None else 99
    if 'contaf' in p: f0, d = p.pop('contaf'); p['conta'] = [ini(f0) + .2, ini(f0) + .2 + d]
    if 'svgf' in p:
        svg = open(p.pop('svgf')).read()
        for k, f in p.pop('passos').items(): svg = svg.replace(f'data-t="{k}"', f'data-t="{round(ini(f), 2)}"')
        p['svg'] = svg
    pa.append(p)
R['cartao'] = dict(a=0.7, b=round(ch - .05, 2), arquivo=tl(C['arquivo']), etiqueta=tl(C['etiqueta']), rotulo=tl(C['rotulo']), paineis=pa,
                   diario=[[round(ini(f) + .3, 2), x] + ([round(ini(e), 2)] if e else []) for f, x, e in [(list(d) + [None])[:3] for d in C.get('diario', [])]])
R['chamada'] = dict(a=round(ch, 2), pilulas=S['PILULAS'], seta=True)
json.dump(R, open(sys.argv[4], 'w'), ensure_ascii=False, indent=1)
print(sys.argv[1], len(R['batidas']), 'batidas')
