const video=document.getElementById("video");
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
