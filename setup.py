import os

def fix_red_border_logic():
    js_path = "tools/doorbin-tashkhis-harekat/app.js"
    
    js_content = """
const video = document.getElementById('video');
const canvas = document.getElementById('output');
const ctx = canvas.getContext('2d');
const statusDiv = document.getElementById('status');
const sensitivityInput = document.getElementById('sensitivity');
const sensitivityVal = document.getElementById('sens-val');
const motionBar = document.getElementById('motion-bar');
const thresholdMarker = document.getElementById('threshold-marker');
const cameraContainer = document.getElementById('camera-container'); // کانتینر اصلی
let stream = null;
let facingMode = 'environment';
let previousFrameData = null;

// تنظیمات اولیه
let sensitivity = 50; 
updateThresholdMarker();

sensitivityInput.addEventListener('input', (e) => {
    sensitivity = parseInt(e.target.value);
    sensitivityVal.textContent = sensitivity + '%';
    updateThresholdMarker();
});

function updateThresholdMarker() {
    // هرچه حساسیت بالاتر (عدد بیشتر)، آستانه پایین‌تر (حرکت کمتر لازم است)
    // حساسیت 100 => آستانه 0 (با کوچکترین حرکت فعال شود)
    // حساسیت 0 => آستانه 50 (نیاز به حرکت زیاد)
    const thresholdPercent = 50 - (sensitivity / 2); 
    thresholdMarker.style.left = thresholdPercent + '%';
}

async function startCamera() {
    if (stream) {
        stream.getTracks().forEach(track => track.stop());
    }
    try {
        statusDiv.textContent = 'در حال راه‌اندازی دوربین...';
        stream = await navigator.mediaDevices.getUserMedia({
            video: { 
                facingMode: facingMode,
                width: { ideal: 640 },
                height: { ideal: 480 }
            },
            audio: false
        });
        video.srcObject = stream;
        
        video.onloadedmetadata = () => {
            statusDiv.textContent = 'دوربین فعال شد. پردازش آغاز...';
            // تنظیم اندازه کانواس برای پردازش سبک (64x48 پیکسل)
            canvas.width = 64; 
            canvas.height = 48;
            detectMotion();
        };
    } catch (err) {
        console.error(err);
        statusDiv.textContent = 'خطا در دسترسی به دوربین: ' + err.message;
    }
}

document.getElementById('switch-camera').addEventListener('click', () => {
    facingMode = facingMode === 'environment' ? 'user' : 'environment';
    startCamera();
});

function detectMotion() {
    if (video.paused || video.ended) return;

    // رسم فریم فعلی روی کانواس کوچک
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    
    const frame = ctx.getImageData(0, 0, canvas.width, canvas.height);
    const data = frame.data;
    const length = data.length;
    
    let diffScore = 0;

    if (previousFrameData) {
        for (let i = 0; i < length; i += 4) {
            // محاسبه تفاوت روشنایی (Grayscale)
            const rDiff = Math.abs(data[i] - previousFrameData[i]);
            const gDiff = Math.abs(data[i+1] - previousFrameData[i+1]);
            const bDiff = Math.abs(data[i+2] - previousFrameData[i+2]);
            
            // اگر تغییر پیکسل قابل توجه بود (بیش از 30 واحد)
            if (rDiff + gDiff + bDiff > 60) {
                diffScore++;
            }
        }
    }

    // ذخیره فریم فعلی برای دور بعد
    // کپی کردن آرایه دیتا بسیار مهم است
    previousFrameData = new Uint8ClampedArray(data);

    // محاسبه درصد حرکت نسبت به کل پیکسل‌ها
    // تعداد کل پیکسل‌ها = width * height
    const totalPixels = canvas.width * canvas.height;
    const motionPercent = (diffScore / totalPixels) * 100;

    // به‌روزرسانی نوار سبز
    // برای نمایش بهتر، عدد را کمی بزرگنمایی می‌کنیم (ضربدر 5) تا حرکات کوچک هم دیده شوند
    const displayMotion = Math.min(motionPercent * 5, 100); 
    motionBar.style.width = displayMotion + '%';

    // آستانه فعلی بر اساس اسلایدر
    // حساسیت 100 => آستانه نزدیک 0
    // فرمول آستانه باید با مکان مارکر قرمز هماهنگ باشد
    const currentThreshold = parseFloat(thresholdMarker.style.left); 

    // بررسی عبور از خط قرمز
    if (displayMotion > currentThreshold) {
        // حرکت تشخیص داده شد!
        cameraContainer.style.border = "5px solid red";
        statusDiv.textContent = "⚠️ حرکت تشخیص داده شد!";
        statusDiv.style.color = "red";
    } else {
        // وضعیت عادی
        cameraContainer.style.border = "none";
        statusDiv.textContent = "در حال نظارت...";
        statusDiv.style.color = "#888";
    }

    requestAnimationFrame(detectMotion);
}

// شروع برنامه
startCamera();
"""
    with open(js_path, "w", encoding="utf-8") as f:
        f.write(js_content)

    print("✅ فایل app.js اصلاح شد: منطق قرمز شدن صفحه اکنون با نوار سبز هماهنگ است.")

if __name__ == "__main__":
    fix_red_border_logic()
