import os
import shutil

# مسیر پوشه هدف
folder_path = "tools/doorbin-tashkhis-harekat"

# 1. عملیات پاک‌سازی کامل (Wipe Out)
if os.path.exists(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")
else:
    os.makedirs(folder_path)

# 2. محتوای فایل HTML (کامل و بسته شده)
# این بار کد فشرده شده تا مطمئن باشیم قطع نمی‌شود
html_content = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
<title>Motion Detector Pro</title>
<style>
:root { --bg: #000; --card: #1c1c1e; --text: #fff; --sub: #8e8e93; --red: #ff453a; --green: #32d74b; --blue: #0a84ff; }
body { background: var(--bg); color: var(--text); font-family: -apple-system, system-ui, sans-serif; margin: 0; padding: 15px; display: flex; flex-direction: column; align-items: center; height: 100vh; overflow: hidden; box-sizing: border-box; }
.video-box { width: 100%; max-width: 500px; aspect-ratio: 4/3; background: #111; border-radius: 12px; overflow: hidden; position: relative; margin-bottom: 15px; border: 1px solid #333; box-shadow: 0 4px 20px rgba(0,0,0,0.5); }
video { width: 100%; height: 100%; object-fit: cover; display: block; }
#alarm-flash { position: absolute; inset: 0; background: rgba(255, 69, 58, 0.4); display: none; z-index: 10; box-shadow: inset 0 0 50px var(--red); }
.controls-card { width: 100%; max-width: 500px; background: var(--card); padding: 20px; border-radius: 16px; display: flex; flex-direction: column; gap: 15px; }
.graph-wrapper { position: relative; height: 45px; background: #2c2c2e; border-radius: 8px; overflow: hidden; margin-bottom: 5px; }
.motion-bar { height: 100%; width: 0%; background: var(--green); transition: width 0.1s linear; opacity: 0.8; }
.threshold-line { position: absolute; top: 0; bottom: 0; width: 4px; background: var(--red); box-shadow: 0 0 8px rgba(255, 69, 58, 0.8); z-index: 5; transform: translateX(-50%); left: 40%; }
.ruler { display: flex; justify-content: space-between; color: var(--sub); font-size: 11px; padding: 0 2px; margin-top: -10px; font-weight: 500; }
.stats-row { display: flex; justify-content: space-between; align-items: center; font-weight: 700; font-size: 15px; }
.stat-left { color: var(--red); } .stat-right { color: var(--green); }
.slider-container { display: flex; flex-direction: column; gap: 8px; }
.slider-label { color: var(--sub); font-size: 13px; }
input[type=range] { -webkit-appearance: none; width: 100%; background: transparent; }
input[type=range]:focus { outline: none; }
input[type=range]::-webkit-slider-runnable-track { width: 100%; height: 6px; background: var(--blue); border-radius: 3px; cursor: pointer; }
input[type=range]::-webkit-slider-thumb { -webkit-appearance: none; height: 24px; width: 24px; border-radius: 50%; background: #fff; cursor: pointer; margin-top: -9px; box-shadow: 0 2px 6px rgba(0,0,0,0.4); }
.buttons-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-top: 10px; }
.btn { border: none; padding: 16px; border-radius: 12px; font-size: 15px; font-weight: 600; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 8px; transition: transform 0.1s; }
.btn:active { transform: scale(0.98); }
.btn-grey { background: #3a3a3c; color: white; }
.btn-red { background: #3a3a3c; color: #ccc; border: 1px solid #444; }
.btn-red.active { background: var(--red); color: white; border: none; box-shadow: 0 0 15px rgba(255, 69, 58, 0.4); }
.back-link { margin-top: auto; color: var(--sub); text-decoration: none; font-size: 13px; padding-bottom: 20px; }
canvas { display: none; }
</style>
</head>
<body>
<div class="video-box">
    <video id="webcam" autoplay playsinline muted></video>
    <div id="alarm-flash"></div>
</div>
<canvas id="proc-canvas"></canvas>
<div class="controls-card">
    <div>
        <div class="graph-wrapper">
            <div id="bar-motion" class="motion-bar"></div>
            <div id="line-thresh" class="threshold-line"></div>
        </div>
        <div class="ruler"><span>0</span><span>20</span><span>40</span><span>60</span><span>80</span><span>100</span></div>
    </div>
    <div class="stats-row">
        <span class="stat-left">Threshold: <span id="txt-thresh">40</span></span>
        <span class="stat-right">Motion: <span id="txt-motion">0</span></span>
    </div>
    <div class="slider-container">
        <span class="slider-label">Threshold Adjustment</span>
        <input type="range" id="input-slider" min="0" max="100" value="40">
    </div>
    <div class="buttons-grid">
        <button class="btn btn-grey" onclick="rotateCamera()">🔄 Rotate Cam</button>
        <button id="btn-siren" class="btn btn-red" onclick="toggleSiren()">🔕 Siren OFF</button>
    </div>
</div>
<a href="../index_tools.html" class="back-link">← Back to Tools</a>
<script>
// CONFIG
const CONF = { procWidth: 64, procHeight: 48, pixelDiffThreshold: 15, motionGain: 4 };
// ELEMENTS
const video = document.getElementById('webcam'), canvas = document.getElementById('proc-canvas'), ctx = canvas.getContext('2d', { willReadFrequently: true });
const alarmFlash = document.getElementById('alarm-flash'), barMotion = document.getElementById('bar-motion'), lineThresh = document.getElementById('line-thresh');
const txtThresh = document.getElementById('txt-thresh'), txtMotion = document.getElementById('txt-motion'), slider = document.getElementById('input-slider'), btnSiren = document.getElementById('btn-siren');
// STATE
let stream = null, facingMode = 'environment', lastFrameData = null, isSirenActive = false, isLoopRunning = false, audioCtx = null;

function init() { canvas.width = CONF.procWidth; canvas.height = CONF.procHeight; updateThresholdUI(slider.value); startCamera(); }

async function startCamera() {
    if (stream) stream.getTracks().forEach(t => t.stop());
    try {
        stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: facingMode, width: { ideal: 640 }, height: { ideal: 480 } }, audio: false });
        video.srcObject = stream; lastFrameData = null;
        if (!isLoopRunning) { isLoopRunning = true; requestAnimationFrame(processLoop); }
    } catch (e) { console.error(e); alert("Camera Error: Allow permissions."); }
}

function rotateCamera() { facingMode = (facingMode === 'environment') ? 'user' : 'environment'; lastFrameData = null; startCamera(); }

function processLoop() {
    if (video.readyState === 4) {
        try {
            ctx.drawImage(video, 0, 0, CONF.procWidth, CONF.procHeight);
            const frame = ctx.getImageData(0, 0, CONF.procWidth, CONF.procHeight);
            const data = frame.data;
            if (lastFrameData) {
                const prevData = lastFrameData.data; let changedPixels = 0;
                for (let i = 0; i < data.length; i += 4) {
                    if ((Math.abs(data[i] - prevData[i]) + Math.abs(data[i+1] - prevData[i+1]) + Math.abs(data[i+2] - prevData[i+2])) > CONF.pixelDiffThreshold) changedPixels++;
                }
                let score = Math.floor((changedPixels / (CONF.procWidth * CONF.procHeight)) * 100 * CONF.motionGain);
                if (score > 100) score = 100;
                updateMotionUI(score); checkAlarm(score);
            }
            lastFrameData = frame;
        } catch (e) { lastFrameData = null; }
    }
    requestAnimationFrame(processLoop);
}

slider.addEventListener('input', (e) => { updateThresholdUI(e.target.value); });
function updateThresholdUI(val) { lineThresh.style.left = val + '%'; txtThresh.innerText = val; }
function updateMotionUI(score) { barMotion.style.width = score + '%'; txtMotion.innerText = score; }

function checkAlarm(score) {
    const th = parseInt(slider.value);
    if (score >= th && th > 0) {
        barMotion.style.background = '#ff453a';
        if (isSirenActive) { alarmFlash.style.display = 'block'; playSirenSound(); }
    } else {
        barMotion.style.background = '#32d74b'; alarmFlash.style.display = 'none';
    }
}

function toggleSiren() {
    if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    if (audioCtx.state === 'suspended') audioCtx.resume();
    isSirenActive = !isSirenActive;
    if (isSirenActive) { btnSiren.classList.add('active'); btnSiren.innerHTML = "🔔 Siren ON"; playSirenSound(0.1); }
    else { btnSiren.classList.remove('active'); btnSiren.innerHTML = "🔕 Siren OFF"; alarmFlash.style.display = 'none'; }
}

function playSirenSound(dur = 0.15) {
    if (!audioCtx) return;
    const osc = audioCtx.createOscillator(), gn = audioCtx.createGain();
    osc.type = 'square';
    osc.frequency.setValueAtTime(800, audioCtx.currentTime);
    osc.frequency.linearRampToValueAtTime(1200, audioCtx.currentTime + dur);
    gn.gain.setValueAtTime(0.1, audioCtx.currentTime);
    gn.gain.linearRampToValueAtTime(0, audioCtx.currentTime + dur);
    osc.connect(gn); gn.connect(audioCtx.destination);
    osc.start(); osc.stop(audioCtx.currentTime + dur);
}

init();
</script>
</body>
</html>"""

# 3. ساخت فایل نهایی
html_file_path = os.path.join(folder_path, "index_doorbin-tashkhis-harekat.html")

try:
    with open(html_file_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Success! File created at: {html_file_path}")
except Exception as e:
    print(f"Write Error: {e}")
