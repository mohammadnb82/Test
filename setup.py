from pathlib import Path
import shutil

BASE = Path("Test/tools/cam1")

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
<title>Motion Detector</title>
<link rel="stylesheet" href="style.css">
</head>
<body>

<div class="video-box">
  <video id="webcam" autoplay playsinline muted></video>
  <div id="alarm-flash"></div>
</div>

<canvas id="proc"></canvas>

<div class="controls">
  <div class="graph">
    <div id="bar" class="motion-bar"></div>
    <div id="line" class="threshold-line"></div>
  </div>

  <div class="stats">
    <span class="red">Trigger: <span id="txt-th">40</span>%</span>
    <span class="green">Motion: <span id="txt-mo">0</span>%</span>
  </div>

  <input type="range" id="slider" min="0" max="100" value="40">

  <div class="buttons">
    <button onclick="flipCam()">🔄 Flip Cam</button>
    <button id="btn-siren" onclick="toggleSiren()">🔔 Siren</button>
  </div>
</div>

<script src="app.js"></script>
</body>
</html>
"""

CSS = """body{
  background:#000;
  margin:0;
  padding:15px;
  font-family:-apple-system,system-ui;
  color:#fff;
}

.video-box{
  max-width:500px;
  margin:auto;
  aspect-ratio:4/3;
  border-radius:12px;
  overflow:hidden;
  position:relative;
  background:#111;
}

video{width:100%;height:100%;object-fit:cover}

#alarm-flash{
  position:absolute;inset:0;
  background:rgba(255,69,58,.45);
  display:none;
  z-index:10;
}

.controls{
  max-width:500px;
  margin:15px auto;
  background:#1c1c1e;
  padding:15px;
  border-radius:16px;
}

.graph{
  position:relative;
  height:45px;
  background:#2c2c2e;
  border-radius:8px;
  overflow:hidden;
}

.motion-bar{
  height:100%;
  width:0%;
  background:#32d74b;
  z-index:1;
}

.threshold-line{
  position:absolute;
  top:0;bottom:0;
  width:4px;
  background:#ff453a;
  left:40%;
  transform:translateX(-50%);
  z-index:5;
  box-shadow:0 0 5px red;
}

.stats{
  display:flex;
  justify-content:space-between;
  margin:8px 0;
  font-weight:700;
}

.red{color:#ff453a}
.green{color:#32d74b}

input{width:100%}

.buttons{
  margin-top:10px;
  display:grid;
  grid-template-columns:1fr 1fr;
  gap:10px;
}

button{
  padding:14px;
  border:none;
  border-radius:12px;
  background:#3a3a3c;
  color:#fff;
  font-size:15px;
}

#btn-siren.active{
  background:#ff453a;
  animation:pulse 1s infinite;
}

@keyframes pulse{
  0%{opacity:1}
  50%{opacity:.8}
  100%{opacity:1}
}

canvas{display:none}
"""

JS = """const CONF={
  w:64,h:48,diff:20,gain:5
};

const video=document.getElementById("webcam");
const canvas=document.getElementById("proc");
const ctx=canvas.getContext("2d",{willReadFrequently:true});

const bar=document.getElementById("bar");
const line=document.getElementById("line");
const txtTh=document.getElementById("txt-th");
const txtMo=document.getElementById("txt-mo");
const slider=document.getElementById("slider");
const flash=document.getElementById("alarm-flash");
const btnS=document.getElementById("btn-siren");

let stream=null,facing="environment";
let last=null,siren=false,ac=null;

canvas.width=CONF.w; canvas.height=CONF.h;

function updateThresh(v){
  line.style.left=v+"%";
  txtTh.textContent=v;
}

slider.oninput=e=>updateThresh(e.target.value);

async function startCam(){
  if(stream) stream.getTracks().forEach(t=>t.stop());
  stream=await navigator.mediaDevices.getUserMedia({video:{facingMode:facing}});
  video.srcObject=stream;
  await video.play();
  last=null;
}

function flipCam(){
  facing=facing==="environment"?"user":"environment";
  startCam();
}

function toggleSiren(){
  if(!ac) ac=new (AudioContext||webkitAudioContext)();
  if(ac.state==="suspended") ac.resume();
  siren=!siren;
  btnS.classList.toggle("active",siren);
}

function beep(){
  if(!siren||!ac||ac.state!=="running")return;
  const o=ac.createOscillator();
  const g=ac.createGain();
  o.frequency.value=800;
  g.gain.value=.3;
  o.connect(g); g.connect(ac.destination);
  o.start(); o.stop(ac.currentTime+.1);
}

function loop(){
  if(video.videoWidth){
    ctx.drawImage(video,0,0,CONF.w,CONF.h);
    const f=ctx.getImageData(0,0,CONF.w,CONF.h);
    if(last){
      let c=0;
      for(let i=0;i<f.data.length;i+=4){
        const d=Math.abs(f.data[i]-last.data[i]);
        if(d>CONF.diff) c++;
      }
      let m=Math.floor(c/(CONF.w*CONF.h)*100*CONF.gain);
      if(m>100)m=100;
      bar.style.width=m+"%";
      txtMo.textContent=m;
      const th=+slider.value;
      if(m>=th && th>0){
        bar.style.background="#ff453a";
        flash.style.display="block";
        beep();
      }else{
        bar.style.background="#32d74b";
        flash.style.display="none";
      }
    }
    last=f;
  }
  requestAnimationFrame(loop);
}

updateThresh(slider.value);
startCam();
loop();
"""

def main():
    if BASE.exists():
        shutil.rmtree(BASE)
    BASE.mkdir(parents=True)

    (BASE/"index.html").write_text(HTML,"utf8")
    (BASE/"style.css").write_text(CSS,"utf8")
    (BASE/"app.js").write_text(JS,"utf8")

    print("✅ cam1 rebuilt – iOS safe logic applied")

if __name__=="__main__":
    main()
