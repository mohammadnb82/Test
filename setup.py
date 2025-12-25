from pathlib import Path
import json

ROOT = Path("Test/tools/guard_camera")
ASSETS = ROOT / "assets"

ASSETS.mkdir(parents=True, exist_ok=True)

# ---------- index.html ----------
(ROOT / "index.html").write_text("""<!DOCTYPE html>
<html lang="fa">
<head>
<meta charset="UTF-8">
<title>Guard Camera</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="manifest" href="manifest.json">
<style>
body{background:#111;color:#eee;font-family:sans-serif;text-align:center}
video{width:90%;max-width:520px;border:2px solid #444}
button{margin:4px;padding:10px}
</style>
</head>
<body>

<h2>🛡 Guard Camera (Client‑Side Full)</h2>

<video id="cam" autoplay muted playsinline></video><br>

<button onclick="Guard.start()">▶ شروع</button>
<button onclick="Guard.stop()">⏹ توقف</button>
<button onclick="Guard.toggleRecord()">⏺ ضبط</button>

<p id="status">آماده</p>

<script src="https://cdn.jsdelivr.net/npm/@tensorflow/tfjs@4.16.0"></script>
<script src="https://cdn.jsdelivr.net/npm/@tensorflow-models/coco-ssd"></script>
<script src="assets/main.js"></script>

<script>
if('serviceWorker' in navigator){
  navigator.serviceWorker.register('sw.js');
}
</script>
</body>
</html>
""", encoding="utf-8")

# ---------- main.js ----------
(ASSETS / "main.js").write_text("""const Guard = (() => {
  let video, stream, canvas, ctx, lastFrame;
  let audioCtx, recorder, chunks=[], recording=false;
  let model;

  const status = t => document.getElementById("status").innerText = t;

  async function start(){
    video = document.getElementById("cam");
    stream = await navigator.mediaDevices.getUserMedia({video:true,audio:true});
    video.srcObject = stream;

    canvas = document.createElement("canvas");
    ctx = canvas.getContext("2d");

    recorder = new MediaRecorder(stream);
    recorder.ondataavailable = e => chunks.push(e.data);
    recorder.onstop = save;

    status("⏳ بارگذاری AI...");
    model = await cocoSsd.load();
    status("✅ فعال");

    requestAnimationFrame(loop);
  }

  function stop(){
    stream.getTracks().forEach(t=>t.stop());
    status("⏹ متوقف شد");
  }

  function toggleRecord(){
    if(!recording){chunks=[];recorder.start();recording=true;status("🔴 ضبط");}
    else{recorder.stop();recording=false;}
  }

  function save(){
    const b=new Blob(chunks,{type:"video/webm"});
    const a=document.createElement("a");
    a.href=URL.createObjectURL(b);
    a.download="guard.webm";
    a.click();
    status("💾 ذخیره شد");
  }

  function beep(){
    if(!audioCtx) audioCtx=new AudioContext();
    const o=audioCtx.createOscillator();
    o.frequency.value=1000;
    o.connect(audioCtx.destination);
    o.start(); setTimeout(()=>o.stop(),200);
  }

  async function loop(){
    if(!video.videoWidth){requestAnimationFrame(loop);return;}
    canvas.width=video.videoWidth; canvas.height=video.videoHeight;
    ctx.drawImage(video,0,0);

    const frame=ctx.getImageData(0,0,canvas.width,canvas.height).data;
    if(lastFrame){
      let diff=0;
      for(let i=0;i<frame.length;i+=60)
        diff+=Math.abs(frame[i]-lastFrame[i]);
      if(diff>6000){status("🚨 حرکت");beep();}
    }
    lastFrame=frame.slice(0);

    const preds = await model.detect(canvas);
    preds.forEach(p=>{
      if(p.class==="person" && p.score>0.6){
        status("🚨 انسان شناسایی شد");
        beep();
      }
    });

    requestAnimationFrame(loop);
  }

  return {start,stop,toggleRecord};
})();
""", encoding="utf-8")

# ---------- PWA ----------
(ROOT / "manifest.json").write_text(json.dumps({
  "name":"Guard Camera",
  "short_name":"Guard",
  "start_url":".",
  "display":"standalone",
  "background_color":"#111",
  "theme_color":"#111"
}, indent=2), encoding="utf-8")

(ROOT / "sw.js").write_text("""self.addEventListener('fetch',e=>{
  e.respondWith(fetch(e.request).catch(()=>new Response()));
});""", encoding="utf-8")

print("✅ Guard Camera FULL ساخ → Test/tools/guard_camera")
