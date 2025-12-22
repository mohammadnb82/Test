import os
import urllib.request
from pathlib import Path

BASE_DIR = Path("tools/durbin_tashkhis_chehre")

JS_DIR = BASE_DIR / "js"
MODELS_DIR = BASE_DIR / "models"
ASSETS_DIR = BASE_DIR / "assets"

def create_dirs():
    for d in [JS_DIR, MODELS_DIR, ASSETS_DIR]:
        d.mkdir(parents=True, exist_ok=True)

def download(url, dest):
    if not dest.exists():
        print(f"Downloading {url}")
        urllib.request.urlretrieve(url, dest)

def create_index_html():
    html_code = """<!DOCTYPE html>
<html lang="fa">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>تشخیص چهره</title>
<style>
body { margin:0; background:#000; color:#fff; font-family:tahoma; overflow:hidden; }
video, canvas { position:absolute; top:0; left:0; }
#controls { position:fixed; bottom:10px; width:100%; display:flex; justify-content:space-around; }
button { padding:10px 15px; font-size:14px; }
#faces { position:fixed; top:10px; right:10px; display:flex; flex-direction:column; gap:5px; }
#faces img { width:80px; border:2px solid red; }
</style>
</head>
<body>

<video id="video" autoplay muted></video>
<canvas id="overlay"></canvas>

<div id="faces"></div>

<div id="controls">
<button onclick="switchCamera()">تغییر دوربین</button>
<button onclick="toggleAlarm()">آژیر</button>
</div>

<audio id="alarm" loop src="assets/alarm.mp3"></audio>

<script src="js/face-api.min.js"></script>
<script src="js/camera.js"></script>
</body>
</html>
"""
    (BASE_DIR / "index.html").write_text(html_code, encoding="utf-8")

def create_camera_js():
    js_code = """
let video = document.getElementById('video');
let canvas = document.getElementById('overlay');
let ctx = canvas.getContext('2d');
let alarm = document.getElementById('alarm');
let alarmOn = true;
let currentFacing = "user";
let knownFaces = [];

async function loadModels() {
  await faceapi.nets.tinyFaceDetector.loadFromUri('models');
  await faceapi.nets.faceLandmark68Net.loadFromUri('models');
  await faceapi.nets.faceRecognitionNet.loadFromUri('models');
}

async function startCamera() {
  let stream = await navigator.mediaDevices.getUserMedia({
    video: { facingMode: currentFacing }
  });
  video.srcObject = stream;
}

function toggleAlarm() {
  alarmOn = !alarmOn;
  if(!alarmOn) alarm.pause();
}

function switchCamera() {
  currentFacing = currentFacing === "user" ? "environment" : "user";
  startCamera();
}

async function detect() {
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;

  const detections = await faceapi
    .detectAllFaces(video, new faceapi.TinyFaceDetectorOptions())
    .withFaceLandmarks()
    .withFaceDescriptors();

  ctx.clearRect(0,0,canvas.width,canvas.height);

  if(detections.length > 0 && alarmOn){
    alarm.play();
  }

  detections.forEach(det => saveFace(det));
}

function saveFace(det){
  const box = det.detection.box;
  const faceCanvas = document.createElement('canvas');
  faceCanvas.width = box.width;
  faceCanvas.height = box.height;
  faceCanvas.getContext('2d').drawImage(
    video,
    box.x, box.y, box.width, box.height,
    0,0,box.width,box.height
  );

  let img = document.createElement('img');
  img.src = faceCanvas.toDataURL();
  document.getElementById('faces').appendChild(img);
}

video.addEventListener('play', () => {
  setInterval(detect, 700);
});

loadModels().then(startCamera);
"""
    (JS_DIR / "camera.js").write_text(js_code, encoding="utf-8")

def main():
    create_dirs()

    download(
        "https://cdn.jsdelivr.net/npm/face-api.js/dist/face-api.min.js",
        JS_DIR / "face-api.min.js"
    )

    create_index_html()
    create_camera_js()

    print("✅ پروژه تشخیص چهره ساخته شد")

if __name__ == "__main__":
    main()
