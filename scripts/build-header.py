#!/usr/bin/env python3
"""Generates assets/header.svg - an animated quantum-circuit banner."""

W, H = 900, 340
X0, X1 = 168, 782          # wire start -> measurement box left edge
MEAS_W = 30
XEND = 852                 # classical wire end
CYCLE = 5.0                # seconds per full cycle
TRAVEL = 0.5               # fraction of cycle spent travelling

LANES = [
    # label,        color,     y,   gates [(letter, x)]
    ("TypeScript",  "#4d9fe8", 148, [("H", 240), ("T", 372), ("X", 596)]),
    ("Python",      "#ffd85e", 186, [("X", 216), ("H", 328), ("S", 512)]),
    ("React",       "#61dafb", 224, [("H", 264), ("Z", 452), ("T", 640)]),
    ("NestJS",      "#f0456b", 262, [("T", 288), ("X", 420), ("H", 556)]),
    ("Qiskit",      "#b088ff", 300, [("H", 228), ("S", 356), ("Z", 484), ("T", 620)]),
]
STAGGER = 0.34
SPAN = X1 - X0


def flash_frac(x):
    """Fraction of the cycle at which the pulse reaches x."""
    return TRAVEL * (x - X0) / SPAN


def gate(letter, x, y, color, begin, delay):
    f = flash_frac(x)
    a, b, c = round(f - 0.015, 4), round(f + 0.006, 4), round(f + 0.055, 4)
    kt = f"0;{a};{b};{c};1"
    return f'''    <g>
      <rect x="{x-16}" y="{y-15}" width="32" height="30" rx="7" fill="{color}" fill-opacity="0.1"
            stroke="{color}" stroke-opacity="0.45" stroke-width="1.2">
        <animate attributeName="fill-opacity" values="0.1;0.1;0.62;0.1;0.1" keyTimes="{kt}"
                 dur="{CYCLE}s" begin="{begin}s" repeatCount="indefinite"/>
        <animate attributeName="stroke-opacity" values="0.45;0.45;1;0.45;0.45" keyTimes="{kt}"
                 dur="{CYCLE}s" begin="{begin}s" repeatCount="indefinite"/>
      </rect>
      <text class="gate" x="{x}" y="{y+5}" fill="{color}">{letter}</text>
    </g>'''


def measure(y):
    x = X1
    return f'''    <g class="meas">
      <rect x="{x}" y="{y-15}" width="{MEAS_W}" height="30" rx="7"/>
      <path d="M {x+7} {y+7} A 8 8 0 0 1 {x+23} {y+7}" fill="none"/>
      <path d="M {x+15} {y+7} L {x+21} {y-3}" fill="none"/>
    </g>'''


parts = []
for i, (label, color, y, gates) in enumerate(LANES):
    begin = round(i * STAGGER, 3)
    parts.append(f'  <g class="lane">')
    # wire
    parts.append(f'    <line x1="{X0}" y1="{y}" x2="{X1}" y2="{y}" stroke="{color}" '
                 f'stroke-opacity="0.28" stroke-width="1.4"/>')
    # classical (double) line after measurement
    parts.append(f'    <line x1="{X1+MEAS_W}" y1="{y-2}" x2="{XEND}" y2="{y-2}" stroke="{color}" '
                 f'stroke-opacity="0.2" stroke-width="1"/>')
    parts.append(f'    <line x1="{X1+MEAS_W}" y1="{y+2}" x2="{XEND}" y2="{y+2}" stroke="{color}" '
                 f'stroke-opacity="0.2" stroke-width="1"/>')
    # qubit index + label
    parts.append(f'    <text class="qidx" x="36" y="{y+4}">q[{i}]</text>')
    parts.append(f'    <text class="lbl" x="152" y="{y+4}" fill="{color}">{label}</text>')
    for letter, x in gates:
        parts.append(gate(letter, x, y, color, begin, 0))
    parts.append(measure(y))
    # travelling pulse
    parts.append(f'''    <g filter="url(#glow)">
      <circle cx="{X0}" cy="{y}" r="4.5" fill="{color}">
        <animate attributeName="cx" values="{X0};{X1};{X1}" keyTimes="0;{TRAVEL};1"
                 dur="{CYCLE}s" begin="{begin}s" repeatCount="indefinite"/>
        <animate attributeName="opacity" values="0;1;1;0;0" keyTimes="0;0.03;{TRAVEL-0.03};{TRAVEL};1"
                 dur="{CYCLE}s" begin="{begin}s" repeatCount="indefinite"/>
      </circle>
    </g>''')
    parts.append('  </g>')

lanes_svg = "\n".join(parts)

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}"
     role="img" aria-label="Alexandru - TypeScript, Python, React, NestJS, Qiskit">
  <title>Alexandru - full-stack developer and quantum computing</title>
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#10102a"/>
      <stop offset="55%" stop-color="#141033"/>
      <stop offset="100%" stop-color="#1c1140"/>
    </linearGradient>
    <linearGradient id="name" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="70%" stop-color="#cbb6ff"/>
      <stop offset="100%" stop-color="#b088ff"/>
    </linearGradient>
    <filter id="glow" x="-120%" y="-120%" width="340%" height="340%">
      <feGaussianBlur stdDeviation="3.4" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>

  <style>
    text {{ font-family: ui-monospace, "SF Mono", "Cascadia Mono", Menlo, Consolas, monospace; }}
    .name {{ font-family: "Segoe UI", Inter, system-ui, -apple-system, "Helvetica Neue", sans-serif;
             font-size: 42px; font-weight: 700; letter-spacing: -0.5px; fill: url(#name); }}
    .kicker {{ font-size: 11.5px; letter-spacing: 3.4px; fill: #7e78b4; }}
    .sub {{ font-size: 13px; letter-spacing: 0.6px; fill: #9d95cf; }}
    .qidx {{ font-size: 11.5px; fill: #5d5790; letter-spacing: 0.5px; }}
    .lbl {{ font-size: 13px; font-weight: 600; text-anchor: end; letter-spacing: 0.3px; }}
    .gate {{ font-size: 13px; font-weight: 700; text-anchor: middle; }}
    .meas rect {{ fill: #2a2350; fill-opacity: 0.55; stroke: #6f68a8; stroke-opacity: 0.5; stroke-width: 1.2; }}
    .meas path {{ stroke: #a89fe0; stroke-width: 1.3; stroke-linecap: round; }}
    .cursor {{ fill: #b088ff; font-weight: 400; animation: blink 1.05s steps(1) infinite; }}
    @keyframes blink {{ 50% {{ opacity: 0; }} }}
    @media (prefers-reduced-motion: reduce) {{
      .cursor {{ animation: none; }}
    }}
  </style>

  <rect width="{W}" height="{H}" rx="16" fill="url(#bg)"/>
  <rect x="0.75" y="0.75" width="{W-1.5}" height="{H-1.5}" rx="15.25" fill="none"
        stroke="#463a7a" stroke-opacity="0.55"/>

  <text class="kicker" x="36" y="48">SOFTWARE ENGINEER</text>
  <text class="name" x="34" y="94">Alexandru<tspan class="cursor" dx="6">|</tspan></text>
  <text class="sub" x="36" y="118">TypeScript on the classical side, Qiskit on the other.</text>

{lanes_svg}
</svg>
'''

import os
os.makedirs("assets", exist_ok=True)
with open("assets/header.svg", "w", encoding="utf-8") as fh:
    fh.write(svg)
print(f"written: {len(svg)} bytes")
