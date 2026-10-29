import sys; sys.path.insert(0, '/tmp/w/shorts/specs'); from base_short import *
ACENTO = '#c0501f'
B = [(0, 'quando Lázaro morreu, ele foi', 'enterrado no|*mesmo dia*'),
     (1, 'por que', 'tanta|*pressa?*'),
     (2, 'na Judeia do tempo de Jesus', 'antes do|*pôr do sol*'),
     (3, 'a Lei mandava', 'nada de corpo|exposto à *noite*'),
     (4, 'sem embalsamar, no calor', '*horas*,|não dias'),
     (5, 'quem tocava num morto', '*7 dias*|impuro'),
     (6, 'quando Jesus chegou a Betânia', '*4 dias*|no túmulo'),
     (7, 'e Marta avisou:', 'ele já|*cheira mal*'),
     (9, 'como se enterrava um morto', 'vídeo completo|no *canal*')]
CHAMADA = 9
PILULAS = ['15 min', 'No Tempo da Bíblia']
CARTAO = dict(arquivo=[(0, 'joao-11.jpg'), (2, 'regras.txt'), (6, 'joao-11.jpg')],
              etiqueta=[(0, '● João 11'), (3, '● Deut. 21:23'), (5, '● Núm. 19'), (6, '● João 11:39')],
              rotulo=[(0, 'LÁZARO · TISSOT'), (2, 'POR QUE NO MESMO DIA'), (6, 'BETÂNIA · 4 DIAS DEPOIS')],
              paineis=[im('tissot-lazaro-retrato', 0, 2),
                       dict(tipo='lista', fa=2, fb=6, itens=[dict(t=0, texto='A *Lei*', nota='Deuteronômio 21:23'), dict(t=0, texto='O *calor*', nota='sem embalsamar'), dict(t=0, texto='A *impureza*', nota='7 dias · Números 19')]),
                       im('tissot-lazaro', 6)],
              diario=[(2, '☀ enterro antes do pôr do sol'), (5, '7 dias · impureza por contato'), (8, '✗ as especiarias não seguravam')])
