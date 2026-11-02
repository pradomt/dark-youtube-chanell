"""Monta o roteiro16.json do vídeo longo "Cinco pães" a partir do tempos.json (um parágrafo por item).
Uso: python montar16.py tempos.json audio.wav saida.json"""
import json, sys
T = json.load(open(sys.argv[1])); A = [e['start'] for e in T]; E = [e['end'] for e in T]
st = lambda p, fr=0: A[p] + fr * (E[p] - A[p])
X = lambda x: 1380 + (x - 540) * .8   # coordenada do Short -> palco 16:9
Y = lambda y: 600 + (y - 1110) * .8

# (apoio, título) por parágrafo; | separa pedaços do título, *x* = cor de acento
B = [("alimentar aquela multidão custaria", "*6 meses*|de salário"),
 ("fora a ressurreição, é o único milagre", "nos *4*|evangelhos"),
 ("hoje a gente refaz", "a *conta*"),
 ("tudo começa com uma notícia ruim:", "João Batista|*morre*"),
 ("Jesus entra num barco e vai", "para um lugar|*deserto*"),
 ("os discípulos voltavam tão cansados", "que nem|*comiam*"),
 ("mas o povo foi a pé", "e chegou|*antes*"),
 ("um detalhe que muda tudo:", "era perto da|*Páscoa*"),
 ("primavera, grama verde e", "a colheita da|*cevada*"),
 ("sem contar mulheres e crianças", "*5 mil*|homens"),
 ("contando todo mundo, talvez", "*15 mil*|pessoas"),
 ("Cafarnaum tinha uns 1.500 moradores:", "*10 cidades*|num campo"),
 ("Jesus testa Filipe:", "onde vamos|comprar *pão*?"),
 ("Filipe faz a conta:", "*200*|denários"),
 ("1 denário era o pagamento de", "*1 dia* de|trabalho"),
 ("uns 7 meses de trabalho, e", "não *dava*"),
 ("André encontra um menino com", "*5 pães*|e 2 peixes"),
 ("trigo era o pão bom; cevada era", "o pão dos|*pobres*"),
 ("1 denário comprava", "1 de trigo|ou *3 de cevada*"),
 ("peixinhos de acompanhar o pão,", "*secos* ou|salgados"),
 ("André pergunta:", "o que é isso|para *tanta gente*?"),
 ("Jesus manda sentar na grama", "em grupos|de *100* e *50*"),
 ("no grego, Marcos escreve", "em *canteiros*"),
 ("como Moisés no deserto:", "chefes de *mil*,|*cem*, *cinquenta*"),
 ("um povo no deserto", "esperando|*comida de Deus*"),
 ("tomou, olhou para o céu,", "*partiu*|e deu"),
 ("tomou, abençoou, partiu, deu:", "os verbos da|*última ceia*"),
 ("ninguém ficou só com um pedaço:", "*todos*|comeram"),
 ("recolham o que sobrou:", "*12*|cestos"),
 ("no tempo de Eliseu,", "*20 pães*|de cevada"),
 ("como pôr isso diante de 100 homens?", "comerão,|e vai *sobrar*"),
 ("20 pães para 100. 5 pães para milhares.", "os dois|com *sobra*"),
 ("uma segunda multiplicação:", "*4 mil* e|*7 cestos*"),
 ("na primeira vez, a palavra é", "*kófinos*"),
 ("na segunda, um cesto grande:", "a *spyrís*"),
 ("Jesus cobra a lembrança", "usando as|*duas palavras*"),
 ("terra judaica e terra de não judeus:", "*12* e *7*"),
 ("o povo quis fazer Jesus", "*rei*|à força"),
 ("vocês me procuram porque", "comeram|*pão*"),
 ("eles lembraram de Moisés:", "o *maná*"),
 ("eu sou", "o *pão*|da vida"),
 ("a partir dali, muitos", "foram|*embora*"),
 ("Senhor, para quem iremos?", "só tu tens|as palavras da *vida*"),
 ("milhares comeram;", "*poucos*|ficaram"),
 ("não era só sobre pão:", "era um|*sinal*"),
 ("nas mãos dele, o pouco", "não faltou.|*Sobrou*."),
 ("toda semana, uma história", "No Tempo|da *Bíblia*")]
assert len(B) == len(T), (len(B), len(T))

bat = []
for i, (ap, tit) in enumerate(B):
    a = A[i]; b = A[i + 1] - .05 if i + 1 < len(B) else 1e6
    pcs = tit.split('|'); dur = E[i] - a
    bat.append(dict(b=round(b, 2), apoio=[round(max(.3, a - .1), 2), ap],
        titulo=[[round(max(.5, a + .2 + k * min(.6, dur / (len(pcs) + 2))), 2), w] for k, w in enumerate(pcs)]))

# cenas: (parágrafo, fração do parágrafo, formação, opções, transição, cesto)
C = [(0, 0, 'calendario', {'acende': [.2, 2.5]}), (0, .55, 'lanche', {}), (1, 0, 'colunas4', {'passo': .8}), (2, 0, 'poeira', {}),
 (3, 0, 'ponto', {'apaga': 1}), (4, 0, 'lago', {'barco': 6}), (6, 0, 'lago', {'barco': .01, 'margem': 1}), (7, 0, 'ponto', {'glow': 160}),
 (8, 0, 'campo', {}), (9, 0, 'multidao', {'n': 100, 'R': 170}), (10, 0, 'multidao', {'n': 300, 'R': 300}), (11, 0, 'cidade', {'cresce': [2.5, 3]}),
 (12, 0, 'multidao', {'n': 300, 'R': 300, 'a': .5}), (13, 0, 'calendario', {'acende': [.3, st(15, .8) - st(13)]}), (16, 0, 'lanche', {}),
 (17, 0, 'preco', {}), (19, 0, 'mapa_peixe', {}), (20, 0, 'encolhe', {}), (21, 0, 'grupos', {}), (22, 0, 'grupos', {'cor': 1}), (23, 0, 'grupos', {}),
 (24, 0, 'ponto', {'R': 20, 'glow': 220}), (25, 0, 'grupos', {}), (25, .35, 'partir', {}), (26, 0, 'luz', {'R': 24}), (27, 0, 'grupos', {'comem': 1}),
 (28, 0, 'grupos', {}), (28, .45, 'cestos', {}, 1.6, 'k12'), (29, 0, 'eliseu', {}), (32, 0, 'sete', {}, 1.4, 's7'), (33, 0, 'compara', {}, 1.2, 'cmp'),
 (34, 0, 'compara', {'pessoa': 1, 'desce': 1}, 1.2, 'cmp'), (35, 0, 'compara', {}, 1.2, 'cmp'), (36, 0, 'regioes', {}), (37, 0, 'rei', {}),
 (38, 0, 'multidao', {'n': 300, 'R': 280}), (39, 0, 'mana', {}), (40, 0, 'luz', {'R': 30, 'glow': 300}), (41, 0, 'afasta', {}), (42, 0, 'afasta', {'ja': 1}),
 (43, 0, 'multidao', {'n': 300, 'R': 300, 'a': .5}), (43, .5, 'afasta', {}), (44, 0, 'luz', {'R': 40, 'glow': 350}), (45, 0, 'cestos', {}, 1.6, 'k12'),
 (45, .8, 'explode', {}, 0), (46, 0, 'ponto', {})]
# no Eliseu, o lado direito (5 pães e a multidão) entra no parágrafo 31
cen = [dict(t=-1, form='poeira', o={}, D=1.2)]
for c in C:
    p, fr, form, o = c[:4]; d = dict(t=round(st(p, fr), 2), form=form, o=dict(o), D=c[4] if len(c) > 4 else 1.2)
    if len(c) > 5: d['cesto'] = c[5]
    cen.append(d)
for k, c in enumerate(cen):
    nxt = cen[k + 1]['t'] if k + 1 < len(cen) else 1e6
    j = k + 1
    while c.get('cesto') and j < len(cen) and cen[j].get('cesto') == c['cesto']: j += 1
    c['fim'] = cen[j]['t'] if c.get('cesto') and j < len(cen) else nxt
    if c.get('cesto') and k > 0 and cen[k - 1].get('cesto') == c['cesto']: c['cesto'] = None  # contorno contínuo, desenhado pela primeira cena
    if c['form'] == 'eliseu': c['o']['t2'] = round(A[31] - c['t'], 2)

# textos sobre o palco
STAGE = 'left:930px;width:900px;'
ov = []
def o(a, b, html, css): ov.append(dict(a=round(a, 2), b=round(b, 2), html=html, css=css))
REF = [(0, 'JOÃO 6:7 · MATEUS 20:2'), (1, 'MT 14 · MC 6 · LC 9 · JO 6'), (3, 'MATEUS 14:1-12'), (4, 'MATEUS 14:13'), (5, 'MARCOS 6:30-31'), (6, 'MARCOS 6:33'),
       (7, 'JOÃO 6:4'), (8, 'MARCOS 6:39'), (9, 'MATEUS 14:21'), (10, 'ESTIMATIVA'), (11, 'ARQUEOLOGIA DE CAFARNAUM'), (12, 'JOÃO 6:5-6'), (13, 'JOÃO 6:7'),
       (14, 'MATEUS 20:2'), (16, 'JOÃO 6:8-9'), (18, 'APOCALIPSE 6:6'), (19, 'JOÃO 6:9 · OPSÁRION'), (20, 'JOÃO 6:9'), (21, 'MARCOS 6:39-40'), (22, 'MARCOS 6:40'),
       (23, 'ÊXODO 18:21'), (25, 'MARCOS 6:41'), (26, 'MARCOS 14:22'), (27, 'MARCOS 6:42'), (28, 'JOÃO 6:12-13 · PARÁFRASE'), (29, '2 REIS 4:42'),
       (30, '2 REIS 4:43-44 · PARÁFRASE'), (32, 'MARCOS 8:1-9'), (33, 'MARCOS 6:43'), (34, 'ATOS 9:25'), (35, 'MARCOS 8:19-20'), (36, 'INTERPRETAÇÃO'),
       (37, 'JOÃO 6:14-15'), (38, 'JOÃO 6:26'), (39, 'JOÃO 6:31'), (40, 'JOÃO 6:35 · PARÁFRASE'), (41, 'JOÃO 6:66'), (42, 'JOÃO 6:67-68 · PARÁFRASE'), (43, '')]
for k, (p, s) in enumerate(REF):
    if s: o(A[p] - .2, (A[REF[k + 1][0]] if k + 1 < len(REF) else A[43]) - .15, s, STAGE + 'top:96px;font:700 24px J,monospace;letter-spacing:5px;color:var(--acc)')
NOTA = 'top:968px;font:500 20px J,monospace;letter-spacing:3px;color:var(--muted)'
for a, b, s in [(0, 1, 'CADA QUADRADO: 1 DIA DE TRABALHO'), (9, 11, 'CADA PONTO: 50 PESSOAS'), (11, 12, 'CADA GRUPO: UMA CAFARNAUM (~1.500 PESSOAS)'),
                (13, 16, 'CADA QUADRADO: 1 DENÁRIO = 1 DIA DE TRABALHO'), (16, 17, 'O LANCHE DE UM MENINO'), (20, 21, 'CADA PONTO: 50 PESSOAS'),
                (21, 25, 'CADA PONTO: 1 PESSOA'), (28, 29, 'O QUE SOBROU'), (32, 33, 'CADA PONTO: 50 PESSOAS'), (37, 38, 'O PONTO LARANJA: JESUS'),
                (41, 43, 'OS DOZE FICAM')]:
    o(A[a] + .3, A[b] - .15, s, STAGE + NOTA)
LBL = 'font:700 24px J,monospace;letter-spacing:3px;color:var(--sub);width:240px;'
for c, nome in enumerate(['MATEUS', 'MARCOS', 'LUCAS', 'JOÃO']):
    o(A[1] + .3 + c * .8, A[2] - .15, nome, f'left:{X(540 + (c - 1.5) * 210) - 120}px;top:{Y(1110 + 270)}px;' + LBL)
o(A[4] + .3, A[7] - .15, 'MAR DA GALILEIA', f'left:{X(540) - 120}px;top:{Y(1110 + 20)}px;' + LBL + 'color:var(--muted)')
o(A[7] + .3, A[8] - .15, 'NISÃ · PRIMAVERA · PÁSCOA', STAGE + 'top:760px;font:700 26px J,monospace;letter-spacing:4px;color:var(--sub)')
o(A[8] + .5, A[9] - .15, 'CEVADA · A PRIMEIRA COLHEITA DO ANO', STAGE + NOTA)
big = 'font:800 40px M;color:var(--ink);width:300px;'
o(A[17] + .7, A[19] - .15, '1 de trigo', f'left:{X(160) - 150}px;top:{Y(1110 - 172)}px;' + big)
o(A[17] + 1.4, A[19] - .15, '3 de cevada', f'left:{X(160) - 150}px;top:{Y(1110 + 128)}px;' + big + 'color:var(--acc)')
o(A[19] + .5, A[20] - .15, 'MAGDALA', f'left:{X(335) - 240}px;top:{Y(1040) - 14}px;' + LBL + 'text-align:right;color:var(--acc)')
for j, (s, dx, dy) in enumerate([('100', -175, 30), ('100', 175, 30), ('50', -175, 255), ('50', 175, 255)]):
    o(A[21] + 1 + j * .25, A[24] - .15, s, f'left:{X(540 + dx) - 120}px;top:{Y(1110 + dy)}px;' + LBL + 'color:var(--muted)')
o(A[22] + .4, A[23] - .15, 'πρασιαὶ πρασιαί', STAGE + 'top:150px;font:800 64px "DejaVu Sans",sans-serif;color:var(--acc)')
o(A[22] + .8, A[23] - .15, 'CANTEIROS, CANTEIROS', STAGE + 'top:240px;font:700 22px J,monospace;letter-spacing:4px;color:var(--sub)')
o(A[23] + .4, A[24] - .15, 'CHEFES DE 1.000 · 100 · 50 · 10', STAGE + 'top:170px;font:800 40px M;color:var(--ink)')
for j, v in enumerate(['tomou', 'abençoou', 'partiu', 'deu']):
    o(A[26] + .6 + j * .5, A[27] - .15, v, f'left:{935 + j * 225}px;width:225px;top:840px;font:900 38px M;color:' + ('var(--acc)' if j == 2 else 'var(--ink)'))
o(A[29] + .6, A[32] - .15, '20 pães · 100 homens', f'left:{X(310) - 200}px;width:400px;top:{Y(1110 - 260)}px;font:800 32px M;color:var(--ink)')
o(A[31] + .2, A[32] - .15, '5 pães · milhares', f'left:{X(770) - 200}px;width:400px;top:{Y(1110 - 260)}px;font:800 32px M;color:var(--acc)')
o(A[33] + .4, A[36] - .15, 'KÓFINOS', f'left:{X(310) - 150}px;width:300px;top:{Y(1110 + 170)}px;font:800 30px "DejaVu Sans",sans-serif;color:var(--ink)')
o(A[33] + .7, A[36] - .15, 'cesto pequeno de viagem', f'left:{X(310) - 150}px;width:300px;top:{Y(1110 + 170) + 42}px;font:500 20px J,monospace;color:var(--muted)')
o(A[34] + .3, A[36] - .15, 'SPYRÍS', f'left:{X(730) - 150}px;width:300px;top:{Y(1110 + 210)}px;font:800 30px "DejaVu Sans",sans-serif;color:var(--acc)')
o(A[34] + .6, A[36] - .15, 'cesto grande', f'left:{X(730) - 150}px;width:300px;top:{Y(1110 + 210) + 42}px;font:500 20px J,monospace;color:var(--muted)')
o(A[36] + .5, A[37] - .15, 'GALILEIA', f'left:{X(320) - 120}px;top:{Y(1110 + 240)}px;' + LBL)
o(A[36] + 1.0, A[37] - .15, 'DECÁPOLIS', f'left:{X(760) - 120}px;top:{Y(1110 + 240)}px;' + LBL)
o(A[39] + .4, A[40] - .15, 'MANÁ', STAGE + 'top:170px;font:900 60px M;color:var(--acc);letter-spacing:6px')
o(A[46] + .6, 1e6, '<span style="display:inline-block;padding:14px 38px;border-radius:60px;font:800 40px M;background:var(--acc);color:#fff">Inscreva-se</span>', STAGE + 'top:700px')
o(A[46] + 1.2, 1e6, 'Fontes e créditos na descrição', STAGE + 'top:800px;font:500 22px J,monospace;color:var(--muted)')
cnt = [dict(a=A[9] + .2, b=A[10] - .1, de=0, para=5000, dur=1.6, leg='HOMENS'), dict(a=A[10] - .1, b=A[11] - .15, de=5000, para=15000, dur=1.8, pre='~', leg='PESSOAS · ESTIMATIVA'),
       dict(a=A[13] + .3, b=A[16] - .15, de=0, para=200, dur=st(15, .8) - st(13), leg='DIAS DE TRABALHO'), dict(a=st(28, .5), b=A[29] - .15, de=0, para=12, dur=.8, leg='CESTOS CHEIOS'),
       dict(a=A[32] + .2, b=A[33] - .15, de=0, para=4000, dur=1.5, leg='HOMENS · 7 CESTOS')]
CAP = ['O contexto', 'A conta', 'O pão de quem tinha *pouco*', 'Os grupos', 'O *milagre*', 'Já tinha acontecido *antes*', 'A *segunda* vez', 'O dia *seguinte*']
sec_ini = {}
for k, e in enumerate(json.load(open('itens.json'))): sec_ini.setdefault(e['sec'], k)
caps = [dict(n=f'PARTE {s}', t=CAP[s - 1], a=round(A[sec_ini[s]] - 1.5, 2), b=round(A[sec_ini[s]] - .2, 2)) for s in range(1, 9)]
R = dict(tema='papel', marca='NO TEMPO DA BÍBLIA', audio=sys.argv[2], decoracao='biblia', acento='#c0501f', batidas=bat, cenas=[], capitulos=caps,
         cenas16=cen, ov=ov, cnt=cnt, extra='cenas16.js', aviso='')
json.dump(R, open(sys.argv[3], 'w'), ensure_ascii=False, indent=1)
print(len(bat), 'batidas', len(cen), 'cenas', len(ov), 'textos')
