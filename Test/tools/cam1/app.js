const CONF={
  w:64,h:48,diff:20,gain:5
};

const video=document.getElementById("webcam");
const canvas=document.getElementById("proc");
const ctx=canvas.getContext("2d",{willReadFrequently:true});

const bar=document.getElementById("bar");
const line=document.getElementById("line");
const txtTh=document.getElementById("txt-th");
const txtMo=document.getElementById("txt-mo");
const slider=document.getElementById("slider");
const flash=document.getElementById("alarm-flash");
const btnS=document.getElementById("btn-siren");

let stream=null,facing="environment";
let last=null,siren=false,ac=null;

canvas.width=CONF.w; canvas.height=CONF.h;

function updateThresh(v){
  line.style.left=v+"%";
  txtTh.textContent=v;
}

slider.oninput=e=>updateThresh(e.target.value);

async function startCam(){
  if(stream) stream.getTracks().forEach(t=>t.stop());
  stream=await navigator.mediaDevices.getUserMedia({video:{facingMode:facing}});
  video.srcObject=stream;
  await video.play();
  last=null;
}

function flipCam(){
  facing=facing==="environment"?"user":"environment";
  startCam();
}

function toggleSiren(){
  if(!ac) ac=new (AudioContext||webkitAudioContext)();
  if(ac.state==="suspended") ac.resume();
  siren=!siren;
  btnS.classList.toggle("active",siren);
}

function beep(){
  if(!siren||!ac||ac.state!=="running")return;
  const o=ac.createOscillator();
  const g=ac.createGain();
  o.frequency.value=800;
  g.gain.value=.3;
  o.connect(g); g.connect(ac.destination);
  o.start(); o.stop(ac.currentTime+.1);
}

function loop(){
  if(video.videoWidth){
    ctx.drawImage(video,0,0,CONF.w,CONF.h);
    const f=ctx.getImageData(0,0,CONF.w,CONF.h);
    if(last){
      let c=0;
      for(let i=0;i<f.data.length;i+=4){
        const d=Math.abs(f.data[i]-last.data[i]);
        if(d>CONF.diff) c++;
      }
      let m=Math.floor(c/(CONF.w*CONF.h)*100*CONF.gain);
      if(m>100)m=100;
      bar.style.width=m+"%";
      txtMo.textContent=m;
      const th=+slider.value;
      if(m>=th && th>0){
        bar.style.background="#ff453a";
        flash.style.display="block";
        beep();
      }else{
        bar.style.background="#32d74b";
        flash.style.display="none";
      }
    }
    last=f;
  }
  requestAnimationFrame(loop);
}

updateThresh(slider.value);
startCam();
loop();
