#!/usr/bin/env python3
"""titulo.py - confere o par título + texto da thumbnail antes de publicar.

    python3 titulo.py --titulo "A bandeira do Brasil mostra um céu que ninguém viu" --thumb "CÉU ESPELHADO"
    python3 titulo.py titulos.txt --thumb "CÉU ESPELHADO"     # um título por linha, em ranking
    python3 titulo.py --titulo "..." --json

O par é a unidade, não o título. Uma thumbnail que repete o título desperdiça metade da área de
clique, e esse é o erro mais comum que este script pega.

Tamanho: o YouTube corta perto de 60 caracteres na busca do computador e perto de 40 no feed do
celular. Os dois aparecem porque são falhas diferentes: no computador some o fim, no celular pode
sumir o assunto.

Adaptado de youtube-agent-skill (Jake Schincariol, licença MIT) para português.
"""
import json, os, re, sys, unicodedata

DESKTOP, MOBILE, HARD = 60, 40, 100
VAGUE = {"incrivel","inacreditavel","chocante","insano","surreal","absurdo","bizarro","epico",
         "perfeito","segredo","segredos","melhor","impressionante","assustador","bombastico",
         "revelado","verdade","tudo","definitivo","louco","inexplicavel","misterioso"}
STOP = {"a","o","as","os","um","uma","de","da","do","das","dos","em","na","no","nas","nos","e","ou",
        "que","por","para","pra","com","se","seu","sua","voce","isso","esse","essa","como","qual",
        "quem","por","porque","nao","ja","mais","so","e"}

def fold(w): return unicodedata.normalize("NFKD", w).encode("ascii", "ignore").decode()
def words(t): return [fold(w) for w in re.findall(r"[0-9a-zà-ü']+", t.lower())]
def stem(w): return w[:-1] if len(w) > 4 and w.endswith("s") else w

def check(title, thumb=None):
    t = title.strip()
    n = len(t)
    issues, good = [], []
    if n > HARD: issues.append(("tamanho", f"{n} caracteres; o limite do YouTube é {HARD}"))
    elif n > DESKTOP: issues.append(("tamanho", f"{n} caracteres; a busca no computador corta perto de {DESKTOP}"))
    else: good.append(f"{n} caracteres, dentro do corte de {DESKTOP}")
    if n > MOBILE:
        head = t[:MOBILE].rsplit(" ", 1)[0]
        issues.append(("celular", f'no feed do celular aparece só "{head}..."; o assunto sobrevive?'))
    caps = [w for w in t.split() if len(w) > 2 and w.isupper()]
    if len(caps) > 2: issues.append(("gritando", f"{len(caps)} palavras em maiúsculas; mais de duas parece spam"))
    v = sorted({w for w in words(t) if w in VAGUE})
    if v: issues.append(("vago", f"{', '.join(v)}: troque por um número, um nome ou uma data"))
    nums = re.findall(r"\d[\d.,]*%?", t)
    names = [w for w in t.split()[1:] if w[:1].isupper() and not w.isupper()]
    if nums: good.append(f"tem número ou data ({', '.join(nums[:3])})")
    if names: good.append(f"tem nome próprio ({', '.join(names[:3])})")
    if not nums and not names: issues.append(("concreto", "sem número, data ou nome próprio; é a correção mais confiável"))
    if t.endswith("?"): good.append("pergunta aberta no título")
    if not [w for w in words(t)[:3] if w not in STOP]:
        issues.append(("começo", "as três primeiras palavras são vazias; traga o assunto para a frente"))
    if thumb:
        tw = {stem(w) for w in words(t)} - STOP
        hw = {stem(w) for w in words(thumb)} - STOP
        shared = tw & hw
        if shared: issues.append(("repetição", f"a thumbnail repete o título em: {', '.join(sorted(shared))}"))
        else: good.append("thumbnail e título usam palavras diferentes")
        if len(words(thumb)) > 3:
            issues.append(("thumb", f"{len(words(thumb))} palavras na thumbnail; três é o teto no tamanho do feed"))
    score = max(0, min(100, 100 - 14 * len(issues) + 4 * len(good)))
    return {"titulo": t, "caracteres": n, "nota": score, "problemas": issues, "ok": good}

def show(r):
    print(f'\n  "{r["titulo"]}"')
    print(f"  {r['caracteres']} caracteres   nota {r['nota']}/100")
    for k, m in r["problemas"]: print(f"    x  {k:<11} {m}")
    for m in r["ok"]:           print(f"    ok             {m}")

def main():
    a = sys.argv[1:]
    as_json = "--json" in a; a = [x for x in a if x != "--json"]
    thumb = a[a.index("--thumb") + 1] if "--thumb" in a else None
    if "--titulo" in a:
        rows = [check(a[a.index("--titulo") + 1], thumb)]
    elif a and os.path.exists(a[0]):
        rows = [check(l, thumb) for l in open(a[0], encoding="utf-8").read().splitlines() if l.strip()]
    else:
        print(__doc__); sys.exit(1)
    rows.sort(key=lambda r: -r["nota"])
    if as_json: print(json.dumps(rows, ensure_ascii=False, indent=1)); return
    for r in rows: show(r)
    print()

if __name__ == "__main__":
    main()
