import os
import requests
import sys

# --- Configuration ---
PROJECT_DIR = "tools/cam3"
ASSETS_DIR = os.path.join(PROJECT_DIR, "assets")

# MediaPipe Assets (Standard Google CDN)
MEDIAPIPE_ASSETS = {
    "face_mesh.js": "https://cdn.jsdelivr.net/npm/@mediapipe/face_mesh/face_mesh.js",
    "face_mesh.wasm": "https://cdn.jsdelivr.net/npm/@mediapipe/face_mesh/face_mesh.wasm",
    "face_mesh.binarypb": "https://cdn.jsdelivr.net/npm/@mediapipe/face_mesh/face_mesh.binarypb",
}

# --- HTML/JS/CSS Content (Advanced Architecture) ---
HTML_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CAM3 | Omni-Surveillance</title>
    <style>
        :root { --primary: #00ff41; --bg: #0d0d0d; --panel-bg: rgba(20, 20, 20, 0.95); --danger: #ff3333; --mute: #ffae00; }
        body { margin: 0; background: var(--bg); color: var(--primary); font-family: 'Consolas', 'Monaco', monospace; overflow: hidden; }
        
        /* Layout Grid for Multi-Camera */
        #view-container { 
            display: grid; width: 100vw; height: 100vh; 
            grid-template-columns: 1fr; grid-template-rows: 1fr; 
            background: #000;
        }
        .cam-wrapper { position: relative; width: 100%; height: 100%; overflow: hidden; border: 1px solid #333; }
        
        /* Dual View Mode */
        body.dual-mode #view-container { grid-template-rows: 50% 50%; }
        @media (min-width: 768px) { body.dual-mode #view-container { grid-template-columns: 50% 50%; grid-template-rows: 1fr; } }

        video { width: 100%; height: 100%; object-fit: cover; }
        canvas { position: absolute; top: 0; left: 0; width: 100%; height: 100%; object-fit: cover; }

        /* HUD & UI */
        .hud-overlay { position: absolute; top: 10px; left: 10px; z-index: 10; font-size: 12px; text-shadow: 0 0 2px #000; pointer-events: none; }
        .rec-dot { color: var(--danger); animation: blink 1s infinite; }
        @keyframes blink { 50% { opacity: 0; } }

        /* Control Panel */
        #control-panel {
            position: absolute; bottom: 0; left: 0; width: 100%; z-index: 100;
            background: var(--panel-bg); border-top: 2px solid var(--primary);
            padding: 15px; box-sizing: border-box; transform: translateY(85%); transition: transform 0.3s ease;
        }
        #control-panel:hover, #control-panel.active { transform: translateY(0); }
        
        .panel-header { display: flex; justify-content: space-between; align-items: center; cursor: pointer; padding-bottom: 10px; }
        .grid-form { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 10px; }
        
        input, select { background: #111; border: 1px solid #444; color: var(--primary); padding: 8px; width: 100%; box-sizing: border-box; }
        button { background: var(--primary); color: #000; border: none; padding: 10px; cursor: pointer; font-weight: bold; width: 100%; margin-top: 10px;}
        button.mute-btn { background: var(--mute); color: #000; }
        button.active-mute { background: #333; color: #888; border: 1px solid #555; }

        /* Loader */
        #loader { position: absolute; top:0; left:0; width:100%; height:100%; background:#000; z-index:200; display:flex; align-items:center; justify-content:center; flex-direction:column;}
    </style>
</head>
<body>

<div id="loader">
    <h2>SYSTEM INITIALIZING...</h2>
    <div id="loader-msg">Loading Neural Engine</div>
</div>

<div id="view-container">
    <!-- Camera Views will be injected here dynamically -->
</div>

<div id="control-panel">
    <div class="panel-header" onclick="document.getElementById('control-panel').classList.toggle('active')">
        <span>⚙️ SYSTEM CONFIGURATION [HOVER TO EXPAND]</span>
        <span id="sys-status">STANDBY</span>
    </div>
    
    <div class="grid-form">
        <select id="cam-select">
            <option value="user">Front Camera (Face)</option>
            <option value="environment">Back Camera (World)</option>
            <option value="dual">⚠️ DUAL CAM (Experimental)</option>
        </select>
        <button id="mute-toggle" class="mute-btn">🔊 SIREN: ON</button>
    </div>

    <div class="grid-form">
        <input type="text" id="tg-token" placeholder="Bot Token (Optional)">
        <input type="text" id="tg-chat" placeholder="Chat ID (Optional)">
    </div>
    
    <button id="save-restart">SAVE CONFIG & RESTART SYSTEM</button>
</div>

<!-- Load MediaPipe Locally -->
<script src="assets/face_mesh.js"></script>

<script>
/**
 * CAM3 v2.0 - Advanced Client-Side Surveillance
 * Architect: Gemini Pro
 */

// --- 1. Sound & Siren Controller ---
class AudioController {
    constructor() {
        this.muted = false;
        this.oscillator = null;
        this.toggleBtn = document.getElementById('mute-toggle');
        
        this.toggleBtn.addEventListener('click', () => this.toggle());
    }

    toggle() {
        this.muted = !this.muted;
        if(this.muted) {
            this.stopSiren(); // Stop immediately if muted
            this.toggleBtn.innerText = "🔇 SIREN: MUTED";
            this.toggleBtn.classList.add('active-mute');
        } else {
            this.toggleBtn.innerText = "🔊 SIREN: ON";
            this.toggleBtn.classList.remove('active-mute');
        }
    }

    playSiren() {
        if(this.muted) return;
        if(this.oscillator) return; // Already playing

        const AudioContext = window.AudioContext || window.webkitAudioContext;
        const ctx = new AudioContext();
        this.oscillator = ctx.createOscillator();
        const gain = ctx.createGain();

        this.oscillator.type = 'sawtooth';
        this.oscillator.frequency.value = 800; // Hz
        
        // Siren effect (LFO)
        const lfo = ctx.createOscillator();
        lfo.type = 'sine';
        lfo.frequency.value = 2; // Speed of siren
        const lfoGain = ctx.createGain();
        lfoGain.gain.value = 600; // Range of pitch change
        
        lfo.connect(lfoGain);
        lfoGain.connect(this.oscillator.frequency);
        lfo.start();

        this.oscillator.connect(gain);
        gain.connect(ctx.destination);
        this.oscillator.start();

        // Auto stop after 2 seconds to avoid annoyance
        setTimeout(() => this.stopSiren(), 2000);
    }

    stopSiren() {
        if(this.oscillator) {
            try { this.oscillator.stop(); } catch(e){}
            this.oscillator = null;
        }
    }
}

// --- 2. Notification Service (Resilient) ---
class NotificationService {
    constructor(audioCtrl) {
        this.audio = audioCtrl;
        this.token = localStorage.getItem('tg_token') || "";
        this.chatId = localStorage.getItem('tg_chat') || "";
    }

    updateCreds(t, c) {
        this.token = t;
        this.chatId = c;
        localStorage.setItem('tg_token', t);
        localStorage.setItem('tg_chat', c);
    }

    async triggerAlert(blob, score, camLabel) {
        // Always trigger local feedback
        console.log(`[ALERT] Intruder on ${camLabel} | Score: ${score}`);
        this.audio.playSiren();
        document.getElementById('sys-status').innerText = `⚠️ DETECTED (${camLabel})`;
        document.getElementById('sys-status').style.color = 'var(--danger)';

        // Optional: Remote Dispatch
        if (!this.token || !this.chatId) {
            console.log("[Network] Credentials missing. Skipping remote alert.");
            return; 
        }

        const formData = new FormData();
        formData.append('chat_id', this.chatId);
        formData.append('photo', blob, `capture_${camLabel}.jpg`);
        formData.append('caption', `🚨 <b>INTRUDER ALERT</b>\\n📷 Source: ${camLabel}\\n🎯 Score: ${score.toFixed(1)}\\n🕒 ${new Date().toLocaleTimeString()}`);
        formData.append('parse_mode', 'HTML');

        try {
            await fetch(`https://api.telegram.org/bot${this.token}/sendPhoto`, {
                method: 'POST', body: formData
            });
        } catch (e) {
            console.error("Network fail:", e);
        }
    }
}

// --- 3. Multi-Camera Manager ---
class CameraManager {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.activeStreams = []; // Array of { video, canvas, type }
    }

    async stopAll() {
        this.activeStreams.forEach(obj => {
            if(obj.video.srcObject) {
                obj.video.srcObject.getTracks().forEach(track => track.stop());
            }
            obj.wrapper.remove();
        });
        this.activeStreams = [];
        this.container.innerHTML = '';
        document.body.classList.remove('dual-mode');
    }

    createView(label) {
        const wrapper = document.createElement('div');
        wrapper.className = 'cam-wrapper';
        
        const vid = document.createElement('video');
        vid.autoplay = true;
        vid.playsInline = true;
        vid.muted = true;
        
        const cvs = document.createElement('canvas');
        
        const hud = document.createElement('div');
        hud.className = 'hud-overlay';
        hud.innerHTML = `${label} <span class="rec-dot">●</span>`;

        wrapper.appendChild(vid);
        wrapper.appendChild(cvs);
        wrapper.appendChild(hud);
        this.container.appendChild(wrapper);

        return { video: vid, canvas: cvs, wrapper: wrapper, label: label };
    }

    async startMode(mode) {
        await this.stopAll();

        if (mode === 'dual') {
            document.body.classList.add('dual-mode');
            // Try to get both. Note: This depends heavily on browser support.
            // Strategy: Open User, then Open Env.
            try {
                const s1 = await this.startStream('user');
                const s2 = await this.startStream('environment');
                if(!s1 && !s2) throw new Error("No cameras found");
            } catch(e) {
                alert("Dual Mode not supported on this device/browser. Falling back to Front.");
                await this.startStream('user');
            }
        } else {
            await this.startStream(mode);
        }
        
        return this.activeStreams;
    }

    async startStream(facingMode) {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({
                video: { facingMode: facingMode, width: {ideal: 1280}, height: {ideal: 720} },
                audio: false
            });
            
            const viewObj = this.createView(facingMode.toUpperCase());
            viewObj.video.srcObject = stream;
            
            // Wait for load
            await new Promise(r => viewObj.video.onloadedmetadata = r);
            viewObj.canvas.width = viewObj.video.videoWidth;
            viewObj.canvas.height = viewObj.video.videoHeight;
            
            this.activeStreams.push(viewObj);
            return true;
        } catch(e) {
            console.error(`Failed to load ${facingMode}:`, e);
            return false;
        }
    }
}

// --- 4. AI Engine & Orchestrator ---
class SecurityCore {
    constructor() {
        this.audio = new AudioController();
        this.notifier = new NotificationService(this.audio);
        this.cameraMgr = new CameraManager('view-container');
        this.faceMesh = null;
        
        // State
        this.isProcessing = false;
        this.coolDowns = {}; // Map: 'USER' -> timestamp
    }

    async init() {
        // Load Config
        document.getElementById('tg-token').value = localStorage.getItem('tg_token') || "";
        document.getElementById('tg-chat').value = localStorage.getItem('tg_chat') || "";
        
        // Init AI
        this.faceMesh = new FaceMesh({locateFile: (file) => `assets/${file}`});
        this.faceMesh.setOptions({
            maxNumFaces: 1,
            refineLandmarks: true,
            minDetectionConfidence: 0.5,
            minTrackingConfidence: 0.5
        });
        
        this.faceMesh.onResults(this.handleAIResults.bind(this));
        await this.faceMesh.initialize();
        
        document.getElementById('loader').style.display = 'none';
        
        // Start Default
        this.startSurveillance();
    }

    async startSurveillance() {
        const mode = document.getElementById('cam-select').value;
        const streams = await this.cameraMgr.startMode(mode);
        
        if(streams.length > 0) {
            this.loop();
        }
    }

    // Round-Robin Processing for Multi-Camera
    async loop() {
        if (!this.cameraMgr.activeStreams.length) return;
        
        for (const cam of this.cameraMgr.activeStreams) {
            // Set context for results callback
            this.currentCam = cam; 
            
            // Clear canvas before drawing new frame
            const ctx = cam.canvas.getContext('2d');
            ctx.clearRect(0, 0, cam.canvas.width, cam.canvas.height);
            
            // Send to MediaPipe
            await this.faceMesh.send({image: cam.video});
        }
        
        requestAnimationFrame(this.loop.bind(this));
    }

    handleAIResults(results) {
        if (!this.currentCam || !results.multiFaceLandmarks || results.multiFaceLandmarks.length === 0) return;

        const cam = this.currentCam;
        const ctx = cam.canvas.getContext('2d');
        const landmarks = results.multiFaceLandmarks[0];

        // 1. Draw Mesh (Hacker Style)
        this.drawMesh(ctx, landmarks, cam.canvas.width, cam.canvas.height);

        // 2. Logic: Completeness Score
        const score = this.calculateScore(landmarks, cam.canvas.width, cam.canvas.height);

        // 3. Logic: Trigger
        const now = Date.now();
        const lastRun = this.coolDowns[cam.label] || 0;
        
        if (now - lastRun > 8000) { // 8 Seconds Cooldown per camera
            // Capture high quality frame from canvas
            // We draw the video frame to a temp canvas to convert to blob
            const tempCanvas = document.createElement('canvas');
            tempCanvas.width = cam.video.videoWidth;
            tempCanvas.height = cam.video.videoHeight;
            tempCanvas.getContext('2d').drawImage(cam.video, 0, 0);
            
            tempCanvas.toBlob(blob => {
                this.notifier.triggerAlert(blob, score, cam.label);
            }, 'image/jpeg', 0.9);
            
            this.coolDowns[cam.label] = now;
        }
    }

    calculateScore(landmarks, w, h) {
        // Simple area calculation for bounding box
        let minX=1, maxX=0, minY=1, maxY=0;
        for(let pt of landmarks) {
            if(pt.x < minX) minX = pt.x;
            if(pt.x > maxX) maxX = pt.x;
            if(pt.y < minY) minY = pt.y;
            if(pt.y > maxY) maxY = pt.y;
        }
        return (maxX - minX) * (maxY - minY) * 100;
    }

    drawMesh(ctx, landmarks, w, h) {
        ctx.strokeStyle = '#00ff41';
        ctx.lineWidth = 1;
        ctx.beginPath();
        // Simplified drawing: Convex Hull or Box
        let minX=1, maxX=0, minY=1, maxY=0;
        for(let pt of landmarks) {
            const x = pt.x * w;
            const y = pt.y * h;
            if(pt.x < minX) minX = pt.x;
            if(pt.x > maxX) maxX = pt.x;
            if(pt.y < minY) minY = pt.y;
            if(pt.y > maxY) maxY = pt.y;
            ctx.rect(x, y, 2, 2); // dots
        }
        ctx.stroke();
        
        // Box
        ctx.strokeStyle = 'rgba(0, 255, 65, 0.5)';
        ctx.lineWidth = 2;
        ctx.strokeRect(minX*w, minY*h, (maxX-minX)*w, (maxY-minY)*h);
    }
}

// --- Bootstrap ---
const core = new SecurityCore();
document.getElementById('save-restart').addEventListener('click', () => {
    core.notifier.updateCreds(
        document.getElementById('tg-token').value,
        document.getElementById('tg-chat').value
    );
    core.startSurveillance();
});

window.onload = () => core.init();

</script>
</body>
</html>
"""

def install():
    print(f"[*] Starting CAM3 v2.0 Installation in: {PROJECT_DIR}")
    
    # 1. Create Directories
    if not os.path.exists(ASSETS_DIR):
        os.makedirs(ASSETS_DIR)
        print(f"[+] Created directory: {ASSETS_DIR}")
    
    # 2. Download MediaPipe Assets
    print("[*] Downloading Offline AI Models...")
    session = requests.Session()
    
    for filename, url in MEDIAPIPE_ASSETS.items():
        file_path = os.path.join(ASSETS_DIR, filename)
        if os.path.exists(file_path):
            print(f"  [i] Exists: {filename}")
            continue
            
        print(f"  [>] Downloading: {filename} ...")
        try:
            resp = session.get(url, stream=True)
            resp.raise_for_status()
            with open(file_path, 'wb') as f:
                for chunk in resp.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"  [+] Downloaded: {filename}")
        except Exception as e:
            print(f"  [!] Failed to download {filename}: {e}")
            sys.exit(1)

    # 3. Create index.html
    index_path = os.path.join(PROJECT_DIR, "index.html")
    try:
        with open(index_path, "w", encoding="utf-8") as f:
            f.write(HTML_CONTENT)
        print(f"[+] Generated System Core: {index_path}")
    except Exception as e:
        print(f"[!] Error writing HTML: {e}")
        sys.exit(1)

    print("\n" + "="*50)
    print("SUCCESS! CAM3 v2.0 Installed.")
    print("Features: Multi-Camera, Dual Stream, Optional Auth, Siren Control")
    print(f"Path: {os.path.abspath(PROJECT_DIR)}")
    print("="*50)

if __name__ == "__main__":
    install()
