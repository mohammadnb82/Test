import os
import urllib.request
import ssl

# مسیر پروژه
project_root = "tools/face_detection_camera"
libs_path = f"{project_root}/js/libs"

# 1. ایجاد ساختار پوشه‌ها
folders = [
    "tools",
    f"{project_root}",
    f"{project_root}/css",
    f"{project_root}/js",
    libs_path, # پوشه جدید برای نگهداری فایل‌های هوش مصنوعی
]

for folder in folders:
    os.makedirs(folder, exist_ok=True)

print("📂 پوشه‌ها ساخته شدند.")

# 2. دانلودر خودکار فایل‌های هوش مصنوعی (برای آفلاین کردن برنامه)
# لینک‌ها به فایل‌های خام (Raw) کتابخانه‌ها اشاره دارند
libraries = {
    "tf.min.js": "https://unpkg.com/@tensorflow/tfjs@3.11.0/dist/tf.min.js",
    "blazeface.min.js": "https://unpkg.com/@tensorflow-models/blazeface@0.0.7/dist/blazeface.min.js",
    "posenet.min.js": "https://unpkg.com/@tensorflow-models/posenet@2.2.2/dist/posenet.min.js"
}

# تنظیمات برای دانلود (نادیده گرفتن SSL در صورت نیاز)
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

print("⏳ در حال دانلود فایل‌های هوش مصنوعی (کمی صبر کنید)...")

for filename, url in libraries.items():
    file_path = f"{libs_path}/{filename}"
    if not os.path.exists(file_path):
        try:
            print(f"   ⬇️ در حال دانلود {filename}...")
            with urllib.request.urlopen(url, context=ctx) as response, open(file_path, 'wb') as out_file:
                out_file.write(response.read())
            print(f"   ✅ {filename} ذخیره شد.")
        except Exception as e:
            print(f"   ❌ خطا در دانلود {filename}: {e}")
            print("      لطفاً اتصال اینترنت را چک کنید و دوباره اسکریپت را اجرا کنید.")
    else:
        print(f"   ℹ️ فایل {filename} از قبل موجود است.")

# 3. تولید فایل HTML (لینک‌دهی به فایل‌های لوکال)
html_content = """<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>سیستم امنیتی آفلاین</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    <div class="app-container">
        <header>
            <h1>📷 سیستم پایش هوشمند (نسخه لوکال)</h1>
            <p id="statusText" class="status-waiting">سیستم آماده است</p>
        </header>

        <main>
            <div class="camera-wrapper">
                <video id="video" playsinline webkit-playsinline muted autoplay></video>
                <canvas id="canvas"></canvas>
            </div>

            <div class="controls">
                <button id="startBtn" class="btn btn-primary">شروع دوربین</button>
                <button id="stopBtn" class="btn btn-danger" disabled>توقف</button>
            </div>
            
            <div class="options">
                <label><input type="checkbox" id="alarmToggle"> 🔊 آژیر</label>
                <label><input type="checkbox" id="aiToggle" checked> 🧠 هوش مصنوعی</label>
            </div>

            <div id="logs" class="logs"></div>
        </main>
    </div>

    <!-- بارگذاری فایل‌ها از پوشه خود برنامه (نه اینترنت) -->
    <script src="js/libs/tf.min.js"></script>
    <script src="js/libs/blazeface.min.js"></script>
    <script src="js/libs/posenet.min.js"></script>
    
    <script src="js/app.js"></script>
</body>
</html>"""

# 4. تولید فایل CSS
css_content = """
body { font-family: system-ui, -apple-system, sans-serif; background: #eef2f6; margin: 0; padding: 10px; text-align: center; }
.app-container { max-width: 600px; margin: 0 auto; background: white; border-radius: 20px; padding: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }

h1 { margin: 10px 0 5px; font-size: 1.3rem; color: #1f2937; }
.status-waiting { color: #6b7280; font-size: 0.9rem; }
.status-active { color: #10b981; font-weight: bold; }
.status-loading { color: #f59e0b; font-weight: bold; }
.status-error { color: #ef4444; font-weight: bold; }

.camera-wrapper {
    position: relative;
    width: 100%;
    border-radius: 16px;
    overflow: hidden;
    background: #000;
    margin: 15px 0;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    min-height: 250px; /* جلوگیری از پرش صفحه */
}

video { width: 100%; height: auto; display: block; object-fit: cover; }
canvas { position: absolute; top: 0; left: 0; width: 100%; height: 100%; }

.controls { display: flex; gap: 12px; margin-bottom: 20px; }
.btn { flex: 1; border: none; padding: 14px; border-radius: 12px; font-size: 1rem; font-weight: 600; cursor: pointer; transition: 0.2s; }
.btn:active { transform: scale(0.98); }
.btn-primary { background: #3b82f6; color: white; }
.btn-danger { background: #ef4444; color: white; }
.btn:disabled { opacity: 0.5; cursor: not-allowed; transform: none; }

.options { 
    display: flex; justify-content: space-around; 
    background: #f3f4f6; padding: 12px; border-radius: 12px; margin-bottom: 15px; 
    font-size: 0.95rem; color: #374151;
}

.logs { 
    text-align: right; height: 120px; overflow-y: auto; 
    font-size: 0.8rem; color: #4b5563; 
    border: 1px solid #e5e7eb; border-radius: 8px; padding: 8px; 
    background: #f9fafb;
}
.log-entry { padding: 4px 0; border-bottom: 1px dashed #e5e7eb; }
"""

# 5. تولید فایل JS (بدون Alert های مزاحم)
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
    
    document.getElementById('startBtn').addEventListener('click', startSystem);
    document.getElementById('stopBtn').addEventListener('click', stopSystem);
};

function updateStatus(text, type) {
    const el = document.getElementById('statusText');
    el.innerText = text;
    el.className = `status-${type}`;
}

async function startSystem() {
    updateStatus('در حال راه‌اندازی دوربین...', 'loading');
    
    // فعال‌سازی صدا در تعامل کاربر (برای آیفون ضروری است)
    if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    if (audioCtx.state === 'suspended') audioCtx.resume();

    try {
        // درخواست دوربین با تنظیمات بهینه برای موبایل
        const stream = await navigator.mediaDevices.getUserMedia({
            audio: false,
            video: { 
                facingMode: 'environment',
                width: { ideal: 640 },
                height: { ideal: 480 }
            }
        });
        
        video.srcObject = stream;
        video.setAttribute('playsinline', ''); // حیاتی برای آیفون
        
        // منتظر می‌مانیم تا ابعاد ویدیو مشخص شود
        await new Promise(resolve => {
            video.onloadedmetadata = () => {
                video.play();
                resolve();
            };
        });
        
        // تنظیم ابعاد کانواس دقیقاً اندازه ویدیو
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        
        document.getElementById('startBtn').disabled = true;
        document.getElementById('stopBtn').disabled = false;
        
        // اگر تیک هوش مصنوعی فعال بود، مدل‌ها را لود کن
        if (document.getElementById('aiToggle').checked) {
            updateStatus('در حال لود مدل‌های هوش مصنوعی...', 'loading');
            
            // تاخیر کوتاه برای اینکه UI رفرش شود
            setTimeout(async () => {
                try {
                    // لود مدل‌ها از فایل‌های لوکال
                    if (!modelFace) modelFace = await blazeface.load();
                    // پوزنت سنگین است، اگر ارور داد فقط چهره کار کند
                    if (!modelPose) {
                        try {
                            modelPose = await posenet.load({
                                architecture: 'MobileNetV1',
                                outputStride: 16,
                                multiplier: 0.5, // مدل سبک‌تر
                                inputResolution: 200 // رزولوشن پایین‌تر برای سرعت
                            });
                        } catch(e) {
                            console.log("PoseNet skip due to memory/load error");
                        }
                    }
                    
                    isRunning = true;
                    updateStatus('✅ سیستم فعال و هوشمند', 'active');
                    detectLoop();
                } catch (aiErr) {
                    console.error(aiErr);
                    // دیگر Alert نمی‌دهیم که برنامه قفل شود
                    updateStatus('⚠️ دوربین فعال (هوش مصنوعی لود نشد)', 'error');
                    logEvent('خطای لود مدل: ' + aiErr.message);
                }
            }, 100);
        } else {
            updateStatus('✅ دوربین فعال (بدون هوش مصنوعی)', 'active');
        }

    } catch (err) {
        console.error(err);
        updateStatus('❌ خطای دسترسی به دوربین', 'error');
        alert('لطفاً دسترسی دوربین را در تنظیمات مرورگر فعال کنید.');
    }
}

function stopSystem() {
    isRunning = false;
    if (video.srcObject) {
        video.srcObject.getTracks().forEach(t => t.stop());
        video.srcObject = null;
    }
    document.getElementById('startBtn').disabled = false;
    document.getElementById('stopBtn').disabled = true;
    updateStatus('متوقف شده', 'waiting');
    ctx.clearRect(0, 0, canvas.width, canvas.height);
}

async function detectLoop() {
    if (!isRunning) return;

    // پاک کردن فریم قبلی
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    let detected = false;
    let type = '';

    try {
        // 1. تشخیص چهره
        if (modelFace) {
            const faces = await modelFace.estimateFaces(video, false);
            if (faces.length > 0) {
                detected = true;
                type = 'چهره';
                faces.forEach(face => {
                    const start = face.topLeft;
                    const end = face.bottomRight;
                    drawBox(start[0], start[1], end[0] - start[0], end[1] - start[1], 'rgba(255, 0, 0, 0.7)', 'Face');
                });
            }
        }

        // 2. تشخیص بدن (اگر چهره نبود)
        if (!detected && modelPose) {
            const pose = await modelPose.estimateSinglePose(video, { flipHorizontal: false });
            if (pose && pose.score > 0.3) { // حساسیت متوسط
                detected = true;
                type = 'حرکت';
                drawKeypoints(pose.keypoints);
            }
        }
    } catch (e) {
        console.log("Detection error:", e);
        // اگر ارور داد، لوپ قطع نشود
    }

    if (detected) {
        playAlarm();
        logEvent(type);
    }

    // درخواست فریم بعدی
    requestAnimationFrame(detectLoop);
}

function drawBox(x, y, w, h, color, label) {
    ctx.strokeStyle = color;
    ctx.lineWidth = 3;
    ctx.strokeRect(x, y, w, h);
}

function drawKeypoints(keypoints) {
    keypoints.forEach(keypoint => {
        if (keypoint.score > 0.5) {
            ctx.beginPath();
            ctx.arc(keypoint.position.x, keypoint.position.y, 5, 0, 2 * Math.PI);
            ctx.fillStyle = 'rgba(255, 255, 0, 0.7)';
            ctx.fill();
        }
    });
}

function playAlarm() {
    if (!document.getElementById('alarmToggle').checked || !audioCtx) return;
    
    const now = Date.now();
    // جلوگیری از آژیر مکرر (هر 1 ثانیه حداکثر یکبار)
    if (now - lastAlarm < 1000) return;
    lastAlarm = now;
    
    try {
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        
        osc.frequency.value = 880; // صدای زیرتر و هشداری‌تر
        osc.type = 'square';
        
        gain.gain.setValueAtTime(0.1, audioCtx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.15);
        
        osc.start();
        osc.stop(audioCtx.currentTime + 0.15);
    } catch(e) {
        console.log("Audio error");
    }
}

function logEvent(type) {
    const logs = document.getElementById('logs');
    // جلوگیری از پر شدن لاگ با پیام‌های تکراری در ثانیه
    if (logs.firstChild && logs.firstChild.innerText.includes('الان')) return;

    const div = document.createElement('div');
    div.className = 'log-entry';
    div.innerText = `⚠️ تشخیص ${type} - ${new Date().toLocaleTimeString('fa-IR')}`;
    logs.insertBefore(div, logs.firstChild);
    
    // محدود کردن تعداد لاگ‌ها به 50 عدد
    if (logs.children.length > 50) {
        logs.removeChild(logs.lastChild);
    }
}
"""

# نوشتن فایل‌ها
with open(f"{project_root}/index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

with open(f"{project_root}/css/style.css", "w", encoding="utf-8") as f:
    f.write(css_content)

with open(f"{project_root}/js/app.js", "w", encoding="utf-8") as f:
    f.write(js_content)

print("\n🎉 تمام! برنامه ساخته شد و فایل‌های هوش مصنوعی هم دانلود شدند.")
print("✅ حالا پوشه 'tools/face_detection_camera' کاملاً مستقل است.")
print("✅ می‌توانید این پوشه را روی هر سروری آپلود کنید و بدون نیاز به اینترنت خارجی کار می‌کند.")
