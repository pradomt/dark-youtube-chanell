# Canal Dark

Ferramentas do canal "Mapa do Céu".

## Skills do Claude Code

Ficam em `.claude/skills/` e ativam sozinhas quando o Claude Code roda neste repositório
(ou pelo comando com barra). Os scripts usam só Python 3, sem instalar nada e sem internet.

| comando | para que serve |
| --- | --- |
| `/yt-retencao` | Lê o CSV de retenção do YouTube Studio e aponta o gancho, as quedas e o que a narração dizia nelas. |
| `/yt-capitulos` | Gera os capítulos a partir do `tempos.json` da narração e confere as regras do YouTube. |
| `/yt-titulo` | Confere título + texto da thumbnail como um par: tamanho, repetição, palavras vagas. |
| `/yt-plano` | Plano do mês que cabe em cerca de 2 h por semana. |

O tom do canal fica em `.claude/youtube/voz.md`.

Adaptadas para português a partir de
[youtube-agent-skill](https://github.com/Jakeschincariol/youtube-agent-skill)
(Copyright (c) 2026 Jake Schincariol, licença MIT). Licença original em
`.claude/skills/LICENSE-youtube-agent-skill`.
