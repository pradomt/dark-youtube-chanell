#!/usr/bin/env python3
"""capitulos.py - capítulos do YouTube a partir da transcrição, já validados.

    python3 capitulos.py tempos.json                 # tempos do nosso pipeline (usa as seções do roteiro)
    python3 capitulos.py legendas.srt --alvo 8       # .srt, .vtt ou .json do Whisper
    python3 capitulos.py --validar descricao-youtube.txt
    python3 capitulos.py legendas.srt --json

Regras do YouTube, checadas aqui em vez de presumidas: a lista começa em 00:00, tem pelo menos três
capítulos, cada um com pelo menos 10 segundos, em ordem crescente. Um bloco que quebra qualquer
uma delas simplesmente não vira capítulo, e o YouTube não avisa.

Adaptado de youtube-agent-skill (Jake Schincariol, licença MIT) para português.
"""
import json, os, re, sys

MIN = 10.0
STOP = set("""a o as os um uma uns umas de da do das dos em na no nas nos por para pra pelo pela com
sem sob e ou mas que se como quando onde porque porquê por que qual quais quem isso isto esse essa
este esta aquele aquela ele ela eles elas eu você vocês nós seu sua seus suas meu minha nosso nossa
lhe já não sim mais menos muito muita muitos muitas tem têm ter tinha foi era são ser está estão
estava há aqui ali lá então também só até sobre entre depois antes ainda cada todo toda todos todas
mesmo mesma outro outra outros outras vai vou fica ficou isso aí esses essas estes estas""".split())

def parse_ts(s):
    s = s.strip().replace(",", ".")
    p = s.split(":")
    return int(p[0]) * 3600 + int(p[1]) * 60 + float(p[2]) if len(p) == 3 else int(p[0]) * 60 + float(p[1])

def load(path):
    """Devolve [(início, fim, texto, seção)]. seção só vem do tempos.json do nosso pipeline."""
    raw = open(path, encoding="utf-8", errors="replace").read()
    if path.endswith(".json"):
        d = json.loads(raw)
        segs = d.get("segments", []) if isinstance(d, dict) else d
        return [(float(s["start"]), float(s["end"]), (s.get("text") or "").strip(), s.get("sec"))
                for s in segs]
    cues, cur = [], None
    for line in raw.splitlines():
        m = re.match(r"\s*(\d[\d:.,]+)\s*-->\s*(\d[\d:.,]+)", line)
        if m:
            cur = [parse_ts(m.group(1)), parse_ts(m.group(2)), []]
            cues.append(cur)
        elif cur is not None and line.strip() and not line.strip().isdigit():
            cur[2].append(line.strip())
    return [(a, b, " ".join(t), None) for a, b, t in cues if t]

def keywords(text):
    return {w for w in re.findall(r"[a-zà-ü']{4,}", text.lower()) if w not in STOP}

def mmss(t):
    t = int(t); h, m, s = t // 3600, (t % 3600) // 60, t % 60
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"

def validate(chs, dur=None):
    """chs = [(segundos, título)]. Devolve a lista de problemas (vazia = válido)."""
    errs = []
    if len(chs) < 3: errs.append(f"só {len(chs)} capítulos; o YouTube exige pelo menos 3")
    if not chs or chs[0][0] != 0: errs.append("o primeiro capítulo precisa ser 00:00")
    for i, (t, title) in enumerate(chs):
        end = chs[i + 1][0] if i + 1 < len(chs) else dur
        if i and t <= chs[i - 1][0]: errs.append(f"{mmss(t)} fora de ordem")
        if end is not None and end - t < MIN:
            errs.append(f"{mmss(t)} \"{title}\" tem {end - t:.0f}s; o mínimo é {MIN:.0f}s")
        if not title.strip(): errs.append(f"{mmss(t)} sem título")
    return errs

def from_sections(cues):
    out, last = [], None
    for s, _, _, sec in cues:
        if sec != last:
            name = re.sub(r"^\d+[-_ ]*", "", sec or "").replace("-", " ").strip().capitalize()
            out.append((0.0 if not out else s, name or "Seção"))
            last = sec
    return out

def from_pauses(cues, target):
    dur = cues[-1][1]
    cand = []
    for i in range(1, len(cues)):
        gap = cues[i][0] - cues[i - 1][1]
        kb = keywords(" ".join(c[2] for c in cues[max(0, i - 12):i]))
        ka = keywords(" ".join(c[2] for c in cues[i:i + 12]))
        shift = 1 - (len(kb & ka) / len(kb | ka)) if (kb | ka) else 0
        cand.append((gap * 1.6 + shift * 3.2, cues[i][0]))
    cand.sort(reverse=True)
    picked = [0.0]
    for _, t in cand:
        if len(picked) >= target: break
        if all(abs(t - p) >= MIN for p in picked) and dur - t >= MIN: picked.append(t)
    picked.sort()
    out = []
    for n, t in enumerate(picked):
        end = picked[n + 1] if n + 1 < len(picked) else dur
        text = " ".join(c[2] for c in cues if c[0] >= t and c[1] <= end)
        kw = sorted(keywords(text), key=lambda w: -text.lower().count(w))
        out.append((t, " ".join(w.capitalize() for w in kw[:3]) or "Seção"))
    return out

def read_block(path):
    chs = []
    for line in open(path, encoding="utf-8", errors="replace"):
        m = re.match(r"\s*((?:\d+:)?\d{1,2}:\d{2})\s+[-–—]?\s*(.+)", line)
        if m: chs.append((parse_ts(m.group(1)), m.group(2).strip()))
    return chs

def main():
    a = sys.argv[1:]
    as_json = "--json" in a; a = [x for x in a if x != "--json"]
    if "--validar" in a:
        path = a[a.index("--validar") + 1]
        chs = read_block(path)
        errs = validate(chs)
        for t, title in chs: print(f"  {mmss(t)} {title}")
        print("\n  " + ("VÁLIDO: o YouTube vai mostrar esses capítulos." if not errs else "INVÁLIDO:"))
        for e in errs: print(f"    x  {e}")
        print(); sys.exit(1 if errs else 0)
    target = int(a[a.index("--alvo") + 1]) if "--alvo" in a else 7
    a = [x for x in a if not x.startswith("--") and not x.isdigit()]
    if not a or not os.path.exists(a[0]): print(__doc__); sys.exit(1)
    cues = load(a[0])
    if len(cues) < 6: print("poucas falas para dividir em capítulos"); sys.exit(1)
    dur = cues[-1][1]
    by_sec = all(c[3] for c in cues)
    chs = from_sections(cues) if by_sec else from_pauses(cues, target)
    errs = validate(chs, dur)
    if as_json:
        print(json.dumps({"valido": not errs, "problemas": errs,
                          "capitulos": [{"inicio": round(t, 2), "rotulo": mmss(t), "titulo": ti}
                                        for t, ti in chs]}, ensure_ascii=False, indent=1)); return
    print()
    for t, title in chs: print(f"{mmss(t)} {title}")
    print(f"\n  {len(chs)} capítulos, {'a partir das seções do roteiro' if by_sec else 'a partir das pausas'}")
    print("  " + ("válido pelas regras do YouTube" if not errs else "INVÁLIDO: " + "; ".join(errs)))
    print("  Reescreva cada título como a promessa do trecho, em 3 a 5 palavras.\n")

if __name__ == "__main__":
    main()
