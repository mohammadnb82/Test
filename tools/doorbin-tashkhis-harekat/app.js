
const video = document.getElementById('video');
const canvas = document.getElementById('output');
const ctx = canvas.getContext('2d');
const statusDiv = document.getElementById('status');
const sensitivityInput = document.getElementById('sensitivity');
const sensitivityVal = document.getElementById('sens-val');
const motionBar = document.getElementById('motion-bar');
const thresholdMarker = document.getElementById('threshold-marker');
const cameraContainer = document.getElementById('camera-container');

let stream = null;
let facingMode = 'environment';
let previousFrameData = null;

// ضریب تقویت حرکت: تغییرات پیکسلی معمولاً کم هستند. 
// این ضریب باعث می‌شود حرکت‌های کوچک هم روی نوار سبز دیده شوند.
const MOTION_AMPLIFY_FACTOR = 10; 

// تنظیمات اولیه
updateThresholdSystem();

// وقتی اسلایدر تغییر می‌کند
sensitivityInput.addEventListener('input', (e) => {
    updateThresholdSystem();
});

function updateThresholdSystem() {
    // مقدار اسلایدر مستقیماً به عنوان "حد آستانه" (Threshold) عمل می‌کند
    const val = parseInt(sensitivityInput.value);
    
    // نمایش عدد به کاربر
    sensitivityVal.textContent = val;
    
    // حرکت خط قرمز دقیقاً به همان درصد اسلایدر
    thresholdMarker.style.left = val + '%';
}

async function startCamera() {
    if (stream) {
        stream.getTracks().forEach(track => track.stop());
    }
    try {
        statusDiv.textContent = 'در حال راه‌اندازی...';
        stream = await navigator.mediaDevices.getUserMedia({
            video: { 
                facingMode: facingMode,
                width: { ideal: 640 }, // رزولوشن مناسب برای سرعت بالا
                height: { ideal: 480 }
            },
            audio: false
        });
        video.srcObject = stream;
        
        video.onloadedmetadata = () => {
            statusDiv.textContent = 'آماده تشخیص حرکت';
            // کانواس بسیار کوچک برای پردازش فوق‌سریع
            canvas.width = 64; 
            canvas.height = 48;
            detectMotion();
        };
    } catch (err) {
        console.error(err);
        statusDiv.textContent = 'خطا: ' + err.message;
    }
}

document.getElementById('switch-camera').addEventListener('click', () => {
    facingMode = facingMode === 'environment' ? 'user' : 'environment';
    startCamera();
});

function detectMotion() {
    if (video.paused || video.ended) return;

    // 1. رسم تصویر روی کانواس کوچک
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    
    // 2. استخراج داده‌های پیکسل
    const frame = ctx.getImageData(0, 0, canvas.width, canvas.height);
    const data = frame.data;
    const length = data.length;
    
    let changedPixels = 0;

    if (previousFrameData) {
        for (let i = 0; i < length; i += 4) {
            // محاسبه تفاوت رنگی با فریم قبلی
            const rDiff = Math.abs(data[i] - previousFrameData[i]);
            const gDiff = Math.abs(data[i+1] - previousFrameData[i+1]);
            const bDiff = Math.abs(data[i+2] - previousFrameData[i+2]);
            
            // اگر تغییر رنگ پیکسل بیشتر از حد نویز بود (30)
            if (rDiff + gDiff + bDiff > 60) {
                changedPixels++;
            }
        }
    }

    // ذخیره فریم فعلی
    previousFrameData = new Uint8ClampedArray(data);

    // 3. محاسبه درصد واقعی تغییرات
    const totalPixels = canvas.width * canvas.height;
    const rawMotionPercent = (changedPixels / totalPixels) * 100;

    // 4. اعمال ضریب تقویت برای نمایش در نوار سبز (0 تا 100)
    let displayValue = rawMotionPercent * MOTION_AMPLIFY_FACTOR;
    if (displayValue > 100) displayValue = 100; // سقف 100

    // 5. به‌روزرسانی نوار سبز
    motionBar.style.width = displayValue + '%';

    // 6. مقایسه با اسلایدر (منطق اصلی)
    // دقیقاً همان عددی که خط قرمز روی آن است را می‌خوانیم
    const thresholdSetting = parseInt(sensitivityInput.value);

    // اگر "مقدار نوار سبز" از "مکان خط قرمز" بیشتر شد -> هشدار
    if (displayValue > thresholdSetting) {
        cameraContainer.style.border = "5px solid red";
        statusDiv.style.color = "red";
        statusDiv.textContent = `حرکت: ${Math.round(displayValue)} (آستانه: ${thresholdSetting})`;
    } else {
        cameraContainer.style.border = "none";
        statusDiv.style.color = "#888";
        statusDiv.textContent = "در حال نظارت...";
    }

    requestAnimationFrame(detectMotion);
}

startCamera();
