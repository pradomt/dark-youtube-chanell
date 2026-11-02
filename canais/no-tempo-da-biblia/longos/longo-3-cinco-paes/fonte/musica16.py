"""Trilha original (sem direitos de terceiros) no estilo do Reel de referência:
pad grave e contínuo, sinos agudos curtos quando um número aparece, corte seco antes da virada e acorde maior depois."""
import json, numpy as np, soundfile as sf
SR = 48000; T = json.load(open('tempos.json')); F = [e['start'] for e in T]
DUR = sf.info('narracao.wav').duration; n = int(DUR * SR); t = np.arange(n) / SR
rng = np.random.default_rng(3)
hz = lambda m: 440 * 2 ** ((m - 69) / 12)
def env(a, b, ataque=1.5, solta=2.0):
    e = np.clip((t - a) / ataque, 0, 1) * np.clip((b - t) / solta, 0, 1); return e * e * (3 - 2 * e)
def pad(notas, a, b, vol=.1, at=1.8, so=2.2):
    out = np.zeros(n); e = env(a, b, at, so); m = e > 0
    for k, nt in enumerate(notas):
        f = hz(nt)
        for d in (-.12, .12):  # dois osciladores levemente desafinados = coro
            ph = rng.uniform(0, 6.28); fd = f * 2 ** (d / 12 / 4)
            x = np.sin(2 * np.pi * fd * t[m] + ph) + .25 * np.sin(4 * np.pi * fd * t[m] + ph) + .08 * np.sin(6 * np.pi * fd * t[m])
            out[m] += x * (1 + .15 * np.sin(2 * np.pi * (.07 + .03 * k) * t[m])) * (.8 if nt < 50 else .45)
    return out * e * vol
def sino(t0, f=3900, vol=.05, dec=1.4):
    out = np.zeros(n); i0 = int(t0 * SR); L = min(n - i0, int(SR * 4)); tt = np.arange(L) / SR
    x = sum(a * np.sin(2 * np.pi * f * r * tt) * np.exp(-tt / (dec / r ** .6)) for r, a in ((1, 1), (2.01, .35), (2.76, .2), (.5, .25)))
    out[i0:i0 + L] = x * vol * np.clip(tt / .004, 0, 1); return out
def subida(t0, t1, vol=.06):  # ruído filtrado que cresce até o corte
    out = np.zeros(n); m = (t > t0) & (t < t1); x = rng.standard_normal(m.sum())
    x = np.convolve(x, np.ones(24) / 24, 'same'); out[m] = x * ((t[m] - t0) / (t1 - t0)) ** 2.5 * vol * 6; return out
def baque(t0, vol=.35):
    out = np.zeros(n); i0 = int(t0 * SR); L = int(SR * 2.5); tt = np.arange(L) / SR
    f = 55 * np.exp(-tt * 1.5) + 38; out[i0:i0 + L] = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 1.8) * vol; return out


IT = json.load(open('itens.json')); sec = [x['sec'] for x in IT]
ini = {}; [ini.setdefault(s_, k) for k, s_ in enumerate(sec)]
m = np.zeros(n)
MENOR = [[45, 52, 57, 60], [41, 48, 57, 60], [38, 50, 53, 57], [40, 47, 56, 59]]
MAIOR = [[36, 48, 55, 60, 64], [41, 48, 57, 60, 65], [45, 52, 57, 60, 64], [43, 50, 55, 59, 62]]
# acordes trocam a cada parágrafo; seções 0 a 4 em menor (o problema), 5 em diante em maior (o milagre)
VIRA = F[ini[5]] - .05; CORTE = T[ini[5] - 1]['end'] + .15
k = 0
for p in range(len(F)):
    a = F[p] - (.6 if p else 0.0); z = F[p + 1] if p + 1 < len(F) else DUR
    if p == ini[5] - 1: z = CORTE
    ac = (MENOR if sec[p] < 5 else MAIOR)[k % 4]; k += 1
    if sec[p] >= 5 and p == ini[5]: k = 0
    m += pad(([ac[0] + 12] + ac) if sec[p] < 5 else ac, max(0, a), z + (.6 if z not in (CORTE, DUR) else .02), .09 if z != DUR else .11, 1.6 if a > 0 else 2.2, 1.4 if z not in (CORTE, DUR) else (.03 if z == CORTE else 3.5))
m += subida(CORTE - 2.6, CORTE); m += baque(VIRA)
# sinos: números e capítulos
for p, d in [(1, 1.0), (9, .9), (10, 1.5), (13, 1.0), (16, 2.5), (28, 4.0), (29, 2.0), (31, 1.0), (32, 1.2), (36, 3.0), (40, 1.0)]: m += sino(F[p] + d, vol=.04)
for s_ in range(1, 9): m += sino(F[ini[s_]] - 1.4, f=1950, vol=.035, dec=2.2)
m += sino(F[45] + (T[45]['end'] - F[45]) * .8, f=1950, vol=.06, dec=3); m += sino(F[45] + (T[45]['end'] - F[45]) * .8, f=2930, vol=.035, dec=3)
kf = np.ones(9) / 9; m = np.convolve(m, kf, 'same')
st = np.stack([m, np.roll(m, int(.011 * SR))], 1); st /= np.abs(st).max() * 1.12
sf.write('trilha.wav', st.astype(np.float32), SR); print('trilha', round(DUR, 1), 's; virada', round(VIRA, 1))
