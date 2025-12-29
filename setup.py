import os
import requests
import sys
import time

# --- Configuration ---
PROJECT_DIR = "tools/cam3"
ASSETS_DIR = os.path.join(PROJECT_DIR, "assets")

# URLs for MediaPipe Face Mesh (Official Google CDN)
# We download these to make the app fully offline/self-contained for the client browser.
MEDIAPIPE_ASSETS = {
    "face_mesh.js": "https://cdn.jsdelivr.net/npm/@mediapipe/face_mesh/face_mesh.js",
    "face_mesh.wasm": "https://cdn.jsdelivr.net/npm/@mediapipe/face_mesh/face_mesh.wasm",
    "face_mesh.binarypb": "https://cdn.jsdelivr.net/npm/@mediapipe/face_mesh/face_mesh.binarypb",
}

# --- HTML/JS/CSS Content (Embedded for Single-Script Deployment) ---

HTML_CONTENT = """<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Security System | CAM3</title>
    <style>
        :root { --primary: #00ff41; --bg: #0d0d0d; --panel: #1a1a1a; --danger: #ff3333; }
        body { margin: 0; background: var(--bg); color: var(--primary); font-family: 'Courier New', monospace; overflow: hidden; }
        #app { position: relative; width: 100vw; height: 100vh; display: flex; flex-direction: column; align-items: center; justify-content: center; }
        
        /* Video is hidden, we verify on Canvas */
        video { display: none; }
        canvas { position: absolute; top: 0; left: 0; width: 100%; height: 100%; object-fit: cover; z-index: 1; }
        
        /* HUD Overlay */
        .hud { position: absolute; z-index: 10; width: 100%; height: 100%; pointer-events: none; box-shadow: inset 0 0 50px rgba(0,0,0,0.8); }
        .scan-line { position: absolute; width: 100%; height: 2px; background: rgba(0, 255, 65, 0.5); animation: scan 3s infinite linear; }
        @keyframes scan { 0% { top: 0; } 100% { top: 100%; } }
        
        /* Control Panel */
        #panel {
            position: absolute; bottom: 20px; right: 20px; z-index: 20;
            background: rgba(0, 0, 0, 0.8); border: 1px solid var(--primary);
            padding: 15px; border-radius: 5px; pointer-events: all;
            width: 300px; transition: opacity 0.3s;
        }
        #panel.hidden { opacity: 0.1; }
        #panel:hover { opacity: 1; }
        
        input { background: #000; border: 1px solid #333; color: var(--primary); width: 95%; padding: 8px; margin-bottom: 10px; font-family: inherit; }
        button { background: var(--primary); color: #000; border: none; padding: 10px; width: 100%; cursor: pointer; font-weight: bold; }
        button:hover { background: #fff; }
        
        .status { font-size: 12px; margin-top: 10px; color: #fff; }
        .blink { animation: blinker 1s linear infinite; color: var(--danger); }
        @keyframes blinker { 50% { opacity: 0; } }

        /* Loader */
        #loader { position: absolute; z-index: 50; background: #000; width: 100%; height: 100%; display: flex; justify-content: center; align-items: center; flex-direction: column; }
    </style>
</head>
<body>

<div id="loader">
    <h1>INITIALIZING CAM3 CORE...</h1>
    <p id="load-status">Loading Neural Networks...</p>
</div>

<div id="app">
    <video id="input-video" playsinline></video>
    <canvas id="output-canvas"></canvas>
    
    <div class="hud">
        <div class="scan-line"></div>
        <div style="position: absolute; top: 10px; left: 10px;">
            CAM3 ACTIVE <span class="blink">● REC</span><br>
            <span id="fps">FPS: 0</span> | SCORE: <span id="q-score">0</span>
        </div>
    </div>

    <div id="panel">
        <h3 style="margin-top:0;">SYSTEM CONFIG</h3>
        <input type="text" id="tg-token" placeholder="Telegram Bot Token">
        <input type="text" id="tg-chat" placeholder="Chat ID">
        <button id="save-btn">SAVE & ARM SYSTEM</button>
        <div class="status" id="log-area">System Standby...</div>
    </div>
</div>

<!-- Load Local MediaPipe Library -->
<script src="assets/face_mesh.js"></script>

<script>
/**
 * SECURITY SURVEILLANCE SYSTEM - CAM3
 * Architecture: OOP / Singleton / Event-Driven
 */

// --- 1. Notification Service (Telegram) ---
class NotificationService {
    constructor() {
        this.token = localStorage.getItem('tg_token');
        this.chatId = localStorage.getItem('tg_chat');
        this.logArea = document.getElementById('log-area');
    }

    updateCreds(token, chatId) {
        this.token = token;
        this.chatId = chatId;
        localStorage.setItem('tg_token', token);
        localStorage.setItem('tg_chat', chatId);
        this.log("Credentials Saved.");
    }

    log(msg) {
        console.log(`[SYS]: ${msg}`);
        if(this.logArea) this.logArea.innerText = `> ${msg}`;
    }

    async sendAlert(blob, bestScore) {
        if (!this.token || !this.chatId) {
            this.log("ERR: Missing Credentials");
            return;
        }

        const formData = new FormData();
        formData.append('chat_id', this.chatId);
        formData.append('photo', blob, 'intruder.jpg');
        formData.append('caption', `⚠️ SECURITY ALERT ⚠️\\n\\n🎯 Detection Score: ${bestScore.toFixed(2)}\\n🕒 Time: ${new Date().toLocaleTimeString()}\\n🛡️ System: CAM3 WebGuard`);

        try {
            this.log("Sending Capture...");
            const res = await fetch(`https://api.telegram.org/bot${this.token}/sendPhoto`, {
                method: 'POST',
                body: formData
            });
            const data = await res.json();
            if(data.ok) this.log("✅ Alert Sent Successfully.");
            else this.log("❌ Telegram Error: " + data.description);
        } catch (e) {
            this.log("❌ Network Error");
        }
    }
}

// --- 2. Camera Manager ---
class CameraManager {
    constructor(videoElement) {
        this.video = videoElement;
    }

    async start() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({
                video: { width: { ideal: 1280 }, height: { ideal: 720 }, facingMode: "user" },
                audio: false
            });
            this.video.srcObject = stream;
            await new Promise(resolve => this.video.onloadedmetadata = resolve);
            this.video.play();
            return true;
        } catch (e) {
            alert("Camera Access Denied. System cannot function.");
            return false;
        }
    }
}

// --- 3. Face Analyzer (The Brain) ---
class FaceMeshAnalyzer {
    constructor(canvas, notificationService) {
        this.canvas = canvas;
        this.ctx = canvas.getContext('2d');
        this.notifier = notificationService;
        this.faceMesh = null;
        
        // Smart Capture State
        this.bestFrameBlob = null;
        this.bestScore = 0;
        this.isCoolingDown = false;
        this.detectionStartTime = 0;
        this.CAPTURE_WINDOW = 1000; // Look for best shot for 1 second after first detection
        this.COOLDOWN_TIME = 8000;  // Wait 8 seconds before next alert
    }

    async init() {
        // Initialize MediaPipe with LOCAL assets
        this.faceMesh = new FaceMesh({locateFile: (file) => {
            return `assets/${file}`; // IMPORTANT: Load from local folder
        }});

        this.faceMesh.setOptions({
            maxNumFaces: 1,
            refineLandmarks: true, // Better attention to eyes/lips
            minDetectionConfidence: 0.5,
            minTrackingConfidence: 0.5
        });

        this.faceMesh.onResults(this.onResults.bind(this));
        await this.faceMesh.initialize();
    }

    async sendFrame(video) {
        await this.faceMesh.send({image: video});
    }

    calculateCompletenessScore(landmarks, width, height) {
        // 1. Bounding Box Area Score (Closer is better)
        let minX = 1, maxX = 0, minY = 1, maxY = 0;
        landmarks.forEach(pt => {
            if (pt.x < minX) minX = pt.x;
            if (pt.x > maxX) maxX = pt.x;
            if (pt.y < minY) minY = pt.y;
            if (pt.y > maxY) maxY = pt.y;
        });
        const area = (maxX - minX) * (maxY - minY);
        
        // 2. Visibility Score (Are landmarks actually confident?)
        // In MediaPipe JS, visibility is implicitly handled by presence, 
        // but we can assume if we have landmarks, we have a face.
        
        // Final Score: Heavy weight on Area (proximity) + Constant factor for detection
        // Multiplier 100 for readability
        return (area * 100); 
    }

    onResults(results) {
        this.ctx.save();
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        this.ctx.drawImage(results.image, 0, 0, this.canvas.width, this.canvas.height);

        if (results.multiFaceLandmarks && results.multiFaceLandmarks.length > 0) {
            const landmarks = results.multiFaceLandmarks[0];
            const score = this.calculateCompletenessScore(landmarks, this.canvas.width, this.canvas.height);
            
            document.getElementById('q-score').innerText = score.toFixed(1);
            
            // Draw Target Box
            this.drawTargetBox(landmarks);

            // --- SMART CAPTURE LOGIC ---
            if (!this.isCoolingDown) {
                const now = Date.now();
                
                // If this is a new detection event
                if (this.detectionStartTime === 0) {
                    this.detectionStartTime = now;
                    this.bestScore = 0;
                    this.bestFrameBlob = null;
                }

                // If within capture window, look for the best frame
                if (now - this.detectionStartTime < this.CAPTURE_WINDOW) {
                    if (score > this.bestScore) {
                        this.bestScore = score;
                        // Capture high quality frame
                        this.canvas.toBlob(blob => {
                            this.bestFrameBlob = blob;
                        }, 'image/jpeg', 0.95);
                    }
                } else {
                    // Window closed, send the best shot we got
                    if (this.bestFrameBlob) {
                        this.notifier.sendAlert(this.bestFrameBlob, this.bestScore);
                        this.isCoolingDown = true;
                        this.detectionStartTime = 0;
                        setTimeout(() => { this.isCoolingDown = false; }, this.COOLDOWN_TIME);
                    }
                }
            }
        } else {
            // No face, reset timer if we haven't sent yet
            if (Date.now() - this.detectionStartTime > 500) {
                this.detectionStartTime = 0;
            }
        }
        this.ctx.restore();
    }

    drawTargetBox(landmarks) {
        // Draw a simple hacker-style box around the face
        let minX = 1, maxX = 0, minY = 1, maxY = 0;
        landmarks.forEach(pt => {
            if (pt.x < minX) minX = pt.x;
            if (pt.x > maxX) maxX = pt.x;
            if (pt.y < minY) minY = pt.y;
            if (pt.y > maxY) maxY = pt.y;
        });

        const w = this.canvas.width;
        const h = this.canvas.height;
        
        this.ctx.strokeStyle = '#00ff41';
        this.ctx.lineWidth = 2;
        this.ctx.strokeRect(minX * w, minY * h, (maxX - minX) * w, (maxY - minY) * h);
    }
}

// --- 4. Main System Controller ---
class SecuritySystem {
    constructor() {
        this.video = document.getElementById('input-video');
        this.canvas = document.getElementById('output-canvas');
        this.camera = new CameraManager(this.video);
        this.notify = new NotificationService();
        this.analyzer = new FaceMeshAnalyzer(this.canvas, this.notify);
        
        this.bindEvents();
    }

    bindEvents() {
        document.getElementById('save-btn').addEventListener('click', () => {
            const t = document.getElementById('tg-token').value;
            const c = document.getElementById('tg-chat').value;
            if(t && c) {
                this.notify.updateCreds(t, c);
                document.getElementById('panel').classList.add('hidden');
            }
        });

        // Load saved creds
        const t = localStorage.getItem('tg_token');
        const c = localStorage.getItem('tg_chat');
        if(t) document.getElementById('tg-token').value = t;
        if(c) document.getElementById('tg-chat').value = c;
    }

    async start() {
        document.getElementById('load-status').innerText = "Accessing Camera...";
        const camReady = await this.camera.start();
        if(!camReady) return;

        document.getElementById('load-status').innerText = "Loading AI Models...";
        await this.analyzer.init();
        
        // Setup Canvas Size
        this.canvas.width = this.video.videoWidth;
        this.canvas.height = this.video.videoHeight;
        
        document.getElementById('loader').style.display = 'none';
        this.notify.log("System ARMED & Monitoring.");

        // Processing Loop
        const loop = async () => {
            await this.analyzer.sendFrame(this.video);
            requestAnimationFrame(loop);
        };
        loop();
    }
}

// Start Application
window.onload = () => {
    const sys = new SecuritySystem();
    sys.start();
};
</script>
</body>
</html>
"""

def install():
    print(f"[*] Starting CAM3 Installation in: {PROJECT_DIR}")
    
    # 1. Create Directories
    if not os.path.exists(ASSETS_DIR):
        os.makedirs(ASSETS_DIR)
        print(f"[+] Created directory: {ASSETS_DIR}")
    
    # 2. Download MediaPipe Assets
    print("[*] Downloading Offline AI Models (This may take a moment)...")
    session = requests.Session()
    
    for filename, url in MEDIAPIPE_ASSETS.items():
        file_path = os.path.join(ASSETS_DIR, filename)
        if os.path.exists(file_path):
            print(f"  [i] Exists: {filename} (Skipping)")
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
            print("  [!] Critical Error: Cannot create offline setup without this file.")
            sys.exit(1)

    # 3. Create index.html
    index_path = os.path.join(PROJECT_DIR, "index.html")
    try:
        with open(index_path, "w", encoding="utf-8") as f:
            f.write(HTML_CONTENT)
        print(f"[+] Generated Core System: {index_path}")
    except Exception as e:
        print(f"[!] Error writing HTML: {e}")
        sys.exit(1)

    print("\n" + "="*50)
    print("SUCCESS! CAM3 Installed Successfully.")
    print(f"Location: {os.path.abspath(PROJECT_DIR)}")
    print("Action: Open 'index.html' in your browser to start surveillance.")
    print("="*50)

if __name__ == "__main__":
    install()
