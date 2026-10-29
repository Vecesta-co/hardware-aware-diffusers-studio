import json
import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Optional
from src.hardware import HardwareProfiler
from src.generator import DiffusersGenerator
from src.models import GenerationRequest

STUDIO_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Diffusers Studio — Hardware-Aware</title>
  <style>
    body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #090d16; color: #f1f5f9; margin: 0; padding: 2rem; }
    .container { max-width: 1100px; margin: 0 auto; }
    h1 { color: #38bdf8; margin: 0 0 0.5rem 0; }
    .subtitle { color: #94a3b8; margin-bottom: 1.5rem; font-size: 0.95rem; }
    .hw-badge { display: inline-block; background: #1e293b; border: 1px solid #334155; padding: 0.4rem 0.8rem; border-radius: 6px; font-size: 0.85rem; margin-bottom: 2rem; }
    .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; }
    .panel { background: #131b2e; border: 1px solid #1e293b; border-radius: 12px; padding: 1.5rem; }
    label { display: block; font-size: 0.85rem; color: #94a3b8; margin-bottom: 0.5rem; text-transform: uppercase; }
    textarea, input, select { width: 100%; box-sizing: border-box; background: #090d16; border: 1px solid #334155; border-radius: 6px; color: #f8fafc; padding: 0.75rem; margin-bottom: 1rem; }
    button { width: 100%; background: #0284c7; color: white; border: none; padding: 0.9rem; border-radius: 6px; font-weight: bold; cursor: pointer; font-size: 1rem; transition: background 0.2s; }
    button:hover { background: #0369a1; }
    #previewBox { width: 100%; min-height: 350px; background: #090d16; border: 2px dashed #334155; border-radius: 8px; display: flex; align-items: center; justify-content: center; overflow: hidden; }
    #previewImg { max-width: 100%; max-height: 450px; border-radius: 6px; display: none; }
    .telemetry { margin-top: 1rem; font-size: 0.85rem; color: #94a3b8; background: #090d16; padding: 0.75rem; border-radius: 6px; }
  </style>
</head>
<body>
  <div class="container">
    <h1>Diffusers Studio</h1>
    <div class="subtitle">Hardware-Aware Stable Diffusion Playground &bull; Vecesta.co</div>
    <div id="hwBadge" class="hw-badge">Probing hardware accelerator...</div>
    <div class="grid">
      <div class="panel">
        <label>Prompt</label>
        <textarea id="promptInput" rows="4" placeholder="A futuristic cybernetic garden at sunset, neon waterfalls, 8k resolution..."></textarea>
        <label>Aspect Ratio</label>
        <select id="resSelect">
          <option value="512x512">Square (512x512)</option>
          <option value="768x512">Landscape (768x512)</option>
          <option value="512x768">Portrait (512x768)</option>
        </select>
        <label>Sampling Steps</label>
        <input id="stepsInput" type="number" min="5" max="50" value="20" />
        <button id="genBtn" onclick="generate()">Generate Image</button>
      </div>
      <div class="panel">
        <label>Generated Canvas</label>
        <div id="previewBox">
          <span id="placeholderText" style="color: #64748b;">Generated image will appear here</span>
          <img id="previewImg" alt="Generated Canvas" />
        </div>
        <div id="telemetryBox" class="telemetry">Status: Idle</div>
      </div>
    </div>
  </div>
  <script>
    fetch('/api/hardware').then(r=>r.json()).then(hw=>{
      document.getElementById('hwBadge').innerHTML = `<b>Device:</b> ${hw.device.toUpperCase()} (${hw.device_name}) &bull; <b>Precision:</b> ${hw.recommended_precision.toUpperCase()} &bull; <b>RAM:</b> ${hw.ram_gb} GB`;
    });
    function generate() {
      const prompt = document.getElementById('promptInput').value || 'A mystical cosmic forest';
      const [w, h] = document.getElementById('resSelect').value.split('x').map(Number);
      const steps = Number(document.getElementById('stepsInput').value) || 20;
      const btn = document.getElementById('genBtn');
      const tel = document.getElementById('telemetryBox');
      btn.disabled = true;
      btn.innerText = 'Synthesizing...';
      tel.innerText = 'Generating latent image with hardware profiling...';

      fetch('/api/generate', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({prompt, width: w, height: h, steps})
      }).then(r=>r.json()).then(res=>{
        btn.disabled = false;
        btn.innerText = 'Generate Image';
        if (res.output_path) {
          const img = document.getElementById('previewImg');
          img.src = '/image?path=' + encodeURIComponent(res.output_path);
          img.style.display = 'block';
          document.getElementById('placeholderText').style.display = 'none';
          tel.innerText = `Generated in ${res.elapsed_seconds}s on ${res.device_used.toUpperCase()} (${res.precision_used}) | Seed: ${res.seed}`;
        }
      }).catch(err=>{
        btn.disabled = false;
        btn.innerText = 'Generate Image';
        tel.innerText = 'Error: ' + err;
      });
    }
  </script>
</body>
</html>
"""

class StudioHTTPHandler(BaseHTTPRequestHandler):
    generator: DiffusersGenerator = None

    def _send_json(self, status: int, data: dict):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

    def do_GET(self):
        if self.path in ("/", "/studio"):
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(STUDIO_HTML.encode("utf-8"))

        elif self.path == "/api/hardware":
            self._send_json(200, self.generator.hardware.model_dump())

        elif self.path.startswith("/image?path="):
            img_path = self.path.split("/image?path=", 1)[1]
            if os.path.exists(img_path):
                self.send_response(200)
                self.send_header("Content-Type", "image/png")
                self.end_headers()
                with open(img_path, "rb") as f:
                    self.wfile.write(f.read())
            else:
                self._send_json(404, {"error": "Image not found"})

        elif self.path == "/health":
            self._send_json(200, {"status": "ok", "service": "hardware-aware-diffusers-studio"})

        else:
            self._send_json(404, {"error": "Not found"})

    def do_POST(self):
        if self.path == "/api/generate":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            data = json.loads(body) if body else {}

            req = GenerationRequest(
                prompt=data.get("prompt", "A cinematic scene"),
                width=int(data.get("width", 512)),
                height=int(data.get("height", 512)),
                steps=int(data.get("steps", 20)),
                seed=data.get("seed"),
            )
            result = self.generator.generate(req)
            self._send_json(200, result.model_dump())
        else:
            self._send_json(404, {"error": "Not found"})

    def log_message(self, format, *args):
        pass

def run_studio(generator: Optional[DiffusersGenerator] = None, host: str = "127.0.0.1", port: int = 7860, background: bool = False) -> HTTPServer:
    gen = generator or DiffusersGenerator()
    handler = StudioHTTPHandler
    handler.generator = gen
    server = HTTPServer((host, port), handler)

    if background:
        t = threading.Thread(target=server.serve_forever, daemon=True)
        t.start()
        return server
    else:
        print(f"Diffusers Studio Web UI running at http://{host}:{port}")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down studio...")
            server.shutdown()
        return server
