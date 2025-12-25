from pathlib import Path
import shutil

BASE = Path("tools/cam1")

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
    <span class="stat-left">Trigger: <span id="txt-thresh">40</span>%</span>
    <span class="stat-right">Motion: <span id="txt-motion">0</span>%</span>
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

CSS = """@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

:root{
 --bg:#000;--card:#1c1c1e;--white:#fff;
 --red:#ff453a;--green:#32d74b;--blue:#0a84ff
}
body{
 background:var(--bg);color:var(--white);
 font-family:Inter,system-ui,sans-serif;
 margin:0;padding:15px;
 display:flex;flex-direction:column;align-items:center;
 height:100vh;box-sizing:border-box;overflow:hidden
}
.video-box{
 width:100%;max-width:500px;
 background:#111;border-radius:12px;
 overflow:hidden;position:relative
}
video{width:100%;height:100%;object-fit:cover}
video.mirrored{transform:scaleX(-1)}
#alarm-flash{
 position:absolute;inset:0;
 background:rgba(255,69,58,.45);
 display:none;z-index:5
}
.controls-card{
 width:100%;max-width:500px;
 background:var(--card);padding:16px;
 border-radius:14px;margin-top:10px
}
.graph-wrapper{
 height:40px;background:#2c2c2e;
 border-radius:8px;overflow:hidden;position:relative
}
.motion-bar{height:100%;width:0%;background:var(--green)}
.threshold-line{
 position:absolute;top:0;bottom:0;width:3px;
 background:var(--red);left:40%
}
.buttons-grid{
 display:grid;grid-template-columns:1fr 1fr;
 gap:10px;margin-top:10px
}
.btn{
 padding:14px;border-radius:10px;
 border:none;font-size:15px;font-weight:600
}
.btn-grey{background:#3a3a3c;color:white}
.btn-red{background:#3a3a3c;color:#eee;border:1px solid #444}
.btn-red.active{background:var(--red);color:white}
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

let stream=null,facing="environment";
let last=null,siren=false,audioCtx=null;

canvas.width=64;canvas.height=48;

async function startCamera(){
 if(stream) stream.getTracks().forEach(t=>t.stop());
 stream = await navigator.mediaDevices.getUserMedia({video:{facingMode:facing}});
 video.srcObject = stream;
 video.onloadedmetadata = ()=>video.play();
 video.classList.toggle("mirrored",facing==="user");
 last=null;
}

function flip(){
 facing = facing==="environment"?"user":"environment";
 startCamera();
}

function toggleSiren(){
 if(!audioCtx){
   audioCtx=new(window.AudioContext||window.webkitAudioContext)();
 }
 if(audioCtx.state==="suspended") audioCtx.resume();
 siren=!siren;
 document.getElementById("btnSiren").classList.toggle("active",siren);
}

function beep(){
 if(!audioCtx||audioCtx.state!=="running") return;
 const o=audioCtx.createOscillator();
 o.frequency.value=900;
 o.connect(audioCtx.destination);
 o.start();setTimeout(()=>o.stop(),150);
}

function loop(){
 if(video.videoWidth){
  ctx.drawImage(video,0,0,64,48);
  const f = ctx.getImageData(0,0,64,48);
  if(last){
   let diff=0;
   for(let i=0;i<f.data.length;i+=40)
     diff+=Math.abs(f.data[i]-last.data[i]);
   let p=Math.min(100,diff*0.02);
   bar.style.width=p+'%';
   txtMotion.innerText=Math.floor(p);
   if(p>=slider.value && siren){ flash.style.display="block";beep();}
   else flash.style.display="none";
  }
  last=f;
 }
 requestAnimationFrame(loop);
}

slider.oninput=e=>txtThresh.innerText=e.target.value;
document.getElementById("btnFlip").onclick=flip;
document.getElementById("btnSiren").onclick=toggleSiren;

startCamera(); loop();
"""

def main():
    if BASE.exists():
        shutil.rmtree(BASE)
    BASE.mkdir(parents=True)

    (BASE / "index.html").write_text(HTML, encoding="utf-8")
    (BASE / "style.css").write_text(CSS, encoding="utf-8")
    (BASE / "app.js").write_text(JS, encoding="utf-8")

    print("✅ cam1 project created in /tools/cam1")

if __name__ == "__main__":
    main()
