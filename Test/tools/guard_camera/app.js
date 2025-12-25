let video = document.getElementById("video");
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
