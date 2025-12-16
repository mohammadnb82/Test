
let video, canvas, ctx;
let tracker;
let task;
let audioCtx;
let lastAlarm = 0;
let isRunning = false;

window.onload = () => {
    video = document.getElementById('video');
    canvas = document.getElementById('canvas');
    ctx = canvas.getContext('2d');
    
    document.getElementById('startBtn').addEventListener('click', startSystem);
    document.getElementById('stopBtn').addEventListener('click', stopSystem);
};

async function startSystem() {
    // راه اندازی صدا
    if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    if (audioCtx.state === 'suspended') audioCtx.resume();

    try {
        const stream = await navigator.mediaDevices.getUserMedia({
            audio: false,
            video: { 
                facingMode: 'environment',
                width: { ideal: 640 },
                height: { ideal: 480 }
            }
        });
        
        video.srcObject = stream;
        video.setAttribute('playsinline', '');
        
        video.onloadedmetadata = () => {
            video.play();
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            
            // شروع تشخیص چهره با Tracking.js
            startTracking();
        };

        document.getElementById('startBtn').disabled = true;
        document.getElementById('stopBtn').disabled = false;
        document.getElementById('statusText').innerText = '✅ سیستم فعال (تشخیص چهره)';
        document.getElementById('statusText').className = 'status-active';
        isRunning = true;

    } catch (err) {
        alert('خطای دوربین: ' + err.message);
    }
}

function startTracking() {
    // تعریف ترکر چهره
    tracker = new tracking.ObjectTracker('face');
    tracker.setInitialScale(4);
    tracker.setStepSize(2);
    tracker.setEdgesDensity(0.1);

    // اتصال ترکر به المنت ویدیو
    task = tracking.track('#video', tracker, { camera: false }); // camera: false چون خودمان استریم را مدیریت کردیم

    tracker.on('track', function(event) {
        if (!isRunning) return;
        
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        if (event.data.length === 0) {
            // هیچ چهره‌ای نیست
        } else {
            event.data.forEach(function(rect) {
                // رسم کادر دور چهره
                ctx.strokeStyle = '#ef4444';
                ctx.lineWidth = 4;
                ctx.strokeRect(rect.x, rect.y, rect.width, rect.height);
                
                // متن
                ctx.fillStyle = '#ef4444';
                ctx.fillText('FACE', rect.x, rect.y - 5);
                
                playAlarm();
                logEvent('چهره');
            });
        }
    });
}

function stopSystem() {
    isRunning = false;
    if (task) {
        task.stop(); // توقف پردازش تصویر
    }
    if (video.srcObject) {
        video.srcObject.getTracks().forEach(t => t.stop());
        video.srcObject = null;
    }
    
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    document.getElementById('startBtn').disabled = false;
    document.getElementById('stopBtn').disabled = true;
    document.getElementById('statusText').innerText = 'متوقف شده';
    document.getElementById('statusText').className = 'status-waiting';
}

function playAlarm() {
    if (!document.getElementById('alarmToggle').checked || !audioCtx) return;
    
    const now = Date.now();
    if (now - lastAlarm < 1000) return;
    lastAlarm = now;
    
    const osc = audioCtx.createOscillator();
    const gain = audioCtx.createGain();
    osc.connect(gain);
    gain.connect(audioCtx.destination);
    
    osc.frequency.setValueAtTime(800, audioCtx.currentTime);
    osc.frequency.exponentialRampToValueAtTime(400, audioCtx.currentTime + 0.2);
    
    gain.gain.setValueAtTime(0.2, audioCtx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.2);
    
    osc.start();
    osc.stop(audioCtx.currentTime + 0.2);
}

function logEvent(type) {
    const logs = document.getElementById('logs');
    if (logs.firstChild && logs.firstChild.innerText.includes('الان')) return;

    const div = document.createElement('div');
    div.className = 'log-entry';
    div.innerText = `⚠️ تشخیص ${type} - ${new Date().toLocaleTimeString('fa-IR')}`;
    logs.insertBefore(div, logs.firstChild);
    
    if (logs.children.length > 20) logs.removeChild(logs.lastChild);
}
