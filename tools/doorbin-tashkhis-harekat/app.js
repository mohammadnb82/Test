
const video = document.getElementById('video');
const canvas = document.getElementById('output');
const ctx = canvas.getContext('2d');
const motionBar = document.getElementById('motion-bar');
const thresholdMarker = document.getElementById('threshold-marker');
const slider = document.getElementById('sensitivity-slider');
const motionText = document.getElementById('motion-val-text');
const threshText = document.getElementById('thresh-val-text');
const container = document.getElementById('camera-container');
const debugInfo = document.getElementById('debug-info');

let stream = null;
let facingMode = 'environment';
let previousFrameData = null;

// ضریب حساسیت: این عدد باعث می‌شود تغییرات کم پیکسل، روی نوار ۰ تا ۱۰۰ دیده شوند.
// اگر محیط خیلی نویز دارد این عدد را کم کنید، اگر خیلی ساکن است زیاد کنید.
const AMPLIFICATION = 15; 

// 1. همگام‌سازی اولیه اسلایدر و مارکر قرمز
updateThreshold();

slider.addEventListener('input', updateThreshold);

function updateThreshold() {
    const val = parseInt(slider.value);
    // خط قرمز دقیقاً روی همان درصدی می‌رود که اسلایدر است
    thresholdMarker.style.left = val + '%';
    threshText.textContent = val;
}

async function startCamera() {
    if (stream) stream.getTracks().forEach(t => t.stop());
    
    try {
        stream = await navigator.mediaDevices.getUserMedia({
            video: { facingMode: facingMode, width: 320, height: 240 }, // رزولوشن پایین برای سرعت
            audio: false
        });
        video.srcObject = stream;
        video.onloadedmetadata = () => {
            canvas.width = 64; // پردازش روی تصویر کوچک
            canvas.height = 48; 
            detectMotion();
        };
    } catch (e) {
        alert("خطا در دوربین: " + e.message);
    }
}

document.getElementById('switch-camera').addEventListener('click', () => {
    facingMode = facingMode === 'environment' ? 'user' : 'environment';
    startCamera();
});

function detectMotion() {
    if (video.paused || video.ended) return;

    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    const frame = ctx.getImageData(0, 0, canvas.width, canvas.height);
    const data = frame.data;
    
    let changedPixels = 0;
    
    // الگوریتم مقایسه پیکسل
    if (previousFrameData) {
        for (let i = 0; i < data.length; i += 4) {
            // میانگین تفاوت RGB
            const diff = (Math.abs(data[i] - previousFrameData[i]) +
                          Math.abs(data[i+1] - previousFrameData[i+1]) +
                          Math.abs(data[i+2] - previousFrameData[i+2])) / 3;
            
            // اگر تغییر پیکسل بیشتر از 20 (نویز جزئی) بود
            if (diff > 20) {
                changedPixels++;
            }
        }
    }
    
    previousFrameData = new Uint8ClampedArray(data); // کپی فریم برای دور بعد

    // محاسبه درصد تغییرات
    const totalPixels = canvas.width * canvas.height;
    let rawPercent = (changedPixels / totalPixels) * 100;
    
    // تبدیل به مقیاس 0 تا 100 برای نمایش
    let displayValue = Math.floor(rawPercent * AMPLIFICATION);
    if (displayValue > 100) displayValue = 100;

    // --- بروزرسانی UI ---
    
    // 1. نوار سبز (دقیقا برابر عدد محاسبه شده)
    motionBar.style.width = displayValue + '%';
    motionText.textContent = displayValue;

    // 2. خواندن مقدار حد مجاز (از اسلایدر)
    const limit = parseInt(slider.value);

    // 3. شرط قرمز شدن
    if (displayValue >= limit) {
        container.style.border = "6px solid red";
        debugInfo.style.background = "#500"; // قرمز شدن پس‌زمینه اعداد
    } else {
        container.style.border = "none";
        debugInfo.style.background = "#000";
    }

    requestAnimationFrame(detectMotion);
}

startCamera();
