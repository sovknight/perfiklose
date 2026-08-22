import re

with open('index.html', 'r') as f:
    html = f.read()

# 1. Add video viewfinder above the Hero card
video_html = """
  <!-- ── In-App Camera Viewfinder ── -->
  <section class="hero-card overflow-hidden relative" style="border-radius:20px;padding:.5rem;display:flex;flex-direction:column;align-items:center;background:#000;">
    <video id="viewfinder" autoplay playsinline style="width:100%;border-radius:16px;background:#111;aspect-ratio:3/4;object-fit:cover;"></video>
    <canvas id="capture-canvas" style="display:none;"></canvas>
  </section>
"""
html = html.replace('<!-- ── Hero Stats Card ── -->', video_html + '\n  <!-- ── Hero Stats Card ── -->')

# 2. Modify Fixed Bottom Dock
dock_html = """
<!-- ══ Fixed Bottom Dock (V2) ══ -->
<div style="position:fixed;bottom:0;left:0;width:100%;z-index:50;
            display:flex;flex-direction:column;align-items:center;gap:.5rem;
            padding:1rem 1.25rem calc(1rem + var(--safe));
            background:linear-gradient(to top, rgba(0,0,0,.95) 70%, transparent);
            pointer-events:none;">

  <!-- Row 1: Shutter Button -->
  <div style="display:flex;justify-content:center;align-items:center;gap:.875rem;width:100%;margin-bottom:.5rem;">
    <button id="shutterBtn" onclick="takePhoto()" class="neon-btn"
           style="pointer-events:auto;display:flex;align-items:center;justify-content:center;gap:.5rem;
                  width:72px;height:72px;border-radius:50%;
                  background:#fff;color:#0058bc;
                  border:4px solid rgba(255,255,255,.2);
                  cursor:pointer;box-shadow:0 0 20px rgba(255,255,255,.3);">
      <span class="material-symbols-outlined filled" style="color:#0058bc;font-size:2rem;">camera</span>
    </button>
  </div>

  <!-- Row 2: 2-Step Export Dock -->
  <div style="display:flex;justify-content:space-between;align-items:center;gap:.5rem;width:100%;max-width:320px;">
    <button id="saveZipBtn" onclick="makeZip(true)" class="neon-btn"
            style="pointer-events:auto;display:flex;align-items:center;justify-content:center;flex:1;
                   padding:.75rem 0;border-radius:999px;
                   background:#0058bc;color:#fff;
                   font-weight:700;font-size:.85rem;letter-spacing:.05em;text-transform:uppercase;
                   border:none;cursor:pointer;font-family:inherit;">
      <span class="material-symbols-outlined" style="color:#fff;font-size:1.2rem;margin-right:.25rem;">download</span>
      1. Save ZIP
    </button>
    <button id="openEmailBtn" onclick="window.location.href='mailto:'" class="glass-card"
            style="pointer-events:auto;display:flex;align-items:center;justify-content:center;flex:1;
                   padding:.75rem 0;border-radius:999px;
                   background:rgba(255,255,255,.1);color:#fff;
                   font-weight:700;font-size:.85rem;letter-spacing:.05em;text-transform:uppercase;
                   border:1px solid rgba(255,255,255,.2);cursor:pointer;font-family:inherit;">
      <span class="material-symbols-outlined" style="color:#fff;font-size:1.2rem;margin-right:.25rem;">mail</span>
      2. Open Mail
    </button>
  </div>
</div>
"""
# Replace the old dock
html = re.sub(r'<!-- ══ Fixed Bottom Dock ══ -->.*?<!-- ══ Settings Modal ══ -->', dock_html + '\n\n<!-- ══ Settings Modal ══ -->', html, flags=re.DOTALL)

with open('index.html', 'w') as f:
    f.write(html)
