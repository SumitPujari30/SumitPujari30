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

WIDTH = 600
HEIGHT = 165
CX = WIDTH // 2  # 300
CY = 80

# Chevrons flanking the name
# Left Chevron: apex at (75, CY), expands to x=135
slope = 46.0 / 46.0  # 1.0
left_lines = []
for x in range(75, 140, 4):
    y_outer_top = CY - (x - 75) * slope if x <= 121 else CY - 46
    y_outer_bot = CY + (x - 75) * slope if x <= 121 else CY + 46
    if x < 94:
        left_lines.append((x, y_outer_top, y_outer_bot))
    else:
        y_inner_top = CY - (x - 94) * slope
        y_inner_bot = CY + (x - 94) * slope
        left_lines.append((x, y_outer_top, y_inner_top))
        left_lines.append((x, y_inner_bot, y_outer_bot))

# Right Chevron: symmetrically mirrored across CX = 300
right_lines = []
for (lx, ly1, ly2) in left_lines:
    rx = WIDTH - lx
    right_lines.append((rx, ly1, ly2))

# Binary Matrix covering the FULL SECTION
random.seed(42)
col_xs = list(range(14, WIDTH - 6, 20))  # 29 columns from x=14 to x=574
row_ys = list(range(16, HEIGHT, 15))    # 10 rows from y=16 to y=151

matrix_cols = []
for c_idx, cx in enumerate(col_xs):
    col_bits = []
    for r_idx, by in enumerate(row_ys):
        val = str(random.choice([0, 1]))
        # Is this directly behind the center name text?
        in_center_text = (CX - 150 <= cx <= CX + 150) and (48 <= by <= 120)
        is_highlight = (not in_center_text) and (random.random() < 0.14)
        if in_center_text:
            opacity = 0.05 + random.random() * 0.04
            color = "#0284c7"
        elif is_highlight:
            opacity = 0.55 + random.random() * 0.25
            color = "#67e8f9"
        else:
            opacity = 0.10 + random.random() * 0.18
            color = "#38bdf8"
        col_bits.append((by, val, opacity, color, is_highlight))
    matrix_cols.append((cx, col_bits))

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {HEIGHT}" width="100%" style="background: transparent;">
  <defs>
    <style>
      @font-face {{
        font-family: 'SatisfyNeon';
        src: url(data:font/woff2;base64,{satisfy_b64}) format('woff2');
        font-weight: normal;
        font-style: normal;
      }}

      /* Refined, clean neon glow */
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
        0%, 100% {{ opacity: 0.25; }}
        50% {{ opacity: 0.85; }}
      }}

      @keyframes chevronShimmer {{
        0%, 100% {{
          opacity: 0.85;
          filter: drop-shadow(0 0 4px rgba(56, 189, 248, 0.4));
        }}
        50% {{
          opacity: 1;
          filter: drop-shadow(0 0 7px rgba(56, 189, 248, 0.8));
        }}
      }}

      .neon-title {{
        font-family: 'SatisfyNeon', 'Segoe Script', 'Brush Script MT', cursive;
        font-size: 52px;
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
        font-size: 11.5px;
        letter-spacing: 1px;
      }}

      .chevrons {{
        animation: chevronShimmer 3s ease-in-out infinite;
      }}
    </style>

    <!-- Subtle, gentle center bloom -->
    <radialGradient id="centerGlow" cx="50%" cy="48%" r="48%">
      <stop offset="0%" stop-color="#0284c7" stop-opacity="0.12" />
      <stop offset="65%" stop-color="#0369a1" stop-opacity="0.03" />
      <stop offset="100%" stop-color="#0d1117" stop-opacity="0" />
    </radialGradient>
  </defs>

  <!-- Ambient Backdrop -->
  <rect x="0" y="0" width="{WIDTH}" height="{HEIGHT}" rx="14" fill="url(#centerGlow)" />

  <!-- Binary Matrix Rain Columns (Covering Entire Section) -->
  <g class="bit-text">
'''

for idx, (cx, bits) in enumerate(matrix_cols):
    delay = (idx * 0.17) % 2.5
    dur = 2.0 + (idx % 4) * 0.5
    svg += f'    <g style="animation: bitPulse {dur:.2f}s ease-in-out infinite; animation-delay: {delay:.2f}s;">\n'
    for (by, bit, op, col, is_hi) in bits:
        svg += f'      <text x="{cx}" y="{by}" fill="{col}" opacity="{op:.2f}">{bit}</text>\n'
    svg += '    </g>\n'

svg += '''  </g>

  <!-- Left Striped Chevron (Direct high-contrast colors) -->
  <g class="chevrons">
'''

for (lx, ly1, ly2) in left_lines:
    svg += f'    <line x1="{lx}" y1="{ly1:.1f}" x2="{lx}" y2="{ly2:.1f}" stroke="#38bdf8" stroke-width="2.4" stroke-linecap="round" />\n'

svg += '''  </g>

  <!-- Right Striped Chevron (Direct high-contrast colors) -->
  <g class="chevrons">
'''

for (rx, ry1, ry2) in right_lines:
    svg += f'    <line x1="{rx}" y1="{ry1:.1f}" x2="{rx}" y2="{ry2:.1f}" stroke="#38bdf8" stroke-width="2.4" stroke-linecap="round" />\n'

svg += f'''  </g>

  <!-- Center Content: Crisp Name & Status Badge -->
  <g>
    <!-- Crisp Neon Name -->
    <text x="{CX}" y="84" class="neon-title">Sumit Pujari</text>

    <!-- Role Tech Tag -->
    <g transform="translate({CX - 138}, 107)">
      <!-- Pill base -->
      <rect x="0" y="0" width="276" height="24" rx="12" fill="#0b1120" fill-opacity="0.88" stroke="#1e293b" stroke-width="1.2" />
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

print(f"Generated {OUT} successfully! Size: {len(svg)} bytes, cols: {len(matrix_cols)}, rows: {len(row_ys)}")
