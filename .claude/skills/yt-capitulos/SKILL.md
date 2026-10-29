---
name: yt-capitulos
description: >-
  Gera e valida capítulos do YouTube (minutagem na descrição) a partir da
  transcrição ou dos tempos da narração. Use para "fazer os capítulos",
  "minutagem", "timestamps", "dividir o vídeo em partes" ou para conferir
  se os capítulos de uma descrição vão aparecer.
---

# yt-capitulos

```bash
python3 .claude/skills/yt-capitulos/capitulos.py tempos.json          # usa as seções do roteiro
python3 .claude/skills/yt-capitulos/capitulos.py legendas.srt --alvo 8
python3 .claude/skills/yt-capitulos/capitulos.py --validar descricao-youtube.txt
```

No nosso fluxo, prefira o `tempos.json` da narração (`video-XX-pronto/audio-v2/`): cada fala tem a
seção do roteiro, então os cortes caem exatamente onde as seções começam. O `.srt` serve para vídeos
sem `tempos.json`; aí o script acha os cortes pelas pausas e pela troca de vocabulário.

## As regras, que não são opcionais

Se uma delas quebrar, o bloco não vira capítulo e o YouTube não avisa:

- O primeiro é **00:00**.
- Pelo menos **três** capítulos.
- Cada um com pelo menos **10 segundos**, em ordem crescente.

Antes de entregar a descrição final, rode sempre `--validar` no arquivo da descrição.

## Reescreva cada título

Os títulos que o script gera são rascunho (nome da seção ou palavras do trecho). Reescreva cada um
como a promessa daquele trecho, em 3 a 5 palavras, no tom do canal (ver `.claude/youtube/voz.md`).
Se um trecho não cabe em cinco palavras, ele é dois trechos ou é enchimento: avise.

## A trava

Nada aqui publica. Termine com o bloco pronto para colar e a pergunta:
**publicar assim, ou mudar?**
