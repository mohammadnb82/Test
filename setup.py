import os
import sys
import urllib.request
import shutil
from pathlib import Path

# ==========================================
# تنظیمات مسیرها
# ==========================================
PROJECT_ROOT = Path(os.getcwd())

class ClientSideAIBuilder:
    def __init__(self):
        self.base_path = PROJECT_ROOT
        print(f"🚀 شروع ساخت سیستم هوشمند سمت کاربر (Client-Side AI)...")

    def ensure_tools_folder(self):
        """ساخت پوشه tools طبق درخواست قدیمی"""
        folder_name = "tools"
        keep_file = ".keep"
        
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        
        with open(os.path.join(folder_name, keep_file), 'w') as f:
            pass
        print("✅ پوشه tools بررسی شد.")

    def create_directory_structure(self):
        """ایجاد ساختار پوشه‌ها برای سایت استاتیک"""
        print("📁 ایجاد ساختار پوشه‌ها...")
        dirs = [
            "assets/css",
            "assets/js/libs",  # محل ذخیره کتابخانه‌های دانلود شده
            "assets/models",   # محل ذخیره مدل‌های هوش مصنوعی
            "assets/img"
        ]
        for d in dirs:
            (self.base_path / d).mkdir(parents=True, exist_ok=True)

    def download_resources(self):
        """دانلود کتابخانه‌های JS و مدل‌های هوش مصنوعی"""
        print("⬇️ در حال دانلود منابع و مدل‌ها (این مرحله مهم است)...")
        
        resources = [
            # 1. کتابخانه تشخیص چهره (face-api.js)
            {
                "url": "https://raw.githubusercontent.com/justadudewhohacks/face-api.js/master/dist/face-api.min.js",
                "dest": "assets/js/libs/face-api.min.js"
            },
            # 2. مدل‌های تشخیص چهره (Tiny Face Detector - سبک برای موبایل)
            {
                "url": "https://raw.githubusercontent.com/justadudewhohacks/face-api.js/master/weights/tiny_face_detector_model-shard1",
                "dest": "assets/models/tiny_face_detector_model-shard1"
            },
            {
                "url": "https://raw.githubusercontent.com/justadudewhohacks/face-api.js/master/weights/tiny_face_detector_model-weights_manifest.json",
                "dest": "assets/models/tiny_face_detector_model-weights_manifest.json"
            },
             {
                "url": "https://raw.githubusercontent.com/justadudewhohacks/face-api.js/master/weights/face_landmark_68_model-shard1",
                "dest": "assets/models/face_landmark_68_model-shard1"
            },
            {
                "url": "https://raw.githubusercontent.com/justadudewhohacks/face-api.js/master/weights/face_landmark_68_model-weights_manifest.json",
                "dest": "assets/models/face_landmark_68_model-weights_manifest.json"
            }
        ]

        for res in resources:
            dest_path = self.base_path / res["dest"]
            if not dest_path.exists():
                print(f"   ⏳ دانلود: {Path(res['dest']).name} ...")
                try:
                    # استفاده از User-Agent برای جلوگیری از خطای 403
                    req = urllib.request.Request(
                        res["url"], 
                        headers={'User-Agent': 'Mozilla/5.0'}
                    )
                    with urllib.request.urlopen(req) as response, open(dest_path, 'wb') as out_file:
                        shutil.copyfileobj(response, out_file)
                except Exception as e:
                    print(f"   ⚠️ خطا در دانلود {res['dest']}: {e}")
            else:
                print(f"   ✅ فایل موجود است: {Path(res['dest']).name}")

    def create_html_files(self):
        print("🎨 ایجاد فایل‌های HTML...")

        # ---------------------------------------------------------
        # 1. فایل اصلی (INDEX.HTML)
        # ---------------------------------------------------------
        index_html = """<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>هوش مصنوعی موبایل - بدون سرور</title>
    <link rel="stylesheet" href="assets/css/style.css">
</head>
<body>
    <div class="container">
        <header>
            <h1>🔮 استودیو هوشمند وب</h1>
            <p>اجرای کامل روی موبایل شما (بدون ارسال به سرور)</p>
        </header>

        <div class="card-grid">
            <div class="card">
                <div class="icon">👤</div>
                <h2>تشخیص چهره</h2>
                <p>تشخیص صورت و نقاط کلیدی مستقیماً در مرورگر.</p>
                <a href="face.html" class="btn btn-primary">شروع ابزار چهره</a>
            </div>
            
            <div class="card">
                <div class="icon">🎵</div>
                <h2>پردازش صدا</h2>
                <p>افزایش باس و شفافیت صدا با Web Audio API.</p>
                <a href="audio.html" class="btn btn-secondary">شروع ابزار صدا</a>
            </div>
        </div>
        
        <footer>
            <p>نسخه: Client-Side v2.0 | طراحی شده برای سایت Test</p>
        </footer>
    </div>
</body>
</html>"""
        (self.base_path / "index.html").write_text(index_html, encoding='utf-8')

        # ---------------------------------------------------------
        # 2. صفحه تشخیص چهره (FACE.HTML)
        # ---------------------------------------------------------
        face_html = """<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>تشخیص چهره</title>
    <link rel="stylesheet" href="assets/css/style.css">
    <script src="assets/js/libs/face-api.min.js"></script>
    <style>
        #container { position: relative; margin: 0 auto; max-width: 100%; }
        #imageUpload { display: none; }
        canvas { position: absolute; top: 0; left: 0; }
        img { max-width: 100%; display: block; border-radius: 10px; }
        .loading { color: #f39c12; font-weight: bold; display: none; margin: 10px 0; }
    </style>
</head>
<body>
    <div class="container">
        <a href="index.html" class="back-link">بازگشت به خانه</a>
        <div class="card">
            <h2>👤 اسکنر چهره (TensorFlow JS)</h2>
            <div id="status" class="loading">⏳ در حال لود مدل‌های هوش مصنوعی...</div>
            
            <div class="upload-box" onclick="document.getElementById('imageUpload').click()">
                📷 انتخاب یا گرفتن عکس
            </div>
            <input type="file" id="imageUpload" accept="image/*">
            
            <div id="container">
                <img id="inputImage" src="" alt="" style="display:none;">
            </div>
        </div>
    </div>

    <script>
        const status = document.getElementById('status');
        const imageUpload = document.getElementById('imageUpload');
        const container = document.getElementById('container');
        const inputImage = document.getElementById('inputImage');
        let canvas;

        // بارگذاری مدل‌ها از پوشه assets/models سایت خودتان
        async function loadModels() {
            status.style.display = 'block';
            status.innerHTML = '⏳ در حال بارگذاری مدل‌ها از سایت...';
            try {
                // آدرس نسبی به پوشه مدل‌ها
                const modelPath = './assets/models'; 
                await faceapi.nets.tinyFaceDetector.loadFromUri(modelPath);
                await faceapi.nets.faceLandmark68Net.loadFromUri(modelPath);
                status.innerHTML = '✅ هوش مصنوعی آماده است! عکس را انتخاب کنید.';
                status.style.color = 'green';
            } catch (err) {
                status.innerHTML = '❌ خطا در بارگذاری مدل‌ها: ' + err;
                console.error(err);
            }
        }

        imageUpload.addEventListener('change', async () => {
            if (canvas) canvas.remove();
            const file = imageUpload.files[0];
            const imgUrl = URL.createObjectURL(file);
            inputImage.src = imgUrl;
            inputImage.style.display = 'block';

            // پردازش تصویر
            status.innerHTML = '🔍 در حال اسکن چهره...';
            status.style.display = 'block';

            // صبر می‌کنیم تصویر لود شود
            inputImage.onload = async () => {
                const displaySize = { width: inputImage.width, height: inputImage.height };
                
                // ایجاد بوم نقاشی روی تصویر
                canvas = faceapi.createCanvasFromMedia(inputImage);
                container.append(canvas);
                faceapi.matchDimensions(canvas, displaySize);

                // تشخیص چهره‌ها
                const detections = await faceapi.detectAllFaces(inputImage, new faceapi.TinyFaceDetectorOptions()).withFaceLandmarks();
                const resizedDetections = faceapi.resizeResults(detections, displaySize);

                // رسم کادر و نقاط
                faceapi.draw.drawDetections(canvas, resizedDetections);
                faceapi.draw.drawFaceLandmarks(canvas, resizedDetections);
                
                status.innerHTML = `✅ انجام شد: ${detections.length} چهره پیدا شد.`;
            };
        });

        loadModels();
    </script>
</body>
</html>"""
        (self.base_path / "face.html").write_text(face_html, encoding='utf-8')

        # ---------------------------------------------------------
        # 3. صفحه پردازش صدا (AUDIO.HTML)
        # ---------------------------------------------------------
        audio_html = """<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>پردازش صدا</title>
    <link rel="stylesheet" href="assets/css/style.css">
</head>
<body>
    <div class="container">
        <a href="index.html" class="back-link">بازگشت به خانه</a>
        <div class="card">
            <h2>🎵 استودیو صدا (Web Audio API)</h2>
            <p>فایل صوتی انتخاب کنید و افکت‌های زنده اعمال کنید.</p>
            
            <div class="upload-box" onclick="document.getElementById('audioInput').click()">
                📂 انتخاب فایل صوتی
            </div>
            <input type="file" id="audioInput" accept="audio/*" style="display:none">
            
            <audio id="audioPlayer" controls style="width:100%; margin: 20px 0; display:none"></audio>
            
            <div class="controls" id="eqControls" style="display:none;">
                <label>باس (Bass): <span id="bassVal">0</span></label>
                <input type="range" id="bassRange" min="-10" max="10" value="0">
                
                <label>تیربل (Treble): <span id="trebleVal">0</span></label>
                <input type="range" id="trebleRange" min="-10" max="10" value="0">
                
                <label>حجم صدا (Volume)</label>
                <input type="range" id="volRange" min="0" max="2" step="0.1" value="1">
            </div>
        </div>
    </div>

    <script>
        const audioInput = document.getElementById('audioInput');
        const audioPlayer = document.getElementById('audioPlayer');
        const eqControls = document.getElementById('eqControls');
        
        let audioContext;
        let source;
        let bassFilter, trebleFilter, gainNode;

        audioInput.addEventListener('change', function() {
            const file = this.files[0];
            const url = URL.createObjectURL(file);
            audioPlayer.src = url;
            audioPlayer.style.display = 'block';
            eqControls.style.display = 'block';
            
            initAudioContext();
        });

        function initAudioContext() {
            if(!audioContext) {
                audioContext = new (window.AudioContext || window.webkitAudioContext)();
                
                // ایجاد سورس مدیا
                source = audioContext.createMediaElementSource(audioPlayer);
                
                // فیلتر باس (Low Shelf)
                bassFilter = audioContext.createBiquadFilter();
                bassFilter.type = "lowshelf";
                bassFilter.frequency.value = 200; // فرکانس‌های زیر 200 هرتز
                
                // فیلتر تریبل (High Shelf)
                trebleFilter = audioContext.createBiquadFilter();
                trebleFilter.type = "highshelf";
                trebleFilter.frequency.value = 2000; // فرکانس‌های بالای 2000 هرتز
                
                // ولوم
                gainNode = audioContext.createGain();
                
                // اتصال گره‌ها: Source -> Bass -> Treble -> Volume -> Output
                source.connect(bassFilter);
                bassFilter.connect(trebleFilter);
                trebleFilter.connect(gainNode);
                gainNode.connect(audioContext.destination);
            }
        }

        // کنترلر باس
        document.getElementById('bassRange').addEventListener('input', function() {
            if(bassFilter) bassFilter.gain.value = this.value;
            document.getElementById('bassVal').innerText = this.value;
        });

        // کنترلر تریبل
        document.getElementById('trebleRange').addEventListener('input', function() {
            if(trebleFilter) trebleFilter.gain.value = this.value;
            document.getElementById('trebleVal').innerText = this.value;
        });
        
        // کنترلر ولوم
        document.getElementById('volRange').addEventListener('input', function() {
            if(gainNode) gainNode.gain.value = this.value;
        });
        
        // حل مشکل AutoPlay Policy در مرورگرها
        audioPlayer.addEventListener('play', () => {
            if(audioContext && audioContext.state === 'suspended') {
                audioContext.resume();
            }
        });
    </script>
</body>
</html>"""
        (self.base_path / "audio.html").write_text(audio_html, encoding='utf-8')

    def create_css(self):
        print("🎨 ایجاد فایل استایل CSS...")
        css_content = """
@import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;500;700&display=swap');

:root {
    --primary: #4e54c8;
    --secondary: #8f94fb;
    --bg: #f0f2f5;
    --card-bg: #ffffff;
    --text: #333;
}

* { box-sizing: border-box; }
body {
    font-family: 'Vazirmatn', Tahoma, sans-serif;
    background: var(--bg);
    color: var(--text);
    margin: 0;
    padding: 20px;
    direction: rtl;
    text-align: right;
}

.container { max-width: 600px; margin: 0 auto; }

header { text-align: center; margin-bottom: 30px; }
h1 { color: var(--primary); margin-bottom: 5px; }
p { color: #666; font-size: 0.9rem; }

.card-grid { display: grid; gap: 20px; }

.card {
    background: var(--card-bg);
    border-radius: 20px;
    padding: 25px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.05);
    text-align: center;
    transition: transform 0.2s;
}

.card:hover { transform: translateY(-5px); }

.icon { font-size: 3rem; margin-bottom: 15px; }

.btn {
    display: inline-block;
    padding: 12px 30px;
    border-radius: 50px;
    text-decoration: none;
    color: white;
    font-weight: bold;
    margin-top: 15px;
    width: 100%;
    transition: opacity 0.3s;
}
.btn-primary { background: linear-gradient(45deg, #4e54c8, #8f94fb); }
.btn-secondary { background: linear-gradient(45deg, #11998e, #38ef7d); }
.btn:hover { opacity: 0.9; }

.upload-box {
    border: 2px dashed #cbd5e0;
    padding: 30px;
    border-radius: 15px;
    color: #718096;
    cursor: pointer;
    margin: 20px 0;
    background: #f7fafc;
}
.upload-box:hover { border-color: var(--primary); color: var(--primary); }

input[type=range] { width: 100%; margin: 10px 0 20px; }
.back-link { display: inline-block; margin-bottom: 20px; text-decoration: none; color: #666; }
"""
        (self.base_path / "assets" / "css" / "style.css").write_text(css_content, encoding='utf-8')

    def run(self):
        self.ensure_tools_folder()
        self.create_directory_structure()
        self.download_resources()
        self.create_css()
        self.create_html_files()
        print("\n✅ تمام فایل‌ها آماده شد!")
        print("🚀 این سایت کاملاً استاتیک است و روی موبایل به خوبی کار می‌کند.")

if __name__ == "__main__":
    builder = ClientSideAIBuilder()
    builder.run()
