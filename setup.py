import os

def add_siren_feature():
    # ---------------------------------------------------------
    # 1. بروزرسانی index.html (اضافه کردن دکمه صدا)
    # ---------------------------------------------------------
    html_path = "index.html" # فرض بر این است که فایل در ریشه است، اگر نیست مسیر را اصلاح کنید
    
    # محتوای کامل و استاندارد HTML (شامل CSSهای اصلاح شده قبلی + دکمه جدید)
    html_content = """<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>دوربین هوشمند</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; touch-action: manipulation; }
        body { 
            font-family: system-ui, -apple-system, sans-serif; 
            background: #111; 
            color: white; 
            height: 100dvh; 
            overflow: hidden; 
            display: flex; 
            flex-direction: column; 
        }

        /* بخش نمایش ویدیو */
        .camera-container {
            flex: 1;
            position: relative;
            overflow: hidden;
            display: flex;
            justify-content: center;
            align-items: center;
            background: #000;
        }

        video {
            width: 100%;
            height: 100%;
            object-fit: contain; /* تضمین نمایش کامل تصویر */
            display: block;
        }

        /* کانواس مخفی برای پردازش */
        #output { display: none; }

        /* لایه آمار روی تصویر */
        .overlay-stats {
            position: absolute;
            top: 10px;
            left: 10px;
            right: 10px;
            display: flex;
            justify-content: space-between;
            z-index: 10;
            pointer-events: none;
        }
        .stat-box {
            background: rgba(0, 0, 0, 0.6);
            padding: 5px 10px;
            border-radius: 8px;
            font-size: 14px;
            font-weight: bold;
        }

        /* کنترل پنل پایین */
        .controls {
            height: auto;
            min-height: 160px;
            background: #222;
            padding: 15px;
            border-top-left-radius: 20px;
            border-top-right-radius: 20px;
            display: flex;
            flex-direction: column;
            gap: 15px;
            z-index: 20;
        }

        /* نوار وضعیت حرکت */
        .motion-meter {
            height: 20px;
            background: #444;
            border-radius: 10px;
            position: relative;
            overflow: hidden;
        }
        .motion-bar {
            height: 100%;
            width: 0%;
            background: #00ff00;
            transition: width 0.1s linear, background 0.2s;
        }
        .threshold-marker {
            position: absolute;
            top: 0;
            bottom: 0;
            width: 2px;
            background: yellow;
            z-index: 5;
        }

        /* اسلایدر تنظیم حساسیت */
        .slider-container {
            display: flex;
            align-items: center;
            gap: 10px;
        }
        input[type=range] {
            flex: 1;
            height: 30px;
        }

        /* دکمه‌ها */
        .buttons-row {
            display: flex;
            gap: 10px;
        }
        
        .btn {
            flex: 1;
            padding: 12px;
            border: none;
            border-radius: 10px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
        }

        .btn-camera { background: #007bff; }
        .btn-camera:active { background: #0056b3; }

        .btn-sound { background: #6c757d; }
        .btn-sound.active { background: #dc3545; animation: pulse 1s infinite; }

        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.02); }
            100% { transform: scale(1); }
        }

    </style>
</head>
<body>

    <div class="camera-container">
        <video id="video" autoplay playsinline muted></video>
        <canvas id="output"></canvas>
        
        <div class="overlay-stats">
            <div class="stat-box">حرکت: <span id="motion-val-text">0</span>%</div>
            <div class="stat-box" style="color: yellow;">حساسیت: <span id="thresh-val-text">50</span>%</div>
        </div>
    </div>

    <div class="controls">
        <!-- نوار نمایشگر حرکت -->
        <div class="motion-meter">
            <div id="motion-bar" class="motion-bar"></div>
            <div id="threshold-marker" class="threshold-marker" style="left: 50%;"></div>
        </div>

        <!-- اسلایدر -->
        <div class="slider-container">
            <span>حساسیت:</span>
            <input type="range" id="sensitivity-slider" min="1" max="100" value="50">
        </div>

        <!-- دکمه‌ها -->
        <div class="buttons-row">
            <button id="switch-camera" class="btn btn-camera">
                📷 چرخش دوربین
            </button>
            <button id="toggle-sound" class="btn btn-sound">
                🔇 آژیر: خاموش
            </button>
        </div>
    </div>

    <script src="app.js"></script>
</body>
</html>
"""

    # ---------------------------------------------------------
    # 2. بروزرسانی app.js (اضافه کردن منطق آژیر به کد اصلاح شده قبلی)
    # ---------------------------------------------------------
    js_path = "tools/doorbin-tashkhis-harekat/app.js"
    if not os.path.exists("tools/doorbin-tashkhis-harekat"):
         js_path = "app.js" # مسیر جایگزین

    js_content = """
let videoStream = null;
let video = document.getElementById('video');
let canvas = document.getElementById('output');
let ctx = canvas.getContext('2d', { willReadFrequently: true });
let sensitivitySlider = document.getElementById('sensitivity-slider');
let motionBar = document.getElementById('motion-bar');
let thresholdMarker = document.getElementById('threshold-marker');
let motionValText = document.getElementById('motion-val-text');
let threshValText = document.getElementById('thresh-val-text');
let switchBtn = document.getElementById('switch-camera');
let soundBtn = document.getElementById('toggle-sound');

// متغیرهای وضعیت
let currentFacingMode = 'environment';
let animationId = null;
let lastFrameData = null;
let isSoundEnabled = false; // وضعیت پیش‌فرض صدا

// سیستم صوتی (Oscillator)
let audioCtx = null;
let oscillator = null;
let gainNode = null;

// اندازه پردازش (ثابت شده برای رفع باگ)
const PROCESS_WIDTH = 64;  
const PROCESS_HEIGHT = 48; 

// تنظیم اولیه اسلایدر
sensitivitySlider.value = 50;
updateThresholdUI(50);

// راه‌اندازی دوربین
async function setupCamera() {
    if (videoStream) {
        videoStream.getTracks().forEach(track => track.stop());
    }

    try {
        const constraints = {
            video: {
                facingMode: currentFacingMode,
                width: { ideal: 640 },
                height: { ideal: 480 }
            },
            audio: false
        };

        videoStream = await navigator.mediaDevices.getUserMedia(constraints);
        video.srcObject = videoStream;

        video.onloadedmetadata = () => {
            canvas.width = PROCESS_WIDTH;
            canvas.height = PROCESS_HEIGHT;
            video.play();
            startDetection();
        };

    } catch (err) {
        console.error("خطا در دسترسی به دوربین:", err);
        alert("لطفاً دسترسی دوربین را فعال کنید.");
    }
}

// توابع کنترل صدا (آژیر)
function initAudio() {
    if (!audioCtx) {
        audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    }
}

function startAlarm() {
    if (oscillator) return; // اگر آژیر روشن است کاری نکن
    
    initAudio();
    if (audioCtx.state === 'suspended') audioCtx.resume();

    oscillator = audioCtx.createOscillator();
    gainNode = audioCtx.createGain();

    oscillator.type = 'sawtooth'; // نوع موج صدا (تیز و آژیر مانند)
    oscillator.frequency.setValueAtTime(600, audioCtx.currentTime); // شروع فرکانس
    
    // افکت بالا و پایین رفتن صدا (آژیر پلیسی)
    oscillator.frequency.linearRampToValueAtTime(900, audioCtx.currentTime + 0.5);
    
    oscillator.connect(gainNode);
    gainNode.connect(audioCtx.destination);
    oscillator.start();

    // تکرار افکت آژیر
    oscillator.onended = () => { oscillator = null; };
}

function stopAlarm() {
    if (oscillator) {
        try {
            oscillator.stop();
            oscillator.disconnect();
            gainNode.disconnect();
        } catch(e) {}
        oscillator = null;
    }
}

// حلقه تشخیص حرکت
function startDetection() {
    if (animationId) cancelAnimationFrame(animationId);

    function loop() {
        if (video.paused || video.ended) return;

        ctx.drawImage(video, 0, 0, PROCESS_WIDTH, PROCESS_HEIGHT);
        
        const frameData = ctx.getImageData(0, 0, PROCESS_WIDTH, PROCESS_HEIGHT);
        const currentData = frameData.data;

        let movementScore = 0;

        if (lastFrameData) {
            let totalDiff = 0;
            const length = currentData.length;

            for (let i = 0; i < length; i += 16) { 
                const rDiff = Math.abs(currentData[i] - lastFrameData[i]);
                const gDiff = Math.abs(currentData[i+1] - lastFrameData[i+1]);
                const bDiff = Math.abs(currentData[i+2] - lastFrameData[i+2]);

                if (rDiff + gDiff + bDiff > 50) {
                    totalDiff++;
                }
            }
            movementScore = Math.min(100, Math.floor((totalDiff / (PROCESS_WIDTH * PROCESS_HEIGHT / 16)) * 300));
        }

        lastFrameData = new Uint8ClampedArray(currentData);

        updateUI(movementScore);

        animationId = requestAnimationFrame(loop);
    }

    loop();
}

// بروزرسانی رابط کاربری و منطق آلارم
function updateUI(score) {
    motionBar.style.width = score + '%';
    motionValText.innerText = score;
    const threshold = parseInt(sensitivitySlider.value);
    
    if (score > threshold) {
        // وضعیت خطر
        document.body.style.boxShadow = "inset 0 0 50px red";
        document.body.style.border = "5px solid red";
        motionBar.style.background = "red";
        
        // پخش آژیر اگر دکمه صدا روشن باشد
        if (isSoundEnabled) {
            startAlarm();
        }
    } else {
        // وضعیت عادی
        document.body.style.boxShadow = "none";
        document.body.style.border = "none";
        motionBar.style.background = "#00ff00";
        
        // قطع آژیر
        stopAlarm();
    }
}

function updateThresholdUI(val) {
    thresholdMarker.style.left = val + '%';
    threshValText.innerText = val;
}

// رویدادهای اسلایدر
sensitivitySlider.addEventListener('input', (e) => {
    updateThresholdUI(e.target.value);
});

// دکمه چرخش دوربین
switchBtn.addEventListener('click', () => {
    currentFacingMode = (currentFacingMode === 'environment') ? 'user' : 'environment';
    setupCamera();
});

// دکمه کنترل صدا
soundBtn.addEventListener('click', () => {
    isSoundEnabled = !isSoundEnabled;
    
    if (isSoundEnabled) {
        // اولین تعامل برای باز کردن قفل AudioContext مرورگر
        initAudio();
        if (audioCtx.state === 'suspended') audioCtx.resume();

        soundBtn.innerHTML = "🔊 آژیر: روشن";
        soundBtn.classList.add('active');
        soundBtn.style.background = "#dc3545"; // قرمز برای حالت آماده باش
    } else {
        stopAlarm();
        soundBtn.innerHTML = "🔇 آژیر: خاموش";
        soundBtn.classList.remove('active');
        soundBtn.style.background = "#6c757d"; // خاکستری
    }
});

// شروع برنامه
setupCamera();
"""

    # نوشتن فایل‌ها
    try:
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"✅ فایل {html_path} با دکمه جدید آپدیت شد.")

        with open(js_path, "w", encoding="utf-8") as f:
            f.write(js_content)
        print(f"✅ فایل {js_path} با منطق آژیر آپدیت شد.")
        
    except Exception as e:
        print(f"❌ خطا در نوشتن فایل‌ها: {e}")

if __name__ == "__main__":
    add_siren_feature()
