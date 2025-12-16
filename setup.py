import os

def create_project_structure():
    """Create necessary directories and files"""
    
    # Create directories
    directories = [
        'static/css',
        'static/js',
        'static/sounds',
        'templates',
        'saved_images'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ Created directory: {directory}")
    
    # Create index.html
    html_content = """<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>دوربین نگهبان هوشمند</title>
    <link rel="stylesheet" href="/static/css/style.css">
</head>
<body>
    <div class="container">
        <h1>🎥 دوربین نگهبان محلی</h1>
        
        <div class="controls">
            <button id="startBtn" class="btn btn-primary">▶️ شروع دوربین</button>
            <button id="stopBtn" class="btn btn-danger" disabled>⏹️ توقف دوربین</button>
        </div>

        <div class="settings-panel">
            <h3>⚙️ تنظیمات</h3>
            <div class="setting-group">
                <label>
                    <input type="checkbox" id="alarmToggle">
                    🔊 فعال‌سازی آژیر
                </label>
            </div>
            <div class="setting-group">
                <label>
                    <input type="checkbox" id="saveToggle">
                    💾 ذخیره خودکار تصاویر
                </label>
            </div>
            <div class="setting-group">
                <label>
                    حساسیت تشخیص:
                    <input type="range" id="sensitivity" min="0.3" max="0.9" step="0.1" value="0.5">
                    <span id="sensitivityValue">0.5</span>
                </label>
            </div>
        </div>

        <div class="status-panel">
            <div class="status-item">
                <span class="status-label">وضعیت:</span>
                <span id="systemStatus" class="status-value">غیرفعال</span>
            </div>
            <div class="status-item">
                <span class="status-label">تعداد تشخیص:</span>
                <span id="detectionCount" class="status-value">0</span>
            </div>
            <div class="status-item">
                <span class="status-label">تصاویر ذخیره شده:</span>
                <span id="savedCount" class="status-value">0</span>
            </div>
        </div>

        <div class="video-container">
            <video id="video" autoplay playsinline></video>
            <canvas id="canvas"></canvas>
        </div>

        <div class="gallery">
            <h3>📸 گالری تصاویر</h3>
            <div id="imageGallery" class="gallery-grid"></div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/@tensorflow/tfjs"></script>
    <script src="https://cdn.jsdelivr.net/npm/@tensorflow-models/blazeface"></script>
    <script src="https://cdn.jsdelivr.net/npm/@tensorflow-models/posenet"></script>
    <script src="/static/js/main.js"></script>
</body>
</html>"""
    
    with open('templates/index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    print("✓ Created templates/index.html")
    
    # Create CSS
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

h1 {
    text-align: center;
    color: #333;
    margin-bottom: 30px;
    font-size: 2.5em;
}

.controls {
    display: flex;
    gap: 15px;
    justify-content: center;
    margin-bottom: 30px;
}

.btn {
    padding: 15px 30px;
    font-size: 16px;
    border: none;
    border-radius: 10px;
    cursor: pointer;
    transition: all 0.3s;
    font-weight: bold;
}

.btn-primary {
    background: #4CAF50;
    color: white;
}

.btn-primary:hover {
    background: #45a049;
    transform: translateY(-2px);
}

.btn-danger {
    background: #f44336;
    color: white;
}

.btn-danger:hover {
    background: #da190b;
    transform: translateY(-2px);
}

.btn:disabled {
    background: #cccccc;
    cursor: not-allowed;
    transform: none;
}

.settings-panel {
    background: #f5f5f5;
    padding: 20px;
    border-radius: 10px;
    margin-bottom: 20px;
}

.settings-panel h3 {
    margin-bottom: 15px;
    color: #555;
}

.setting-group {
    margin-bottom: 15px;
}

.setting-group label {
    display: flex;
    align-items: center;
    gap: 10px;
    cursor: pointer;
}

input[type="checkbox"] {
    width: 20px;
    height: 20px;
    cursor: pointer;
}

input[type="range"] {
    flex: 1;
    margin: 0 10px;
}

.status-panel {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 15px;
    margin-bottom: 30px;
}

.status-item {
    background: #e3f2fd;
    padding: 15px;
    border-radius: 10px;
    text-align: center;
}

.status-label {
    display: block;
    font-size: 14px;
    color: #666;
    margin-bottom: 5px;
}

.status-value {
    display: block;
    font-size: 24px;
    font-weight: bold;
    color: #1976d2;
}

.video-container {
    position: relative;
    width: 100%;
    max-width: 640px;
    margin: 0 auto 30px;
    border-radius: 15px;
    overflow: hidden;
    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
}

#video {
    width: 100%;
    display: block;
}

#canvas {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
}

.gallery {
    margin-top: 30px;
}

.gallery h3 {
    margin-bottom: 20px;
    color: #555;
}

.gallery-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 15px;
}

.gallery-item {
    position: relative;
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    transition: transform 0.3s;
}

.gallery-item:hover {
    transform: scale(1.05);
}

.gallery-item img {
    width: 100%;
    height: 200px;
    object-fit: cover;
    display: block;
}

.gallery-item .delete-btn {
    position: absolute;
    top: 10px;
    right: 10px;
    background: rgba(244, 67, 54, 0.9);
    color: white;
    border: none;
    border-radius: 50%;
    width: 30px;
    height: 30px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    opacity: 0;
    transition: opacity 0.3s;
}

.gallery-item:hover .delete-btn {
    opacity: 1;
}

.gallery-item .type-badge {
    position: absolute;
    bottom: 10px;
    left: 10px;
    background: rgba(0,0,0,0.7);
    color: white;
    padding: 5px 10px;
    border-radius: 5px;
    font-size: 12px;
}

@media (max-width: 768px) {
    .container {
        padding: 15px;
    }
    
    h1 {
        font-size: 1.8em;
    }
    
    .controls {
        flex-direction: column;
    }
    
    .btn {
        width: 100%;
    }
}"""
    
    with open('static/css/style.css', 'w', encoding='utf-8') as f:
        f.write(css_content)
    print("✓ Created static/css/style.css")
    
    # Create JavaScript
    js_content = """let video, canvas, ctx;
let blazefaceModel, posenetModel;
let isRunning = false;
let detectionCount = 0;
let savedImages = [];
let alarmEnabled = false;
let saveEnabled = false;
let sensitivity = 0.5;

async function init() {
    video = document.getElementById('video');
    canvas = document.getElementById('canvas');
    ctx = canvas.getContext('2d');

    document.getElementById('startBtn').addEventListener('click', startCamera);
    document.getElementById('stopBtn').addEventListener('click', stopCamera);
    document.getElementById('alarmToggle').addEventListener('change', (e) => {
        alarmEnabled = e.target.checked;
    });
    document.getElementById('saveToggle').addEventListener('change', (e) => {
        saveEnabled = e.target.checked;
    });
    document.getElementById('sensitivity').addEventListener('input', (e) => {
        sensitivity = parseFloat(e.target.value);
        document.getElementById('sensitivityValue').textContent = sensitivity;
    });

    await loadModels();
    loadSavedImages();
}

async function loadModels() {
    try {
        document.getElementById('systemStatus').textContent = 'در حال بارگذاری مدل‌ها...';
        blazefaceModel = await blazeface.load();
        posenetModel = await posenet.load({
            architecture: 'MobileNetV1',
            outputStride: 16,
            multiplier: 0.75
        });
        document.getElementById('systemStatus').textContent = 'آماده';
        console.log('✓ Models loaded successfully');
    } catch (error) {
        console.error('Error loading models:', error);
        document.getElementById('systemStatus').textContent = 'خطا در بارگذاری';
    }
}

async function startCamera() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({
            video: {
                facingMode: 'user',
                width: { ideal: 640 },
                height: { ideal: 480 }
            },
            audio: false
        });

        video.srcObject = stream;
        
        video.onloadedmetadata = () => {
            video.play();
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            isRunning = true;
            document.getElementById('startBtn').disabled = true;
            document.getElementById('stopBtn').disabled = false;
            document.getElementById('systemStatus').textContent = 'فعال';
            detectFrame();
        };
    } catch (error) {
        console.error('Camera error:', error);
        alert('خطا در دسترسی به دوربین!');
    }
}

function stopCamera() {
    isRunning = false;
    if (video.srcObject) {
        video.srcObject.getTracks().forEach(track => track.stop());
    }
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    document.getElementById('startBtn').disabled = false;
    document.getElementById('stopBtn').disabled = true;
    document.getElementById('systemStatus').textContent = 'غیرفعال';
}

async function detectFrame() {
    if (!isRunning) return;

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    let detectionMade = false;

    // Face Detection
    const faces = await blazefaceModel.estimateFaces(video, false);
    if (faces.length > 0) {
        faces.forEach(face => {
            if (face.probability && face.probability[0] > sensitivity) {
                const start = face.topLeft;
                const end = face.bottomRight;
                const size = [end[0] - start[0], end[1] - start[1]];

                ctx.strokeStyle = '#00ff00';
                ctx.lineWidth = 3;
                ctx.strokeRect(start[0], start[1], size[0], size[1]);

                ctx.fillStyle = '#00ff00';
                ctx.font = '16px Arial';
                ctx.fillText('👤 چهره', start[0], start[1] - 10);

                detectionMade = true;
            }
        });
    }

    // Body Detection
    const poses = await posenetModel.estimateSinglePose(video, {
        flipHorizontal: false
    });

    if (poses.score > sensitivity) {
        poses.keypoints.forEach(keypoint => {
            if (keypoint.score > sensitivity) {
                ctx.beginPath();
                ctx.arc(keypoint.position.x, keypoint.position.y, 5, 0, 2 * Math.PI);
                ctx.fillStyle = '#ff0000';
                ctx.fill();
            }
        });

        ctx.fillStyle = '#ff0000';
        ctx.font = '16px Arial';
        ctx.fillText('🚶 بدن', 10, 30);

        detectionMade = true;
    }

    if (detectionMade) {
        detectionCount++;
        document.getElementById('detectionCount').textContent = detectionCount;

        if (alarmEnabled) {
            playAlarm();
        }

        if (saveEnabled) {
            saveImage();
        }
    }

    requestAnimationFrame(detectFrame);
}

function playAlarm() {
    // Simple beep using Web Audio API
    const audioContext = new (window.AudioContext || window.webkitAudioContext)();
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

async function saveImage() {
    const tempCanvas = document.createElement('canvas');
    tempCanvas.width = video.videoWidth;
    tempCanvas.height = video.videoHeight;
    const tempCtx = tempCanvas.getContext('2d');
    tempCtx.drawImage(video, 0, 0);

    const imageData = tempCanvas.toDataURL('image/jpeg');
    const timestamp = new Date().toISOString();

    try {
        const response = await fetch('/save_image', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                image: imageData,
                timestamp: timestamp
            })
        });

        if (response.ok) {
            const result = await response.json();
            addImageToGallery(result.filename, timestamp);
            document.getElementById('savedCount').textContent = savedImages.length;
        }
    } catch (error) {
        console.error('Error saving image:', error);
    }
}

function addImageToGallery(filename, timestamp) {
    savedImages.push({ filename, timestamp });

    const gallery = document.getElementById('imageGallery');
    const item = document.createElement('div');
    item.className = 'gallery-item';
    item.innerHTML = `
        <img src="/saved_images/${filename}" alt="Detection">
        <button class="delete-btn" onclick="deleteImage('${filename}')">×</button>
        <div class="type-badge">${new Date(timestamp).toLocaleString('fa-IR')}</div>
    `;
    gallery.insertBefore(item, gallery.firstChild);
}

async function deleteImage(filename) {
    try {
        const response = await fetch(`/delete_image/${filename}`, {
            method: 'DELETE'
        });

        if (response.ok) {
            savedImages = savedImages.filter(img => img.filename !== filename);
            document.getElementById('savedCount').textContent = savedImages.length;
            loadSavedImages();
        }
    } catch (error) {
        console.error('Error deleting image:', error);
    }
}

async function loadSavedImages() {
    try {
        const response = await fetch('/list_images');
        const images = await response.json();
        
        const gallery = document.getElementById('imageGallery');
        gallery.innerHTML = '';
        
        images.forEach(img => {
            addImageToGallery(img.filename, img.timestamp);
        });
        
        savedImages = images;
        document.getElementById('savedCount').textContent = images.length;
    } catch (error) {
        console.error('Error loading images:', error);
    }
}

window.addEventListener('load', init);"""
    
    with open('static/js/main.js', 'w', encoding='utf-8') as f:
        f.write(js_content)
    print("✓ Created static/js/main.js")
    
    print("\n✅ Project structure created successfully!")
    print("\nNext steps:")
    print("1. Run: python app.py")
    print("2. Open: http://localhost:5000")

if __name__ == "__main__":
    create_project_structure()
