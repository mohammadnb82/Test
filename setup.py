import os

# Define the target file path
target_file_path = "tools/doorbin-tashkhis-harekat/index_doorbin-tashkhis-harekat.html"

# The complete HTML content with integrated Web Audio API siren
html_content = """<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>دوربین تشخیص حرکت + آژیر دیجیتال</title>
    <style>
        body { font-family: system-ui; background: #000; color: white; display: flex; flex-direction: column; align-items: center; min-height: 100vh; margin: 0; padding: 20px; }
        
        .video-container { position: relative; width: 100%; max-width: 640px; margin-bottom: 20px; border: 2px solid #333; border-radius: 10px; overflow: hidden; }
        video, canvas { width: 100%; height: auto; display: block; }
        canvas { position: absolute; top: 0; left: 0; pointer-events: none; }
        
        .controls { width: 100%; max-width: 640px; background: #222; padding: 20px; border-radius: 12px; display: flex; flex-direction: column; gap: 15px; }
        
        .control-row { display: flex; justify-content: space-between; align-items: center; }
        
        input[type=range] { width: 60%; }
        
        #sirenBtn {
            background: #444; color: #aaa; border: none; padding: 12px 20px; border-radius: 8px; font-weight: bold; cursor: pointer; transition: 0.3s; display: flex; align-items: center; gap: 8px; font-size: 16px; width: 100%; justify-content: center;
        }
        #sirenBtn.active {
            background: #dc3545; color: white; animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0% { box-shadow: 0 0 0 0 rgba(220, 53, 69, 0.4); }
            70% { box-shadow: 0 0 0 10px rgba(220, 53, 69, 0); }
            100% { box-shadow: 0 0 0 0 rgba(220, 53, 69, 0); }
        }

        .status { font-size: 14px; color: #888; margin-top: 5px; text-align: center; }
        .back-link { margin-top: 30px; color: #666; text-decoration: none; }
    </style>
</head>
<body>

    <div class="video-container">
        <video id="video" autoplay playsinline muted></video>
        <canvas id="canvas"></canvas>
    </div>

    <div class="controls">
        <div class="control-row">
            <span>حساسیت: <span id="valDisplay">20</span></span>
            <input type="range" id="sensitivity" min="5" max="100" value="20">
        </div>

        <button id="sirenBtn" onclick="toggleSiren()">
            🔕 آژیر خاموش است
        </button>
        
        <div class="status" id="motionStatus">وضعیت: عادی</div>
    </div>

    <a href="../index_tools.html" class="back-link">⬅️ بازگشت به ابزارها</a>

    <script>
        const video = document.getElementById('video');
        const canvas = document.getElementById('canvas');
        const ctx = canvas.getContext('2d');
        const statusEl = document.getElementById('motionStatus');
        const rangeEl = document.getElementById('sensitivity');
        const valDisplay = document.getElementById('valDisplay');
        const sirenBtn = document.getElementById('sirenBtn');

        let isSirenEnabled = false;
        let lastFrameData = null;
        let diffCanvas = document.createElement('canvas');
        let diffCtx = diffCanvas.getContext('2d');
        let motionTimeout;
        
        // --- تنظیمات سیستم صوتی (Web Audio API) ---
        let audioCtx;
        let oscillator = null;
        let gainNode = null;

        // تابع راه‌اندازی سیستم صوتی
        function initAudioContext() {
            if (!audioCtx) {
                // پشتیبانی از مرورگرهای جدید و سافاری قدیمی
                const AudioContext = window.AudioContext || window.webkitAudioContext;
                audioCtx = new AudioContext();
            }
            // اگر مرورگر صدا را غیرفعال کرده باشد، آن را فعال می‌کنیم
            if (audioCtx.state === 'suspended') {
                audioCtx.resume();
            }
        }

        function startBeep() {
            if (oscillator) return; // اگر صدا در حال پخش است، دوباره شروع نکن

            initAudioContext();
            
            oscillator = audioCtx.createOscillator();
            gainNode = audioCtx.createGain();

            // نوع موج صدا (sawtooth صدای خشن‌تر و شبیه دزدگیر دارد)
            oscillator.type = 'sawtooth'; 
            oscillator.frequency.setValueAtTime(800, audioCtx.currentTime); // فرکانس شروع
            
            // افکت آژیر (تغییر فرکانس)
            oscillator.frequency.exponentialRampToValueAtTime(1200, audioCtx.currentTime + 0.1);
            oscillator.frequency.exponentialRampToValueAtTime(800, audioCtx.currentTime + 0.2);
            
            // اتصال گره‌ها
            oscillator.connect(gainNode);
            gainNode.connect(audioCtx.destination);
            
            oscillator.start();
        }

        function stopBeep() {
            if (oscillator) {
                try {
                    oscillator.stop();
                    oscillator.disconnect();
                } catch(e) {}
                oscillator = null;
            }
        }
        // ---------------------------------------------

        navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } })
            .then(stream => { video.srcObject = stream; })
            .catch(err => console.error("دسترسی به دوربین داده نشد", err));

        rangeEl.addEventListener('input', (e) => {
            valDisplay.innerText = e.target.value;
        });

        function toggleSiren() {
            // برای فعال کردن AudioContext در مرورگرهای موبایل، حتما باید داخل رویداد کلیک باشد
            initAudioContext(); 
            
            isSirenEnabled = !isSirenEnabled;
            if (isSirenEnabled) {
                sirenBtn.classList.add('active');
                sirenBtn.innerHTML = "🔔 آژیر فعال است (آماده هشدار)";
                // یک صدای خیلی کوتاه تست پخش می‌کنیم تا قفل صدای مرورگر باز شود
                startBeep();
                setTimeout(stopBeep, 50); 
            } else {
                sirenBtn.classList.remove('active');
                sirenBtn.innerHTML = "🔕 آژیر خاموش است";
                stopBeep();
            }
        }

        function processVideo() {
            if (video.readyState === 4) {
                canvas.width = video.videoWidth;
                canvas.height = video.videoHeight;
                diffCanvas.width = 64; 
                diffCanvas.height = 48;

                diffCtx.drawImage(video, 0, 0, 64, 48);
                let currentFrameData = diffCtx.getImageData(0, 0, 64, 48);

                if (lastFrameData) {
                    let score = 0;
                    for (let i = 0; i < currentFrameData.data.length; i += 4) {
                        let rDiff = Math.abs(currentFrameData.data[i] - lastFrameData.data[i]);
                        let gDiff = Math.abs(currentFrameData.data[i+1] - lastFrameData.data[i+1]);
                        let bDiff = Math.abs(currentFrameData.data[i+2] - lastFrameData.data[i+2]);
                        
                        if (rDiff + gDiff + bDiff > 100) { 
                            score++;
                        }
                    }

                    let threshold = (105 - rangeEl.value) * 10; 

                    if (score > threshold) {
                        onMotionDetected();
                    } else {
                        // اگر حرکتی نیست، صدا را قطع کن
                        if (isSirenEnabled && oscillator) {
                            // صدا با تایمر پایین قطع می‌شود
                        }
                    }
                }

                lastFrameData = currentFrameData;
            }
            requestAnimationFrame(processVideo);
        }

        function onMotionDetected() {
            statusEl.innerText = "⚠️ حرکت تشخیص داده شد!";
            statusEl.style.color = "#ff4444";
            
            ctx.strokeStyle = "red";
            ctx.lineWidth = 10;
            ctx.strokeRect(0, 0, canvas.width, canvas.height);

            // پخش آژیر اگر دکمه فعال باشد
            if (isSirenEnabled) {
                startBeep();
            }

            clearTimeout(motionTimeout);
            motionTimeout = setTimeout(() => {
                statusEl.innerText = "وضعیت: عادی";
                statusEl.style.color = "#888";
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                
                // قطع صدا وقتی حرکت تمام شد
                stopBeep();
            }, 300); // قطع صدا 300 میلی ثانیه بعد از آخرین فریم حرکت
        }

        video.addEventListener('play', processVideo);
    </script>
</body>
</html>"""

# Write the content to the file
try:
    with open(target_file_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"✅ فایل {target_file_path} با موفقیت به‌روزرسانی شد.")
    print("ویژگی آژیر دیجیتال (بدون فایل صوتی خارجی) اضافه شد.")
except FileNotFoundError:
    print(f"❌ خطا: مسیر {target_file_path} پیدا نشد.")
    print("لطفاً مطمئن شوید که ساختار پوشه‌ها درست است.")
except Exception as e:
    print(f"❌ خطای غیرمنتظره: {e}")
