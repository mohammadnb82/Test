const video=document.getElementById("webcam");
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
