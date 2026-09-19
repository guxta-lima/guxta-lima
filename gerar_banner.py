#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gera um banner SVG animado (estilo terminal verde-neon) para o README do GitHub.

Edite as variaveis abaixo e rode:  python3 gerar_banner.py
O arquivo sai como assets/banner.svg
"""

import os
from xml.sax.saxutils import escape

# ----------------------------------------------------------------------
# EDITE AQUI
# ----------------------------------------------------------------------
USUARIO   = "guxta-lima"
NOME      = "GUSTAVO LIMA"
COMANDO   = "./whoami --live"
CARGO     = "Estudante de ADS na FATEC  //  Itapetininga, SP"
CHIPS     = ["estudando", "construindo", "publicando"]
SAIDA     = "assets/banner.svg"
# ----------------------------------------------------------------------

W, H = 880, 260
CICLO = 10.0  # segundos por volta da animacao

VERDE      = "#00FF9C"
VERDE_SUAVE = "#9FE8C4"
VERDE_FRACO = "#4F8C74"
FUNDO      = "#07100C"
BARRA      = "#0B1A14"
BORDA      = "#1D3A2C"
TEXTO      = "#E6FFF4"

MONO = "ui-monospace,'SF Mono','JetBrains Mono','Fira Code',Menlo,Consolas,monospace"


def largura_char(tamanho):
    """Largura aproximada de um caractere em fonte monoespacada."""
    return tamanho * 0.601


def animacao_digitando(x, y_ignorado, texto, tamanho, inicio, fim):
    """Retorna (values, keyTimes) para um rect de clipPath revelando o texto."""
    cw = largura_char(tamanho)
    n = len(texto)
    values, key_times = ["0"], ["0"]
    for i in range(1, n + 1):
        t = inicio + (fim - inicio) * (i / n)
        values.append(f"{cw * i:.2f}")
        key_times.append(f"{t / CICLO:.4f}")
    values.append(f"{cw * n:.2f}")
    key_times.append("1")
    return ";".join(values), ";".join(key_times)


def posicoes_cursor(x0, texto, tamanho, inicio, fim):
    cw = largura_char(tamanho)
    n = len(texto)
    values, key_times = [f"{x0:.2f}"], ["0"]
    for i in range(1, n + 1):
        t = inicio + (fim - inicio) * (i / n)
        values.append(f"{x0 + cw * i:.2f}")
        key_times.append(f"{t / CICLO:.4f}")
    values.append(f"{x0 + cw * n:.2f}")
    key_times.append("1")
    return ";".join(values), ";".join(key_times)


# --- tempos ---
T_CMD_INI, T_CMD_FIM   = 0.4, 1.6
T_NOME_INI, T_NOME_FIM = 2.0, 3.4
T_CARGO                = 3.7
T_CHIP                 = 4.1

# --- geometria ---
PAD_X   = 34
Y_CMD   = 86
TAM_CMD = 16
Y_NOME  = 148
TAM_NOME = 44
Y_CARGO = 182
TAM_CARGO = 15
Y_CHIP  = 206
ALT_CHIP = 26
TAM_CHIP = 12

prompt = "$ "
cmd_completo = prompt + COMANDO
cmd_vals, cmd_keys = animacao_digitando(PAD_X, Y_CMD, cmd_completo, TAM_CMD, T_CMD_INI, T_CMD_FIM)
cur_vals, cur_keys = posicoes_cursor(PAD_X, cmd_completo, TAM_CMD, T_CMD_INI, T_CMD_FIM)
nome_vals, nome_keys = animacao_digitando(PAD_X, Y_NOME, NOME, TAM_NOME, T_NOME_INI, T_NOME_FIM)

larg_cmd  = largura_char(TAM_CMD) * len(cmd_completo) + 4
larg_nome = largura_char(TAM_NOME) * len(NOME) + 8
cw_cmd = largura_char(TAM_CMD)

# chips
chips_svg = []
x_chip = PAD_X
for i, chip in enumerate(CHIPS):
    larg = largura_char(TAM_CHIP) * len(chip) + 26
    ini = T_CHIP + i * 0.18
    chips_svg.append(f'''
  <g opacity="0">
    <animate attributeName="opacity" dur="{CICLO}s" repeatCount="indefinite"
             values="0;0;1;1;0" keyTimes="0;{ini/CICLO:.4f};{(ini+0.45)/CICLO:.4f};0.955;1"/>
    <rect x="{x_chip:.1f}" y="{Y_CHIP}" width="{larg:.1f}" height="{ALT_CHIP}" rx="{ALT_CHIP/2:.1f}"
          fill="#0C2018" stroke="{BORDA}"/>
    <circle cx="{x_chip + 13:.1f}" cy="{Y_CHIP + ALT_CHIP/2:.1f}" r="3.5" fill="{VERDE}">
      <animate attributeName="opacity" dur="2.2s" repeatCount="indefinite" values="1;0.25;1"/>
    </circle>
    <text x="{x_chip + 22:.1f}" y="{Y_CHIP + ALT_CHIP/2 + 4.2:.1f}" font-family="{MONO}"
          font-size="{TAM_CHIP}" fill="{VERDE_SUAVE}">{escape(chip)}</text>
  </g>''')
    x_chip += larg + 10

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"
     role="img" aria-label="{escape(NOME)} — {escape(CARGO)}">
  <title>{escape(NOME)} — {escape(CARGO)}</title>

  <defs>
    <linearGradient id="fundo" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#08140E"/>
      <stop offset="55%" stop-color="{FUNDO}"/>
      <stop offset="100%" stop-color="#050C09"/>
    </linearGradient>

    <radialGradient id="brilho" cx="18%" cy="30%" r="70%">
      <stop offset="0%" stop-color="{VERDE}" stop-opacity="0.13"/>
      <stop offset="100%" stop-color="{VERDE}" stop-opacity="0"/>
    </radialGradient>

    <linearGradient id="varredura" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="{VERDE}" stop-opacity="0"/>
      <stop offset="50%" stop-color="{VERDE}" stop-opacity="0.09"/>
      <stop offset="100%" stop-color="{VERDE}" stop-opacity="0"/>
    </linearGradient>

    <pattern id="grade" width="22" height="22" patternUnits="userSpaceOnUse">
      <circle cx="1" cy="1" r="1" fill="{VERDE}" opacity="0.07"/>
    </pattern>

    <filter id="neon" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="5" result="b"/>
      <feMerge>
        <feMergeNode in="b"/><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="neon-fraco" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="2" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>

    <clipPath id="janela"><rect x="1" y="1" width="{W-2}" height="{H-2}" rx="15"/></clipPath>
    <clipPath id="clip-cmd"><rect x="{PAD_X}" y="{Y_CMD - TAM_CMD}" height="{TAM_CMD + 8}" width="0">
      <animate attributeName="width" dur="{CICLO}s" repeatCount="indefinite"
               calcMode="discrete" values="{cmd_vals}" keyTimes="{cmd_keys}"/>
    </rect></clipPath>
    <clipPath id="clip-nome"><rect x="{PAD_X}" y="{Y_NOME - TAM_NOME}" height="{TAM_NOME + 14}" width="0">
      <animate attributeName="width" dur="{CICLO}s" repeatCount="indefinite"
               calcMode="discrete" values="{nome_vals}" keyTimes="{nome_keys}"/>
    </rect></clipPath>
  </defs>

  <g clip-path="url(#janela)">
    <rect width="{W}" height="{H}" fill="url(#fundo)"/>
    <rect width="{W}" height="{H}" fill="url(#grade)"/>
    <rect width="{W}" height="{H}" fill="url(#brilho)"/>

    <rect x="0" y="-80" width="{W}" height="80" fill="url(#varredura)">
      <animate attributeName="y" dur="{CICLO}s" repeatCount="indefinite"
               values="-80;{H}" keyTimes="0;1"/>
    </rect>

    <!-- barra da janela -->
    <rect x="0" y="0" width="{W}" height="34" fill="{BARRA}"/>
    <line x1="0" y1="34" x2="{W}" y2="34" stroke="{BORDA}"/>
    <circle cx="22" cy="17" r="5" fill="#FF5F57"/>
    <circle cx="40" cy="17" r="5" fill="#FEBC2E"/>
    <circle cx="58" cy="17" r="5" fill="#28C840"/>
    <text x="{W/2}" y="21" text-anchor="middle" font-family="{MONO}" font-size="11.5"
          fill="{VERDE_FRACO}">{escape(USUARIO)} — zsh — 80x24</text>

    <!-- linha de comando -->
    <g clip-path="url(#clip-cmd)">
      <text x="{PAD_X}" y="{Y_CMD}" font-family="{MONO}" font-size="{TAM_CMD}" fill="{VERDE_SUAVE}">
        <tspan fill="{VERDE}">$</tspan> {escape(COMANDO)}
      </text>
    </g>

    <!-- cursor -->
    <rect y="{Y_CMD - TAM_CMD + 2}" width="{cw_cmd:.1f}" height="{TAM_CMD + 2}" fill="{VERDE}" x="{PAD_X}">
      <animate attributeName="x" dur="{CICLO}s" repeatCount="indefinite"
               calcMode="discrete" values="{cur_vals}" keyTimes="{cur_keys}"/>
      <animate attributeName="opacity" dur="1.05s" repeatCount="indefinite"
               calcMode="discrete" values="1;0" keyTimes="0;0.5"/>
    </rect>

    <!-- nome -->
    <g clip-path="url(#clip-nome)" filter="url(#neon)">
      <text x="{PAD_X}" y="{Y_NOME}" font-family="{MONO}" font-size="{TAM_NOME}"
            font-weight="700" letter-spacing="1.5" fill="{TEXTO}">{escape(NOME)}</text>
    </g>
    <rect x="{PAD_X}" y="{Y_NOME + 12}" width="0" height="2" fill="{VERDE}" opacity="0.55">
      <animate attributeName="width" dur="{CICLO}s" repeatCount="indefinite"
               values="0;0;{larg_nome:.1f};{larg_nome:.1f};0"
               keyTimes="0;{T_NOME_INI/CICLO:.4f};{T_NOME_FIM/CICLO:.4f};0.955;1"/>
    </rect>

    <!-- cargo -->
    <text x="{PAD_X}" y="{Y_CARGO}" font-family="{MONO}" font-size="{TAM_CARGO}"
          fill="{VERDE_SUAVE}" opacity="0" filter="url(#neon-fraco)">
      {escape(CARGO)}
      <animate attributeName="opacity" dur="{CICLO}s" repeatCount="indefinite"
               values="0;0;0.92;0.92;0"
               keyTimes="0;{T_CARGO/CICLO:.4f};{(T_CARGO+0.5)/CICLO:.4f};0.955;1"/>
    </text>
{''.join(chips_svg)}

    <rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="15" fill="none" stroke="{BORDA}"/>
  </g>
</svg>
'''

os.makedirs(os.path.dirname(SAIDA) or ".", exist_ok=True)
with open(SAIDA, "w", encoding="utf-8") as f:
    f.write(svg)
print(f"ok -> {SAIDA}")
