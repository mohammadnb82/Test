const Guard = (() => {
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
