// متغیرهای سراسری
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
});