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

# فایل .keep
with open("tools/.keep", "w", encoding="utf-8") as f:
    f.write("")

# محتوای HTML به‌روزرسانی شده
html_content = """<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>دوربین نگهبان تشخیص چهره و بدن</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    <div class="container">
        <header>
            <h1>🎥 دوربین نگهبان تشخیص چهره و بدن</h1>
            <div class="status" id="status">آماده</div>
        </header>

        <div class="controls">
            <button id="startBtn" class="btn btn-primary">▶️ شروع دوربین</button>
            <button id="stopBtn" class="btn btn-danger" disabled>⏹️ توقف دوربین</button>
            <button id="clearBtn" class="btn btn-warning">🗑️ پاک کردن تصاویر</button>
            
            <div class="toggle-controls">
                <label class="toggle-switch">
                    <input type="checkbox" id="saveToggle">
                    <span class="toggle-slider"></span>
                    <span class="toggle-label">💾 ذخیره تصاویر</span>
                </label>
                
                <label class="toggle-switch">
                    <input type="checkbox" id="alarmToggle">
                    <span class="toggle-slider"></span>
                    <span class="toggle-label">🔔 صدای آژیر</span>
                </label>
            </div>
        </div>

        <div class="video-container">
            <video id="video" autoplay playsinline></video>
            <canvas id="canvas"></canvas>
            <div class="detection-info" id="detectionInfo"></div>
        </div>

        <div class="faces-section">
            <h2>موارد شناسایی شده</h2>
            <div id="facesContainer" class="faces-grid"></div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/@tensorflow/tfjs"></script>
    <script src="https://cdn.jsdelivr.net/npm/@tensorflow-models/blazeface"></script>
    <script src="https://cdn.jsdelivr.net/npm/@tensorflow-models/posenet"></script>
    <script src="js/app.js"></script>
</body>
</html>"""

# محتوای CSS (بدون تغییر)
css_content = """* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
    padding: 20px;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    background: white;
    border-radius: 20px;
    padding: 30px;
    box-shadow: 0 20px 60px rgba(0,0,0,0.3);
}

header {
    text-align: center;
    margin-bottom: 30px;
}

h1 {
    color: #333;
    margin-bottom: 15px;
    font-size: 2.5em;
}

.status {
    display: inline-block;
    padding: 8px 20px;
    background: #4CAF50;
    color: white;
    border-radius: 20px;
    font-weight: bold;
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.7; }
}

.controls {
    display: flex;
    gap: 15px;
    justify-content: center;
    flex-wrap: wrap;
    margin-bottom: 30px;
}

.btn {
    padding: 12px 30px;
    border: none;
    border-radius: 10px;
    font-size: 16px;
    font-weight: bold;
    cursor: pointer;
    transition: all 0.3s;
    color: white;
}

.btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(0,0,0,0.2);
}

.btn-primary {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.btn-danger {
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}

.btn-warning {
    background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
}

.btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
    transform: none;
}

.toggle-controls {
    display: flex;
    gap: 20px;
    align-items: center;
    width: 100%;
    justify-content: center;
    margin-top: 15px;
}

.toggle-switch {
    display: flex;
    align-items: center;
    gap: 10px;
    cursor: pointer;
    user-select: none;
}

.toggle-switch input {
    display: none;
}

.toggle-slider {
    position: relative;
    width: 50px;
    height: 26px;
    background: #ccc;
    border-radius: 26px;
    transition: 0.3s;
}

.toggle-slider::before {
    content: '';
    position: absolute;
    width: 22px;
    height: 22px;
    background: white;
    border-radius: 50%;
    top: 2px;
    left: 2px;
    transition: 0.3s;
}

.toggle-switch input:checked + .toggle-slider {
    background: #4CAF50;
}

.toggle-switch input:checked + .toggle-slider::before {
    transform: translateX(24px);
}

.toggle-label {
    font-weight: bold;
    color: #333;
    font-size: 14px;
}

.video-container {
    position: relative;
    width: 100%;
    max-width: 800px;
    margin: 0 auto 30px;
    border-radius: 15px;
    overflow: hidden;
    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
}

#video, #canvas {
    width: 100%;
    display: block;
    border-radius: 15px;
}

#canvas {
    position: absolute;
    top: 0;
    left: 0;
}

.detection-info {
    position: absolute;
    top: 10px;
    left: 10px;
    background: rgba(0,0,0,0.7);
    color: white;
    padding: 10px 15px;
    border-radius: 10px;
    font-weight: bold;
    font-size: 14px;
}

.faces-section {
    margin-top: 40px;
}

.faces-section h2 {
    color: #333;
    margin-bottom: 20px;
    text-align: center;
}

.faces-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 20px;
}

.face-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 15px;
    padding: 15px;
    text-align: center;
    box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    transition: transform 0.3s;
    animation: slideIn 0.5s;
}

@keyframes slideIn {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.face-card:hover {
    transform: translateY(-5px);
}

.face-card img {
    width: 100%;
    height: 200px;
    object-fit: cover;
    border-radius: 10px;
    margin-bottom: 10px;
    border: 3px solid white;
}

.face-card .face-id {
    color: white;
    font-weight: bold;
    font-size: 14px;
    margin-bottom: 5px;
}

.face-card .face-time {
    color: rgba(255,255,255,0.8);
    font-size: 12px;
}

.face-card .face-area {
    color: rgba(255,255,255,0.9);
    font-size: 11px;
    margin-top: 5px;
}

@media (max-width: 768px) {
    .container {
        padding: 20px;
    }
    
    h1 {
        font-size: 1.8em;
    }
    
    .controls {
        flex-direction: column;
    }
    
    .toggle-controls {
        flex-direction: column;
        gap: 15px;
    }
    
    .faces-grid {
        grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
    }
}"""

# محتوای JavaScript با تشخیص چهره و بدن
js_content = """let video, canvas, ctx;
let faceModel, poseModel;
let isDetecting = false;
let detectedItems = [];
let saveEnabled = false;
let alarmEnabled = false;
let audioContext;
let lastAlarmTime = 0;
const ALARM_COOLDOWN = 1000; // 1 ثانیه فاصله بین آژیرها

// بارگذاری تصاویر
function loadSavedItems() {
    const saved = localStorage.getItem('detectedItems');
    if (saved) {
        detectedItems = JSON.parse(saved);
        updateItemsDisplay();
    }
}

// ذخیره تصاویر
function saveItems() {
    if (saveEnabled) {
        localStorage.setItem('detectedItems', JSON.stringify(detectedItems));
    }
}

// پاک کردن تصاویر
function clearItems() {
    if (confirm('آیا مطمئن هستید که می‌خواهید تمام تصاویر را پاک کنید؟')) {
        detectedItems = [];
        localStorage.removeItem('detectedItems');
        sessionStorage.removeItem('tempItems');
        updateItemsDisplay();
    }
}

// ایجاد صدای آژیر
function createAlarmSound() {
    audioContext = new (window.AudioContext || window.webkitAudioContext)();
}

function playAlarm() {
    if (!alarmEnabled || !audioContext) return;
    
    const currentTime = Date.now();
    if (currentTime - lastAlarmTime < ALARM_COOLDOWN) return;
    lastAlarmTime = currentTime;
    
    const oscillator = audioContext.createOscillator();
    const gainNode = audioContext.createGain();
    
    oscillator.connect(gainNode);
    gainNode.connect(audioContext.destination);
    
    oscillator.frequency.value = 800;
    oscillator.type = 'sine';
    
    gainNode.gain.setValueAtTime(0.3, audioContext.currentTime);
    gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.5);
    
    oscillator.start(audioContext.currentTime);
    oscillator.stop(audioContext.currentTime + 0.5);
}

// محاسبه فاصله
function calculateDistance(point1, point2) {
    const dx = point1.x - point2.x;
    const dy = point1.y - point2.y;
    return Math.sqrt(dx * dx + dy * dy);
}

// بررسی شباهت
function areItemsSimilar(item1, item2, threshold = 100) {
    if (item1.type !== item2.type) return false;
    
    const center1 = item1.center;
    const center2 = item2.center;
    
    const distance = calculateDistance(center1, center2);
    const sizeRatio = Math.abs(item1.area - item2.area) / Math.max(item1.area, item2.area);
    
    return distance < threshold && sizeRatio < 0.5;
}

// پردازش چهره
function processFace(predictions) {
    predictions.forEach(prediction => {
        const box = {
            x: prediction.topLeft[0],
            y: prediction.topLeft[1],
            width: prediction.bottomRight[0] - prediction.topLeft[0],
            height: prediction.bottomRight[1] - prediction.topLeft[1]
        };
        
        const area = box.width * box.height;
        const center = {
            x: box.x + box.width / 2,
            y: box.y + box.height / 2
        };
        
        // پخش آژیر
        playAlarm();
        
        // کپچر عکس
        const itemCanvas = document.createElement('canvas');
        const itemCtx = itemCanvas.getContext('2d');
        
        const padding = 20;
        const x = Math.max(0, box.x - padding);
        const y = Math.max(0, box.y - padding);
        const width = box.width + (padding * 2);
        const height = box.height + (padding * 2);
        
        itemCanvas.width = width;
        itemCanvas.height = height;
        itemCtx.drawImage(video, x, y, width, height, 0, 0, width, height);
        
        const itemImage = itemCanvas.toDataURL('image/jpeg', 0.8);
        
        // یافتن آیتم مشابه
        let matchedIndex = -1;
        for (let i = 0; i < detectedItems.length; i++) {
            if (areItemsSimilar({ type: 'face', center, area }, detectedItems[i])) {
                matchedIndex = i;
                break;
            }
        }
        
        if (matchedIndex === -1) {
            detectedItems.push({
                id: Date.now(),
                type: 'face',
                image: itemImage,
                timestamp: new Date().toLocaleString('fa-IR'),
                area: area,
                center: center
            });
        } else {
            if (area > detectedItems[matchedIndex].area) {
                detectedItems[matchedIndex].image = itemImage;
                detectedItems[matchedIndex].timestamp = new Date().toLocaleString('fa-IR');
                detectedItems[matchedIndex].area = area;
                detectedItems[matchedIndex].center = center;
            }
        }
        
        if (saveEnabled) {
            saveItems();
        } else {
            sessionStorage.setItem('tempItems', JSON.stringify(detectedItems));
        }
        
        updateItemsDisplay();
    });
}

// پردازش بدن
function processPose(poses) {
    poses.forEach(pose => {
        if (pose.score < 0.3) return; // حداقل اطمینان
        
        const keypoints = pose.keypoints.filter(kp => kp.score > 0.3);
        if (keypoints.length < 3) return; // حداقل 3 نقطه برای تشخیص بدن
        
        // محاسبه کادر محدوده بدن
        const xs = keypoints.map(kp => kp.position.x);
        const ys = keypoints.map(kp => kp.position.y);
        const minX = Math.min(...xs);
        const maxX = Math.max(...xs);
        const minY = Math.min(...ys);
        const maxY = Math.max(...ys);
        
        const box = {
            x: minX,
            y: minY,
            width: maxX - minX,
            height: maxY - minY
        };
        
        const area = box.width * box.height;
        const center = {
            x: box.x + box.width / 2,
            y: box.y + box.height / 2
        };
        
        // پخش آژیر
        playAlarm();
        
        // کپچر عکس
        const itemCanvas = document.createElement('canvas');
        const itemCtx = itemCanvas.getContext('2d');
        
        const padding = 30;
        const x = Math.max(0, box.x - padding);
        const y = Math.max(0, box.y - padding);
        const width = box.width + (padding * 2);
        const height = box.height + (padding * 2);
        
        itemCanvas.width = width;
        itemCanvas.height = height;
        itemCtx.drawImage(video, x, y, width, height, 0, 0, width, height);
        
        const itemImage = itemCanvas.toDataURL('image/jpeg', 0.8);
        
        // یافتن آیتم مشابه
        let matchedIndex = -1;
        for (let i = 0; i < detectedItems.length; i++) {
            if (areItemsSimilar({ type: 'body', center, area }, detectedItems[i])) {
                matchedIndex = i;
                break;
            }
        }
        
        if (matchedIndex === -1) {
            detectedItems.push({
                id: Date.now(),
                type: 'body',
                image: itemImage,
                timestamp: new Date().toLocaleString('fa-IR'),
                area: area,
                center: center
            });
        } else {
            if (area > detectedItems[matchedIndex].area) {
                detectedItems[matchedIndex].image = itemImage;
                detectedItems[matchedIndex].timestamp = new Date().toLocaleString('fa-IR');
                detectedItems[matchedIndex].area = area;
                detectedItems[matchedIndex].center = center;
            }
        }
        
        if (saveEnabled) {
            saveItems();
        } else {
            sessionStorage.setItem('tempItems', JSON.stringify(detectedItems));
        }
        
        updateItemsDisplay();
    });
}

// نمایش تصاویر
function updateItemsDisplay() {
    const container = document.getElementById('facesContainer');
    container.innerHTML = '';
    
    detectedItems.forEach((item, index) => {
        const icon = item.type === 'face' ? '👤' : '🚶';
        const label = item.type === 'face' ? 'چهره' : 'بدن';
        
        const card = document.createElement('div');
        card.className = 'face-card';
        card.innerHTML = `
            <img src="${item.image}" alt="${label} ${index + 1}">
            <div class="face-id">${icon} ${label} شماره ${index + 1}</div>
            <div class="face-time">⏰ ${item.timestamp}</div>
            <div class="face-area">📐 مساحت: ${Math.round(item.area)} پیکسل</div>
        `;
        container.appendChild(card);
    });
}

// شروع دوربین
async function startCamera() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ 
            video: { 
                facingMode: 'environment',
                width: { ideal: 1280 },
                height: { ideal: 720 }
            } 
        });
        
        video.srcObject = stream;
        
        video.onloadedmetadata = () => {
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
        };
        
        document.getElementById('status').textContent = 'در حال بارگذاری مدل‌ها...';
        document.getElementById('status').style.background = '#FF9800';
        
        // بارگذاری مدل‌ها
        faceModel = await blazeface.load();
        poseModel = await posenet.load({
            architecture: 'MobileNetV1',
            outputStride: 16,
            inputResolution: { width: 640, height: 480 },
            multiplier: 0.75
        });
        
        document.getElementById('status').textContent = '✓ فعال';
        document.getElementById('status').style.background = '#4CAF50';
        document.getElementById('startBtn').disabled = true;
        document.getElementById('stopBtn').disabled = false;
        
        isDetecting = true;
        detectHumans();
        
    } catch (error) {
        console.error('خطا:', error);
        alert('دسترسی به دوربین امکان‌پذیر نیست.');
        document.getElementById('status').textContent = '❌ خطا';
        document.getElementById('status').style.background = '#f44336';
    }
}

// توقف دوربین
function stopCamera() {
    isDetecting = false;
    
    if (video.srcObject) {
        video.srcObject.getTracks().forEach(track => track.stop());
        video.srcObject = null;
    }
    
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    document.getElementById('status').textContent = 'متوقف شده';
    document.getElementById('status').style.background = '#9E9E9E';
    document.getElementById('startBtn').disabled = false;
    document.getElementById('stopBtn').disabled = true;
    document.getElementById('detectionInfo').textContent = '';
}

// تشخیص انسان (چهره + بدن)
async function detectHumans() {
    if (!isDetecting) return;
    
    try {
        // تشخیص چهره
        const facePredictions = await faceModel.estimateFaces(video, false);
        
        // تشخیص بدن
        const pose = await poseModel.estimateSinglePose(video, {
            flipHorizontal: false
        });
        
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        let totalDetections = 0;
        
        // رسم چهره‌ها
        if (facePredictions.length > 0) {
            totalDetections += facePredictions.length;
            
            facePredictions.forEach(prediction => {
                ctx.strokeStyle = '#00FF00';
                ctx.lineWidth = 3;
                ctx.strokeRect(
                    prediction.topLeft[0],
                    prediction.topLeft[1],
                    prediction.bottomRight[0] - prediction.topLeft[0],
                    prediction.bottomRight[1] - prediction.topLeft[1]
                );
                
                ctx.fillStyle = '#00FF00';
                ctx.font = 'bold 16px Arial';
                ctx.fillText('👤 چهره', prediction.topLeft[0], prediction.topLeft[1] - 10);
            });
            
            processFace(facePredictions);
        }
        
        // رسم بدن
        if (pose.score > 0.3) {
            const keypoints = pose.keypoints.filter(kp => kp.score > 0.3);
            
            if (keypoints.length >= 3) {
                totalDetections += 1;
                
                // رسم نقاط
                keypoints.forEach(kp => {
                    ctx.beginPath();
                    ctx.arc(kp.position.x, kp.position.y, 5, 0, 2 * Math.PI);
                    ctx.fillStyle = '#FF9800';
                    ctx.fill();
                });
                
                // رسم کادر محدوده
                const xs = keypoints.map(kp => kp.position.x);
                const ys = keypoints.map(kp => kp.position.y);
                const minX = Math.min(...xs);
                const maxX = Math.max(...xs);
                const minY = Math.min(...ys);
                const maxY = Math.max(...ys);
                
                ctx.strokeStyle = '#FF9800';
                ctx.lineWidth = 3;
                ctx.strokeRect(minX, minY, maxX - minX, maxY - minY);
                
                ctx.fillStyle = '#FF9800';
                ctx.font = 'bold 16px Arial';
                ctx.fillText('🚶 بدن', minX, minY - 10);
                
                processPose([pose]);
            }
        }
        
        // به‌روزرسانی اطلاعات
        if (totalDetections > 0) {
            document.getElementById('detectionInfo').textContent = 
                `🎯 ${totalDetections} مورد شناسایی شد`;
        } else {
            document.getElementById('detectionInfo').textContent = '🔍 در حال اسکن...';
        }
        
    } catch (error) {
        console.error('خطا در تشخیص:', error);
    }
    
    requestAnimationFrame(detectHumans);
}

// راه‌اندازی
window.addEventListener('load', () => {
    video = document.getElementById('video');
    canvas = document.getElementById('canvas');
    ctx = canvas.getContext('2d');
    
    createAlarmSound();
    
    const tempItems = sessionStorage.getItem('tempItems');
    if (tempItems) {
        detectedItems = JSON.parse(tempItems);
        updateItemsDisplay();
    } else {
        loadSavedItems();
    }
    
    document.getElementById('startBtn').addEventListener('click', startCamera);
    document.getElementById('stopBtn').addEventListener('click', stopCamera);
    document.getElementById('clearBtn').addEventListener('click', clearItems);
    
    document.getElementById('saveToggle').addEventListener('change', (e) => {
        saveEnabled = e.target.checked;
        if (saveEnabled) {
            saveItems();
            console.log('✅ ذخیره فعال');
        } else {
            sessionStorage.setItem('tempItems', JSON.stringify(detectedItems));
            console.log('⚠️ ذخیره غیرفعال');
        }
    });
    
    document.getElementById('alarmToggle').addEventListener('change', (e) => {
        alarmEnabled = e.target.checked;
        console.log(alarmEnabled ? '🔔 آژیر فعال' : '🔕 آژیر غیرفعال');
    });
    
    window.addEventListener('beforeunload', () => {
        if (!saveEnabled) {
            sessionStorage.removeItem('tempItems');
        }
    });
});"""

# ذخیره فایل‌ها
with open(f"{project_root}/index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

with open(f"{project_root}/css/style.css", "w", encoding="utf-8") as f:
    f.write(css_content)

with open(f"{project_root}/js/app.js", "w", encoding="utf-8") as f:
    f.write(js_content)

# README به‌روزرسانی شده
readme_content = """# 🎥 دوربین نگهبان تشخیص چهره و بدن

## ویژگی‌های جدید:
- ✅ تشخیص خودکار **چهره** با BlazeFace
- ✅ تشخیص خودکار **بدن** با PoseNet
- ✅ آژیر هشدار برای **چهره یا بدن**
- ✅ ذخیره هوشمند تصاویر
- ✅ قابلیت فعال/غیرفعال کردن ذخیره و آژیر
- ✅ کاملاً محلی و آفلاین

## نحوه کار:
1. دوربین هم چهره و هم بدن را تشخیص می‌دهد
2. به محض دیدن **هر کدام**، آژیر می‌زند (اگر فعال باشد)
3. تصویر را ذخیره می‌کند (اگر فعال باشد)
4. فقط تصاویر با جزئیات بیشتر ذخیره می‌شوند

## رنگ‌ها:
- 🟢 سبز = چهره
- 🟠 نارنجی = بدن

## استفاده:
1. دکمه "شروع دوربین" را بزنید
2. به دوربین اجازه دهید
3. دوربین به طور خودکار کار می‌کند
"""

with open(f"{project_root}/README.md", "w", encoding="utf-8") as f:
    f.write(readme_content)

print("✅ پروژه با تشخیص چهره و بدن آماده شد!")
print(f"🌐 آدرس: https://mohammadnb82.github.io/Test/tools/face_detection_camera/")
print("\n🎯 قابلیت‌های جدید:")
print("  - 👤 تشخیص چهره (سبز)")
print("  - 🚶 تشخیص بدن (نارنجی)")
print("  - 🔔 آژیر برای هر دو")
