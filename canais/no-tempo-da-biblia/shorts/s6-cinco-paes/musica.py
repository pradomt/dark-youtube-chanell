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

CORTE = T[7]['end'] + .15; VIRA = F[8] - .05
m = np.zeros(n)
# parte 1 (o problema): lá menor -> fá -> ré menor -> mi, acordes longos
p1 = [(33, [45, 52, 57, 60]), (29, [41, 48, 57, 60]), (26, [38, 50, 53, 57]), (28, [40, 47, 56, 59])]
cs = [0, F[2] - .5, F[4] - .5, F[6] - .5, CORTE]
for (b, ac), a, z in zip(p1, cs, cs[1:]): m += pad([b + 12] + ac, max(0, a - .6), z + (.6 if z != CORTE else .02), .1, 2.2 if a == 0 else 1.6, 1.4 if z != CORTE else .03)
m += subida(CORTE - 2.6, CORTE)
# parte 2 (a virada): dó maior -> fá -> lá menor -> sol -> dó, mais aberto
p2 = [[36, 48, 55, 60, 64], [41, 48, 57, 60, 65], [45, 52, 57, 60, 64], [43, 50, 55, 59, 62], [36, 48, 55, 60, 64, 67]]
cs2 = [VIRA, F[10] - .5, F[12] - .5, F[14] - .5, F[16] - .3, DUR]
for ac, a, z in zip(p2, cs2, cs2[1:]): m += pad(ac, a - (0 if a == VIRA else .6), z + .6 if z != DUR else DUR, .1 if z != DUR else .12, .4 if a == VIRA else 1.6, 1.4 if z != DUR else 3.5)
m += baque(VIRA)
# sinos quando um número aterrissa (como no Reel)
for f, d in [(1, .9), (2, 1.5), (3, 1.0), (5, .4), (6, 2.0), (8, 1.0), (11, .3), (13, 1.6), (16, .1)]: m += sino(F[f] + d, vol=.045)
m += sino(F[16] + .1, f=1950, vol=.06, dec=3); m += sino(F[16] + .1, f=2930, vol=.035, dec=3)
# passa-baixa suave e estéreo leve
k = np.ones(9) / 9; m = np.convolve(m, k, 'same')
st = np.stack([m, np.roll(m, int(.011 * SR))], 1); st /= np.abs(st).max() * 1.12
sf.write('trilha.wav', st.astype(np.float32), SR); print('trilha', round(DUR, 1), 's; corte', round(CORTE, 2), '-> virada', round(VIRA, 2))
