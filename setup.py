import os
import urllib.request
from pathlib import Path

def download_file(url, filepath):
    """دانلود فایل با مدیریت خطا"""
    try:
        print(f"Downloading {filepath}...")
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        urllib.request.urlretrieve(url, filepath)
        print(f"✅ Downloaded: {filepath}")
    except Exception as e:
        print(f"❌ Error downloading {filepath}: {e}")

def create_project_structure():
    """ایجاد ساختار پروژه و دانلود فایل‌ها"""
    
    # ایجاد پوشه‌ها
    folders = ['css', 'js/libs', 'js/models', 'sounds']
    for folder in folders:
        Path(folder).mkdir(parents=True, exist_ok=True)
        print(f"✅ Created folder: {folder}")
    
    # دانلود کتابخانه‌ها
    libraries = {
        'js/libs/face-api.min.js': 'https://cdn.jsdelivr.net/npm/@vladmandic/face-api/dist/face-api.min.js',
        'js/libs/tracking-min.js': 'https://cdn.jsdelivr.net/npm/tracking@1.1.3/build/tracking-min.js'
    }
    
    for filepath, url in libraries.items():
        download_file(url, filepath)
    
    # دانلود مدل‌های Face-API
    base_model_url = 'https://cdn.jsdelivr.net/npm/@vladmandic/face-api/model/'
    models = [
        'tiny_face_detector_model-weights_manifest.json',
        'tiny_face_detector_model-shard1',
        'face_landmark_68_model-weights_manifest.json',
        'face_landmark_68_model-shard1',
        'face_recognition_model-weights_manifest.json',
        'face_recognition_model-shard1',
        'face_recognition_model-shard2'
    ]
    
    for model in models:
        download_file(base_model_url + model, f'js/models/{model}')
    
    # ایجاد index.html
    html_content = '''<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>سیستم امنیتی دوربین</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    <div class="container">
        <header>
            <h1>🔒 سیستم امنیتی دوربین</h1>
            <div class="status" id="status">در حال بارگذاری...</div>
        </header>

        <div class="controls">
            <button id="switchCamera" class="btn">🔄 تغییر دوربین</button>
            <button id="startBtn" class="btn btn-primary">▶ شروع</button>
            <button id="stopBtn" class="btn btn-danger">⏹ توقف</button>
        </div>

        <div class="video-container">
            <video id="video" autoplay playsinline muted></video>
            <canvas id="overlay"></canvas>
        </div>

        <div class="stats">
            <div class="stat-item">
                <span class="stat-label">افراد شناسایی شده:</span>
                <span class="stat-value" id="totalPeople">0</span>
            </div>
            <div class="stat-item">
                <span class="stat-label">دوربین فعال:</span>
                <span class="stat-value" id="currentCamera">جلو</span>
            </div>
        </div>

        <div class="gallery">
            <h2>📸 گالری تصاویر</h2>
            <div id="gallery" class="gallery-grid"></div>
        </div>
    </div>

    <audio id="alarm" loop>
        <source src="sounds/alarm.mp3" type="audio/mpeg">
    </audio>

    <script src="js/libs/face-api.min.js"></script>
    <script src="js/libs/tracking-min.js"></script>
    <script src="js/app.js"></script>
</body>
</html>'''
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    print("✅ Created: index.html")
    
    # ایجاد style.css
    css_content = '''* {
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
    box-shadow: 0 20px 60px rgba(0,0,0,0.3);
    overflow: hidden;
}

header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 30px;
    text-align: center;
}

header h1 {
    font-size: 2rem;
    margin-bottom: 10px;
}

.status {
    display: inline-block;
    padding: 8px 20px;
    background: rgba(255,255,255,0.2);
    border-radius: 20px;
    font-size: 0.9rem;
}

.controls {
    display: flex;
    gap: 15px;
    padding: 20px;
    justify-content: center;
    flex-wrap: wrap;
}

.btn {
    padding: 12px 30px;
    border: none;
    border-radius: 10px;
    font-size: 1rem;
    cursor: pointer;
    transition: all 0.3s;
    font-weight: bold;
}

.btn-primary {
    background: #10b981;
    color: white;
}

.btn-primary:hover {
    background: #059669;
    transform: translateY(-2px);
}

.btn-danger {
    background: #ef4444;
    color: white;
}

.btn-danger:hover {
    background: #dc2626;
    transform: translateY(-2px);
}

.btn:active {
    transform: translateY(0);
}

.video-container {
    position: relative;
    max-width: 640px;
    margin: 0 auto;
    background: #000;
    border-radius: 10px;
    overflow: hidden;
}

#video {
    width: 100%;
    height: auto;
    display: block;
}

#overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
}

.stats {
    display: flex;
    justify-content: space-around;
    padding: 30px;
    background: #f8fafc;
    flex-wrap: wrap;
    gap: 20px;
}

.stat-item {
    text-align: center;
}

.stat-label {
    display: block;
    color: #64748b;
    font-size: 0.9rem;
    margin-bottom: 5px;
}

.stat-value {
    display: block;
    font-size: 2rem;
    font-weight: bold;
    color: #667eea;
}

.gallery {
    padding: 30px;
}

.gallery h2 {
    color: #1e293b;
    margin-bottom: 20px;
    text-align: center;
}

.gallery-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 20px;
}

.gallery-item {
    position: relative;
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    transition: transform 0.3s;
}

.gallery-item:hover {
    transform: scale(1.05);
}

.gallery-item img {
    width: 100%;
    height: 200px;
    object-fit: cover;
}

.gallery-item .info {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    background: linear-gradient(to top, rgba(0,0,0,0.8), transparent);
    color: white;
    padding: 10px;
    font-size: 0.8rem;
}

@media (max-width: 768px) {
    header h1 {
        font-size: 1.5rem;
    }
    
    .controls {
        flex-direction: column;
    }
    
    .btn {
        width: 100%;
    }
    
    .gallery-grid {
        grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
    }
}'''
    
    with open('css/style.css', 'w', encoding='utf-8') as f:
        f.write(css_content)
    print("✅ Created: css/style.css")
    
    # ایجاد app.js
    js_content = '''// متغیرهای سراسری
let video, canvas, ctx, alarm;
let stream = null;
let isRunning = false;
let currentCamera = 'user'; // 'user' = جلو, 'environment' = پشت
let detectedPeople = [];
let modelsLoaded = false;

// بارگذاری مدل‌های Face-API
async function loadModels() {
    try {
        document.getElementById('status').textContent = 'در حال بارگذاری مدل‌های هوش مصنوعی...';
        
        await faceapi.nets.tinyFaceDetector.loadFromUri('js/models');
        await faceapi.nets.faceLandmark68Net.loadFromUri('js/models');
        await faceapi.nets.faceRecognitionNet.loadFromUri('js/models');
        
        modelsLoaded = true;
        document.getElementById('status').textContent = '✅ آماده به کار';
        console.log('✅ Models loaded successfully');
    } catch (error) {
        console.error('❌ Error loading models:', error);
        document.getElementById('status').textContent = '❌ خطا در بارگذاری مدل‌ها';
    }
}

// راه‌اندازی اولیه
window.addEventListener('DOMContentLoaded', async () => {
    video = document.getElementById('video');
    canvas = document.getElementById('overlay');
    ctx = canvas.getContext('2d');
    alarm = document.getElementById('alarm');
    
    await loadModels();
    
    document.getElementById('startBtn').addEventListener('click', startDetection);
    document.getElementById('stopBtn').addEventListener('click', stopDetection);
    document.getElementById('switchCamera').addEventListener('click', switchCamera);
});

// شروع دوربین
async function startCamera() {
    try {
        if (stream) {
            stream.getTracks().forEach(track => track.stop());
        }
        
        const constraints = {
            video: {
                facingMode: currentCamera,
                width: { ideal: 640 },
                height: { ideal: 480 }
            },
            audio: false
        };
        
        stream = await navigator.mediaDevices.getUserMedia(constraints);
        video.srcObject = stream;
        
        video.onloadedmetadata = () => {
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
        };
        
        document.getElementById('currentCamera').textContent = 
            currentCamera === 'user' ? 'جلو' : 'پشت';
        
        return true;
    } catch (error) {
        console.error('❌ Camera error:', error);
        document.getElementById('status').textContent = '❌ خطا در دسترسی به دوربین';
        return false;
    }
}

// تغییر دوربین
async function switchCamera() {
    currentCamera = currentCamera === 'user' ? 'environment' : 'user';
    if (isRunning) {
        await startCamera();
    }
}

// شروع تشخیص
async function startDetection() {
    if (!modelsLoaded) {
        alert('لطفاً صبر کنید تا مدل‌ها بارگذاری شوند');
        return;
    }
    
    const cameraStarted = await startCamera();
    if (!cameraStarted) return;
    
    isRunning = true;
    document.getElementById('status').textContent = '🔴 در حال تشخیص...';
    detectFaces();
}

// توقف تشخیص
function stopDetection() {
    isRunning = false;
    if (stream) {
        stream.getTracks().forEach(track => track.stop());
        stream = null;
    }
    alarm.pause();
    alarm.currentTime = 0;
    document.getElementById('status').textContent = '⏸ متوقف شده';
    ctx.clearRect(0, 0, canvas.width, canvas.height);
}

// تشخیص چهره
async function detectFaces() {
    if (!isRunning) return;
    
    try {
        const detections = await faceapi
            .detectAllFaces(video, new faceapi.TinyFaceDetectorOptions())
            .withFaceLandmarks()
            .withFaceDescriptors();
        
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        if (detections.length > 0) {
            detections.forEach(detection => {
                drawDetection(detection);
                processPerson(detection);
            });
        }
        
        requestAnimationFrame(detectFaces);
    } catch (error) {
        console.error('Detection error:', error);
        requestAnimationFrame(detectFaces);
    }
}

// رسم کادر تشخیص
function drawDetection(detection) {
    const box = detection.detection.box;
    const landmarks = detection.landmarks.positions;
    
    // رسم کادر
    ctx.strokeStyle = '#00ff00';
    ctx.lineWidth = 3;
    ctx.strokeRect(box.x, box.y, box.width, box.height);
    
    // رسم نقاط صورت
    ctx.fillStyle = '#ff0000';
    landmarks.forEach(point => {
        ctx.beginPath();
        ctx.arc(point.x, point.y, 2, 0, 2 * Math.PI);
        ctx.fill();
    });
}

// پردازش فرد جدید
function processPerson(detection) {
    const descriptor = detection.descriptor;
    const landmarks = detection.landmarks.positions;
    const landmarkCount = landmarks.length;
    
    // بررسی آیا این فرد قبلاً شناسایی شده
    let existingPerson = null;
    let minDistance = 0.6; // آستانه تشخیص (پایین‌تر = دقیق‌تر)
    
    for (let person of detectedPeople) {
        const distance = faceapi.euclideanDistance(descriptor, person.descriptor);
        if (distance < minDistance) {
            minDistance = distance;
            existingPerson = person;
        }
    }
    
    if (existingPerson) {
        // اگر تعداد اجزای صورت بیشتر است، عکس را به‌روز کن
        if (landmarkCount > existingPerson.landmarkCount) {
            existingPerson.landmarkCount = landmarkCount;
            existingPerson.image = captureFrame();
            updateGallery();
        }
    } else {
        // فرد جدید
        const newPerson = {
            id: Date.now(),
            descriptor: descriptor,
            landmarkCount: landmarkCount,
            image: captureFrame(),
            timestamp: new Date().toLocaleString('fa-IR')
        };
        
        detectedPeople.push(newPerson);
        updateGallery();
        playAlarm();
    }
}

// ضبط فریم
function captureFrame() {
    const captureCanvas = document.createElement('canvas');
    captureCanvas.width = video.videoWidth;
    captureCanvas.height = video.videoHeight;
    const captureCtx = captureCanvas.getContext('2d');
    captureCtx.drawImage(video, 0, 0);
    return captureCanvas.toDataURL('image/jpeg');
}

// به‌روزرسانی گالری
function updateGallery() {
    const gallery = document.getElementById('gallery');
    gallery.innerHTML = '';
    
    detectedPeople.forEach(person => {
        const item = document.createElement('div');
        item.className = 'gallery-item';
        item.innerHTML = `
            <img src="${person.image}" alt="Person ${person.id}">
            <div class="info">
                <div>زمان: ${person.timestamp}</div>
                <div>اجزای صورت: ${person.landmarkCount}</div>
            </div>
        `;
        gallery.appendChild(item);
    });
    
    document.getElementById('totalPeople').textContent = detectedPeople.length;
}

// پخش آژیر
function playAlarm() {
    alarm.play().catch(e => console.log('Alarm play error:', e));
    setTimeout(() => alarm.pause(), 3000);
}

// پاک کردن داده‌ها هنگام بستن
window.addEventListener('beforeunload', () => {
    detectedPeople = [];
    stopDetection();
});'''
    
    with open('js/app.js', 'w', encoding='utf-8') as f:
        f.write(js_content)
    print("✅ Created: js/app.js")
    
    print("\n" + "="*50)
    print("✅ تمام فایل‌ها با موفقیت ساخته شدند!")
    print("="*50)
    print("\n⚠️ یادآوری:")
    print("فایل sounds/alarm.mp3 را دستی آپلود کنید")

if __name__ == '__main__':
    create_project_structure()
