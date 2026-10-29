"""Narra cada frase separadamente e grava o áudio contínuo + tempos (frases e parágrafos)."""
import sys, glob, os, re, json, numpy as np, soundfile as sf
from kokoro_onnx import Kokoro

model, voices, src, out, voice, speed = sys.argv[1:7]
k = Kokoro(model, voices)
SR = 24000
GAP_S, GAP_P, GAP_SEC = 0.22, 0.45, 0.8
PRON = {'hesed': 'réssed'}  # grafia só para a voz; a legenda mantém o texto original
pieces, t, timeline = [], 0.0, []

def add(a):
    global t
    pieces.append(a.astype(np.float32)); t += len(a) / SR

for f in sorted(glob.glob(os.path.join(src, "*.txt"))):
    sec = os.path.basename(f)[:-4]
    paras = [p.strip() for p in open(f, encoding="utf-8").read().split("\n") if p.strip()]
    lento = 'oracao' in sec  # oração: pausas mais longas entre frases
    gs, gp = (0.65, 1.3) if lento else (GAP_S, GAP_P)
    for pi, para in enumerate(paras):
        frases = [s for s in re.split(r"(?<=[.!?:])\s+", para) if s]
        p_start = t
        for fr in frases:
            fala = fr
            for a0, b0 in PRON.items(): fala = re.sub(rf'\b{a0}\b', b0, fala)
            a, sr = k.create(fala, voice=voice, speed=float(speed), lang="pt-br")
            st = t; add(a)
            timeline.append({"sec": sec, "para": pi, "start": round(st, 3), "end": round(t, 3), "text": fr})
            add(np.zeros(int(SR * gs)))
        add(np.zeros(int(SR * (gp - gs))))
    add(np.zeros(int(SR * GAP_SEC)))

sf.write(os.path.join(out, "narracao.wav"), np.concatenate(pieces), SR)
json.dump(timeline, open(os.path.join(out, "tempos.json"), "w"), ensure_ascii=False, indent=1)

def ts(x):
    h, r = divmod(x, 3600); m, s = divmod(r, 60)
    return f"{int(h):02d}:{int(m):02d}:{int(s):02d},{int((s % 1) * 1000):03d}"

with open(os.path.join(out, "legendas.srt"), "w", encoding="utf-8") as fh:
    for i, e in enumerate(timeline, 1):
        fh.write(f"{i}\n{ts(e['start'])} --> {ts(e['end'] + 0.15)}\n{e['text']}\n\n")
print("duração total", round(t, 1), "s;", len(timeline), "frases")
