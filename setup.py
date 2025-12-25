from pathlib import Path
import shutil

BASE = Path("Test/tools/cam1")

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
<title>Cam1 – Motion Guard</title>
<link rel="stylesheet" href="style.css">
</head>
<body>

<div class="video-box">
  <video id="webcam" autoplay playsinline muted></video>
  <div id="alarm-flash"></div>
</div>

<canvas id="proc-canvas"></canvas>

<div class="controls-card">

  <div class="graph-wrapper">
    <div id="bar-motion" class="motion-bar"></div>
    <div id="line-thresh" class="threshold-line"></div>
  </div>

  <div class="stats-row">
    <span>Trigger: <b><span id="txt-thresh">40</span>%</b></span>
    <span>Motion: <b><span id="txt-motion">0</span>%</b></span>
  </div>

  <input type="range" id="input-slider" min="0" max="100" value="40">

  <div class="buttons-grid">
    <button class="btn btn-grey" id="btnFlip">🔄 Flip Cam</button>
    <button class="btn btn-red" id="btnSiren">🔔 Siren</button>
  </div>

</div>

<script src="app.js"></script>
</body>
</html>
"""

CSS = """body{
 margin:0;padding:12px;background:#000;color:#fff;
 font-family:system-ui,-apple-system
}
.video-box{max-width:500px;margin:auto;position:relative;border-radius:12px;overflow:hidden}
video{width:100%;height:auto}
video.mirror{transform:scaleX(-1)}
#alarm-flash{position:absolute;inset:0;background:rgba(255,0,0,.4);display:none}
.controls-card{max-width:500px;margin:10px auto;background:#1c1c1e;padding:12px;border-radius:12px}
.graph-wrapper{height:40px;background:#2c2c2e;border-radius:6px;position:relative;overflow:hidden}
.motion-bar{height:100%;width:0%;background:#32d74b}
.threshold-line{position:absolute;top:0;bottom:0;width:3px;background:red;left:40%}
.stats-row{display:flex;justify-content:space-between;margin:6px 0;font-size:14px}
.buttons-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:8px}
.btn{padding:12px;border-radius:8px;border:none;font-size:15px}
.btn-grey{background:#3a3a3c;color:#fff}
.btn-red{background:#3a3a3c;color:#fff}
.btn-red.active{background:#ff453a}
canvas{display:none}
"""

JS = """const video = document.getElementById("webcam");
const canvas = document.getElementById("proc-canvas");
const ctx = canvas.getContext("2d",{willReadFrequently:true});

const bar = document.getElementById("bar-motion");
const flash = document.getElementById("alarm-flash");
const slider = document.getElementById("input-slider");
const txtThresh = document.getElementById("txt-thresh");
const txtMotion = document.getElementById("txt-motion");
const threshLine = document.getElementById("line-thresh");

let facing="environment",stream=null;
let lastFrame=null;
let siren=false,audioCtx=null;

canvas.width=64; canvas.height=48;

async function startCamera(){
 if(stream) stream.getTracks().forEach(t=>t.stop());
 stream = await navigator.mediaDevices.getUserMedia({video:{facingMode:facing}});
 video.srcObject = stream;
 video.play();
 video.classList.toggle("mirror",facing==="user");
 lastFrame=null;
}

function flipCam(){
 facing = facing==="environment"?"user":"environment";
 startCamera();
}

function toggleSiren(){
 if(!audioCtx) audioCtx=new(window.AudioContext||window.webkitAudioContext)();
 if(audioCtx.state==="suspended") audioCtx.resume();
 siren=!siren;
 document.getElementById("btnSiren").classList.toggle("active",siren);
}

function beep(){
 if(!siren||!audioCtx) return;
 const o=audioCtx.createOscillator();
 o.frequency.value=800;
 o.connect(audioCtx.destination);
 o.start(); setTimeout(()=>o.stop(),120);
}

function updateThreshold(val){
 txtThresh.innerText=val;
 threshLine.style.left=val+"%";
}

slider.oninput=e=>updateThreshold(e.target.value);

function loop(){
 if(video.videoWidth){
  ctx.drawImage(video,0,0,64,48);
  const cur=ctx.getImageData(0,0,64,48);
  if(lastFrame){
   let diff=0;
   for(let i=0;i<cur.data.length;i+=32){
    diff+=Math.abs(cur.data[i]-lastFrame.data[i]);
   }
   let motion=Math.min(100,diff*0.025);
   bar.style.width=motion+"%";
   txtMotion.innerText=Math.floor(motion);
   if(motion>=slider.value && siren){
     flash.style.display="block"; beep();
   } else flash.style.display="none";
  }
  lastFrame=cur;
 }
 requestAnimationFrame(loop);
}

document.getElementById("btnFlip").onclick=flipCam;
document.getElementById("btnSiren").onclick=toggleSiren;

updateThreshold(slider.value);
startCamera(); loop();
"""

def main():
    if BASE.exists():
        shutil.rmtree(BASE)
    BASE.mkdir(parents=True)

    (BASE/"index.html").write_text(HTML,encoding="utf-8")
    (BASE/"style.css").write_text(CSS,encoding="utf-8")
    (BASE/"app.js").write_text(JS,encoding="utf-8")

    print("✅ cam1 fixed & rebuilt successfully")

if __name__=="__main__":
    main()
