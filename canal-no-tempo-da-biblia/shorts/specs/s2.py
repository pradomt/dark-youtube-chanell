import sys; sys.path.insert(0, '/tmp/w/shorts/specs'); from base_short import *
ACENTO = '#c0501f'
B = [(0, 'nos filmes, a pedra do túmulo é', 'uma *roda*|gigante'),
     (1, 'mas a arqueologia', 'conta *outra*|história'),
     (2, 'Amos Kloner estudou', '*+900*|túmulos'),
     (3, 'com pedra redonda:', 'só|*quatro*'),
     (4, 'o comum era', 'uma pedra|*quadrada*'),
     (5, 'mas José de Arimateia era', 'um homem|*rico*'),
     (7, 'uma pedra redonda de 1,5 m', 'mais de|*1 tonelada*'),
     (8, 'as mulheres perguntavam:', 'quem vai|*remover?*'),
     (10, 'a história completa está', 'no|*canal*')]
CHAMADA = 10
PILULAS = ['15 min', 'No Tempo da Bíblia']
CARTAO = dict(arquivo=[(0, 'pedra-redonda.jpg'), (2, 'kloner-1999.txt'), (4, 'pedras.svg'), (5, 'tumulo-dos-reis.jpg'), (8, 'marcos-16.jpg')],
              etiqueta=[(0, '● réplica'), (2, '● 1999'), (4, '● esquema'), (5, '● séc. I'), (8, '● Marcos 16:3')],
              rotulo=[(0, 'RECONSTITUIÇÃO · NAZARETH VILLAGE'), (2, 'TÚMULOS DO 2º TEMPLO'), (4, 'DOIS TIPOS DE FECHAMENTO'), (5, 'PEDRA REDONDA · TÚMULO DOS REIS'), (8, 'AS MULHERES NO TÚMULO · TISSOT')],
              paineis=[im('pedra-nazare', 0, 2),
                       dict(tipo='numero', fa=2, fb=3, de=0, para=900, prefixo='+', legenda='TÚMULOS ESTUDADOS', contaf=(2, 2)),
                       dict(tipo='numero', fa=3, fb=4, de=0, para=4, legenda='COM PEDRA REDONDA', contaf=(3, 1)),
                       dict(tipo='svg', fa=4, fb=5, svgf='/tmp/w/longo/svg/pedras.svg', passos={'A': 4, 'B': 4}),
                       im('pedra-tumulo-reis', 5, 8),
                       im('tissot-mulheres-tumulo', 8)],
              diario=[(3, '✓ famílias muito ricas'), (7, 'estimativa: calcário ≈ 2,5 t/m³'), (9, 'Marcos 16:3')])
