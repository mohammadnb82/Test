
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
