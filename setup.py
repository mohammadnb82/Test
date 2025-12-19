import os

def apply_precision_mode():
    tool_dir = "tools/doorbin-tashkhis-harekat"
    html_path = os.path.join(tool_dir, "index.html")
    js_path = os.path.join(tool_dir, "app.js")

    # 1. HTML & CSS: اضافه کردن خط‌کش مدرج و حذف انیمیشن
    html_content = """
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>دوربین تشخیص حرکت دقیق</title>
    <style>
        body { 
            margin: 0; 
            background: #000; 
            color: white; 
            font-family: monospace; /* فونت منو-اسپیس برای خوانایی اعداد */
            overflow: hidden;
            display: flex;
            flex-direction: column;
            height: 100vh;
        }
        
        #camera-container {
            position: relative;
            flex-grow: 1;
            display: flex;
            justify-content: center;
            align-items: center;
            background: #111;
            box-sizing: border-box; /* برای محاسبه دقیق بردر */
        }
        
        video {
            width: 100%;
            height: 100%;
            object-fit: contain;
        }

        canvas {
            display: none; /* کانواس پردازشی دیده نشود */
        }

        #controls {
            padding: 10px 15px;
            background: #222;
            border-top: 2px solid #444;
            display: flex;
            flex-direction: column;
            gap: 5px;
        }

        /* ناحیه نوار و خط‌کش */
        .meter-wrapper {
            position: relative;
            margin-bottom: 5px;
            padding-top: 5px;
        }

        #motion-bar-container {
            width: 100%;
            height: 15px; /* کمی ضخیم‌تر */
            background: #333;
            position: relative;
            direction: ltr; /* جهت چپ به راست */
            border: 1px solid #555;
        }

        #motion-bar {
            height: 100%;
            background: #00ff00;
            width: 0%;
            /* transition حذف شد تا لگ نداشته باشد */
        }

        #threshold-marker {
            position: absolute;
            top: 0;
            bottom: 0;
            width: 2px;
            background: red;
            left: 0%;
            z-index: 5;
            transform: translateX(-50%); /* مرکز کردن خط روی عدد دقیق */
            box-shadow: 0 0 4px red;
        }

        /* خط‌کش اعداد */
        #ruler {
            display: flex;
            justify-content: space-between;
            direction: ltr;
            font-size: 10px;
            color: #aaa;
            margin-top: 2px;
            padding: 0 2px; /* برای تراز شدن با لبه‌ها */
        }

        .slider-row {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-top: 5px;
        }
        
        input[type=range] {
            flex-grow: 1;
            height: 30px;
            direction: ltr;
            cursor: pointer;
        }

        #debug-info {
            text-align: center;
            font-size: 14px;
            margin-top: 5px;
            padding: 5px;
            background: #000;
            border-radius: 4px;
            border: 1px solid #333;
        }

        button {
            padding: 8px 15px;
            border-radius: 5px;
            border: 1px solid #555;
            background: #333;
            color: white;
            margin: 0 auto;
            display: block;
            margin-top: 5px;
        }
    </style>
</head>
<body>

    <div id="camera-container">
        <video id="video" autoplay playsinline muted></video>
        <canvas id="output"></canvas>
    </div>

    <div id="controls">
        <!-- نوار حرکت و خط قرمز -->
        <div class="meter-wrapper">
            <div id="motion-bar-container">
                <div id="motion-bar"></div>
                <div id="threshold-marker"></div>
            </div>
            <!-- اعداد راهنما -->
            <div id="ruler">
                <span>0</span>
                <span>20</span>
                <span>40</span>
                <span>60</span>
                <span>80</span>
                <span>100</span>
            </div>
        </div>

        <!-- نمایشگر دقیق اعداد -->
        <div id="debug-info">
            حرکت: <span id="motion-val-text" style="color: #0f0; font-weight:bold;">0</span> | 
            حد آستانه: <span id="thresh-val-text" style="color: #f55; font-weight:bold;">50</span>
        </div>

        <!-- اسلایدر کنترل -->
        <div class="slider-row">
            <span>تنظیم حد مجاز:</span>
            <input type="range" id="sensitivity-slider" min="0" max="100" value="50" step="1">
        </div>

        <button id="switch-camera">🔄 چرخش دوربین</button>
    </div>

    <script src="app.js"></script>
</body>
</html>
"""

    # 2. JavaScript: منطق همگام‌سازی شده و خطی
    js_content = """
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
"""

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    with open(js_path, "w", encoding="utf-8") as f:
        f.write(js_content)

    print("✅ اصلاحات انجام شد:\n1. خط‌کش مدرج (0-100) اضافه شد.\n2. انیمیشن تاخیری حذف شد.\n3. نمایش عددی دقیق برای مقایسه اضافه شد.")

if __name__ == "__main__":
    apply_precision_mode()
