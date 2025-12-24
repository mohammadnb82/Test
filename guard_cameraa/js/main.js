const logEl = document.getElementById("log");
const video = document.getElementById("cam");

const App = {
    stream: null,
    facing: "environment",
    coco: null,
    mode: "balanced",
    recorder: null,
    chunks: [],

    log(msg){
        logEl.textContent += msg + "\n";
    },

    async start(){
        this.log("شروع سیستم...");
        await this.startCamera();
        await this.loadAI();
        this.watch();
    },

    async startCamera(){
        if(this.stream) this.stream.getTracks().forEach(t=>t.stop());
        this.stream = await navigator.mediaDevices.getUserMedia({
            video:{facingMode:this.facing},
            audio:false
        });
        video.srcObject = this.stream;
        await video.play();
    },

    switchCamera(){
        this.facing = this.facing==="user"?"environment":"user";
        this.startCamera();
    },

    async loadAI(){
        this.log("بارگذاری مدل‌ها...");
        this.coco = await cocoSsd.load();
        await faceapi.nets.tinyFaceDetector.loadFromUri("https://cdn.jsdelivr.net/npm/face-api.js/models");
        this.log("AI آماده است");
    },

    toggleMode(){
        this.mode = this.mode==="balanced"?"power":"balanced";
        this.log("Mode: "+this.mode);
    },

    async watch(){
        const canvas = document.createElement("canvas");
        const ctx = canvas.getContext("2d");
        let last = null;

        setInterval(async ()=>{
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            ctx.drawImage(video,0,0);

            const frame = ctx.getImageData(0,0,canvas.width,canvas.height);
            let motion = false;

            if(last){
                let diff=0;
                for(let i=0;i<frame.data.length;i+=4){
                    if(Math.abs(frame.data[i]-last.data[i])>30) diff++;
                }
                motion = diff>3000;
            }
            last = frame;

            if(!motion) return;

            this.log("حرکت!");

            if(this.coco){
                const r = await this.coco.detect(video);
                if(r.some(x=>x.class==="person" && x.score>0.6)){
                    this.log("👤 انسان شناسایی شد");
                    this.beep();
                    this.record();
                }
            }

        }, this.mode==="power"?3000:1000);
    },

    record(){
        if(this.recorder && this.recorder.state==="recording") return;

        this.log("🎥 ضبط آغاز شد");
        this.recorder = new MediaRecorder(this.stream);
        this.chunks=[];

        this.recorder.ondataavailable=e=>this.chunks.push(e.data);
        this.recorder.onstop=()=>{
            const blob=new Blob(this.chunks,{type:"video/webm"});
            const url=URL.createObjectURL(blob);
            const a=document.createElement("a");
            a.href=url;
            a.download="event_"+Date.now()+".webm";
            a.click();
        };

        this.recorder.start();
        setTimeout(()=>this.recorder.stop(),5000);
    },

    beep(){
        const ctx=new AudioContext();
        const o=ctx.createOscillator();
        o.connect(ctx.destination);
        o.frequency.value=880;
        o.start();
        setTimeout(()=>o.stop(),400);
    }
};

window.App=App;