---
name: yt-titulo
description: >-
  Escreve e confere título e texto da thumbnail de um vídeo do YouTube como
  um par: tamanho, repetição e palavras vagas. Use para "ideias de título",
  "que nome dou", "texto da thumbnail", "CTR baixo" ou para renomear um vídeo
  já publicado.
---

# yt-titulo

Título e thumbnail são UMA coisa. Escrever separado é o motivo de a thumbnail repetir o título e
metade da área de clique dizer a mesma coisa duas vezes.

```bash
python3 .claude/skills/yt-titulo/titulo.py --titulo "..." --thumb "CÉU ESPELHADO"
python3 .claude/skills/yt-titulo/titulo.py titulos.txt --thumb "CÉU ESPELHADO"   # um por linha
```

## Antes de escrever

1. Leia `.claude/youtube/voz.md`: o tom do canal, o público e o que o canal não promete.
2. Nunca invente número, resultado ou fonte. Se um número ajudaria e não está no roteiro, peça ou
   escreva sem ele.
3. Sem caça-clique: o título tem que ser cumprido nos primeiros 30 segundos do vídeo.

## O que o script confere, e por quê

- **60 caracteres** é onde a busca no computador corta; **40** é o feed do celular.
- **A thumbnail não repete o título.** Palavras diferentes, mesma promessa.
- **No máximo três palavras na thumbnail.** No tamanho do feed, a quarta vira borrão.
- **Um número, um nome ou uma data** vale mais que qualquer adjetivo ("incrível", "segredo").
- **No máximo duas palavras em maiúsculas** no título.

A nota é uma heurística, não uma previsão de cliques.

## Escreva dez, fique com dois

Gere dez títulos, salve num arquivo, rode todos no script e mostre os três melhores com a nota e o
problema de cada um. Para o vencedor, escreva o briefing da thumbnail: as até três palavras, o que a
imagem mostra (fundo do Canva, céu, bandeira) e como manter contraste no tamanho do feed.

## A trava

Nada aqui publica. Termine com o bloco pronto para colar e a pergunta:
**publicar assim, ou mudar?**
