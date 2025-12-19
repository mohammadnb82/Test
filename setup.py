import os

def fix_app_logic():
    js_path = "tools/doorbin-tashkhis-harekat/app.js"
    
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

// متغیرهای وضعیت
let currentFacingMode = 'environment';
let animationId = null;
let lastFrameData = null;

// اندازه پردازش (کم برای سرعت بالا)
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
            // تنظیم دقیق اندازه کانواس برای جلوگیری از کشیدگی
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

// حلقه تشخیص حرکت
function startDetection() {
    if (animationId) cancelAnimationFrame(animationId);

    function loop() {
        if (video.paused || video.ended) return;

        // 1. رسم فریم فعلی ویدیو روی کانواس کوچک
        ctx.drawImage(video, 0, 0, PROCESS_WIDTH, PROCESS_HEIGHT);
        
        // 2. دریافت داده‌های پیکسل
        const frameData = ctx.getImageData(0, 0, PROCESS_WIDTH, PROCESS_HEIGHT);
        const currentData = frameData.data;

        // 3. محاسبه تفاوت با فریم قبلی
        let movementScore = 0;

        if (lastFrameData) {
            let totalDiff = 0;
            const length = currentData.length; // 4 * width * height

            // پیمایش پیکسل‌ها (هر 4 مقدار: R, G, B, Alpha)
            // گام 4 تایی برای سرعت بیشتر (هر پیکسل را چک نکنیم)
            for (let i = 0; i < length; i += 16) { 
                // تفاوت رنگ قرمز
                const rDiff = Math.abs(currentData[i] - lastFrameData[i]);
                // تفاوت رنگ سبز
                const gDiff = Math.abs(currentData[i+1] - lastFrameData[i+1]);
                // تفاوت رنگ آبی
                const bDiff = Math.abs(currentData[i+2] - lastFrameData[i+2]);

                // اگر تفاوت رنگ‌ها زیاد بود، حرکت ثبت کن
                if (rDiff + gDiff + bDiff > 50) {
                    totalDiff++;
                }
            }

            // نرمال‌سازی نمره حرکت (بین 0 تا 100)
            // عدد 300 تجربی است و بر اساس تعداد پیکسل‌ها تنظیم شده
            movementScore = Math.min(100, Math.floor((totalDiff / (PROCESS_WIDTH * PROCESS_HEIGHT / 16)) * 300));
        }

        // ذخیره فریم فعلی برای مقایسه در دور بعد
        // کپی کردن آرایه بسیار مهم است
        lastFrameData = new Uint8ClampedArray(currentData);

        // 4. بروزرسانی رابط کاربری
        updateUI(movementScore);

        animationId = requestAnimationFrame(loop);
    }

    loop();
}

// بروزرسانی نوار و اعداد
function updateUI(score) {
    // بروزرسانی نوار سبز
    motionBar.style.width = score + '%';
    
    // بروزرسانی عدد حرکت
    motionValText.innerText = score;

    // بررسی آستانه
    const threshold = parseInt(sensitivitySlider.value);
    
    // منطق هشدار
    if (score > threshold) {
        document.body.style.boxShadow = "inset 0 0 50px red";
        document.body.style.border = "5px solid red";
    } else {
        document.body.style.boxShadow = "none";
        document.body.style.border = "none";
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

// شروع برنامه
setupCamera();
"""

    with open(js_path, "w", encoding="utf-8") as f:
        f.write(js_content)
    
    print("✅ فایل app.js اصلاح شد.")

if __name__ == "__main__":
    fix_app_logic()
