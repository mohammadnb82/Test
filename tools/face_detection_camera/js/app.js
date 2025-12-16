
let video, canvas, ctx;
let modelFace, modelPose;
let isRunning = false;
let audioCtx;
let lastAlarm = 0;

window.onload = () => {
    video = document.getElementById('video');
    canvas = document.getElementById('canvas');
    ctx = canvas.getContext('2d');
    
    document.getElementById('startBtn').onclick = startCamera;
    document.getElementById('stopBtn').onclick = stopCamera;
    document.getElementById('clearLogs').onclick = () => { document.getElementById('logContainer').innerHTML = ''; };
};

async function startCamera() {
    // 1. فعال کردن صدا برای iOS (باید در کلیک کاربر باشد)
    if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    if (audioCtx.state === 'suspended') audioCtx.resume();

    document.getElementById('status').innerText = 'در حال درخواست دوربین...';
    
    // 2. تنظیمات بسیار ساده (راز موفقیت کدهای قبلی)
    // هیچ عدد خاصی برای رزولوشن نمی‌دهیم تا هر دوربینی کار کند
    const constraints = {
        audio: false,
        video: {
            facingMode: 'environment' // فقط می‌گوییم دوربین پشت
        }
    };

    try {
        const stream = await navigator.mediaDevices.getUserMedia(constraints);
        
        video.srcObject = stream;
        // ویژگی‌های مهم برای جلوگیری از سیاه شدن صفحه در iOS
        video.setAttribute('playsinline', '');
        video.setAttribute('webkit-playsinline', '');
        
        await video.play();
        
        // تنظیم اندازه بوم نقاشی بعد از لود شدن ویدیو
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;

        document.getElementById('status').innerText = 'در حال لود هوش مصنوعی (کمی صبر کنید)...';
        document.getElementById('startBtn').disabled = true;
        
        // لود مدل‌ها
        modelFace = await blazeface.load();
        modelPose = await posenet.load({
            architecture: 'MobileNetV1',
            outputStride: 16,
            inputResolution: { width: 320, height: 240 }, // مدل سبک
            multiplier: 0.5
        });

        document.getElementById('status').innerText = '✅ فعال - دوربین روشن است';
        document.getElementById('status').style.color = 'green';
        document.getElementById('stopBtn').disabled = false;
        
        isRunning = true;
        detectLoop();

    } catch (err) {
        console.error(err);
        alert('خطا: ' + err.name + '\n' + err.message);
        document.getElementById('status').innerText = '❌ خطا: دسترسی رد شد';
    }
}

function stopCamera() {
    isRunning = false;
    if (video.srcObject) {
        video.srcObject.getTracks().forEach(t => t.stop());
    }
    document.getElementById('startBtn').disabled = false;
    document.getElementById('stopBtn').disabled = true;
    document.getElementById('status').innerText = 'متوقف شده';
    ctx.clearRect(0, 0, canvas.width, canvas.height);
}

async function detectLoop() {
    if (!isRunning) return;

    // تشخیص چهره
    const faces = await modelFace.estimateFaces(video, false);
    
    // تشخیص بدن (فقط اگر چهره نبود یا برای تکمیل)
    let pose = null;
    if (faces.length === 0) {
        pose = await modelPose.estimateSinglePose(video);
    }

    // پاک کردن بوم
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    let detected = false;
    let type = '';

    // رسم چهره
    if (faces.length > 0) {
        detected = true;
        type = 'چهره';
        faces.forEach(face => {
            const start = face.topLeft;
            const end = face.bottomRight;
            const size = [end[0] - start[0], end[1] - start[1]];
            drawRect(start[0], start[1], size[0], size[1], 'red', 'Face');
        });
    } 
    // رسم بدن (اگر چهره نبود و دقت بدن بالا بود)
    else if (pose && pose.score > 0.4) {
        detected = true;
        type = 'بدن';
        const keypoints = pose.keypoints;
        // پیدا کردن محدوده بدن
        let minX = canvas.width, minY = canvas.height, maxX = 0, maxY = 0;
        keypoints.forEach(k => {
            if (k.score > 0.5) {
                if (k.position.x < minX) minX = k.position.x;
                if (k.position.x > maxX) maxX = k.position.x;
                if (k.position.y < minY) minY = k.position.y;
                if (k.position.y > maxY) maxY = k.position.y;
            }
        });
        if (maxX > minX) {
            drawRect(minX, minY, maxX - minX, maxY - minY, 'orange', 'Body');
        }
    }

    document.getElementById('msg').innerText = detected ? `⚠️ تشخیص: ${type}` : '...';
    
    if (detected) {
        playAlarm();
        logDetection(type);
    }

    requestAnimationFrame(detectLoop);
}

function drawRect(x, y, w, h, color, text) {
    ctx.strokeStyle = color;
    ctx.lineWidth = 4;
    ctx.strokeRect(x, y, w, h);
    ctx.fillStyle = color;
    ctx.fillText(text, x, y - 5);
}

function playAlarm() {
    const toggle = document.getElementById('alarmToggle');
    if (!toggle.checked || !audioCtx) return;
    
    const now = Date.now();
    if (now - lastAlarm < 1000) return; // هر 1 ثانیه بوق بزن
    lastAlarm = now;

    const osc = audioCtx.createOscillator();
    const gain = audioCtx.createGain();
    osc.connect(gain);
    gain.connect(audioCtx.destination);
    osc.frequency.value = 800;
    osc.type = 'square';
    gain.gain.setValueAtTime(0.1, audioCtx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.1);
    osc.start();
    osc.stop(audioCtx.currentTime + 0.1);
}

function logDetection(type) {
    // لاگ کردن ساده (بدون عکس برای سرعت بالاتر)
    // اگر نیاز به عکس بود می‌توان اضافه کرد اما گاهی باعث کندی می‌شود
}
