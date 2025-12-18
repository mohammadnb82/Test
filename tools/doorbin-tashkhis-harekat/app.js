
const video = document.getElementById('video');
const canvas = document.getElementById('output');
const ctx = canvas.getContext('2d');
const statusElement = document.getElementById('status');
const sensitivityInput = document.getElementById('sensitivity');
const sensValSpan = document.getElementById('sens-val');
const motionBar = document.getElementById('motion-bar');
const thresholdMarker = document.getElementById('threshold-marker');
const switchBtn = document.getElementById('switch-camera');

// تنظیمات
let facingMode = 'environment';
let width = 640;
let height = 480;

// متغیرهای تشخیص حرکت
let previousFrameData = null; // داده‌های پیکسل فریم قبل
let lastMotionTime = 0;
let motionThreshold = 50; // مقدار اولیه (برعکس اسلایدر: اسلایدر بالا = آستانه پایین)

// ۱. مدیریت اسلایدر حساسیت
sensitivityInput.addEventListener('input', (e) => {
    const val = e.target.value;
    sensValSpan.innerText = val + '%';
    
    // تبدیل حساسیت (0-100) به آستانه خطا (Threshold)
    // حساسیت ۱۰۰ یعنی کوچکترین تغییر (آستانه کم)
    // حساسیت ۰ یعنی تغییر بزرگ (آستانه زیاد)
    
    // فرمول معکوس:
    // حساسیت بالا (100) -> آستانه حدود 5
    // حساسیت پایین (0) -> آستانه حدود 1000
    // یک فرمول ساده:
    const maxThreshold = 200000; // عددی تجربی بر اساس تعداد پیکسل‌ها
    const inverted = 101 - val; // 1 تا 100
    // آستانه نهایی
    motionThreshold = (inverted * inverted) * 20; 
    
    // آپدیت مکان نشانگر قرمز
    // هرچه حساسیت بالاتر (اسلایدر راست)، نشانگر باید به چپ (راحت‌تر پر شود) برود؟
    // بیایید ساده کنیم: نوار سبز مقدار حرکت است.
    // نشانگر قرمز خطی است که اگر سبز از آن رد شود، حرکت ثبت می‌شود.
    // حساسیت بالا = خط قرمز سمت چپ (زود پر شود).
    // حساسیت پایین = خط قرمز سمت راست (دیر پر شود).
    
    const markerPosition = 100 - val; 
    thresholdMarker.style.left = markerPosition + '%';
});

// تریگر کردن رویداد اینپوت برای تنظیم اولیه
sensitivityInput.dispatchEvent(new Event('input'));


// ۲. روشن کردن دوربین
async function startCamera() {
    statusElement.innerText = 'دسترسی به دوربین...';
    
    const constraints = {
        audio: false,
        video: {
            facingMode: facingMode,
            width: { ideal: width },
            height: { ideal: height }
        }
    };

    try {
        const stream = await navigator.mediaDevices.getUserMedia(constraints);
        video.srcObject = stream;
        
        video.onloadedmetadata = () => {
            video.play();
            statusElement.innerText = '✅ تشخیص حرکت فعال';
            
            // تنظیم سایز کانواس (برای پردازش سبکتر، سایز کوچک استفاده می‌کنیم)
            // پردازش 640x480 سنگین است. برای حرکت، 64x48 کافیست.
            canvas.width = 64; 
            canvas.height = 48;
            
            // شروع لوپ پردازش
            processFrame();
        };

    } catch (err) {
        statusElement.innerText = '❌ خطا: ' + err.message;
        console.error(err);
    }
}

// ۳. پردازش فریم به فریم (تشخیص حرکت)
function processFrame() {
    if (video.paused || video.ended) return;

    // رسم ویدیو روی کانواس کوچک
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    
    // دریافت اطلاعات پیکسل‌ها
    const frameData = ctx.getImageData(0, 0, canvas.width, canvas.height);
    const data = frameData.data; // آرایه‌ای از [R, G, B, A, R, G, B, A, ...]
    
    if (previousFrameData) {
        let diffScore = 0;
        
        // مقایسه با فریم قبلی
        // گام ۴تایی برمی‌داریم (فقط پیکسل‌ها را می‌خوانیم، آلفا مهم نیست)
        for (let i = 0; i < data.length; i += 4) {
            const rDiff = Math.abs(data[i] - previousFrameData[i]);
            const gDiff = Math.abs(data[i+1] - previousFrameData[i+1]);
            const bDiff = Math.abs(data[i+2] - previousFrameData[i+2]);
            
            // اگر تغییر رنگ پیکسل زیاد بود، به امتیاز اضافه کن
            if (rDiff + gDiff + bDiff > 50) { // حد نویز رنگ
                diffScore++;
            }
        }
        
        // آپدیت نوار وضعیت (برای نمایش بصری به کاربر)
        // نرمال‌سازی اسکور برای نمایش در CSS (تقریبی)
        let visualPercent = Math.min(100, (diffScore / 500) * 100); 
        motionBar.style.width = visualPercent + '%';

        // بررسی آستانه
        if (diffScore > motionThreshold) {
            // حرکت تشخیص داده شد!
            motionDetected();
        } else {
            document.body.style.borderColor = 'black'; // حالت عادی
        }
    }

    // ذخیره فریم فعلی برای دور بعد
    // باید کپی بگیریم چون data رفرنس است
    previousFrameData = new Uint8ClampedArray(data);

    requestAnimationFrame(processFrame);
}

function motionDetected() {
    statusElement.innerText = '⚠️ حرکت تشخیص داده شد!';
    statusElement.style.color = 'red';
    
    // افکت فلش زدن بردر صفحه
    document.body.style.border = '5px solid red';
    
    // بازگشت متن بعد از ۱ ثانیه
    clearTimeout(window.resetTimer);
    window.resetTimer = setTimeout(() => {
        statusElement.innerText = 'در حال پایش...';
        statusElement.style.color = '#888';
        document.body.style.border = 'none';
    }, 200);
}

// سوییچ دوربین
switchBtn.addEventListener('click', () => {
    facingMode = facingMode === 'user' ? 'environment' : 'user';
    startCamera();
});

window.addEventListener('load', startCamera);
