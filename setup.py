import os

# مسیر دقیق فایل دوربین
target_file_path = "tools/doorbin-tashkhis-harekat/index_doorbin-tashkhis-harekat.html"

# محتوای کامل HTML شامل: آژیر، تغییر دوربین، نوار حرکت و تنظیمات
html_content = """<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>دوربین هوشمند کامل</title>
    <style>
        body { font-family: system-ui, -apple-system, sans-serif; background: #000; color: white; display: flex; flex-direction: column; align-items: center; min-height: 100vh; margin: 0; padding: 10px; box-sizing: border-box; }
        
        .video-wrapper { position: relative; width: 100%; max-width: 600px; border: 2px solid #333; border-radius: 12px; overflow: hidden; background: #111; aspect-ratio: 4/3; }
        video { width: 100%; height: 100%; object-fit: cover; display: block; }
        canvas { display: none; } /* بوم پردازش مخفی است */
        
        /* لایه هشدار قرمز روی ویدیو */
        #alarmOverlay {
            position: absolute; top: 0; left: 0; right: 0; bottom: 0;
            background: rgba(255, 0, 0, 0.3); border: 4px solid red;
            display: none; pointer-events: none; z-index: 10;
        }

        .controls { width: 100%; max-width: 600px; background: #1a1a1a; padding: 15px; border-radius: 15px; margin-top: 15px; display: flex; flex-direction: column; gap: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.5); }
        
        .row { display: flex; justify-content: space-between; align-items: center; width: 100%; gap: 10px; }
        
        label { font-size: 14px; color: #ccc; white-space: nowrap; }
        
        /* استایل اسلایدر */
        input[type=range] { flex-grow: 1; height: 6px; border-radius: 5px; background: #444; outline: none; -webkit-appearance: none; }
        input[type=range]::-webkit-slider-thumb { -webkit-appearance: none; width: 20px; height: 20px; background: #3b82f6; border-radius: 50%; cursor: pointer; }

        /* نوار میزان حرکت */
        .motion-meter-container { width: 100%; height: 10px; background: #333; border-radius: 5px; overflow: hidden; position: relative; margin-top: 5px; }
        .motion-meter-fill { height: 100%; width: 0%; background: lime; transition: width 0.1s linear, background 0.2s; }
        
        /* دکمه‌ها */
        .btn { border: none; padding: 12px; border-radius: 10px; font-weight: bold; font-size: 14px; cursor: pointer; flex: 1; display: flex; align-items: center; justify-content: center; gap: 5px; transition: 0.2s; }
        
        .btn-camera { background: #333; color: white; }
        .btn-camera:active { background: #555; }

        .btn-siren { background: #333; color: #aaa; }
        .btn-siren.active { background: #dc3545; color: white; animation: pulse 1.5s infinite; }
        
        @keyframes pulse { 0% { box-shadow: 0 0 0 0 rgba(220, 53, 69, 0.4); } 70% { box-shadow: 0 0 0 10px rgba(220, 53, 69, 0); } 100% { box-shadow: 0 0 0 0 rgba(220, 53, 69, 0); } }

        .status-text { text-align: center; color: #888; font-size: 13px; margin-top: 5px; }
        .back-link { margin-top: 20px; color: #666; text-decoration: none; font-size: 14px; }
    </style>
</head>
<body>

    <div class="video-wrapper">
        <video id="video" autoplay playsinline muted></video>
        <div id="alarmOverlay"></div>
    </div>
    <canvas id="canvas"></canvas>

    <div class="controls">
        <!-- ردیف حساسیت -->
        <div class="row">
            <label>حساسیت (<span id="sensVal">20</span>):</label>
            <input type="range" id="sensitivity" min="5" max="100" value="20">
        </div>

        <!-- نوار نمایش حرکت -->
        <div>
            <div class="row" style="margin-bottom: 2px;">
                <label style="font-size: 12px;">میزان حرکت:</label>
            </div>
            <div class="motion-meter-container">
                <div id="motionBar" class="motion-meter-fill"></div>
            </div>
        </div>

        <!-- دکمه‌ها -->
        <div class="row">
            <button class="btn btn-camera" onclick="switchCamera()">
                📷 چرخش دوربین
            </button>
            <button id="sirenBtn" class="btn btn-siren" onclick="toggleSiren()">
                🔕 آژیر خاموش
            </button>
        </div>

        <div class="status-text" id="status">وضعیت: عادی</div>
    </div>

    <a href="../index_tools.html" class="back-link">⬅️ بازگشت به ابزارها</a>

    <script>
        const video = document.getElementById('video');
        const canvas = document.getElementById('canvas');
        const ctx = canvas.getContext('2d');
        const alarmOverlay = document.getElementById('alarmOverlay');
        const motionBar = document.getElementById('motionBar');
        const statusEl = document.getElementById('status');
        const sensInput = document.getElementById('sensitivity');
        const sensVal = document.getElementById('sensVal');
        const sirenBtn = document.getElementById('sirenBtn');

        let currentFacingMode = 'environment';
        let stream = null;
        let lastFrameData = null;
        let isSirenEnabled = false;
        let motionTimeout;

        // --- تنظیمات صدای دیجیتال (Web Audio API) ---
        let audioCtx;
        let oscillator = null;
        
        function initAudio() {
            if (!audioCtx) {
                const AudioContext = window.AudioContext || window.webkitAudioContext;
                audioCtx = new AudioContext();
            }
            if (audioCtx.state === 'suspended') audioCtx.resume();
        }

        function startBeep() {
            if (oscillator) return;
            initAudio();
            oscillator = audioCtx.createOscillator();
            let gainNode = audioCtx.createGain();
            
            oscillator.type = 'sawtooth';
            oscillator.frequency.setValueAtTime(800, audioCtx.currentTime);
            oscillator.frequency.linearRampToValueAtTime(1200, audioCtx.currentTime + 0.1);
            oscillator.frequency.linearRampToValueAtTime(800, audioCtx.currentTime + 0.2);
            
            oscillator.connect(gainNode);
            gainNode.connect(audioCtx.destination);
            oscillator.start();
        }

        function stopBeep() {
            if (oscillator) {
                try { oscillator.stop(); oscillator.disconnect(); } catch(e){}
                oscillator = null;
            }
        }
        // ---------------------------------------------

        // راه‌اندازی دوربین
        async function startCamera() {
            if (stream) {
                stream.getTracks().forEach(track => track.stop());
            }
            try {
                stream = await navigator.mediaDevices.getUserMedia({ 
                    video: { facingMode: currentFacingMode } 
                });
                video.srcObject = stream;
            } catch (err) {
                alert("خطا در دسترسی به دوربین: " + err);
            }
        }

        function switchCamera() {
            currentFacingMode = (currentFacingMode === 'environment') ? 'user' : 'environment';
            startCamera();
        }

        // پردازش تصویر برای تشخیص حرکت
        function processFrame() {
            if (video.readyState === 4) {
                // تنظیم اندازه کانواس کوچک برای پردازش سریع
                const w = 64;
                const h = 48;
                canvas.width = w;
                canvas.height = h;
                
                ctx.drawImage(video, 0, 0, w, h);
                const currentData = ctx.getImageData(0, 0, w, h);

                if (lastFrameData) {
                    let score = 0;
                    // مقایسه پیکسل به پیکسل
                    for (let i = 0; i < currentData.data.length; i += 4) {
                        const r = Math.abs(currentData.data[i] - lastFrameData.data[i]);
                        const g = Math.abs(currentData.data[i+1] - lastFrameData.data[i+1]);
                        const b = Math.abs(currentData.data[i+2] - lastFrameData.data[i+2]);
                        if (r+g+b > 100) score++; // شمارش پیکسل‌های تغییر کرده
                    }

                    // به‌روزرسانی نوار حرکت (ویژوال)
                    // عدد 1000 یک عدد تقریبی برای نرمال‌سازی است
                    let barPercent = Math.min((score / 500) * 100, 100);
                    motionBar.style.width = barPercent + "%";
                    
                    // تغییر رنگ نوار بر اساس شدت
                    if (barPercent > 50) motionBar.style.background = "red";
                    else motionBar.style.background = "lime";

                    // منطق آستانه
                    const threshold = (105 - sensInput.value) * 5; 

                    if (score > threshold) {
                        triggerAlarm();
                    } else {
                        resetAlarm();
                    }
                }
                lastFrameData = currentData;
            }
            requestAnimationFrame(processFrame);
        }

        function triggerAlarm() {
            statusEl.innerText = "⚠️ حرکت تشخیص داده شد!";
            statusEl.style.color = "#ff4444";
            alarmOverlay.style.display = "block";

            if (isSirenEnabled) {
                startBeep();
            }

            clearTimeout(motionTimeout);
            motionTimeout = setTimeout(() => {
                resetAlarm(true); // توقف کامل
            }, 300);
        }

        function resetAlarm(fullStop = false) {
            if (fullStop) {
                statusEl.innerText = "وضعیت: عادی";
                statusEl.style.color = "#888";
                alarmOverlay.style.display = "none";
                stopBeep();
            }
        }

        // رویدادها
        sensInput.addEventListener('input', (e) => sensVal.innerText = e.target.value);
        
        function toggleSiren() {
            initAudio(); // فعال‌سازی زمینه صوتی
            isSirenEnabled = !isSirenEnabled;
            if (isSirenEnabled) {
                sirenBtn.classList.add('active');
                sirenBtn.innerHTML = "🔔 آژیر فعال";
                // پخش صدای تست کوتاه
                startBeep(); setTimeout(stopBeep, 100);
            } else {
                sirenBtn.classList.remove('active');
                sirenBtn.innerHTML = "🔕 آژیر خاموش";
                stopBeep();
            }
        }

        // شروع برنامه
        startCamera();
        video.addEventListener('play', processFrame);

    </script>
</body>
</html>"""

# نوشتن فایل
try:
    with open(target_file_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"✅ فایل {target_file_path} با موفقیت کامل بازنویسی شد.")
    print("ویژگی‌های بازگردانده شده: دکمه چرخش دوربین، نوار حرکت، آژیر دیجیتال.")
except Exception as e:
    print(f"❌ خطا: {e}")
