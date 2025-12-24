import os
import subprocess

# ===================================================================
# ۱. محتوای پروژه دوربین نگهبان (نسخه پایه اولیه)
# ===================================================================

GUARD_CAM_SERVER_CONTENT = """
from flask import Flask, send_from_directory
import os

app = Flask(__name__)

GUARD_CAM_PATH = 'tools/guard_camera'
os.makedirs(GUARD_CAM_PATH, exist_ok=True)

@app.route('/')
def index():
    return send_from_directory(GUARD_CAM_PATH, 'index.html')

if __name__ == '__main__':
    print("--- اجرای پروژه دوربین نگهبان (نسخه پایه) ---")
    # توجه: برای اجرای کامل، نیاز به بارگذاری مدل‌های TF.js در assets/ است.
    app.run(debug=True, port=5000)
"""

GUARD_CAM_HTML_CONTENT = """
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>دوربین نگهبان (پایه)</title>
    <style>
        body { font-family: Tahoma; text-align: center; padding-top: 50px; }
        #videoFeed { border: 1px solid black; width: 640px; height: 480px; margin: 20px auto; display: block; }
        .controls button { padding: 10px 20px; margin: 5px; cursor: pointer; }
        #alarmStatus { font-weight: bold; color: green; }
    </style>
</head>
<body>
    <h1>دوربین نگهبان (فریم اولیه)</h1>
    <video id="videoFeed" autoplay muted></video>
    
    <div class="controls">
        <button onclick="switchCamera()">تغییر دوربین</button>
        <button onclick="toggleAlarm()">کنترل آژیر</button>
        <span id="alarmStatus">آژیر: خاموش</span>
    </div>

    <script>
        let stream;
        let currentDeviceId = null;

        async function startStream(deviceId = null) {
            try {
                const constraints = { video: { deviceId: deviceId ? { exact: deviceId } : true } };
                stream = await navigator.mediaDevices.getUserMedia(constraints);
                const video = document.getElementById('videoFeed');
                video.srcObject = stream;
                
                // دریافت لیست دستگاه‌ها برای سوییچینگ
                const devices = await navigator.mediaDevices.enumerateDevices();
                const videoDevices = devices.filter(device => device.kind === 'videoinput');
                
                if (videoDevices.length > 0 && !currentDeviceId) {
                    // تنظیم دوربین پیش‌فرض برای اولین بار
                    currentDeviceId = videoDevices[0].deviceId;
                }

            } catch (err) {
                console.error("خطا در دسترسی به دوربین:", err);
                alert("اجازه دسترسی به دوربین داده نشده است یا دوربینی یافت نشد.");
            }
        }

        async function switchCamera() {
            if (!stream) return;
            stream.getTracks().forEach(track => track.stop());
            
            const devices = await navigator.mediaDevices.enumerateDevices();
            const videoDevices = devices.filter(device => device.kind === 'videoinput');
            
            if (videoDevices.length > 1) {
                const currentIndex = videoDevices.findIndex(d => d.deviceId === currentDeviceId);
                const nextIndex = (currentIndex + 1) % videoDevices.length;
                currentDeviceId = videoDevices[nextIndex].deviceId;
                startStream(currentDeviceId);
            } else {
                alert("فقط یک دوربین در دسترس است.");
            }
        }

        let isAlarmOn = false;
        function toggleAlarm() {
            isAlarmOn = !isAlarmOn;
            const statusSpan = document.getElementById('alarmStatus');
            statusSpan.innerText = isAlarmOn ? "آژیر: فعال" : "آژیر: خاموش";
            statusSpan.style.color = isAlarmOn ? 'red' : 'green';
            // در نسخه نهایی، این بخش منطق تشخیص چهره را فعال/غیرفعال می‌کرد.
        }

        window.onload = () => {
            startStream();
        };
    </script>
</body>
</html>
"""

# ===================================================================
# ۲. محتوای پروژه تولید محتوای هوشمند (نسخه نهایی)
# ===================================================================

CONTENT_CURATOR_SERVER_CONTENT = """
from flask import Flask, send_from_directory
import os

app = Flask(__name__)

CONTENT_APP_PATH = 'tools/content_curator'
os.makedirs(CONTENT_APP_PATH, exist_ok=True)

@app.route('/')
def index():
    return send_from_directory(CONTENT_APP_PATH, 'index.html')

@app.route('/<path:path>')
def send_static(path):
    return send_from_directory(CONTENT_APP_PATH, path)

if __name__ == '__main__':
    print("--- اجرای پروژه تولید محتوای هوشمند ---")
    # اجرای روی پورت 5001 برای جلوگیری از تداخل
    app.run(debug=True, port=5001)
"""

CONTENT_CURATOR_HTML_CONTENT = """
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>حلقه‌ساز - تولید کننده محتوای هوشمند</title>
    <style>
        body { font-family: Tahoma, sans-serif; background-color: #f4f7f9; color: #333; display: flex; justify-content: center; padding: 20px; }
        .container { background: #ffffff; padding: 30px; border-radius: 12px; box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1); max-width: 800px; width: 100%; }
        h1 { color: #007bff; text-align: center; margin-bottom: 25px; }
        #keywordsInput { width: 100%; padding: 12px; margin-bottom: 15px; border: 1px solid #ccc; border-radius: 6px; box-sizing: border-box; font-size: 16px; }
        .buttons { display: flex; gap: 10px; margin-bottom: 20px; }
        button { padding: 10px 20px; border: none; border-radius: 6px; cursor: pointer; font-size: 16px; transition: background-color 0.3s; flex-grow: 1; }
        #generateBtn { background-color: #007bff; color: white; }
        #generateBtn:hover { background-color: #0056b3; }
        #regenerateBtn { background-color: #ffc107; color: #333; }
        #regenerateBtn:hover { background-color: #e0a800; }
        #output { margin-top: 25px; padding: 20px; border: 2px dashed #ccc; min-height: 100px; white-space: pre-wrap; line-height: 1.8; border-radius: 6px; font-size: 1.1em; }
        .highlight { font-weight: bold; color: #28a745; }
        #status { text-align: center; color: #6c757d; margin-bottom: 15px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>تولید کننده محتوای الگو-محور</h1>
        <p id="status">آماده به کار.</p>
        
        <input type="text" id="keywordsInput" placeholder="کلیدواژه‌ها را با کاما جدا کنید (مثال: انرژی خورشیدی, تکنولوژی, پایداری)">
        
        <div class="buttons">
            <button id="generateBtn">تولید محتوای جدید</button>
            <button id="regenerateBtn" disabled>تولید مجدد (با همین کلمات)</button>
        </div>

        <h3>محتوای تولید شده:</h3>
        <div id="output">خروجی شما در اینجا نمایش داده خواهد شد.</div>
    </div>

    <script>
        const Templates = [
            "امروزه، موضوع {KEYWORD1} به یکی از مباحث حیاتی در جهان تبدیل شده است. پیشرفت‌های اخیر در زمینه {KEYWORD2} نشان می‌دهد که آینده‌ای روشن پیش روی ماست.",
            "آیا می‌دانستید که ارتباط عمیقی بین {KEYWORD2} و {KEYWORD1} وجود دارد؟ متخصصان تاکید دارند که درک این رابطه کلید موفقیت است.",
            "برای غرق شدن در عمق موضوع {KEYWORD1}، ابتدا باید اصول اولیه {KEYWORD2} را فرا بگیریم. این دو مولفه مکمل یکدیگرند.",
            "تحلیلگران معتقدند که {KEYWORD1} نیروی محرکه‌ی نوآوری در بخش {KEYWORD2} خواهد بود. فرصت‌های سرمایه‌گذاری در این حوزه بسیار زیاد است.",
            "نقل قول روز: «مهم‌ترین درس درباره‌ی {KEYWORD1} این است که هرگز نباید {KEYWORD2} را دست کم گرفت.»",
            "چگونه می‌توانیم با استفاده از {KEYWORD1} به اهداف خود در زمینه {KEYWORD2} برسیم؟ این یک چالش مدیریتی پیچیده است.",
            "گزارش‌ها حاکی از آن است که {KEYWORD2} تأثیر مستقیمی بر رشد {KEYWORD1} دارد. این همبستگی باید بیشتر مورد مطالعه قرار گیرد."
        ];

        let lastKeywords = [];
        let lastTemplateIndex = -1;

        const statusElement = document.getElementById('status');
        const outputElement = document.getElementById('output');
        const keywordsInput = document.getElementById('keywordsInput');
        const generateBtn = document.getElementById('generateBtn');
        const regenerateBtn = document.getElementById('regenerateBtn');

        function updateStatus(message) {
            statusElement.innerText = message;
        }

        function applyFormatting(text, keywords) {
            let formattedText = text;
            const keywordSet = new Set(keywords.map(k => k.toLowerCase()).filter(k => k.length > 0));

            keywordSet.forEach(keyword => {
                const regex = new RegExp(`(${keyword})`, 'gi');
                formattedText = formattedText.replace(regex, '<span class="highlight">$1</span>');
            });
            
            return formattedText;
        }

        function generateContent(keywords, forceNewTemplate = false) {
            const sanitizedKeywords = keywords.map(k => k.trim()).filter(k => k.length > 0);
            
            if (sanitizedKeywords.length < 1) {
                return { formatted: "لطفاً حداقل یک کلیدواژه وارد کنید.", keywords: [] };
            }

            let templateIndex;
            if (forceNewTemplate && lastTemplateIndex !== -1) {
                do {
                    templateIndex = Math.floor(Math.random() * Templates.length);
                } while (templateIndex === lastTemplateIndex && Templates.length > 1);
            } else {
                templateIndex = Math.floor(Math.random() * Templates.length);
            }
            
            lastTemplateIndex = templateIndex;
            const template = Templates[templateIndex];
            
            let result = template;
            
            result = result.replace(/\{KEYWORD1\}/g, sanitizedKeywords[0]);
            const secondKeyword = sanitizedKeywords.length > 1 ? sanitizedKeywords[1] : sanitizedKeywords[0];
            result = result.replace(/\{KEYWORD2\}/g, secondKeyword);

            const formatted = applyFormatting(result, sanitizedKeywords);
            return { formatted, keywords };
        }

        function handleGeneration(forceNewTemplate = false) {
            const keywordsStr = keywordsInput.value;
            const keywordsArray = keywordsStr.split(',').map(k => k.trim());
            
            updateStatus("در حال پردازش و تولید محتوا...");
            
            const { formatted, keywords } = generateContent(keywordsArray, forceNewTemplate);
            
            outputElement.innerHTML = formatted;
            lastKeywords = keywords;

            if (keywords.length > 0) {
                regenerateBtn.disabled = false;
            } else {
                 regenerateBtn.disabled = true;
            }
            updateStatus(`تولید محتوا با ${keywords.length} کلیدواژه انجام شد.`);
        }

        generateBtn.onclick = () => handleGeneration(false);
        regenerateBtn.onclick = () => handleGeneration(true);
        
        window.onload = () => {
            // به صورت خودکار یک بار تولید را انجام می دهیم
            keywordsInput.value = "هوش مصنوعی, آینده";
            handleGeneration(false);
        };

    </script>
</body>
</html>
"""

# ===================================================================
# ۳. منطق اجرای ساختاردهی
# ===================================================================

BASE_DIR = 'tools'

PROJECTS = [
    {
        "name": "guard_camera",
        "base_path": os.path.join(BASE_DIR, "guard_camera"),
        "server_file": "server.py",
        "server_content": GUARD_CAM_SERVER_CONTENT,
        "index_file": "index.html",
        "index_content": GUARD_CAM_HTML_CONTENT
    },
    {
        "name": "content_curator",
        "base_path": os.path.join(BASE_DIR, "content_curator"),
        "server_file": "server.py",
        "server_content": CONTENT_CURATOR_SERVER_CONTENT,
        "index_file": "index.html",
        "index_content": CONTENT_CURATOR_HTML_CONTENT
    }
]

def create_files_and_directories():
    print("--- شروع فرآیند ساخت و استقرار پروژه‌ها ---")
    
    # ۱. اطمینان از وجود پوشه ابزارها
    os.makedirs(BASE_DIR, exist_ok=True)

    for project in PROJECTS:
        path = project["base_path"]
        print(f"\n[*] ساخت ساختار برای پروژه: {project['name']} در {path}")
        os.makedirs(path, exist_ok=True)

        # نوشتن فایل سرور (Flask)
        server_path = os.path.join(path, project["server_file"])
        with open(server_path, 'w', encoding='utf-8') as f:
            f.write(project["server_content"])
        print(f"  - فایل سرور ایجاد شد: {server_path}")

        # نوشتن فایل ایندکس (HTML/JS)
        index_path = os.path.join(path, project["index_file"])
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(project["index_content"])
        print(f"  - فایل رابط کاربری ایجاد شد: {index_path}")

    print("\n--- ساختاردهی کامل شد. ---")
    print("\nتوجه: برای اجرای پروژه‌ها، نیاز به نصب Flask دارید.")
    try:
        # اجرای دستور نصب Flask
        print("تلاش برای نصب Flask (اگر نصب نیست)...")
        subprocess.run(['pip', 'install', 'flask'], check=True)
        print("نصب Flask با موفقیت انجام شد.")
    except subprocess.CalledProcessError:
        print("خطا در نصب Flask. لطفاً آن را به صورت دستی نصب کنید (pip install flask).")
    except FileNotFoundError:
        print("دستور 'pip' یافت نشد. لطفاً مطمئن شوید که Python و pip در مسیر PATH شما هستند.")

    print("\nبرای اجرای پروژه 'دوربین نگهبان' (پورت 5000):")
    print(f"۱. به دایرکتوری {os.path.join(BASE_DIR, 'guard_camera')} بروید.")
    print("۲. اجرا کنید: python server.py")
    
    print("\nبرای اجرای پروژه 'تولید محتوا' (پورت 5001):")
    print(f"۱. به دایرکتوری {os.path.join(BASE_DIR, 'content_curator')} بروید.")
    print("۲. اجرا کنید: python server.py")


if __name__ == "__main__":
    create_files_and_directories()
