#!/bin/bash
# Uso: mixar.sh narracao.wav trilha.wav saida.wav [volume_musica_dB]   (padrão do canal: -8 dB; antes era -14)
V=${4:--8}
ffmpeg -y -loglevel error -i "$1" -i "$2" -filter_complex "[0]aresample=48000,pan=stereo|c0=c0|c1=c0,highpass=f=70,acompressor=threshold=-20dB:ratio=3:attack=5:release=120,loudnorm=I=-16:TP=-2[v];[1]aresample=48000,volume=${V}dB[m];[v][m]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11" -ar 48000 "$3"
