import os

def fix_mobile_layout():
    html_path = "tools/doorbin-tashkhis-harekat/index.html"
    
    html_content = """
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>دوربین تشخیص حرکت دقیق</title>
    <style>
        * { box-sizing: border-box; }

        body { 
            margin: 0; 
            padding: 0;
            background: #000; 
            color: white; 
            font-family: system-ui, -apple-system, sans-serif;
            overflow: hidden; /* جلوگیری از اسکرول صفحه */
            display: flex;
            flex-direction: column;
            /* استفاده از dvh برای حل مشکل نوار آدرس سافاری در آیفون */
            height: 100dvh; 
        }
        
        /* کانتینر دوربین: مهمترین بخش */
        #camera-container {
            position: relative;
            flex: 1; /* تمام فضای خالی را پر کن */
            min-height: 0; /* حیاتی: اجازه می‌دهد ویدیو در صورت کمبود جا کوچک شود */
            display: flex;
            justify-content: center;
            align-items: center;
            background: #111;
            overflow: hidden;
        }
        
        video {
            width: 100%;
            height: 100%;
            object-fit: contain; /* حفظ نسبت تصویر بدون دفرمه شدن */
        }

        canvas { display: none; }

        /* بخش کنترل‌ها: فشرده و همیشه در دسترس */
        #controls {
            flex-shrink: 0; /* جلوگیری از جمع شدن کنترل‌ها */
            padding: 10px 15px;
            background: #1a1a1a;
            border-top: 1px solid #333;
            display: flex;
            flex-direction: column;
            gap: 8px;
            /* اطمینان از دیده شدن در آیفون‌های بدون دکمه */
            padding-bottom: env(safe-area-inset-bottom, 10px);
            z-index: 10;
        }

        /* استایل نوار و خط‌کش */
        .meter-wrapper {
            position: relative;
            margin-bottom: 2px;
        }

        #motion-bar-container {
            width: 100%;
            height: 12px;
            background: #333;
            position: relative;
            direction: ltr;
            border: 1px solid #555;
            border-radius: 2px;
        }

        #motion-bar {
            height: 100%;
            background: #00ff00;
            width: 0%;
        }

        #threshold-marker {
            position: absolute;
            top: 0;
            bottom: 0;
            width: 2px;
            background: red;
            left: 0%;
            z-index: 5;
            transform: translateX(-50%);
            box-shadow: 0 0 4px red;
        }

        #ruler {
            display: flex;
            justify-content: space-between;
            direction: ltr;
            font-size: 9px;
            color: #777;
            margin-top: 2px;
        }

        /* ردیف اطلاعات و اسلایدر کنار هم */
        .info-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 12px;
            background: #000;
            padding: 5px 8px;
            border-radius: 4px;
            border: 1px solid #333;
        }

        .slider-container {
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 12px;
        }
        
        input[type=range] {
            flex-grow: 1;
            height: 25px; /* کمی کوتاه‌تر */
            direction: ltr;
        }

        button {
            padding: 10px;
            border-radius: 6px;
            border: 1px solid #444;
            background: #333;
            color: white;
            font-size: 14px;
            width: 100%;
            cursor: pointer;
        }
        button:active { background: #555; }

    </style>
</head>
<body>

    <div id="camera-container">
        <video id="video" autoplay playsinline muted></video>
        <canvas id="output"></canvas>
    </div>

    <div id="controls">
        <!-- نوار حرکت -->
        <div class="meter-wrapper">
            <div id="motion-bar-container">
                <div id="motion-bar"></div>
                <div id="threshold-marker"></div>
            </div>
            <div id="ruler">
                <span>0</span><span>20</span><span>40</span><span>60</span><span>80</span><span>100</span>
            </div>
        </div>

        <!-- نمایشگر اعداد -->
        <div class="info-row">
            <div>حرکت: <span id="motion-val-text" style="color: #0f0; font-weight:bold;">0</span></div>
            <div>آستانه: <span id="thresh-val-text" style="color: #f55; font-weight:bold;">50</span></div>
        </div>

        <!-- اسلایدر -->
        <div class="slider-container">
            <span>حساسیت:</span>
            <input type="range" id="sensitivity-slider" min="0" max="100" value="50" step="1">
        </div>

        <button id="switch-camera">🔄 چرخش دوربین</button>
    </div>

    <script src="app.js"></script>
</body>
</html>
"""

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print("✅ فایل index.html آپدیت شد. مشکل بیرون زدن کنترل‌ها در موبایل حل شد.")

if __name__ == "__main__":
    fix_mobile_layout()
