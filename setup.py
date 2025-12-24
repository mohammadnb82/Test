import os
from textwrap import dedent

BASE = "guard_camera"

files = {
    "index.html": dedent("""
    <!DOCTYPE html>
    <html lang="fa">
    <head>
        <meta charset="UTF-8"/>
        <title>دوربین نگهبان</title>
        <meta name="viewport" content="width=device-width,initial-scale=1"/>
        <link rel="manifest" href="manifest.json"/>
        <link rel="stylesheet" href="css/style.css"/>
    </head>
    <body>
        <h1>📷 دوربین نگهبان (Client-Side)</h1>

        <video id="cam" autoplay muted playsinline></video>

        <div class="controls">
            <button onclick="App.start()">شروع</button>
            <button onclick="App.switchCamera()">سوئیچ دوربین</button>
            <button onclick="App.toggleMode()">حالت مصرف</button>
        </div>

        <pre id="log"></pre>

        <!-- AI -->
        <script src="https://cdn.jsdelivr.net/npm/@tensorflow/tfjs@4"></script>
        <script src="https://cdn.jsdelivr.net/npm/@tensorflow-models/coco-ssd"></script>
        <script src="https://cdn.jsdelivr.net/npm/face-api.js"></script>

        <script src="js/main.js"></script>
    </body>
    </html>
    """),

    "css/style.css": dedent("""
    body {
        background: #0f172a;
        color: #e5e7eb;
        font-family: sans-serif;
        text-align: center;
        padding: 20px;
    }
    video {
        width: 100%;
        max-width: 500px;
        border-radius: 10px;
        margin: 20px 0;
        box-shadow: 0 0 20px #000;
    }
    button {
        padding: 10px 16px;
        margin: 5px;
        font-size: 16px;
        border-radius: 6px;
        border: none;
        cursor: pointer;
    }
    pre {
        text-align: left;
        max-width: 500px;
        margin: auto;
        background: #020617;
        padding: 10px;
    }
    """),

    "js/main.js": dedent("""
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
            logEl.textContent += msg + "\\n";
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
    """),

    "manifest.json": dedent("""
    {
      "name": "دوربین نگهبان",
      "short_name": "GuardCam",
      "start_url": "./index.html",
      "display": "standalone",
      "background_color": "#000000",
      "theme_color": "#000000"
    }
    """),
}

def write(path, content):
    full = os.path.join(BASE, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content.strip())

def main():
    os.makedirs(BASE, exist_ok=True)
    for path, content in files.items():
        write(path, content)
    print("✅ پروژه guard_camera ساخته شد")

if __name__ == "__main__":
    main()
