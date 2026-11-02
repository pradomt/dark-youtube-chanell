import json
T = json.load(open('tempos.json')); F = [e['start'] for e in T]
B = [("alimentar a multidão custaria mais de", "*6 meses*|de salário"),
 ("sem contar mulheres e crianças", "*5 mil*|homens"),
 ("contando todo mundo, talvez", "*15 mil*|pessoas"),
 ("Filipe fez a conta:", "*200*|denários"),
 ("1 denário era o pagamento de", "*1 dia* de|trabalho"),
 ("200 dias de trabalho, e", "não *dava*|para todos"),
 ("tudo o que havia:", "*5 pães*|e 2 peixes"),
 ("pão de cevada era", "o pão dos|*pobres*"),
 ("mas Jesus mandou sentar", "em grupos|de *100* e *50*"),
 ("deu graças e partiu os pães", "*todos*|comeram"),
 ("recolham o que sobrou", "para que nada|se *perca*"),
 ("e encheram", "*12*|cestos"),
 ("no grego, sobrar e abundância", "têm a mesma|*raiz*"),
 ("eu vim para que tenham vida", "e vida em|*abundância*"),
 ("o que você tem", "parece|*pouco*?"),
 ("nas mãos dele,", "não falta."),
 ("nas mãos dele, não falta.", "*sobra*.")]
bat = []
for i, (ap, tit) in enumerate(B):
    a = F[i]; b = F[i + 1] - .05 if i + 1 < len(B) else 99
    pcs = tit.split('|'); dur = T[i]['end'] - a
    bat.append(dict(b=round(b, 2), apoio=[round(max(.3, a - .1), 2), ap],
        titulo=[[round(max(.5, a + .15 + k * min(.55, dur / (len(pcs) + 1))), 2), w] for k, w in enumerate(pcs)]))
ch = T[-1]['end'] + .5
R = dict(tema='papel', marca='NO TEMPO DA BÍBLIA', audio='../mix.wav', decoracao='biblia', acento='#c0501f', cartao=None,
         batidas=bat,
         chamada=dict(a=round(ch, 2), pilulas=['Mt 14 · Mc 6 · Jo 6', 'No Tempo da Bíblia'], seta=False), extra='paes.js', frases=F)
json.dump(R, open('palco/roteiro.json', 'w'), ensure_ascii=False, indent=1)
print('chamada', ch)
