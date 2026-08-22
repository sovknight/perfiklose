import re

with open('index.html', 'r') as f:
    html = f.read()

# 1. Inject getUserMedia and takePhoto logic
camera_js = """
// ── In-App Camera Logic (V2) ───────────────────────────────────────────────
let videoStream = null;

async function startCamera() {
  const video = document.getElementById('viewfinder');
  try {
    if (videoStream) {
      videoStream.getTracks().forEach(t => t.stop());
    }
    const constraints = {
      video: {
        facingMode: 'environment', // back camera
        width: { ideal: 1920 },
        height: { ideal: 1080 }
      },
      audio: false
    };
    videoStream = await navigator.mediaDevices.getUserMedia(constraints);
    video.srcObject = videoStream;
    // Play is handled by autoplay, but just in case:
    await video.play().catch(e => console.warn('video play error', e));
  } catch (err) {
    console.error('Camera access denied or error:', err);
    toast('Camera access required!', 'err');
  }
}

// Start camera when DOM loads
window.addEventListener('load', () => {
  startCamera();
});

function takePhoto() {
  const video = document.getElementById('viewfinder');
  const canvas = document.getElementById('capture-canvas');
  if (!videoStream || video.videoWidth === 0) {
    toast('Camera not ready', 'err');
    return;
  }
  
  // Flash effect on video
  video.style.opacity = '0.2';
  setTimeout(() => video.style.opacity = '1', 100);
  
  const w = video.videoWidth;
  const h = video.videoHeight;
  
  // Set canvas dimensions to match video
  canvas.width = w;
  canvas.height = h;
  
  const ctx = canvas.getContext('2d');
  ctx.drawImage(video, 0, 0, w, h);
  
  // Convert to blob and add to queue
  canvas.toBlob(blob => {
    if (!blob) { toast('Capture failed', 'err'); return; }
    
    const existingNames = new Set(photos.map(p => p.name));
    let raw = 'photo.jpg';
    let base = 'photo';
    let n = raw;
    let counter = 1;
    while (existingNames.has(n)) {
      n = `${base}_${counter}.jpg`;
      counter++;
    }
    
    const p = {
      id:     'p' + Date.now() + '_' + Math.random().toString(36).slice(2, 8),
      name:   n,
      origSz: blob.size,
      compSz: 0,
      blob:   blob,
      comp:   null,
      url:    '',
      status: 'q'
    };
    photos.push(p);
    queue.push(p);
    render();
    runQueue();
  }, 'image/jpeg', 1.0); // full quality for raw capture, will be compressed by queue
}
"""

# Replace the saveAndEmailFlow and surrounding logic
pattern = r'// ── Save & Email \(Unified Flow\) ──.*?(?=function promptClear)'
replacement = camera_js + """
// ── 2-Step Export (V2) ─────────────────────────────────────────────────────
window.makeZip = async function(triggerDownloadFlag = false) {
  const readyPhotos = photos.filter(p => p.status === 'ok' && p.comp);
  if (!readyPhotos.length) { toast('No compressed photos ready yet', 'err'); return; }

  toast('Preparing ZIP…');
  const z = new JSZip();
  const f = z.folder(folderName);
  const usedNames = new Set();
  readyPhotos.forEach((p, idx) => {
    let fileName = p.name || `photo_${idx + 1}.jpg`;
    let finalName = fileName;
    let counter = 1;
    const dot = fileName.lastIndexOf('.');
    const base = dot > -1 ? fileName.slice(0, dot) : fileName;
    const ext = dot > -1 ? fileName.slice(dot) : '.jpg';
    while (usedNames.has(finalName)) {
      finalName = `${base}_${counter}${ext}`;
      counter++;
    }
    usedNames.add(finalName);
    f.file(finalName, p.comp);
  });
  
  const zipBlob = await z.generateAsync({ type: 'blob' });
  const zipFileName = folderName + '.zip';
  
  if (triggerDownloadFlag) {
    triggerDownload(zipBlob, zipFileName);
    toast('✅ ZIP saved!', 'ok');
  }
  
  return zipBlob;
};

// Make sure global makeZip uses this new version.
"""
html = re.sub(pattern, replacement, html, flags=re.DOTALL)

# Delete the old makeZip function since we redefine it.
old_makeZip_pattern = r'async function makeZip\(\) \{[\s\S]*?return z\.generateAsync\(\{ type: \'blob\' \}\);\n\}'
html = re.sub(old_makeZip_pattern, '', html)

with open('index.html', 'w') as f:
    f.write(html)
