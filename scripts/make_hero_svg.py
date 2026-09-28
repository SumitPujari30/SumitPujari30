import base64
import urllib.request
import random
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "hero-banner.svg")

# Fetch Satisfy woff2 from Google Fonts CDN
url = "https://fonts.gstatic.com/s/satisfy/v22/rP2Hp2yn6lkG50LoCZOIHQ.woff2"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
satisfy_woff2 = urllib.request.urlopen(req).read()
satisfy_b64 = base64.b64encode(satisfy_woff2).decode('utf-8')

WIDTH = 580
HEIGHT = 160
CX = WIDTH // 2  # 290
CY = 78

# Left Chevron geometry: apex at (95, CY), expands to x=155
# Outer: (95, CY) to (142, CY - 46) and (142, CY + 46)
# Inner: (113, CY) to (160, CY - 46) and (160, CY + 46)
slope = 46.0 / 47.0  # ~0.978
left_lines = []
for x in range(95, 161, 4):
    y_outer_top = CY - (x - 95) * slope if x <= 142 else CY - 46
    y_outer_bot = CY + (x - 95) * slope if x <= 142 else CY + 46
    if x < 113:
        left_lines.append((x, y_outer_top, y_outer_bot))
    else:
        y_inner_top = CY - (x - 113) * slope
        y_inner_bot = CY + (x - 113) * slope
        left_lines.append((x, y_outer_top, y_inner_top))
        left_lines.append((x, y_inner_bot, y_outer_bot))

# Right Chevron: symmetrically mirrored across CX = 290
right_lines = []
for (lx, ly1, ly2) in left_lines:
    rx = WIDTH - lx
    right_lines.append((rx, ly1, ly2))

# Binary columns across background
random.seed(2026)
col_xs = [25, 52, 78, 105, 132, 160, 185, 395, 420, 448, 475, 502, 528, 555]
binary_cols = []
for cx in col_xs:
    bits = []
    for row in range(8):
        val = str(random.choice([0, 1]))
        is_highlight = random.random() < 0.12
        bits.append((val, is_highlight))
    binary_cols.append((cx, bits))

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {HEIGHT}" width="100%" style="background: transparent;">
  <defs>
    <style>
      @font-face {{
        font-family: 'SatisfyNeon';
        src: url(data:font/woff2;base64,{satisfy_b64}) format('woff2');
        font-weight: normal;
        font-style: normal;
      }}

      /* Refined, crisp neon glow without heavy hazy cloud */
      @keyframes neonSubtle {{
        0%, 100% {{
          filter: drop-shadow(0 0 2px #38bdf8) drop-shadow(0 0 5px rgba(14, 165, 233, 0.45));
          opacity: 0.98;
        }}
        50% {{
          filter: drop-shadow(0 0 2.5px #67e8f9) drop-shadow(0 0 7px rgba(56, 189, 248, 0.6));
          opacity: 1;
        }}
      }}

      @keyframes bitPulse {{
        0%, 100% {{ opacity: 0.12; }}
        50% {{ opacity: 0.35; }}
      }}

      @keyframes chevronShimmer {{
        0%, 100% {{
          opacity: 0.85;
          filter: drop-shadow(0 0 3px rgba(56, 189, 248, 0.4));
        }}
        50% {{
          opacity: 1;
          filter: drop-shadow(0 0 6px rgba(56, 189, 248, 0.75));
        }}
      }}

      .neon-title {{
        font-family: 'SatisfyNeon', 'Segoe Script', 'Brush Script MT', cursive;
        font-size: 50px;
        fill: #ffffff;
        text-anchor: middle;
        animation: neonSubtle 3.5s ease-in-out infinite;
      }}

      .role-tag {{
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Inter', 'Roboto', sans-serif;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 2.8px;
        text-transform: uppercase;
        fill: #38bdf8;
        text-anchor: middle;
      }}

      .bit-text {{
        font-family: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace;
        font-size: 11px;
        fill: #38bdf8;
        letter-spacing: 2px;
      }}

      .chevrons {{
        animation: chevronShimmer 3s ease-in-out infinite;
      }}
    </style>

    <!-- Linear gradient for chevrons -->
    <linearGradient id="chevGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#818cf8" stop-opacity="0.9" />
      <stop offset="50%" stop-color="#38bdf8" stop-opacity="1" />
      <stop offset="100%" stop-color="#0284c7" stop-opacity="0.85" />
    </linearGradient>

    <!-- Subtle, gentle center illumination (no heavy fog) -->
    <radialGradient id="centerGlow" cx="50%" cy="48%" r="45%">
      <stop offset="0%" stop-color="#0284c7" stop-opacity="0.10" />
      <stop offset="60%" stop-color="#0369a1" stop-opacity="0.03" />
      <stop offset="100%" stop-color="#0d1117" stop-opacity="0" />
    </radialGradient>
  </defs>

  <!-- Ambient Backdrop -->
  <rect x="0" y="0" width="{WIDTH}" height="{HEIGHT}" rx="14" fill="url(#centerGlow)" />

  <!-- Binary Matrix Rain Columns -->
  <g class="bit-text">
'''

for idx, (cx, bits) in enumerate(binary_cols):
    delay = (idx * 0.28) % 2.4
    dur = 2.4 + (idx % 3) * 0.5
    svg += f'    <g style="animation: bitPulse {dur:.2f}s ease-in-out infinite; animation-delay: {delay:.2f}s;">\n'
    for b_idx, (bit, is_hi) in enumerate(bits):
        by = 22 + b_idx * 16
        if is_hi:
            fill_color = "#67e8f9"
            opacity = 0.45
        else:
            fill_color = "#38bdf8"
            opacity = 0.07 + ((b_idx * 2 + idx) % 5) * 0.03
        svg += f'      <text x="{cx}" y="{by}" fill="{fill_color}" opacity="{opacity:.2f}">{bit}</text>\n'
    svg += '    </g>\n'

svg += '''  </g>

  <!-- Left Striped Chevron (Right beside name) -->
  <g class="chevrons">
'''

for (lx, ly1, ly2) in left_lines:
    svg += f'    <line x1="{lx}" y1="{ly1:.1f}" x2="{lx}" y2="{ly2:.1f}" stroke="url(#chevGrad)" stroke-width="2.2" stroke-linecap="round" />\n'

svg += '''  </g>

  <!-- Right Striped Chevron (Right beside name) -->
  <g class="chevrons">
'''

for (rx, ry1, ry2) in right_lines:
    svg += f'    <line x1="{rx}" y1="{ry1:.1f}" x2="{rx}" y2="{ry2:.1f}" stroke="url(#chevGrad)" stroke-width="2.2" stroke-linecap="round" />\n'

svg += f'''  </g>

  <!-- Center Content: Crisp Name & Status Badge -->
  <g>
    <!-- Crisp Neon Name -->
    <text x="{CX}" y="82" class="neon-title">Sumit Pujari</text>

    <!-- Role Tech Tag -->
    <g transform="translate({CX - 138}, 104)">
      <!-- Pill base -->
      <rect x="0" y="0" width="276" height="24" rx="12" fill="#0b1120" fill-opacity="0.85" stroke="#1e293b" stroke-width="1.2" />
      <rect x="1" y="1" width="274" height="22" rx="11" fill="none" stroke="#38bdf8" stroke-width="0.8" stroke-opacity="0.4" />

      <!-- Pulsing live status beacon -->
      <circle cx="15" cy="12" r="3" fill="#38bdf8">
        <animate attributeName="opacity" values="0.3;1;0.3" dur="2s" repeatCount="indefinite" />
      </circle>
      <circle cx="15" cy="12" r="6" fill="none" stroke="#38bdf8" stroke-width="0.7">
        <animate attributeName="r" values="3;7" dur="2s" repeatCount="indefinite" />
        <animate attributeName="opacity" values="0.7;0" dur="2s" repeatCount="indefinite" />
      </circle>

      <!-- Subtitle text -->
      <text x="145" y="15.8" class="role-tag">Forward Deployed Engineer</text>
    </g>
  </g>
</svg>
'''

with open(OUT, "w", encoding="utf-8") as f:
    f.write(svg)

print(f"Generated {OUT} successfully! Size: {len(svg)} bytes")
