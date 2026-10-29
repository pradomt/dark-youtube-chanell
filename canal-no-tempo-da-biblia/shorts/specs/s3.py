import sys; sys.path.insert(0, '/tmp/w/shorts/specs'); from base_short import *
ACENTO = '#c0501f'
B = [(0, 'o vale da sombra da morte', 'era um lugar|*de verdade?*'),
     (1, 'no deserto da Judeia', 'vales chamados|*uádis*'),
     (2, 'em alguns trechos', 'o sol quase|*não chega*'),
     (3, 'a sombra é fria', 'e o perigo fica|*depois da curva*'),
     (4, 'uma tradição aponta', 'o uádi|*Qelt*'),
     (5, 'mas o texto', '*não diz*|o lugar'),
     (6, 'a palavra hebraica pode ser', '*escuridão*|profunda'),
     (7, 'talvez por isso', 'cada um tem|o seu *vale*'),
     (8, 'Salmo 23 verso a verso', 'vídeo completo|no *canal*')]
CHAMADA = 8
PILULAS = ['12 min', 'No Tempo da Bíblia']
CARTAO = dict(arquivo=[(0, 'salmo-23.txt'), (1, 'uadi-qelt.jpg'), (4, 'mosteiro-qelt.jpg'), (6, 'tsalmavet.txt')],
              etiqueta=[(0, '● verso 4'), (1, '● hoje'), (4, '● c. 1900'), (6, '● hebraico')],
              rotulo=[(0, 'SALMO 23:4'), (1, 'UÁDI QELT · DESERTO DA JUDEIA'), (4, 'MOSTEIRO DE SÃO JORGE · UÁDI QELT'), (6, 'A PALAVRA')],
              paineis=[dict(tipo='lista', fa=0, fb=1, itens=[dict(t=0.8, texto='Ainda que eu ande pelo *vale da sombra da morte*…', nota='tradução livre')]),
                       im('uadi-qelt-1', 1, 3), im('uadi-qelt-3', 3, 4),
                       im('mosteiro-qelt', 4, 6),
                       dict(tipo='lista', fa=6, itens=[dict(t=0, texto='*tsalmavet*', nota='sombra da morte'), dict(t=0, texto='ou *escuridão profunda*', nota='as duas leituras existem')])],
              diario=[(1, '↓ vales estreitos e profundos'), (4, 'entre Jerusalém e Jericó'), (5, '? tradição, não prova')])
