const video = document.getElementById("webcam");
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
