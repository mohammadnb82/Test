from pathlib import Path
import shutil

BASE = Path("Test/tools/guard_camera")

def reset():
    if BASE.exists():
        shutil.rmtree(BASE)
    BASE.mkdir(parents=True)

def write(name, content):
    (BASE / name).write_text(content, encoding="utf-8")

def main():
    reset()

    # ---------- index.html ----------
    write("index.html", """<!DOCTYPE html>
<html lang="fa">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Guard Camera</title>
<link rel="manifest" href="manifest.json">
<link rel="stylesheet" href="style.css">
</head>
<body>

<h3>🛡 دوربین نگهبان</h3>
<div id="status">آماده…</div>

<video id="video" autoplay playsinline muted></video>
<canvas id="canvas"></canvas>

<button id="startBtn">فعال‌سازی سیستم</button>

<script src="https://cdn.jsdelivr.net/npm/@tensorflow/tfjs@4.14.0"></script>
<script src="https://cdn.jsdelivr.net/npm/@tensorflow-models/coco-ssd"></script>
<script src="app.js"></script>

</body>
</html>
""")

    # ---------- style.css ----------
    write("style.css", """body{
background:#000;color:#fff;
font-family:sans-serif;
text-align:center;margin:0;padding:10px
}
video,canvas{width:100%;max-height:60vh}
button{padding:12px;font-size:16px;margin-top:10px}
#status{color:#0f0;margin:8px}
""")

    # ---------- app.js ----------
    write("app.js", """const video=document.getElementById("video");
const canvas=document.getElementById("canvas");
const ctx=canvas.getContext("2d");
const statusEl=document.getElementById("status");
const btn=document.getElementById("startBtn");

let stream,lastFrame=null,audioCtx,model=null,aiReady=false;

/* ---- storage ---- */
const armed=()=>localStorage.getItem("armed")==="1";
const setArmed=v=>localStorage.setItem("armed",v?"1":"0");

/* ---- audio ---- */
function unlockAudio(){
 audioCtx=new(window.AudioContext||window.webkitAudioContext)();
 audioCtx.resume();
}
function siren(){
 if(!audioCtx)return;
 const o=audioCtx.createOscillator();
 o.frequency.value=900;
 o.connect(audioCtx.destination);
 o.start();
 setTimeout(()=>o.stop(),600);
}

/* ---- camera ---- */
async function startCamera(){
 stream=await navigator.mediaDevices.getUserMedia({video:{facingMode:"environment"}});
 video.srcObject=stream;
 return new Promise(r=>video.onloadedmetadata=()=>{video.play();r();});
}

/* ---- motion ---- */
function detectMotion(){
 if(video.videoWidth===0)return;
 canvas.width=video.videoWidth;
 canvas.height=video.videoHeight;
 ctx.drawImage(video,0,0);
 const f=ctx.getImageData(0,0,canvas.width,canvas.height);
 if(lastFrame){
  let d=0;
  for(let i=0;i<f.data.length;i+=50)
   d+=Math.abs(f.data[i]-lastFrame.data[i]);
  if(d>3000){
   statusEl.textContent="🚨 حرکت";
   siren();
   if(aiReady)detectHuman();
  }
 }
 lastFrame=f;
}

/* ---- AI ---- */
async function startAI(){
 model=await cocoSsd.load();
 aiReady=true;
 statusEl.textContent="✅ AI فعال";
}
async function detectHuman(){
 const p=await model.detect(video);
 p.forEach(x=>{
  if(x.class==="person"&&x.score>0.6){
   statusEl.textContent="🧍 انسان";
   siren();
  }
 });
}

/* ---- loop ---- */
function loop(){
 detectMotion();
 setTimeout(loop,800);
}

/* ---- start ---- */
async function arm(){
 unlockAudio();
 await startCamera();
 loop();
 setTimeout(startAI,3000);
 setArmed(true);
 statusEl.textContent="🟢 فعال";
}

/* manual */
btn.onclick=arm;

/* auto */
window.onload=()=>{
 if(armed()){
  statusEl.textContent="🔄 فعال‌سازی خودکار";
  arm();
 }
};
""")

    # ---------- manifest.json ----------
    write("manifest.json", """{
"name":"Guard Camera",
"short_name":"GuardCam",
"start_url":".",
"display":"standalone",
"theme_color":"#000",
"background_color":"#000"
}""")

    print("✅ Guard Camera site built successfully.")

if __name__ == "__main__":
    main()
