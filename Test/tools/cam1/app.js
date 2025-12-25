const video = document.getElementById("webcam");
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
