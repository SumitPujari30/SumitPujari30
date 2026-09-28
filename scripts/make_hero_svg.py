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

WIDTH = 620
HEIGHT = 170

# Chevron geometry
# Left chevron: apex at (50, 82), expands to x=122
# Slope: (138 - 82) / (122 - 50) = 56 / 72 = 0.7778
left_lines = []
for x in range(48, 126, 4):
    y_outer_top = 82 - (x - 48) * 0.78
    y_outer_bot = 82 + (x - 48) * 0.78
    if x < 72:
        left_lines.append((x, y_outer_top, y_outer_bot))
    else:
        y_inner_top = 82 - (x - 72) * 0.78
        y_inner_bot = 82 + (x - 72) * 0.78
        left_lines.append((x, y_outer_top, y_inner_top))
        left_lines.append((x, y_inner_bot, y_outer_bot))

# Right chevron: mirrored across center x=310
# Center = 310. Left apex is at 48 (offset from center = 262). Right apex is at 310 + 262 = 572.
right_lines = []
for (lx, ly1, ly2) in left_lines:
    rx = 620 - lx
    right_lines.append((rx, ly1, ly2))

# Binary columns across the full canvas width
random.seed(2026)
col_xs = [20, 45, 75, 105, 135, 165, 195, 230, 390, 425, 455, 485, 515, 545, 575, 600]
binary_cols = []
for cx in col_xs:
    bits = []
    for row in range(9):
        val = str(random.choice([0, 1]))
        is_highlight = random.random() < 0.15
        bits.append((val, is_highlight))
    binary_cols.append((cx, bits))

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {HEIGHT}" width="100%" height="{HEIGHT}" style="background: transparent;">
  <defs>
    <style>
      @font-face {{
        font-family: 'SatisfyNeon';
        src: url(data:font/woff2;base64,{satisfy_b64}) format('woff2');
        font-weight: normal;
        font-style: normal;
      }}

      @keyframes neonGlow {{
        0%, 100% {{
          filter: drop-shadow(0 0 3px #67e8f9) drop-shadow(0 0 10px #0ea5e9) drop-shadow(0 0 22px rgba(14, 165, 233, 0.65));
          opacity: 0.98;
        }}
        50% {{
          filter: drop-shadow(0 0 5px #a5f3fc) drop-shadow(0 0 16px #38bdf8) drop-shadow(0 0 32px rgba(56, 189, 248, 0.95));
          opacity: 1;
        }}
      }}

      @keyframes bitPulse {{
        0%, 100% {{ opacity: 0.15; }}
        50% {{ opacity: 0.45; }}
      }}

      @keyframes chevronShimmer {{
        0%, 100% {{
          opacity: 0.85;
          filter: drop-shadow(0 0 4px rgba(56, 189, 248, 0.4));
        }}
        50% {{
          opacity: 1;
          filter: drop-shadow(0 0 10px rgba(56, 189, 248, 0.85));
        }}
      }}

      .neon-title {{
        font-family: 'SatisfyNeon', 'Segoe Script', 'Brush Script MT', cursive;
        font-size: 52px;
        fill: #f0f9ff;
        text-anchor: middle;
        animation: neonGlow 3.5s ease-in-out infinite;
      }}

      .role-tag {{
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Inter', 'Roboto', sans-serif;
        font-size: 11.5px;
        font-weight: 700;
        letter-spacing: 3px;
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

    <!-- Ambient Center Bloom (fades seamlessly into any GitHub theme) -->
    <radialGradient id="centerGlow" cx="50%" cy="48%" r="48%">
      <stop offset="0%" stop-color="#0284c7" stop-opacity="0.32" />
      <stop offset="45%" stop-color="#0369a1" stop-opacity="0.12" />
      <stop offset="85%" stop-color="#0f172a" stop-opacity="0.04" />
      <stop offset="100%" stop-color="#0f172a" stop-opacity="0" />
    </radialGradient>

    <!-- Fine grid pattern for cyber texture -->
    <pattern id="cyberGrid" width="24" height="24" patternUnits="userSpaceOnUse">
      <path d="M 24 0 L 0 0 0 24" fill="none" stroke="#38bdf8" stroke-width="0.5" stroke-opacity="0.06" />
    </pattern>
  </defs>

  <!-- Seamless Ambient Backdrop (No harsh box border!) -->
  <rect x="0" y="0" width="{WIDTH}" height="{HEIGHT}" rx="16" fill="url(#centerGlow)" />
  <rect x="0" y="0" width="{WIDTH}" height="{HEIGHT}" rx="16" fill="url(#cyberGrid)" />

  <!-- Subtle Cyber Corner Accents -->
  <g stroke="#38bdf8" stroke-width="1.2" stroke-opacity="0.3" fill="none">
    <!-- Top-left -->
    <path d="M 8 24 L 8 8 L 24 8" />
    <!-- Top-right -->
    <path d="M {WIDTH - 24} 8 L {WIDTH - 8} 8 L {WIDTH - 8} 24" />
    <!-- Bottom-left -->
    <path d="M 8 {HEIGHT - 24} L 8 {HEIGHT - 8} L 24 {HEIGHT - 8}" />
    <!-- Bottom-right -->
    <path d="M {WIDTH - 24} {HEIGHT - 8} L {WIDTH - 8} {HEIGHT - 8} L {WIDTH - 8} {HEIGHT - 24}" />
  </g>

  <!-- Binary Matrix Rain Columns (Floating across entire background) -->
  <g class="bit-text">
'''

for idx, (cx, bits) in enumerate(binary_cols):
    delay = (idx * 0.3) % 2.5
    dur = 2.2 + (idx % 4) * 0.5
    svg += f'    <g style="animation: bitPulse {dur:.2f}s ease-in-out infinite; animation-delay: {delay:.2f}s;">\n'
    for b_idx, (bit, is_hi) in enumerate(bits):
        by = 18 + b_idx * 16
        if is_hi:
            fill_color = "#67e8f9"
            opacity = 0.65
        else:
            fill_color = "#38bdf8"
            opacity = 0.08 + ((b_idx * 2 + idx) % 5) * 0.04
        svg += f'      <text x="{cx}" y="{by}" fill="{fill_color}" opacity="{opacity:.2f}">{bit}</text>\n'
    svg += '    </g>\n'

svg += '''  </g>

  <!-- Left Striped Chevron (Direct scanlines for 100% reliable rendering) -->
  <g class="chevrons">
'''

for (lx, ly1, ly2) in left_lines:
    svg += f'    <line x1="{lx}" y1="{ly1:.1f}" x2="{lx}" y2="{ly2:.1f}" stroke="url(#chevGrad)" stroke-width="2.4" stroke-linecap="round" />\n'

svg += '''  </g>

  <!-- Right Striped Chevron -->
  <g class="chevrons">
'''

for (rx, ry1, ry2) in right_lines:
    svg += f'    <line x1="{rx}" y1="{ry1:.1f}" x2="{rx}" y2="{ry2:.1f}" stroke="url(#chevGrad)" stroke-width="2.4" stroke-linecap="round" />\n'

svg += f'''  </g>

  <!-- Center Content: Name & Status Badge -->
  <g>
    <!-- Glowing Neon Name -->
    <text x="310" y="86" class="neon-title">Sumit Pujari</text>

    <!-- Role Tech Tag -->
    <g transform="translate(167, 110)">
      <!-- Glassmorphic pill base -->
      <rect x="0" y="0" width="286" height="26" rx="13" fill="#0b1120" fill-opacity="0.82" stroke="#1e293b" stroke-width="1.2" />
      <rect x="1" y="1" width="284" height="24" rx="12" fill="none" stroke="#38bdf8" stroke-width="0.8" stroke-opacity="0.45" />

      <!-- Pulsing live status beacon -->
      <circle cx="16" cy="13" r="3.5" fill="#38bdf8">
        <animate attributeName="opacity" values="0.3;1;0.3" dur="2s" repeatCount="indefinite" />
      </circle>
      <circle cx="16" cy="13" r="7" fill="none" stroke="#38bdf8" stroke-width="0.8">
        <animate attributeName="r" values="3.5;8" dur="2s" repeatCount="indefinite" />
        <animate attributeName="opacity" values="0.8;0" dur="2s" repeatCount="indefinite" />
      </circle>

      <!-- Subtitle text -->
      <text x="151" y="17" class="role-tag">Forward Deployed Engineer</text>
    </g>
  </g>
</svg>
'''

with open(OUT, "w", encoding="utf-8") as f:
    f.write(svg)

print(f"Generated {OUT} successfully! Size: {len(svg)} bytes")
