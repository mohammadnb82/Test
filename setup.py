import os
import shutil
from pathlib import Path

BASE = Path("Test/tools/guard_camera")

def reset_dir():
    if BASE.exists():
        shutil.rmtree(BASE)
    BASE.mkdir(parents=True)

def write(path, content):
    path.write_text(content, encoding="utf-8")

def build():
    reset_dir()

    # index.html
    write(BASE / "index.html", """<!DOCTYPE html>
<html lang="fa">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Guard Camera</title>
<link rel="manifest" href="manifest.json">
<link rel="stylesheet" href="style.css">
</head>
<body>

<h2>🛡 دوربین نگهبان</h2>

<div id="status">⏳ آماده‌سازی…</div>

<video id="video" playsinline autoplay muted></video>
<canvas id="canvas"></canvas>

<div class="controls">
  <button id="startBtn">فعال‌سازی سیستم</button>
  <button id="switchBtn">تغییر دوربین</button>
  <button id="sirenBtn">تست آژیر</button>
</div>

<script src="https://cdn.jsdelivr.net/npm/@tensorflow/tfjs@4.14.0"></script>
<script src="https://cdn.jsdelivr.net/npm/@tensorflow-models/coco-ssd"></script>
<script src="app.js"></script>

</body>
</html>
""")

    # style.css
    write(BASE / "style.css", """body {
  margin:0;
  padding:10px;
  font-family:sans-serif;
  background:#0b0b0b;
  color:#fff;
  text-align:center;
}
video, canvas {
  width:100%;
  max-height:60vh;
  background:#000;
}
.controls button {
  margin:5px;
  padding:10px;
  font-size:16px;
}
#status {
  margin:8px;
  color:#0f0;
}
""")

    # app.js
    write(BASE / "app.js", """let video = document.getElementById("video");
let canvas = document.getElementById("canvas");
let ctx = canvas.getContext("2d");
let statusEl = document.getElementById("status");

let stream;
let facing = "environment";
let audioCtx;
let sirenOsc;
let model;
let aiOn = false;
let lastFrame = null;

async function setupCamera() {
  stream = await navigator.mediaDevices.getUserMedia({
    video: { facingMode: facing },
    audio: false
  });
  video.srcObject = stream;
}

function unlockAudio() {
  audioCtx = new (window.AudioContext || window.webkitAudioContext)();
}

function siren() {
  if (!audioCtx) return;
  sirenOsc = audioCtx.createOscillator();
  sirenOsc.frequency.value = 800;
  sirenOsc.connect(audioCtx.destination);
  sirenOsc.start();
  setTimeout(() => sirenOsc.stop(), 800);
}

async function loadAI() {
  model = await cocoSsd.load();
  aiOn = true;
  statusEl.textContent = "✅ AI فعال است";
}

function detectMotion() {
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  ctx.drawImage(video,0,0);
  let frame = ctx.getImageData(0,0,canvas.width,canvas.height);

  if (lastFrame) {
    let diff = 0;
    for (let i=0;i<frame.data.length;i+=40) {
      diff += Math.abs(frame.data[i] - lastFrame.data[i]);
    }
    if (diff > 5000) {
      siren();
      if (aiOn) detectHuman();
    }
  }
  lastFrame = frame;
}

async function detectHuman() {
  const preds = await model.detect(video);
  preds.forEach(p=>{
    if(p.class==="person" && p.score>0.6){
      statusEl.textContent = "🚨 انسان شناسایی شد";
      siren();
    }
  });
}

function loop() {
  if(video.readyState === 4) detectMotion();
  requestAnimationFrame(loop);
}

document.getElementById("startBtn").onclick = async ()=>{
  unlockAudio();
  await setupCamera();
  await loadAI();
  loop();
  statusEl.textContent = "🟢 سیستم فعال شد";
};

document.getElementById("switchBtn").onclick = async ()=>{
  facing = facing==="environment"?"user":"environment";
  stream.getTracks().forEach(t=>t.stop());
  await setupCamera();
};

document.getElementById("sirenBtn").onclick = siren;
""")

    # manifest.json
    write(BASE / "manifest.json", """{
  "name": "Guard Camera",
  "short_name": "GuardCam",
  "start_url": ".",
  "display": "standalone",
  "background_color": "#000000",
  "theme_color": "#000000"
}
""")

    print("✅ Guard Camera rebuilt successfully.")

if __name__ == "__main__":
    build()
