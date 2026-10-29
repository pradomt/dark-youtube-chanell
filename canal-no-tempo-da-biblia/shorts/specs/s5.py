import sys; sys.path.insert(0, '/tmp/w/shorts/specs'); from base_short import *
TEMA = 'noite'
ACENTO = '#ec7a35'
B = [(0, 'antes de dormir', 'um verso|*só*'),
     (1, 'Salmo 23:4', 'porque *tu*|estás comigo'),
     (2, 'repare:', 'o salmo falava|*sobre* Deus'),
     (4, 'no vale escuro', 'passa a falar|*com* Deus'),
     (5, 'se hoje foi difícil, diga:', '*tu estás*|comigo'),
     (7, 'e descanse.', 'boa|*noite*')]
CHAMADA = 8
PILULAS = ['Salmo 23', 'No Tempo da Bíblia']
CARTAO = dict(arquivo=[(0, 'salmo-23.txt'), (2, 'quem-fala.svg'), (5, 'pastores.jpg')],
              etiqueta=[(0, '● verso 4'), (2, '● versos 1 a 4'), (5, '● boa noite')],
              rotulo=[(0, 'SALMO 23:4 · TRADUÇÃO LIVRE'), (2, 'QUEM FALA COM QUEM'), (5, 'PASTORES À NOITE · c. 1900')],
              paineis=[dict(tipo='lista', fa=0, fb=2, itens=[dict(t=0, texto='Ainda que eu ande pelo vale da sombra da morte, não temerei mal nenhum, *porque tu estás comigo*.', nota='Salmo 23:4')]),
                       dict(tipo='svg', fa=2, fb=5, svgf='/tmp/w/longo/svg/pessoa-verbo.svg', passos={'A': 3, 'B': 4}),
                       im('pastores-noite', 5)])
