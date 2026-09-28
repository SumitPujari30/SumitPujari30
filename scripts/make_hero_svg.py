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

# Fixed seed for consistent, beautiful binary layout
random.seed(1337)
binary_cols = []
col_xs = [28, 55, 88, 125, 160, 420, 455, 492, 525, 552]
for cx in col_xs:
    bits = [str(random.choice([0, 1])) for _ in range(8)]
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
          opacity: 0.97;
        }}
        50% {{
          filter: drop-shadow(0 0 5px #a5f3fc) drop-shadow(0 0 16px #38bdf8) drop-shadow(0 0 30px rgba(56, 189, 248, 0.9));
          opacity: 1;
        }}
      }}

      @keyframes bitPulse {{
        0%, 100% {{ opacity: 0.12; }}
        50% {{ opacity: 0.38; }}
      }}

      @keyframes chevronShimmer {{
        0%, 100% {{
          opacity: 0.82;
          filter: drop-shadow(0 0 4px rgba(56, 189, 248, 0.35));
        }}
        50% {{
          opacity: 1;
          filter: drop-shadow(0 0 10px rgba(56, 189, 248, 0.75));
        }}
      }}

      .neon-title {{
        font-family: 'SatisfyNeon', 'Segoe Script', 'Brush Script MT', cursive;
        font-size: 50px;
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

      .striped-chevron {{
        animation: chevronShimmer 3.5s ease-in-out infinite;
      }}
    </style>

    <!-- Linear gradient for chevrons -->
    <linearGradient id="chevGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#818cf8" stop-opacity="0.85" />
      <stop offset="50%" stop-color="#38bdf8" stop-opacity="1" />
      <stop offset="100%" stop-color="#0284c7" stop-opacity="0.85" />
    </linearGradient>

    <!-- Left chevron mask (angled sharp code chevron) -->
    <mask id="leftMask">
      <polygon points="42,80 90,26 114,26 66,80 114,134 90,134" fill="#ffffff" />
    </mask>

    <!-- Right chevron mask -->
    <mask id="rightMask">
      <polygon points="538,80 490,26 466,26 514,80 466,134 490,134" fill="#ffffff" />
    </mask>

    <!-- Vertical scanline stripes pattern -->
    <pattern id="vStripes" width="4" height="4" patternUnits="userSpaceOnUse">
      <line x1="1" y1="0" x2="1" y2="4" stroke="url(#chevGrad)" stroke-width="2" />
    </pattern>

    <!-- Ambient background spotlight behind text -->
    <radialGradient id="ambientSpot" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#0284c7" stop-opacity="0.25" />
      <stop offset="50%" stop-color="#0369a1" stop-opacity="0.08" />
      <stop offset="100%" stop-color="#0d1117" stop-opacity="0" />
    </radialGradient>
  </defs>

  <!-- Container Box (matches GitHub Dark theme card style) -->
  <rect x="1" y="1" width="{WIDTH - 2}" height="{HEIGHT - 2}" rx="12" fill="#0d1117" stroke="#21262d" stroke-width="1.2" />

  <!-- Ambient Blue Spotlight -->
  <rect x="80" y="10" width="420" height="140" fill="url(#ambientSpot)" />

  <!-- Binary Matrix Rain Columns -->
  <g class="bit-text">
'''

for idx, (cx, bits) in enumerate(binary_cols):
    delay = (idx * 0.35) % 2.8
    dur = 2.4 + (idx % 3) * 0.6
    svg += f'    <g style="animation: bitPulse {dur:.2f}s ease-in-out infinite; animation-delay: {delay:.2f}s;">\n'
    for b_idx, bit in enumerate(bits):
        by = 22 + b_idx * 16
        opacity = 0.08 + ((b_idx * 2 + idx) % 5) * 0.04
        svg += f'      <text x="{cx}" y="{by}" opacity="{opacity:.2f}">{bit}</text>\n'
    svg += '    </g>\n'

svg += f'''  </g>

  <!-- Left Striped Chevron -->
  <g class="striped-chevron" mask="url(#leftMask)">
    <rect x="30" y="15" width="95" height="130" fill="url(#vStripes)" />
  </g>

  <!-- Right Striped Chevron -->
  <g class="striped-chevron" mask="url(#rightMask)">
    <rect x="455" y="15" width="95" height="130" fill="url(#vStripes)" />
  </g>

  <!-- Center Content: Name & Status Badge -->
  <g>
    <!-- Glowing Neon Name -->
    <text x="290" y="84" class="neon-title">Sumit Pujari</text>

    <!-- Role Tech Tag -->
    <g transform="translate(147, 107)">
      <!-- Pill base -->
      <rect x="0" y="0" width="286" height="26" rx="13" fill="#090d16" stroke="#1e293b" stroke-width="1.2" />
      <rect x="1" y="1" width="284" height="24" rx="12" fill="none" stroke="#0ea5e9" stroke-width="0.8" opacity="0.45" />

      <!-- Pulsing live status dot -->
      <circle cx="16" cy="13" r="3.5" fill="#38bdf8">
        <animate attributeName="opacity" values="0.3;1;0.3" dur="2s" repeatCount="indefinite" />
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
