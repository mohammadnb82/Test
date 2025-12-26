from pathlib import Path
import shutil

BASE = Path("Test/tools/cam1")

HTML = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no">
<title>Cam1 Motion Tool</title>
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

  <div class="buttons">
    <button id="flip">🔄 Flip</button>
    <button id="siren">🔔 Siren</button>
  </div>

</div>

<script src="app.js"></script>
</body>
</html>
"""

CSS = """body{
  margin:0;
  background:#000;
  color:#fff;
  font-family:system-ui,-apple-system;
}

.video-box{
  max-width:500px;
  margin:10px auto;
  border-radius:12px;
  overflow:hidden;
  position:relative;
}

video{width:100%}

#alarm-flash{
  position:absolute;
  inset:0;
  background:rgba(255,0,0,.4);
  display:none;
}

.panel{
  max-width:500px;
  margin:10px auto;
  background:#1c1c1e;
  padding:12px;
  border-radius:12px;
}

.graph{
  height:36px;
  background:#2c2c2e;
  border-radius:8px;
  position:relative;
  overflow:hidden;
}

.bar{
  height:100%;
  width:0;
  background:#30d158;
}

.line{
  position:absolute;
  top:0;
  bottom:0;
  width:3px;
  background:#ff453a;
  transform:translateX(0);
}

.stats{
  display:flex;
  justify-content:space-between;
  margin:6px 0;
}

input[type=range]{width:100%}

.buttons{
  display:grid;
  grid-template-columns:1fr 1fr;
  gap:10px;
}

button{
  padding:12px;
  border-radius:8px;
  border:none;
  font-size:15px;
}

#siren.active{
  background:#ff453a;
  color:#fff;
}

canvas{display:none}
"""

JS = """const video = document.getElementById("webcam");
const canvas = document.getElementById("proc");
const ctx = canvas.getContext("2d",{willReadFrequently:true});

const bar = document.getElementById("bar");
const line = document.getElementById("line");
const graph = document.getElementById("graph");

const slider = document.getElementById("slider");
const tval = document.getElementById("tval");
const mval = document.getElementById("mval");

let lastFrame=null;
let stream=null;
let facing="environment";
let siren=false;
let audio=null;

canvas.width=64;
canvas.height=48;

function updateThreshold(v){
  tval.textContent = v;
  const w = graph.clientWidth;
  const x = (v/100)*w;
  line.style.transform = `translateX(${x}px)`;
}

slider.addEventListener("input", e=>{
  updateThreshold(+e.target.value);
});

async function startCam(){
  if(stream) stream.getTracks().forEach(t=>t.stop());
  stream = await navigator.mediaDevices.getUserMedia({
    video:{facingMode:facing}
  });
  video.srcObject = stream;
  await video.play();
  lastFrame=null;
}

function flipCam(){
  facing = facing==="environment" ? "user" : "environment";
  startCam();
}

function toggleSiren(){
  if(!audio)
    audio = new (window.AudioContext||window.webkitAudioContext)();
  if(audio.state==="suspended") audio.resume();
  siren=!siren;
  document.getElementById("siren")
    .classList.toggle("active",siren);
}

function beep(){
  if(!siren) return;
  const o = audio.createOscillator();
  o.frequency.value = 900;
  o.connect(audio.destination);
  o.start();
  setTimeout(()=>o.stop(),120);
}

function loop(){
  if(video.videoWidth){
    ctx.drawImage(video,0,0,64,48);
    const frame = ctx.getImageData(0,0,64,48);

    if(lastFrame){
      let diff=0;
      for(let i=0;i<frame.data.length;i+=32){
        diff += Math.abs(frame.data[i] - lastFrame.data[i]);
      }
      const motion = Math.min(100,diff*0.03);
      bar.style.width = motion + "%";
      mval.textContent = motion.toFixed(0);

      if(motion >= slider.value && siren){
        document.getElementById("alarm-flash").style.display="block";
        beep();
      }else{
        document.getElementById("alarm-flash").style.display="none";
      }
    }
    lastFrame = frame;
  }
  requestAnimationFrame(loop);
}

document.getElementById("flip").onclick = flipCam;
document.getElementById("siren").onclick = toggleSiren;

updateThreshold(slider.value);
startCam();
loop();
"""

def main():
    if BASE.exists():
        shutil.rmtree(BASE)

    BASE.mkdir(parents=True, exist_ok=True)

    (BASE / "index.html").write_text(HTML, encoding="utf8")
    (BASE / "style.css").write_text(CSS, encoding="utf8")
    (BASE / "app.js").write_text(JS, encoding="utf8")

    print("✅ cam1 rebuilt successfully")

if __name__ == "__main__":
    main()
