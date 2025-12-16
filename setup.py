import os

project_root = "tools/face_detection_camera"

# کد JavaScript اصلاح شده با پشتیبانی کامل Safari
js_content = """let video, canvas, ctx;
let faceModel, poseModel;
let isDetecting = false;
let detectedItems = [];
let saveEnabled = false;
let alarmEnabled = false;
let audioContext;
let lastAlarmTime = 0;
const ALARM_COOLDOWN = 1000;

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

async function startCamera() {
    try {
        document.getElementById('status').textContent = 'درخواست دسترسی...';
        document.getElementById('status').style.background = '#FF9800';
        
        // بررسی پشتیبانی مرورگر
        if (!navigator.mediaDevices?.getUserMedia) {
            throw new Error('مرورگر شما از دوربین پشتیبانی نمی‌کند');
        }
        
        // تنظیمات دوربین برای Safari iOS
        const constraints = {
            video: {
                facingMode: 'environment',
                width: { ideal: 1280, max: 1920 },
                height: { ideal: 720, max: 1080 }
            },
            audio: false
        };
        
        // درخواست دسترسی
        const stream = await navigator.mediaDevices.getUserMedia(constraints);
        
        video.srcObject = stream;
        video.setAttribute('playsinline', 'true'); // مهم برای iOS
        video.setAttribute('autoplay', 'true');
        
        // صبر برای بارگذاری ویدیو
        await new Promise((resolve, reject) => {
            video.onloadedmetadata = () => {
                canvas.width = video.videoWidth;
                canvas.height = video.videoHeight;
                resolve();
            };
            
            setTimeout(() => reject(new Error('Timeout')), 10000);
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
        
        let errorMessage = '';
        let helpText = '';
        
        if (error.name === 'NotAllowedError') {
            errorMessage = '❌ دسترسی رد شد';
            helpText = 'لطفاً در تنظیمات Safari:\\n1. تنظیمات > Safari > دوربین > اجازه\\n2. دکمه "شروع" را دوباره بزنید';
        } else if (error.name === 'NotFoundError') {
            errorMessage = '❌ دوربین پیدا نشد';
            helpText = 'لطفاً مطمئن شوید دستگاه دوربین دارد';
        } else if (error.name === 'NotReadableError') {
            errorMessage = '❌ دوربین در حال استفاده';
            helpText = 'دوربین توسط برنامه دیگری استفاده می‌شود';
        } else if (error.message === 'Timeout') {
            errorMessage = '❌ تایم‌اوت';
            helpText = 'اتصال خیلی کند است. دوباره امتحان کنید';
        } else {
            errorMessage = '❌ خطای ناشناخته';
            helpText = 'لطفاً مرورگر Chrome را امتحان کنید\\nیا از HTTPS استفاده کنید';
        }
        
        alert(errorMessage + '\\n\\n' + helpText);
        
        document.getElementById('status').textContent = errorMessage;
        document.getElementById('status').style.background = '#f44336';
        
        // آزاد کردن منابع
        if (video.srcObject) {
            video.srcObject.getTracks().forEach(track => track.stop());
        }
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
    
    // بررسی HTTPS
    const isSecure = window.location.protocol === 'https:' || 
                     window.location.hostname === 'localhost' || 
                     window.location.hostname === '127.0.0.1';
    
    if (!isSecure) {
        alert('⚠️ این برنامه فقط با HTTPS کار می‌کند');
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
        } else {
            sessionStorage.setItem('tempItems', JSON.stringify(detectedItems));
        }
    });
    
    document.getElementById('alarmToggle').addEventListener('change', (e) => {
        alarmEnabled = e.target.checked;
    });
    
    window.addEventListener('beforeunload', () => {
        if (!saveEnabled) {
            sessionStorage.removeItem('tempItems');
        }
    });
});"""

# ذخیره کد
with open(f"{project_root}/js/app.js", "w", encoding="utf-8") as f:
    f.write(js_content)

print("✅ کد برای Safari اصلاح شد!")
