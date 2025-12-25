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
<link rel="stylesheet" href="style.css">
</head>
<body>

<h3>🛡 Guard Camera</h3>
<div id="status">آماده</div>

<video id="video" autoplay playsinline muted></video>
<canvas id="canvas"></canvas>

<div class="buttons">
  <button id="frontCam">📷 جلو</button>
  <button id="backCam">📷 پشت</button>
  <button id="sirenBtn">🚨 آژیر</button>
</div>

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
video,canvas{
 width:100%;max-height:60vh;margin-top:5px
}
.buttons{margin-top:10px}
button{
 padding:10px;font-size:16px;
 margin:4px;border-radius:6px
}
#status{color:#0f0;margin:8px}
""")

    # ---------- app.js ----------
    write("app.js", """const video=document.getElementById("video");
const canvas=document.getElementById("canvas");
const ctx=canvas.getContext("2d");
const statusEl=document.getElementById("status");

let stream,audioCtx,model,lastFrame=null;
let facing="environment";

/* ---------- audio ---------- */
function unlockAudio(){
 audioCtx=new(window.AudioContext||window.webkitAudioContext)();
 audioCtx.resume();
}
function siren(){
 if(!audioCtx)return;
 const o=audioCtx.createOscillator();
 o.type="sawtooth";
 o.frequency.value=800;
 o.connect(audioCtx.destination);
 o.start();
 setTimeout(()=>o.stop(),800);
}

/* ---------- camera ---------- */
async function startCamera(){
 if(stream)stream.getTracks().forEach(t=>t.stop());
 stream=await navigator.mediaDevices.getUserMedia({video:{facingMode:facing}});
 video.srcObject=stream;
 return new Promise(r=>video.onloadedmetadata=()=>{video.play();r();});
}

/* ---------- motion ---------- */
function detectMotion(){
 if(video.videoWidth===0)return;
 canvas.width=video.videoWidth;
 canvas.height=video.videoHeight;
 ctx.drawImage(video,0,0);
 const frame=ctx.getImageData(0,0,canvas.width,canvas.height);
 if(lastFrame){
  let diff=0;
  for(let i=0;i<frame.data.length;i+=80){
   diff+=Math.abs(frame.data[i]-lastFrame.data[i]);
  }
  if(diff>2500){
   statusEl.textContent="🚨 حرکت";
   siren();
   detectHuman();
  }
 }
 lastFrame=frame;
}

/* ---------- AI ---------- */
async function loadAI(){
 model=await cocoSsd.load();
 statusEl.textContent="✅ AI آماده";
}
async function detectHuman(){
 if(!model)return;
 const preds=await model.detect(video);
 preds.forEach(p=>{
  if(p.class==="person"&&p.score>0.6){
   statusEl.textContent="🧍 انسان";
   siren();
  }
 });
}

/* ---------- loop ---------- */
function loop(){
 detectMotion();
 setTimeout(loop,900);
}

/* ---------- buttons ---------- */
document.getElementById("frontCam").onclick=async()=>{
 unlockAudio();
 facing="user";
 statusEl.textContent="📷 جلو";
 await startCamera();
};
document.getElementById("backCam").onclick=async()=>{
 unlockAudio();
 facing="environment";
 statusEl.textContent="📷 پشت";
 await startCamera();
};
document.getElementById("sirenBtn").onclick=()=>{
 unlockAudio();
 siren();
};

/* ---------- init ---------- */
(async()=>{
 await startCamera();
 loadAI();
 loop();
})();
""")

    print("✅ New Guard Camera project created.")

if __name__ == "__main__":
    main()
