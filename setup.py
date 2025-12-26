from pathlib import Path
import shutil

BASE = Path("Test/tools/cam1")

HTML = """<!doctype html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no">
<title>Cam1</title>
<link rel="stylesheet" href="style.css">
</head>
<body>

<div class="video-box">
  <video id="webcam" autoplay playsinline muted></video>
  <div id="alarm-flash"></div>
</div>

<canvas id="proc"></canvas>

<div class="panel">
  <div id="graph" class="graph">
    <div id="bar" class="bar"></div>
    <div id="line" class="line"></div>
  </div>

  <div class="stats">
    <span>Trigger: <b><span id="tval">40</span>%</b></span>
    <span>Motion: <b><span id="mval">0</span>%</b></span>
  </div>

  <input id="slider" type="range" min="0" max="100" value="40">

  <div class="btns">
    <button id="flip">🔄 Flip Cam</button>
    <button id="siren">🔔 Siren</button>
  </div>
</div>

<script src="app.js"></script>
</body>
</html>
"""

CSS = """body{margin:0;background:#000;color:#fff;font-family:system-ui}
.video-box{max-width:500px;margin:auto;position:relative;border-radius:12px;overflow:hidden}
video{width:100%}
#alarm-flash{position:absolute;inset:0;background:rgba(255,0,0,.4);display:none}

.panel{max-width:500px;margin:10px auto;background:#1c1c1e;padding:12px;border-radius:12px}

.graph{
  height:36px;
  background:#2c2c2e;
  border-radius:8px;
  position:relative;
  overflow:hidden;
}

.bar{
  position:absolute;
  left:0;top:0;bottom:0;
  width:0%;
  background:#30d158;
  z-index:1;
}

.line{
  position:absolute;
  top:0;bottom:0;
  width:3px;
  background:#ff453a;
  z-index:2;
  transform:translateX(0);
}

.stats{display:flex;justify-content:space-between;margin:6px 0}
input{width:100%}
.btns{display:grid;grid-template-columns:1fr 1fr;gap:10px}
button{padding:12px;border-radius:8px;border:none}
#siren.active{background:#ff453a;color:#fff}
canvas{display:none}
"""

JS = """const video=document.getElementById("webcam");
const canvas=document.getElementById("proc");
const ctx=canvas.getContext("2d",{willReadFrequently:true});

const graph=document.getElementById("graph");
const bar=document.getElementById("bar");
const line=document.getElementById("line");

const slider=document.getElementById("slider");
const tval=document.getElementById("tval");
const mval=document.getElementById("mval");

let last=null,stream=null,facing="environment";
let siren=false,audio=null;

canvas.width=64; canvas.height=48;

function updateLine(v){
  tval.textContent=v;
  requestAnimationFrame(()=>{
    const w=graph.clientWidth;
    const x=(v/100)*w;
    const center=x-(line.offsetWidth/2);
    line.style.transform=`translateX(${center}px)`;
  });
}

slider.addEventListener("input",e=>updateLine(+e.target.value));

async function cam(){
  if(stream) stream.getTracks().forEach(t=>t.stop());
  stream=await navigator.mediaDevices.getUserMedia({video:{facingMode:facing}});
  video.srcObject=stream;
  await video.play();
  last=null;
}

function flip(){
  facing=facing==="environment"?"user":"environment";
  cam();
}

function toggleSiren(){
  if(!audio) audio=new (AudioContext||webkitAudioContext)();
  if(audio.state==="suspended") audio.resume();
  siren=!siren;
  document.getElementById("siren").classList.toggle("active",siren);
}

function beep(){
  if(!siren) return;
  const o=audio.createOscillator();
  o.frequency.value=900;
  o.connect(audio.destination);
  o.start();
  setTimeout(()=>o.stop(),120);
}

function loop(){
  if(video.videoWidth){
    ctx.drawImage(video,0,0,64,48);
    const f=ctx.getImageData(0,0,64,48);
    if(last){
      let d=0;
      for(let i=0;i<f.data.length;i+=32)
        d+=Math.abs(f.data[i]-last.data[i]);
      const m=Math.min(100,d*0.03);
      bar.style.width=m+"%";
      mval.textContent=m.toFixed(0);
      if(m>=slider.value && siren){
        document.getElementById("alarm-flash").style.display="block";
        beep();
      }else{
        document.getElementById("alarm-flash").style.display="none";
      }
    }
    last=f;
  }
  requestAnimationFrame(loop);
}

document.getElementById("flip").onclick=flip;
document.getElementById("siren").onclick=toggleSiren;

updateLine(slider.value);
cam(); loop();
"""

def main():
    if BASE.exists():
        shutil.rmtree(BASE)
    BASE.mkdir(parents=True)
    (BASE/"index.html").write_text(HTML,"utf8")
    (BASE/"style.css").write_text(CSS,"utf8")
    (BASE/"app.js").write_text(JS,"utf8")
    print("✅ cam1 rebuilt – line visibility fixed")

if __name__=="__main__":
    main()
