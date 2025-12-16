import os

# مسیر پروژه
project_root = "tools/face_detection_camera"

# ایجاد ساختار پوشه‌ها
folders = [
    "tools",
    f"{project_root}",
    f"{project_root}/css",
    f"{project_root}/js",
]

for folder in folders:
    os.makedirs(folder, exist_ok=True)

# فایل .keep برای گیت
with open("tools/.keep", "w", encoding="utf-8") as f:
    f.write("")

# --- محتوای HTML (با اضافه کردن ویژگی‌های حیاتی برای iOS) ---
html_content = """<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>دوربین نگهبان هوشمند</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    <div class="container">
        <header>
            <h1>🎥 دوربین نگهبان هوشمند</h1>
            <div class="status" id="status">آماده به کار</div>
        </header>

        <div class="controls">
            <button id="startBtn" class="btn btn-primary">▶️ روشن کردن دوربین</button>
            <button id="stopBtn" class="btn btn-danger" disabled>⏹️ خاموش</button>
            
            <div class="toggle-wrapper">
                <label class="toggle">
                    <input type="checkbox" id="alarmToggle">
                    <span class="slider"></span>
                    <span class="label-text">🔊 صدای آژیر</span>
                </label>
            </div>
        </div>

        <div class="video-wrapper">
            <!-- ویژگی playsinline برای آیفون حیاتی است -->
            <video id="video" playsinline webkit-playsinline muted autoplay></video>
            <canvas id="canvas"></canvas>
            <div class="overlay-msg" id="msg">...</div>
        </div>

        <div class="logs">
            <h3>📝 گزارش‌ها</h3>
            <div id="logContainer"></div>
            <button id="clearLogs" class="btn btn-small">پاک کردن لیست</button>
        </div>
    </div>

    <!-- کتابخانه‌های هوش مصنوعی -->
    <script src="https://cdn.jsdelivr.net/npm/@tensorflow/tfjs"></script>
    <script src="https://cdn.jsdelivr.net/npm/@tensorflow-models/blazeface"></script>
    <script src="https://cdn.jsdelivr.net/npm/@tensorflow-models/posenet"></script>
    <script src="js/app.js"></script>
</body>
</html>"""

# --- محتوای CSS (ساده و تمیز) ---
css_content = """
body { font-family: system-ui, -apple-system, sans-serif; background: #eee; margin: 0; padding: 10px; }
.container { max-width: 800px; margin: 0 auto; background: #fff; border-radius: 15px; padding: 15px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
header { text-align: center; margin-bottom: 15px; }
h1 { font-size: 1.2rem; margin: 0; }
.status { font-size: 0.9rem; color: #666; margin-top: 5px; }

.controls { display: flex; flex-direction: column; gap: 10px; margin-bottom: 15px; }
.btn { border: none; padding: 12px; border-radius: 10px; font-size: 1rem; font-weight: bold; cursor: pointer; width: 100%; }
.btn-primary { background: #007bff; color: white; }
.btn-danger { background: #dc3545; color: white; }
.btn:disabled { opacity: 0.5; }
.btn-small { padding: 5px 10px; font-size: 0.8rem; background: #6c757d; color: white; margin-top: 5px; }

.toggle-wrapper { display: flex; justify-content: center; margin-top: 5px; }
.toggle { display: flex; align-items: center; cursor: pointer; gap: 10px; }
.slider { width: 40px; height: 20px; background: #ccc; border-radius: 20px; position: relative; transition: .3s; }
.slider:before { content: ""; position: absolute; height: 16px; width: 16px; left: 2px; bottom: 2px; background: white; border-radius: 50%; transition: .3s; }
input:checked + .slider { background: #28a745; }
input:checked + .slider:before { transform: translateX(20px); }
input { display: none; }

.video-wrapper { position: relative; width: 100%; background: #000; border-radius: 10px; overflow: hidden; min-height: 200px; }
video { width: 100%; height: auto; display: block; transform: scaleX(1); } /* آینه نشود */
canvas { position: absolute; top: 0; left: 0; width: 100%; height: 100%; }
.overlay-msg { position: absolute; bottom: 10px; left: 10px; background: rgba(0,0,0,0.7); color: white; padding: 5px 10px; border-radius: 5px; font-size: 0.8rem; }

.logs { margin-top: 20px; border-top: 1px solid #eee; padding-top: 10px; }
.log-item { display: flex; align-items: center; gap: 10px; padding: 5px 0; border-bottom: 1px solid #f0f0f0; }
.log-item img { width: 50px; height: 50px; object-fit: cover; border-radius: 5px; }
"""

# --- محتوای JS (اصلاح شده: بازگشت به روش ساده قدیمی) ---
js_content = """
let video, canvas, ctx;
let modelFace, modelPose;
let isRunning = false;
let audioCtx;
let lastAlarm = 0;

window.onload = () => {
    video = document.getElementById('video');
    canvas = document.getElementById('canvas');
    ctx = canvas.getContext('2d');
    
    document.getElementById('startBtn').onclick = startCamera;
    document.getElementById('stopBtn').onclick = stopCamera;
    document.getElementById('clearLogs').onclick = () => { document.getElementById('logContainer').innerHTML = ''; };
};

async function startCamera() {
    // 1. فعال کردن صدا برای iOS (باید در کلیک کاربر باشد)
    if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    if (audioCtx.state === 'suspended') audioCtx.resume();

    document.getElementById('status').innerText = 'در حال درخواست دوربین...';
    
    // 2. تنظیمات بسیار ساده (راز موفقیت کدهای قبلی)
    // هیچ عدد خاصی برای رزولوشن نمی‌دهیم تا هر دوربینی کار کند
    const constraints = {
        audio: false,
        video: {
            facingMode: 'environment' // فقط می‌گوییم دوربین پشت
        }
    };

    try {
        const stream = await navigator.mediaDevices.getUserMedia(constraints);
        
        video.srcObject = stream;
        // ویژگی‌های مهم برای جلوگیری از سیاه شدن صفحه در iOS
        video.setAttribute('playsinline', '');
        video.setAttribute('webkit-playsinline', '');
        
        await video.play();
        
        // تنظیم اندازه بوم نقاشی بعد از لود شدن ویدیو
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;

        document.getElementById('status').innerText = 'در حال لود هوش مصنوعی (کمی صبر کنید)...';
        document.getElementById('startBtn').disabled = true;
        
        // لود مدل‌ها
        modelFace = await blazeface.load();
        modelPose = await posenet.load({
            architecture: 'MobileNetV1',
            outputStride: 16,
            inputResolution: { width: 320, height: 240 }, // مدل سبک
            multiplier: 0.5
        });

        document.getElementById('status').innerText = '✅ فعال - دوربین روشن است';
        document.getElementById('status').style.color = 'green';
        document.getElementById('stopBtn').disabled = false;
        
        isRunning = true;
        detectLoop();

    } catch (err) {
        console.error(err);
        alert('خطا: ' + err.name + '\\n' + err.message);
        document.getElementById('status').innerText = '❌ خطا: دسترسی رد شد';
    }
}

function stopCamera() {
    isRunning = false;
    if (video.srcObject) {
        video.srcObject.getTracks().forEach(t => t.stop());
    }
    document.getElementById('startBtn').disabled = false;
    document.getElementById('stopBtn').disabled = true;
    document.getElementById('status').innerText = 'متوقف شده';
    ctx.clearRect(0, 0, canvas.width, canvas.height);
}

async function detectLoop() {
    if (!isRunning) return;

    // تشخیص چهره
    const faces = await modelFace.estimateFaces(video, false);
    
    // تشخیص بدن (فقط اگر چهره نبود یا برای تکمیل)
    let pose = null;
    if (faces.length === 0) {
        pose = await modelPose.estimateSinglePose(video);
    }

    // پاک کردن بوم
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    let detected = false;
    let type = '';

    // رسم چهره
    if (faces.length > 0) {
        detected = true;
        type = 'چهره';
        faces.forEach(face => {
            const start = face.topLeft;
            const end = face.bottomRight;
            const size = [end[0] - start[0], end[1] - start[1]];
            drawRect(start[0], start[1], size[0], size[1], 'red', 'Face');
        });
    } 
    // رسم بدن (اگر چهره نبود و دقت بدن بالا بود)
    else if (pose && pose.score > 0.4) {
        detected = true;
        type = 'بدن';
        const keypoints = pose.keypoints;
        // پیدا کردن محدوده بدن
        let minX = canvas.width, minY = canvas.height, maxX = 0, maxY = 0;
        keypoints.forEach(k => {
            if (k.score > 0.5) {
                if (k.position.x < minX) minX = k.position.x;
                if (k.position.x > maxX) maxX = k.position.x;
                if (k.position.y < minY) minY = k.position.y;
                if (k.position.y > maxY) maxY = k.position.y;
            }
        });
        if (maxX > minX) {
            drawRect(minX, minY, maxX - minX, maxY - minY, 'orange', 'Body');
        }
    }

    document.getElementById('msg').innerText = detected ? `⚠️ تشخیص: ${type}` : '...';
    
    if (detected) {
        playAlarm();
        logDetection(type);
    }

    requestAnimationFrame(detectLoop);
}

function drawRect(x, y, w, h, color, text) {
    ctx.strokeStyle = color;
    ctx.lineWidth = 4;
    ctx.strokeRect(x, y, w, h);
    ctx.fillStyle = color;
    ctx.fillText(text, x, y - 5);
}

function playAlarm() {
    const toggle = document.getElementById('alarmToggle');
    if (!toggle.checked || !audioCtx) return;
    
    const now = Date.now();
    if (now - lastAlarm < 1000) return; // هر 1 ثانیه بوق بزن
    lastAlarm = now;

    const osc = audioCtx.createOscillator();
    const gain = audioCtx.createGain();
    osc.connect(gain);
    gain.connect(audioCtx.destination);
    osc.frequency.value = 800;
    osc.type = 'square';
    gain.gain.setValueAtTime(0.1, audioCtx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.1);
    osc.start();
    osc.stop(audioCtx.currentTime + 0.1);
}

function logDetection(type) {
    // لاگ کردن ساده (بدون عکس برای سرعت بالاتر)
    // اگر نیاز به عکس بود می‌توان اضافه کرد اما گاهی باعث کندی می‌شود
}
"""

# ذخیره فایل‌ها
with open(f"{project_root}/index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

with open(f"{project_root}/css/style.css", "w", encoding="utf-8") as f:
    f.write(css_content)

with open(f"{project_root}/js/app.js", "w", encoding="utf-8") as f:
    f.write(js_content)

print("✅ فایل‌ها ساخته شدند.")
print("این نسخه دقیقاً مثل برنامه‌های قبلی، سخت‌گیری روی کیفیت دوربین ندارد و باید روی آیفون شما کار کند.")
