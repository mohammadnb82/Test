
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
