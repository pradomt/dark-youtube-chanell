"""Narra uma frase por linha (formato 'pausa_antes|texto') e grava narracao.wav + tempos.json + legendas.srt."""
import sys, json, numpy as np, soundfile as sf
from kokoro_onnx import Kokoro
model, voices, txt, voice, speed = sys.argv[1:6]
k = Kokoro(model, voices); SR = 24000; parts = []; t = 0.0; T = []
def add(a):
    global t; parts.append(a.astype(np.float32)); t += len(a) / SR
add(np.zeros(int(SR * .35)))
for ln in open(txt, encoding='utf-8'):
    if not ln.strip(): continue
    gap, fr = ln.rstrip('\n').split('|', 1)
    add(np.zeros(int(SR * float(gap))))
    a, _ = k.create(fr, voice=voice, speed=float(speed), lang='pt-br')
    # corta silêncio que o Kokoro deixa nas pontas
    nz = np.where(np.abs(a) > 0.01)[0]; a = a[max(0, nz[0] - 600): nz[-1] + 1800]
    st = t; add(a); T.append({'start': round(st, 3), 'end': round(t, 3), 'text': fr})
add(np.zeros(int(SR * 4.5)))  # cauda para a chamada final
sf.write('narracao.wav', np.concatenate(parts), SR)
json.dump(T, open('tempos.json', 'w'), ensure_ascii=False, indent=1)
ts = lambda x: f"00:{int(x // 60):02d}:{int(x % 60):02d},{int((x % 1) * 1000):03d}"
with open('legendas.srt', 'w', encoding='utf-8') as f:
    for i, e in enumerate(T, 1): f.write(f"{i}\n{ts(e['start'])} --> {ts(e['end'] + .15)}\n{e['text']}\n\n")
w = sum(len(e['text'].split()) for e in T); fala = sum(e['end'] - e['start'] for e in T)
print('duração', round(t, 1), 's | palavras/min na fala', round(w / fala * 60))
for e in T: print(e['start'], e['end'], e['text'])
