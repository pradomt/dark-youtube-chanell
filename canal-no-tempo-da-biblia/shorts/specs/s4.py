import sys; sys.path.insert(0, '/tmp/w/shorts/specs'); from base_short import *
ACENTO = '#c0501f'
B = [(0, 'Davi era', '*rei*'),
     (1, 'então por que chamou Deus de', '*pastor*,|e não de rei?'),
     (2, 'primeiro:', 'antes de rei,|*pastor*'),
     (3, '1 Samuel 17', 'o *leão*|e o urso'),
     (4, 'segundo: no Oriente antigo', 'pastor era|*título de rei*'),
     (5, 'até no código de', '*Hamurabi*'),
     (6, 'quando um rei diz', '"o Senhor é|o meu *pastor*"'),
     (8, 'ele está dizendo', 'eu também preciso|de *cuidado*'),
     (9, 'Salmo 23 verso a verso', 'vídeo completo|no *canal*')]
CHAMADA = 9
PILULAS = ['12 min', 'No Tempo da Bíblia']
CARTAO = dict(arquivo=[(0, 'davi.jpg'), (3, '1-samuel-17.txt'), (4, 'hamurabi.jpg'), (6, 'salmo-23.jpg')],
              etiqueta=[(0, '● 1 Samuel 16'), (3, '● 17:34-35'), (4, '● c. 1750 a.C.'), (6, '● verso 1')],
              rotulo=[(0, 'DAVI APRESENTADO A SAMUEL · TISSOT'), (3, 'DAVI A SAUL'), (4, 'CÓDIGO DE HAMURABI · LOUVRE'), (6, 'OVELHAS NA JUDEIA · c. 1900')],
              paineis=[im('tissot-davi-samuel', 0, 3, foco='50% 30%'),
                       dict(tipo='lista', fa=3, fb=4, itens=[dict(t=0, texto='Um *leão*', nota='e um urso'), dict(t=0, texto='Salvou a *ovelha*', nota='tirou da boca do animal')]),
                       im('hamurabi', 4, 6, foco='50% 20%'),
                       im('salmo23-a', 6)],
              diario=[(2, '✓ pastor antes de ser rei'), (5, '"o pastor chamado pelo deus"'), (8, '→ até o rei precisa de um pastor')])
