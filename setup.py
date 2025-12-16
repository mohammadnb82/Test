import os
import urllib.request

# ---------------------------------------------------------
# تنظیمات مسیر پروژه
# ---------------------------------------------------------
base_dir = "tools/face_detection_camera_fixed"
js_dir = os.path.join(base_dir, "js")
css_dir = os.path.join(base_dir, "css")

# ساخت پوشه‌ها
os.makedirs(js_dir, exist_ok=True)
os.makedirs(css_dir, exist_ok=True)

print("⏳ در حال بررسی و دانلود کتابخانه‌های هوش مصنوعی...")

# ---------------------------------------------------------
# دانلودر فایل‌های جاوا اسکریپت (برای آفلاین سازی)
# ---------------------------------------------------------
libs = {
    "tf.min.js": "https://cdn.jsdelivr.net/npm/@tensorflow/tfjs@3.11.0/dist/tf.min.js",
    "blazeface.min.js": "https://cdn.jsdelivr.net/npm/@tensorflow-models/blazeface@0.0.7/dist/blazeface.min.js",
    "posenet.min.js": "https://cdn.jsdelivr.net/npm/@tensorflow-models/posenet@2.2.2/dist/posenet.min.js"
}

for filename, url in libs.items():
    file_path = os.path.join(js_dir, filename)
    if not os.path.exists(file_path):
        try:
            print(f"   ⬇️ دانلود {filename}...")
            urllib.request.urlretrieve(url, file_path)
        except Exception as e:
            print(f"❌ خطا در دانلود {filename}: {e}")
    else:
        print(f"   ✅ فایل {filename} از قبل موجود است.")

# ---------------------------------------------------------
# 1. HTML (index.html)
# ---------------------------------------------------------
html_content = """<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>شکارگر چهره (بر اساس وضوح)</title>
    <link rel="stylesheet" href="css/style.css">
    
    <!-- کتابخانه‌های لوکال -->
    <script src="js/tf.min.js"></script>
    <script src="js/blazeface.min.js"></script>
    <script src="js/posenet.min.js"></script>
</head>
<body>

<div class="app-container">
    <div class="top-bar">
        <h3>📷 سیستم تشخیص هوشمند</h3>
        <div class="status-indicator waiting" id="statusBadge">در حال لود...</div>
    </div>

    <div class="camera-wrapper">
        <video id="video" playsinline muted autoplay></video>
        <canvas id="canvas"></canvas>
    </div>

    <div class="controls-area">
        <div class="row">
            <select id="cameraSelect" class="input-select">
                <option value="" disabled selected>انتخاب دوربین...</option>
            </select>
            <button id="startBtn" class="btn btn-primary" disabled>شروع</button>
            <button id="stopBtn" class="btn btn-danger" disabled>توقف</button>
        </div>
        
        <div class="row settings-row">
            <label class="toggle-label">
                <span>🔔 آژیر</span>
                <input type="checkbox" id="alarmToggle" checked>
                <span class="toggle-switch"></span>
            </label>
            <button id="clearGallery" class="btn btn-sm">پاکسازی</button>
        </div>
        <div class="info-text">ملاک جایگزینی: فقط وضوح اجزای صورت (فاصله مهم نیست)</div>
    </div>

    <div class="gallery-section">
        <h4>لیست افراد (بهترین تصویر)</h4>
        <div id="galleryGrid" class="gallery-grid"></div>
    </div>
</div>

<script src="js/app.js"></script>
</body>
</html>"""

# ---------------------------------------------------------
# 2. CSS (css/style.css)
# ---------------------------------------------------------
css_content = """@import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;700&display=swap');
:root { --primary: #2563eb; --danger: #dc2626; --bg: #f8fafc; --card: #ffffff; }
* { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Vazirmatn', sans-serif; -webkit-tap-highlight-color: transparent; }
body { background: var(--bg); padding: 10px; color: #334155; }
.app-container { max-width: 600px; margin: 0 auto; display: flex; flex-direction: column; gap: 10px; }
.top-bar { display: flex; justify-content: space-between; align-items: center; background: var(--card); padding: 10px; border-radius: 10px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
.status-indicator { padding: 3px 8px; border-radius: 15px; font-size: 0.75rem; font-weight: bold; }
.waiting { background: #e2e8f0; color: #64748b; }
.active { background: #dcfce7; color: #166534; }
.camera-wrapper { position: relative; width: 100%; aspect-ratio: 4/3; background: #000; border-radius: 12px; overflow: hidden; }
video { width: 100%; height: 100%; object-fit: cover; }
canvas { position: absolute; top: 0; left: 0; width: 100%; height: 100%; }
.controls-area { background: var(--card); padding: 12px; border-radius: 10px; display: flex; flex-direction: column; gap: 8px; }
.row { display: flex; gap: 8px; }
.settings-row { justify-content: space-between; align-items: center; margin-top: 5px; border-top: 1px solid #f1f5f9; padding-top: 8px; }
.input-select { flex: 2; padding: 8px; border: 1px solid #cbd5e1; border-radius: 6px; background: white; }
.btn { border: none; padding: 8px 12px; border-radius: 6px; font-weight: bold; cursor: pointer; color: white; }
.btn:disabled { opacity: 0.5; }
.btn-primary { background: var(--primary); flex: 1; }
.btn-danger { background: var(--danger); flex: 1; }
.btn-sm { background: #94a3b8; font-size: 0.75rem; padding: 5px 10px; flex: 0; }
.info-text { font-size: 0.7rem; color: #64748b; text-align: center; margin-top: 4px; }
.toggle-label { display: flex; align-items: center; gap: 6px; font-size: 0.85rem; }
.toggle-label input { display: none; }
.toggle-switch { width: 32px; height: 18px; background: #cbd5e1; border-radius: 20px; position: relative; transition: 0.3s; display: inline-block; }
.toggle-switch::after { content: ''; position: absolute; top: 2px; left: 2px; width: 14px; height: 14px; background: white; border-radius: 50%; transition: 0.3s; }
input:checked + .toggle-switch { background: var(--primary); }
input:checked + .toggle-switch::after { transform: translateX(14px); }
.gallery-section { background: var(--card); padding: 10px; border-radius: 10px; min-height: 150px; }
.gallery-section h4 { font-size: 0.85rem; color: #64748b; margin-bottom: 8px; border-bottom: 1px solid #f1f5f9; padding-bottom: 4px; }
.gallery-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(90px, 1fr)); gap: 8px; }
.person-card { background: #f8fafb; border: 1px solid #e2e8f0; border-radius: 6px; overflow: hidden; position: relative; }
.person-card img { width: 100%; height: 90px; object-fit: cover; display: block; }
.card-info { padding: 4px; font-size: 0.65rem; color: #475569; text-align: center; background: #fff; }
.score-tag { position: absolute; top: 2px; right: 2px; background: rgba(0,0,0,0.6); color: #fff; padding: 1px 4px; border-radius: 3px; font-size: 0.6rem; }
.update-badge { position: absolute; top: 2px; left: 2px; background: #10b981; color: white; font-size: 0.6rem; padding: 2px 4px; border-radius: 3px; opacity: 0; transition: opacity 0.5s; }
.person-card.updated .update-badge { opacity: 1; }
"""

# ---------------------------------------------------------
# 3. JavaScript (js/app.js) - اصلاح منطق جایگزینی
# ---------------------------------------------------------
js_content = """
const SETTINGS = {
    alarmCooldown: 2000,
    similarityThreshold: 80, // پیکسل برای تشخیص هویت (ترکینگ)
};

let video, canvas, ctx;
let faceModel, poseModel;
let isDetecting = false;
let stream = null;
let lastAlarmTime = 0;
let trackedPersons = []; 
let personIdCounter = 1;

const els = {
    status: document.getElementById('statusBadge'),
    cameraSelect: document.getElementById('cameraSelect'),
    startBtn: document.getElementById('startBtn'),
    stopBtn: document.getElementById('stopBtn'),
    gallery: document.getElementById('galleryGrid'),
    alarmToggle: document.getElementById('alarmToggle')
};

const alarmSound = new Audio('https://actions.google.com/sounds/v1/alarms/beep_short.ogg');

async function init() {
    video = document.getElementById('video');
    canvas = document.getElementById('canvas');
    ctx = canvas.getContext('2d');
    await getCameras();

    try {
        els.status.innerText = "⏳ لود هوش مصنوعی...";
        faceModel = await blazeface.load(); 
        poseModel = await posenet.load({
            architecture: 'MobileNetV1',
            outputStride: 16,
            inputResolution: { width: 320, height: 240 },
            multiplier: 0.5
        });
        els.status.innerText = "✅ آماده";
        els.status.className = "status-indicator active";
        els.startBtn.disabled = false;
    } catch (err) {
        console.error(err);
        els.status.innerText = "❌ خطا در لود مدل";
        alert("لطفا اینترنت را چک کنید (فقط بار اول).");
    }
}

async function getCameras() {
    try {
        const devices = await navigator.mediaDevices.enumerateDevices();
        const videoDevices = devices.filter(device => device.kind === 'videoinput');
        els.cameraSelect.innerHTML = '<option value="" disabled>انتخاب دوربین...</option>';
        videoDevices.forEach((device, index) => {
            const option = document.createElement('option');
            option.value = device.deviceId;
            option.text = device.label || `دوربین ${index + 1}`;
            els.cameraSelect.appendChild(option);
        });
        if (videoDevices.length > 0) els.cameraSelect.selectedIndex = videoDevices.length > 1 ? 1 : 0;
    } catch (e) { console.error(e); }
}

els.startBtn.addEventListener('click', () => startCamera(els.cameraSelect.value));
els.stopBtn.addEventListener('click', stopCamera);
els.cameraSelect.addEventListener('change', () => { if(isDetecting) startCamera(els.cameraSelect.value); });

async function startCamera(deviceId) {
    stopCamera();
    const constraints = {
        video: {
            deviceId: deviceId ? { exact: deviceId } : undefined,
            width: { ideal: 640 },
            height: { ideal: 480 }
        },
        audio: false
    };
    try {
        stream = await navigator.mediaDevices.getUserMedia(constraints);
        video.srcObject = stream;
        video.onloadedmetadata = () => {
            video.play();
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            isDetecting = true;
            els.startBtn.disabled = true;
            els.stopBtn.disabled = false;
            els.status.innerText = "👁‍🗨 در حال شکار...";
            detectLoop();
        };
    } catch (err) { alert("خطا در دوربین: " + err.name); }
}

function stopCamera() {
    isDetecting = false;
    if (stream) { stream.getTracks().forEach(t => t.stop()); stream = null; }
    video.srcObject = null;
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    els.startBtn.disabled = false;
    els.stopBtn.disabled = true;
    els.status.innerText = "⏹ متوقف";
}

async function detectLoop() {
    if (!isDetecting) return;
    const faces = await faceModel.estimateFaces(video, false);
    const pose = await poseModel.estimateSinglePose(video, { flipHorizontal: false });
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    let detectedAnything = false;
    if (faces.length > 0) {
        detectedAnything = true;
        faces.forEach(processFace);
    }
    if (pose.score >= 0.4) {
        detectedAnything = true;
        drawSkeleton(pose.keypoints);
    }
    if (detectedAnything && els.alarmToggle.checked) {
        const now = Date.now();
        if (now - lastAlarmTime > SETTINGS.alarmCooldown) {
            alarmSound.play().catch(e => {});
            lastAlarmTime = now;
        }
    }
    requestAnimationFrame(detectLoop);
}

// -------------------------------------------------------------
// بخش مهم: منطق جایگزینی فقط بر اساس کیفیت اجزا
// -------------------------------------------------------------
function processFace(face) {
    const start = face.topLeft;
    const end = face.bottomRight;
    const w = end[0] - start[0];
    const h = end[1] - start[1];
    const centerX = start[0] + w/2;
    const centerY = start[1] + h/2;

    // *** تغییر اصلی اینجاست ***
    // ما فاکتور اندازه (w*h) را کاملا حذف کردیم.
    // face.probability عددی بین 0 و 1 است که نشان‌دهنده اطمینان مدل از وجود اجزای صورت است.
    // هرچه این عدد بیشتر باشد، یعنی اجزای صورت (چشم، بینی) واضح‌تر دیده شده‌اند، حتی اگر دور باشد.
    const currentQuality = face.probability[0]; 

    // رسم باکس
    ctx.strokeStyle = '#00ff00';
    ctx.lineWidth = 2;
    ctx.strokeRect(start[0], start[1], w, h);

    // شناسایی فرد (Tracking)
    let matchIndex = -1;
    for (let i = 0; i < trackedPersons.length; i++) {
        const p = trackedPersons[i];
        const dist = Math.sqrt(Math.pow(p.x - centerX, 2) + Math.pow(p.y - centerY, 2));
        if (dist < SETTINGS.similarityThreshold) {
            matchIndex = i;
            break;
        }
    }

    if (matchIndex !== -1) {
        // --- فرد تکراری ---
        const person = trackedPersons[matchIndex];
        person.x = centerX;
        person.y = centerY;
        person.lastSeen = Date.now();

        // شرط جایگزینی: فقط اگر کیفیت وضوح فعلی (Probability) بیشتر از قبلی بود
        // بدون توجه به سایز
        if (currentQuality > person.qualityScore + 0.01) { // 0.01 حاشیه خطا برای جلوگیری از پرش
            console.log(`📸 تصویر واضح‌تر یافت شد (امتیاز: ${currentQuality.toFixed(2)})`);
            person.qualityScore = currentQuality;
            updateGalleryImage(person.id, captureCrop(start[0], start[1], w, h), currentQuality);
        }

    } else {
        // --- فرد جدید ---
        const newId = personIdCounter++;
        const newPerson = {
            id: newId,
            x: centerX,
            y: centerY,
            qualityScore: currentQuality,
            lastSeen: Date.now()
        };
        trackedPersons.push(newPerson);
        addToGallery(newId, captureCrop(start[0], start[1], w, h), currentQuality);
    }
}

setInterval(() => {
    const now = Date.now();
    trackedPersons = trackedPersons.filter(p => (now - p.lastSeen) < 5000);
}, 5000);

function drawSkeleton(keypoints) {
    keypoints.forEach(point => {
        if (point.score > 0.5) {
            ctx.beginPath();
            ctx.arc(point.position.x, point.position.y, 3, 0, 2 * Math.PI);
            ctx.fillStyle = "rgba(255, 0, 0, 0.5)";
            ctx.fill();
        }
    });
}

function captureCrop(x, y, w, h) {
    const tCanvas = document.createElement('canvas');
    const tCtx = tCanvas.getContext('2d');
    const pad = 10;
    const sx = Math.max(0, x - pad);
    const sy = Math.max(0, y - pad);
    const sw = Math.min(video.videoWidth - sx, w + (pad*2));
    const sh = Math.min(video.videoHeight - sy, h + (pad*2));
    tCanvas.width = sw;
    tCanvas.height = sh;
    tCtx.drawImage(video, sx, sy, sw, sh, 0, 0, sw, sh);
    return tCanvas.toDataURL('image/jpeg', 0.85);
}

function addToGallery(id, imgData, score) {
    const div = document.createElement('div');
    div.className = 'person-card';
    div.id = `person-${id}`;
    div.innerHTML = `
        <span class="update-badge">بهتر شد!</span>
        <span class="score-tag">وضوح: ${(score*100).toFixed(0)}%</span>
        <img src="${imgData}" id="img-${id}">
        <div class="card-info">شناسه: ${id}</div>
    `;
    els.gallery.prepend(div);
}

function updateGalleryImage(id, newImgData, score) {
    const imgEl = document.getElementById(`img-${id}`);
    const cardEl = document.getElementById(`person-${id}`);
    if (imgEl && cardEl) {
        imgEl.src = newImgData;
        cardEl.querySelector('.score-tag').innerText = `وضوح: ${(score*100).toFixed(0)}%`;
        cardEl.classList.add('updated');
        setTimeout(() => cardEl.classList.remove('updated'), 2000);
    }
}

document.getElementById('clearGallery').addEventListener('click', () => {
    els.gallery.innerHTML = '';
    trackedPersons = [];
});
window.onload = init;
"""

# ---------------------------------------------------------
# نوشتن فایل‌ها
# ---------------------------------------------------------
with open(os.path.join(base_dir, "index.html"), "w", encoding="utf-8") as f:
    f.write(html_content)

with open(os.path.join(css_dir, "style.css"), "w", encoding="utf-8") as f:
    f.write(css_content)

with open(os.path.join(js_dir, "app.js"), "w", encoding="utf-8") as f:
    f.write(js_content)

print(f"✅ اصلاح انجام شد: فاکتور فاصله حذف شد. پروژه در '{base_dir}' آماده است.")
