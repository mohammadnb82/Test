import os

# مسیر پروژه
project_root = "tools/face_detection_camera"

# JavaScript اصلاح شده با مدیریت خطا
js_content = """let video, canvas, ctx;
let faceModel, poseModel;
let isDetecting = false;
let detectedItems = [];
let saveEnabled = false;
let alarmEnabled = false;
let audioContext;
let lastAlarmTime = 0;
const ALARM_COOLDOWN = 1000;

// بارگذاری تصاویر
function loadSavedItems() {
    const saved = localStorage.getItem('detectedItems');
    if (saved) {
        detectedItems = JSON.parse(saved);
        updateItemsDisplay();
    }
}

function saveItems() {
    if (saveEnabled) {
        localStorage.setItem('detectedItems', JSON.stringify(detectedItems));
    }
}

function clearItems() {
    if (confirm('آیا مطمئن هستید که می‌خواهید تمام تصاویر را پاک کنید؟')) {
        detectedItems = [];
        localStorage.removeItem('detectedItems');
        sessionStorage.removeItem('tempItems');
        updateItemsDisplay();
    }
}

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

function calculateDistance(point1, point2) {
    const dx = point1.x - point2.x;
    const dy = point1.y - point2.y;
    return Math.sqrt(dx * dx + dy * dy);
}

function areItemsSimilar(item1, item2, threshold = 100) {
    if (item1.type !== item2.type) return false;
    
    const center1 = item1.center;
    const center2 = item2.center;
    
    const distance = calculateDistance(center1, center2);
    const sizeRatio = Math.abs(item1.area - item2.area) / Math.max(item1.area, item2.area);
    
    return distance < threshold && sizeRatio < 0.5;
}

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
        
        playAlarm();
        
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

function processPose(poses) {
    poses.forEach(pose => {
        if (pose.score < 0.3) return;
        
        const keypoints = pose.keypoints.filter(kp => kp.score > 0.3);
        if (keypoints.length < 3) return;
        
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
        
        playAlarm();
        
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

function updateItemsDisplay() {
    const container = document.getElementById('facesContainer');
    container.innerHTML = '';
    
    detectedItems.forEach((item, index) => {
        const icon = item.type === 'face' ? '👤' : '🚶';
        const label = item.type === 'face' ? 'چهره' : 'بدن';
        const bgColor = item.type === 'face' ? 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' : 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)';
        
        const card = document.createElement('div');
        card.className = 'face-card';
        card.style.background = bgColor;
        card.innerHTML = `
            <img src="${item.image}" alt="${label} ${index + 1}">
            <div class="face-id">${icon} ${label} شماره ${index + 1}</div>
            <div class="face-time">⏰ ${item.timestamp}</div>
            <div class="face-area">📐 مساحت: ${Math.round(item.area)} پیکسل</div>
        `;
        container.appendChild(card);
    });
}

// شروع دوربین با مدیریت خطا بهتر
async function startCamera() {
    try {
        document.getElementById('status').textContent = 'درخواست دسترسی...';
        document.getElementById('status').style.background = '#FF9800';
        
        // چک کردن پشتیبانی مرورگر
        if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
            throw new Error('مرورگر شما از دوربین پشتیبانی نمی‌کند');
        }
        
        // درخواست دسترسی به دوربین
        const stream = await navigator.mediaDevices.getUserMedia({ 
            video: { 
                facingMode: 'environment',
                width: { ideal: 1280 },
                height: { ideal: 720 }
            },
            audio: false
        });
        
        video.srcObject = stream;
        
        await new Promise((resolve) => {
            video.onloadedmetadata = () => {
                canvas.width = video.videoWidth;
                canvas.height = video.videoHeight;
                resolve();
            };
        });
        
        await video.play();
        
        document.getElementById('status').textContent = 'بارگذاری مدل‌ها...';
        
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
        
        let errorMessage = 'خطا در دسترسی به دوربین';
        
        if (error.name === 'NotAllowedError') {
            errorMessage = 'لطفاً دسترسی به دوربین را تایید کنید';
        } else if (error.name === 'NotFoundError') {
            errorMessage = 'دوربینی یافت نشد';
        } else if (error.name === 'NotReadableError') {
            errorMessage = 'دوربین در حال استفاده است';
        } else if (error.message) {
            errorMessage = error.message;
        }
        
        alert('⚠️ ' + errorMessage + '\\n\\nتوجه: این برنامه فقط با HTTPS کار می‌کند.\\nلطفاً از مرورگر Chrome یا Safari استفاده کنید.');
        
        document.getElementById('status').textContent = '❌ ' + errorMessage;
        document.getElementById('status').style.background = '#f44336';
    }
}

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

async function detectHumans() {
    if (!isDetecting) return;
    
    try {
        const facePredictions = await faceModel.estimateFaces(video, false);
        const pose = await poseModel.estimateSinglePose(video, {
            flipHorizontal: false
        });
        
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        let totalDetections = 0;
        
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
        
        if (pose.score > 0.3) {
            const keypoints = pose.keypoints.filter(kp => kp.score > 0.3);
            
            if (keypoints.length >= 3) {
                totalDetections += 1;
                
                keypoints.forEach(kp => {
                    ctx.beginPath();
                    ctx.arc(kp.position.x, kp.position.y, 5, 0, 2 * Math.PI);
                    ctx.fillStyle = '#FF9800';
                    ctx.fill();
                });
                
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

window.addEventListener('load', () => {
    video = document.getElementById('video');
    canvas = document.getElementById('canvas');
    ctx = canvas.getContext('2d');
    
    // چک کردن HTTPS
    if (window.location.protocol !== 'https:' && window.location.hostname !== 'localhost') {
        alert('⚠️ هشدار: این برنامه نیاز به HTTPS دارد.\\n\\nلطفاً به آدرس زیر بروید:\\nhttps://' + window.location.host + window.location.pathname);
        document.getElementById('status').textContent = '❌ نیاز به HTTPS';
        document.getElementById('status').style.background = '#f44336';
        document.getElementById('startBtn').disabled = true;
        return;
    }
    
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

# ذخیره فایل JavaScript جدید
with open(f"{project_root}/js/app.js", "w", encoding="utf-8") as f:
    f.write(js_content)

print("✅ کد اصلاح شد!")
print("\n📱 راهنمای رفع خطا:")
print("1. GitHub Pages باید HTTPS فعال باشد")
print("2. در مرورگر Safari یا Chrome موبایل باز کنید")
print("3. وقتی دکمه 'شروع دوربین' را بزنید، دسترسی را تایید کنید")
print("4. اگر باز هم کار نکرد، تنظیمات مرورگر > سایت‌ها > دسترسی به دوربین را چک کنید")
