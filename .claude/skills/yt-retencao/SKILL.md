---
name: yt-retencao
description: >-
  Lê a exportação de retenção de público do YouTube Studio e mostra onde o
  público sai e o que mudar. Use para "por que as pessoas param de assistir",
  "minha retenção está ruim", um CSV ou print do gráfico de retenção, ou
  "ajustar o ritmo".
---

# yt-retencao

O gráfico de retenção é o retorno mais honesto que o YouTube dá. Quase ninguém exporta.

```bash
python3 .claude/skills/yt-retencao/retencao.py retencao.csv --transcricao tempos.json
python3 .claude/skills/yt-retencao/retencao.py retencao.csv --duracao 305
```

Use sempre `--transcricao` com o `tempos.json` (ou `legendas.srt`) do vídeo, que fica em
`/mnt/project-files/canal-astronomia/video-XX-pronto/audio-v2/`. Assim o relatório diz o que a
narração falava em cada queda, e a duração sai sozinha.

Como pegar o arquivo: YouTube Studio -> o vídeo -> Análise -> Engajamento -> gráfico de retenção
de público -> ícone de download. Se o Moises mandar só um print do gráfico, leia os pontos do print
e monte o CSV (posição; retenção) antes de rodar. Diga que os valores foram lidos do print.

## Três problemas diferentes

- **GANCHO**: quanto se perdeu nos primeiros 30 segundos. Abaixo de 25 pontos é saudável. É sempre
  a primeira coisa a corrigir, e a correção é sempre nos primeiros 15 segundos do roteiro.
- **QUEDAS**: descidas bruscas num momento. Uma queda é uma troca de assunto sem aviso, uma
  explicação longa demais ou uma imagem parada por muito tempo.
- **DESLIZE**: a perda contínua no meio. Deslize alto é ritmo: a correção é cortar, não reescrever.

## O que entregar

Aponte o maior vazamento e UMA mudança para ele, citando a frase do roteiro e o arquivo de texto da
seção (`narracao-roteiro-XX/textos/`). Não entregue lista de cinco. Se o gancho estiver saudável e o
deslize baixo, diga que o vídeo está bom e o problema é título e thumbnail: mande para `/yt-titulo`.

Canal novo tem poucos dados. Com menos de umas 100 visualizações, diga que a curva ainda é ruído e
que a conclusão é provisória. Nunca invente um número que não está no CSV.

## A trava

Nada aqui publica. A skill escreve, o Moises publica. Termine sempre com a pergunta:
**publicar assim, ou mudar?**
