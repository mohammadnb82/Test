const video = document.getElementById("webcam");
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
