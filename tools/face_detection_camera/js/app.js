
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
