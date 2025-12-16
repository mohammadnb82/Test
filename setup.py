import os
import urllib.request
import ssl

# مسیر پروژه
project_root = "tools/face_detection_camera"
libs_path = f"{project_root}/js/libs"
data_path = f"{project_root}/js/data"

# 1. ایجاد ساختار پوشه‌ها
folders = [
    "tools",
    project_root,
    f"{project_root}/css",
    f"{project_root}/js",
    libs_path,
    data_path
]

for folder in folders:
    os.makedirs(folder, exist_ok=True)

# 2. دانلود کتابخانه tracking.js (بسیار سبک و بدون نیاز به اینترنت برای اجرا)
tracking_url = "https://cdnjs.cloudflare.com/ajax/libs/tracking.js/1.1.3/tracking-min.js"
face_model_url = "https://cdnjs.cloudflare.com/ajax/libs/tracking.js/1.1.3/data/face-min.js"

files_to_download = {
    f"{libs_path}/tracking-min.js": tracking_url,
    f"{data_path}/face-min.js": face_model_url
}

# تنظیمات دانلود
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

print("⏳ در حال دانلود موتور هوشمند سبک (Tracking.js)...")

for path, url in files_to_download.items():
    if not os.path.exists(path):
        try:
            with urllib.request.urlopen(url, context=ctx) as response, open(path, 'wb') as out_file:
                out_file.write(response.read())
            print(f"   ✅ {os.path.basename(path)} دانلود شد.")
        except Exception as e:
            print(f"   ❌ خطا در دانلود {os.path.basename(path)}: {e}")
    else:
        print(f"   ℹ️ فایل {os.path.basename(path)} موجود است.")

# 3. HTML (ساده شده و بدون وابستگی به TensorFlow)
html_content = """<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>سیستم امنیتی کاملاً آفلاین</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    <div class="app-container">
        <header>
            <h1>📷 سیستم پایش (تکنولوژی Tracking.js)</h1>
            <p id="statusText" class="status-waiting">آماده به کار</p>
        </header>

        <main>
            <div class="camera-wrapper">
                <video id="video" playsinline webkit-playsinline muted autoplay></video>
                <canvas id="canvas"></canvas>
            </div>

            <div class="controls">
                <button id="startBtn" class="btn btn-primary">شروع سیستم</button>
                <button id="stopBtn" class="btn btn-danger" disabled>توقف</button>
            </div>
            
            <div class="options">
                <label class="switch-label">
                    <input type="checkbox" id="alarmToggle"> 
                    <span>🔊 آژیر</span>
                </label>
            </div>

            <div id="logs" class="logs"></div>
        </main>
    </div>

    <!-- کتابخانه‌های کاملاً لوکال -->
    <script src="js/libs/tracking-min.js"></script>
    <script src="js/data/face-min.js"></script>
    
    <script src="js/app.js"></script>
</body>
</html>"""

# 4. CSS (بهبود یافته)
css_content = """
body { font-family: system-ui, -apple-system, sans-serif; background: #e0e7ff; margin: 0; padding: 10px; text-align: center; }
.app-container { max-width: 600px; margin: 0 auto; background: white; border-radius: 24px; padding: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.1); }

h1 { margin: 5px 0; font-size: 1.2rem; color: #3730a3; }
.status-waiting { color: #6b7280; font-size: 0.9rem; }
.status-active { color: #059669; font-weight: bold; font-size: 0.9rem; }

.camera-wrapper {
    position: relative;
    width: 100%;
    border-radius: 20px;
    overflow: hidden;
    background: #000;
    margin: 20px 0;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
}

video, canvas { 
    position: absolute; 
    top: 0; 
    left: 0;
    width: 100%; 
    height: 100%;
    object-fit: cover;
}
/* ارتفاع ثابت برای کانتینر دوربین تا پرش نداشته باشد */
.camera-wrapper { padding-bottom: 75%; /* نسبت 4:3 */ height: 0; }

.controls { display: flex; gap: 15px; margin-bottom: 20px; }
.btn { flex: 1; border: none; padding: 16px; border-radius: 16px; font-size: 1rem; font-weight: 700; cursor: pointer; transition: transform 0.1s; }
.btn:active { transform: scale(0.96); }
.btn-primary { background: #4f46e5; color: white; box-shadow: 0 4px 6px rgba(79, 70, 229, 0.3); }
.btn-danger { background: #ef4444; color: white; box-shadow: 0 4px 6px rgba(239, 68, 68, 0.3); }
.btn:disabled { opacity: 0.5; cursor: not-allowed; box-shadow: none; }

.options { display: flex; justify-content: center; margin-bottom: 15px; }
.switch-label { 
    display: flex; align-items: center; gap: 10px; 
    background: #f3f4f6; padding: 10px 20px; border-radius: 50px;
    cursor: pointer; user-select: none;
}

.logs { 
    text-align: right; height: 100px; overflow-y: auto; 
    font-size: 0.8rem; color: #4b5563; 
    border-top: 2px solid #f3f4f6; padding-top: 10px;
}
.log-entry { padding: 4px 0; border-bottom: 1px dashed #e5e7eb; color: #b91c1c; }
"""

# 5. JS (با استفاده از Tracking.js - بسیار پایدارتر)
js_content = """
let video, canvas, ctx;
let tracker;
let task;
let audioCtx;
let lastAlarm = 0;
let isRunning = false;

window.onload = () => {
    video = document.getElementById('video');
    canvas = document.getElementById('canvas');
    ctx = canvas.getContext('2d');
    
    document.getElementById('startBtn').addEventListener('click', startSystem);
    document.getElementById('stopBtn').addEventListener('click', stopSystem);
};

async function startSystem() {
    // راه اندازی صدا
    if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    if (audioCtx.state === 'suspended') audioCtx.resume();

    try {
        const stream = await navigator.mediaDevices.getUserMedia({
            audio: false,
            video: { 
                facingMode: 'environment',
                width: { ideal: 640 },
                height: { ideal: 480 }
            }
        });
        
        video.srcObject = stream;
        video.setAttribute('playsinline', '');
        
        video.onloadedmetadata = () => {
            video.play();
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            
            // شروع تشخیص چهره با Tracking.js
            startTracking();
        };

        document.getElementById('startBtn').disabled = true;
        document.getElementById('stopBtn').disabled = false;
        document.getElementById('statusText').innerText = '✅ سیستم فعال (تشخیص چهره)';
        document.getElementById('statusText').className = 'status-active';
        isRunning = true;

    } catch (err) {
        alert('خطای دوربین: ' + err.message);
    }
}

function startTracking() {
    // تعریف ترکر چهره
    tracker = new tracking.ObjectTracker('face');
    tracker.setInitialScale(4);
    tracker.setStepSize(2);
    tracker.setEdgesDensity(0.1);

    // اتصال ترکر به المنت ویدیو
    task = tracking.track('#video', tracker, { camera: false }); // camera: false چون خودمان استریم را مدیریت کردیم

    tracker.on('track', function(event) {
        if (!isRunning) return;
        
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        if (event.data.length === 0) {
            // هیچ چهره‌ای نیست
        } else {
            event.data.forEach(function(rect) {
                // رسم کادر دور چهره
                ctx.strokeStyle = '#ef4444';
                ctx.lineWidth = 4;
                ctx.strokeRect(rect.x, rect.y, rect.width, rect.height);
                
                // متن
                ctx.fillStyle = '#ef4444';
                ctx.fillText('FACE', rect.x, rect.y - 5);
                
                playAlarm();
                logEvent('چهره');
            });
        }
    });
}

function stopSystem() {
    isRunning = false;
    if (task) {
        task.stop(); // توقف پردازش تصویر
    }
    if (video.srcObject) {
        video.srcObject.getTracks().forEach(t => t.stop());
        video.srcObject = null;
    }
    
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    document.getElementById('startBtn').disabled = false;
    document.getElementById('stopBtn').disabled = true;
    document.getElementById('statusText').innerText = 'متوقف شده';
    document.getElementById('statusText').className = 'status-waiting';
}

function playAlarm() {
    if (!document.getElementById('alarmToggle').checked || !audioCtx) return;
    
    const now = Date.now();
    if (now - lastAlarm < 1000) return;
    lastAlarm = now;
    
    const osc = audioCtx.createOscillator();
    const gain = audioCtx.createGain();
    osc.connect(gain);
    gain.connect(audioCtx.destination);
    
    osc.frequency.setValueAtTime(800, audioCtx.currentTime);
    osc.frequency.exponentialRampToValueAtTime(400, audioCtx.currentTime + 0.2);
    
    gain.gain.setValueAtTime(0.2, audioCtx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.2);
    
    osc.start();
    osc.stop(audioCtx.currentTime + 0.2);
}

function logEvent(type) {
    const logs = document.getElementById('logs');
    if (logs.firstChild && logs.firstChild.innerText.includes('الان')) return;

    const div = document.createElement('div');
    div.className = 'log-entry';
    div.innerText = `⚠️ تشخیص ${type} - ${new Date().toLocaleTimeString('fa-IR')}`;
    logs.insertBefore(div, logs.firstChild);
    
    if (logs.children.length > 20) logs.removeChild(logs.lastChild);
}
"""

with open(f"{project_root}/index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

with open(f"{project_root}/css/style.css", "w", encoding="utf-8") as f:
    f.write(css_content)

with open(f"{project_root}/js/app.js", "w", encoding="utf-8") as f:
    f.write(js_content)

print("\n🚀 سیستم جدید آماده شد!")
print("✅ از کتابخانه Tracking.js استفاده شد که نیاز به دانلود مدل سنگین ندارد.")
print("✅ صد در صد آفلاین کار خواهد کرد.")
