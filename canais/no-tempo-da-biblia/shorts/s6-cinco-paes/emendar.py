import sys, json, numpy as np, soundfile as sf
i, f = int(sys.argv[1]), sys.argv[2]
y, SR = sf.read('narracao.wav'); a, sr2 = sf.read(f); assert sr2 == SR; T = json.load(open('tempos.json'))
nz = np.where(np.abs(a) > 0.01)[0]; a = a[max(0, nz[0] - int(.03 * SR)): nz[-1] + int(.08 * SR)]
s, e = int(T[i]['start'] * SR), int(T[i]['end'] * SR); d = (len(a) - (e - s)) / SR
y = np.concatenate([y[:s], a, y[e:]]); T[i]['end'] = round(T[i]['start'] + len(a) / SR, 3)
for x in T[i + 1:]: x['start'] = round(x['start'] + d, 3); x['end'] = round(x['end'] + d, 3)
sf.write('narracao.wav', y, SR); json.dump(T, open('tempos.json', 'w'), ensure_ascii=False, indent=1)
ts = lambda x: f"00:{int(x // 60):02d}:{int(x % 60):02d},{int((x % 1) * 1000):03d}"
with open('legendas.srt', 'w', encoding='utf-8') as fh:
    for k, x in enumerate(T, 1): fh.write(f"{k}\n{ts(x['start'])} --> {ts(x['end'] + .15)}\n{x['text']}\n\n")
print('emendado', i, round(d, 2))
