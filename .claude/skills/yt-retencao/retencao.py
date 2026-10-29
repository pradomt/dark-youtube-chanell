#!/usr/bin/env python3
"""retencao.py - lê a exportação de retenção do YouTube Studio e mostra onde o público sai.

    python3 retencao.py retencao.csv --transcricao tempos.json   # diz o que a narração falava em cada queda
    python3 retencao.py retencao.csv --duracao 305
    python3 retencao.py retencao.csv --json

O arquivo vem do Studio: um vídeo -> Análise -> Engajamento -> gráfico "Retenção de público" ->
ícone de download. Duas colunas: posição no vídeo (% ou tempo) e % do público que ainda assiste.
Aceita vírgula decimal ("45,3%"), frações (0,453) e tempos "1:23".

Três problemas diferentes, com três correções diferentes:
  GANCHO      quanto se perdeu nos primeiros 30 segundos
  QUEDAS      descidas bruscas: um momento específico em que o público saiu
  DESLIZE     a perda contínua no meio do vídeo

Adaptado de youtube-agent-skill (Jake Schincariol, licença MIT) para português.
"""
import csv, json, os, re, sys

def num(c):
    c = c.strip().replace("%", "").replace(" ", "").replace(" ", "")
    if not c: return None
    if re.fullmatch(r"\d+(:\d{1,2}){1,2}(\.\d+)?", c):
        p = [float(x) for x in c.split(":")]
        return p[0] * 60 + p[1] if len(p) == 2 else p[0] * 3600 + p[1] * 60 + p[2]
    if "," in c and "." in c:  # o separador que vem por último é o decimal
        c = c.replace(".", "").replace(",", ".") if c.rfind(",") > c.rfind(".") else c.replace(",", "")
    else:
        c = c.replace(",", ".")
    try: return float(c)
    except ValueError: return None

def load_csv(path):
    raw = open(path, encoding="utf-8-sig", errors="replace").read()
    delim = ";" if raw.count(";") > raw.count(",") / 2 and ";" in raw else ","
    rows = []
    for r in csv.reader(raw.splitlines(), delimiter=delim):
        vals = [v for v in (num(c) for c in r) if v is not None]
        if len(vals) >= 2: rows.append((vals[0], vals[1]))
    if rows and max(y for _, y in rows) <= 1.5:  # retenção em fração (0-1)
        rows = [(x, y * 100) for x, y in rows]
    if rows and max(x for x, _ in rows) <= 1.0:  # posição em fração (0-1)
        rows = [(x * 100, y) for x, y in rows]
    return rows

def load_cues(path):
    if path.endswith(".json"):
        d = json.load(open(path, encoding="utf-8"))
        segs = d.get("segments", []) if isinstance(d, dict) else d
        return [(float(s["start"]), float(s["end"]), (s.get("text") or "").strip()) for s in segs]
    cues, cur = [], None
    for line in open(path, encoding="utf-8", errors="replace").read().splitlines():
        m = re.match(r"\s*(\d[\d:.,]+)\s*-->\s*(\d[\d:.,]+)", line)
        if m:
            cur = [num(m.group(1).replace(",", ".")), num(m.group(2).replace(",", ".")), []]
            cues.append(cur)
        elif cur is not None and line.strip() and not line.strip().isdigit():
            cur[2].append(line.strip())
    return [(a, b, " ".join(t)) for a, b, t in cues if t]

def mmss(t): t = int(round(t)); return f"{t // 60}:{t % 60:02d}"

def main():
    a = sys.argv[1:]
    as_json = "--json" in a; a = [x for x in a if x != "--json"]
    tr = a[a.index("--transcricao") + 1] if "--transcricao" in a else None
    dur = float(a[a.index("--duracao") + 1].replace(",", ".")) if "--duracao" in a else None
    files = [x for x in a if not x.startswith("--") and x not in (tr,) and not re.fullmatch(r"[\d.,]+", x)]
    if not files or not os.path.exists(files[0]): print(__doc__); sys.exit(1)
    rows = load_csv(files[0])
    if len(rows) < 8: print("não consegui ler pelo menos 8 pontos desse CSV"); sys.exit(1)
    cues = load_cues(tr) if tr and os.path.exists(tr) else []
    if cues and not dur: dur = cues[-1][1]
    xs = [r[0] for r in rows]; ys = [r[1] for r in rows]
    pct_axis = max(xs) <= 100.5
    def sec(x): return (x / 100.0 * dur) if pct_axis and dur else (None if pct_axis else x)
    start = ys[0] or 100.0
    cutoff = 30.0 if not pct_axis else (30.0 / dur * 100 if dur else 10.0)
    hook_end = min((y for x, y in rows if x <= cutoff), default=start)
    hook_leak = start - hook_end
    drops = []
    for i in range(1, len(rows)):
        d = ys[i - 1] - ys[i]
        drops.append((d / (xs[i] - xs[i - 1] or 1), xs[i - 1], xs[i], d))
    mid = [r[0] for r in drops if r[1] > cutoff]
    slide = sum(mid) / len(mid) if mid else 0
    drops.sort(reverse=True)
    cliffs = []
    for _, x0, x1, d in [r for r in drops if r[1] >= cutoff and r[3] > 0.8][:5]:  # a abertura já está no GANCHO
        t = sec(x0)
        said = " ".join(c[2] for c in cues if t is not None and c[0] <= t + 4 and c[1] >= t - 4)[:160]
        cliffs.append({"de": round(x0, 2), "ate": round(x1, 2), "perda": round(d, 2),
                       "segundo": round(t, 1) if t is not None else None, "falando": said})
    cliffs.sort(key=lambda c: c["de"])
    out = {"pontos": len(rows), "inicio": start, "fim": ys[-1], "gancho": round(hook_leak, 2),
           "quedas": cliffs, "deslize": round(slide, 3), "unidade": "% do vídeo" if pct_axis else "segundo"}
    if as_json: print(json.dumps(out, ensure_ascii=False, indent=1)); return
    print(f"\n  {files[0]}   {len(rows)} pontos   {ys[0]:.1f}% -> {ys[-1]:.1f}%\n")
    verdict = "saudável" if hook_leak < 25 else "vazando" if hook_leak < 40 else "grave"
    print(f"  GANCHO      {hook_leak:.1f} pontos perdidos na abertura   [{verdict}]")
    print( "              abaixo de 25 é saudável. Se vazar, mexa na primeira frase antes de tudo.\n")
    print( "  QUEDAS      os momentos em que o público saiu")
    for c in cliffs:
        where = mmss(c["segundo"]) if c["segundo"] is not None else f"{c['de']}%"
        print(f"    -{c['perda']:5.1f}  em {where:>6}" + (f'   "{c["falando"]}"' if c["falando"] else ""))
    if not cliffs: print("    nenhuma acima de 0,8 ponto depois da abertura: a perda é deslize, não momentos")
    if pct_axis and not dur: print("    (passe --duracao ou --transcricao para ver o segundo exato)")
    print(f"\n  DESLIZE     {slide:.3f} ponto por {out['unidade']} no meio do vídeo")
    print( "              deslize alto é ritmo, não assunto. Corte o meio, não reescreva.\n")

if __name__ == "__main__":
    main()
