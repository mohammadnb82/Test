#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
modular_builder.py - سازنده ابزارهای مستقل
هر ابزار با تمام وابستگی‌هایش در پوشه جداگانه
"""

import os
import sys
import json
import subprocess
import urllib.request
import shutil
from pathlib import Path

class ModularToolsBuilder:
    """سازنده ابزارهای مستقل و جداگانه"""
    
    def __init__(self):
        self.root = Path.cwd()
        self.tools_dir = self.root / 'tools'
        
    def build_all(self):
        """ساخت کل پروژه"""
        print("=" * 60)
        print("🚀 شروع ساخت پروژه با معماری Modular")
        print("=" * 60)
        
        # 1. صفحه اصلی سایت
        self.create_main_page()
        
        # 2. ابزار تشخیص چهره
        self.build_face_recognition_tool()
        
        # 3. ابزار پردازش صدا
        self.build_audio_mastering_tool()
        
        print("\n" + "=" * 60)
        print("✅ پروژه با موفقیت ساخته شد!")
        print("=" * 60)
        print("\n📋 دستورالعمل اجرا:")
        print("1. برای اجرای ابزار تشخیص چهره:")
        print("   cd tools/face_recognition && pip install -r requirements.txt && python app.py")
        print("\n2. برای اجرای ابزار پردازش صدا:")
        print("   cd tools/audio_mastering && pip install -r requirements.txt && python app.py")
        print("\n3. یا اجرای همزمان از ریشه:")
        print("   python run_all_tools.py")
    
    def create_main_page(self):
        """ایجاد صفحه اصلی سایت"""
        print("\n📄 ایجاد صفحه اصلی...")
        
        # ساختار پوشه‌ها
        (self.root / 'static' / 'css').mkdir(parents=True, exist_ok=True)
        (self.root / 'static' / 'js').mkdir(parents=True, exist_ok=True)
        
        # HTML صفحه اصلی
        index_html = '''<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>استودیو هوش مصنوعی</title>
    <link rel="stylesheet" href="static/css/main.css">
</head>
<body>
    <div class="container">
        <header class="main-header">
            <h1>🤖 استودیو هوش مصنوعی</h1>
            <p class="subtitle">مجموعه ابزارهای پیشرفته پردازش تصویر و صدا</p>
        </header>

        <main class="tools-grid">
            <div class="tool-card">
                <div class="tool-icon">👤</div>
                <h2>تشخیص چهره</h2>
                <p>شناسایی و تحلیل چهره‌ها با دقت بالا</p>
                <ul class="features">
                    <li>✓ شناسایی چندین چهره</li>
                    <li>✓ مقایسه با پایگاه داده</li>
                    <li>✓ تشخیص احساسات</li>
                </ul>
                <a href="tools/face_recognition/index.html" class="btn-primary">ورود به ابزار</a>
            </div>

            <div class="tool-card">
                <div class="tool-icon">🎵</div>
                <h2>مستر کردن صدا</h2>
                <p>بهبود کیفیت صدا به صورت حرفه‌ای</p>
                <ul class="features">
                    <li>✓ حذف نویز هوشمند</li>
                    <li>✓ EQ خودکار</li>
                    <li>✓ نرمال‌سازی صدا</li>
                </ul>
                <a href="tools/audio_mastering/index.html" class="btn-primary">ورود به ابزار</a>
            </div>
        </main>

        <footer>
            <p>تمامی ابزارها به صورت مستقل قابل اجرا هستند</p>
        </footer>
    </div>
</body>
</html>'''
        
        # CSS صفحه اصلی
        main_css = '''* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 20px;
}

.container {
    max-width: 1200px;
    width: 100%;
}

.main-header {
    text-align: center;
    color: white;
    margin-bottom: 50px;
}

.main-header h1 {
    font-size: 3rem;
    margin-bottom: 10px;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
}

.subtitle {
    font-size: 1.2rem;
    opacity: 0.9;
}

.tools-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
    gap: 30px;
    margin-bottom: 40px;
}

.tool-card {
    background: white;
    border-radius: 20px;
    padding: 40px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.tool-card:hover {
    transform: translateY(-10px);
    box-shadow: 0 15px 40px rgba(0,0,0,0.3);
}

.tool-icon {
    font-size: 4rem;
    text-align: center;
    margin-bottom: 20px;
}

.tool-card h2 {
    color: #667eea;
    font-size: 1.8rem;
    margin-bottom: 15px;
    text-align: center;
}

.tool-card p {
    color: #666;
    text-align: center;
    margin-bottom: 20px;
    line-height: 1.6;
}

.features {
    list-style: none;
    margin-bottom: 30px;
}

.features li {
    padding: 8px 0;
    color: #444;
    font-size: 0.95rem;
}

.btn-primary {
    display: block;
    width: 100%;
    padding: 15px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    text-align: center;
    text-decoration: none;
    border-radius: 10px;
    font-weight: bold;
    font-size: 1.1rem;
    transition: opacity 0.3s ease;
}

.btn-primary:hover {
    opacity: 0.9;
}

footer {
    text-align: center;
    color: white;
    opacity: 0.8;
    margin-top: 20px;
}

@media (max-width: 768px) {
    .main-header h1 {
        font-size: 2rem;
    }
    
    .tools-grid {
        grid-template-columns: 1fr;
    }
}'''
        
        (self.root / 'index.html').write_text(index_html, encoding='utf-8')
        (self.root / 'static' / 'css' / 'main.css').write_text(main_css, encoding='utf-8')
        
        # اسکریپت اجرای همزمان
        run_all = '''#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path

def run_tool(tool_name, port):
    """اجرای یک ابزار"""
    tool_dir = Path(f"tools/{tool_name}")
    
    print(f"\\n🚀 در حال اجرای {tool_name} روی پورت {port}...")
    
    # نصب وابستگی‌ها
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", 
                   "-r", str(tool_dir / "requirements.txt")])
    
    # اجرای اپلیکیشن
    subprocess.Popen([sys.executable, str(tool_dir / "app.py"), 
                     "--port", str(port)], 
                    cwd=tool_dir)

if __name__ == "__main__":
    print("=" * 60)
    print("🎯 اجرای همزمان تمام ابزارها")
    print("=" * 60)
    
    run_tool("face_recognition", 5001)
    run_tool("audio_mastering", 5002)
    
    print("\\n✅ تمام ابزارها در حال اجرا هستند:")
    print("   - تشخیص چهره: http://localhost:5001")
    print("   - پردازش صدا: http://localhost:5002")
    print("\\nبرای توقف: Ctrl+C")
    
    input()
'''
        
        (self.root / 'run_all_tools.py').write_text(run_all, encoding='utf-8')
        
        print("  ✓ صفحه اصلی ایجاد شد")
    
    def build_face_recognition_tool(self):
        """ساخت ابزار تشخیص چهره (مستقل)"""
        print("\n👤 ساخت ابزار تشخیص چهره...")
        
        tool_dir = self.tools_dir / 'face_recognition'
        
        # ساختار پوشه‌ها
        folders = [
            'modules',
            'static/css',
            'static/js',
            'static/uploads',
            'static/results',
            'models',
            'data/known_faces'
        ]
        
        for folder in folders:
            (tool_dir / folder).mkdir(parents=True, exist_ok=True)
            (tool_dir / folder / '.gitkeep').touch()
        
        # requirements.txt
        requirements = '''flask==3.0.0
werkzeug==3.0.1
numpy==1.24.3
opencv-python-headless==4.8.1.78
pillow==10.1.0
face-recognition==1.3.0
dlib==19.24.2
requests==2.31.0'''
        
        (tool_dir / 'requirements.txt').write_text(requirements)
        
        # ماژول تشخیص چهره
        face_module = '''# -*- coding: utf-8 -*-
import cv2
import numpy as np
from pathlib import Path
import pickle
import uuid

class FaceRecognitionSystem:
    """سیستم تشخیص چهره"""
    
    def __init__(self, tool_root):
        self.tool_root = Path(tool_root)
        self.known_faces_dir = self.tool_root / 'data' / 'known_faces'
        self.models_dir = self.tool_root / 'models'
        
        try:
            import face_recognition
            self.use_face_recognition = True
            self.known_encodings = []
            self.known_names = []
            self.load_known_faces()
        except ImportError:
            self.use_face_recognition = False
            self.setup_opencv_detector()
    
    def setup_opencv_detector(self):
        """OpenCV Detector"""
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
    
    def load_known_faces(self):
        """بارگذاری چهره‌های ذخیره شده"""
        encodings_file = self.known_faces_dir / 'encodings.pkl'
        if encodings_file.exists():
            with open(encodings_file, 'rb') as f:
                data = pickle.load(f)
                self.known_encodings = data.get('encodings', [])
                self.known_names = data.get('names', [])
    
    def add_known_face(self, image_path, name):
        """افزودن چهره جدید"""
        if not self.use_face_recognition:
            return {'success': False, 'error': 'face_recognition unavailable'}
        
        import face_recognition
        image = face_recognition.load_image_file(image_path)
        encodings = face_recognition.face_encodings(image)
        
        if not encodings:
            return {'success': False, 'error': 'چهره یافت نشد'}
        
        self.known_encodings.append(encodings[0])
        self.known_names.append(name)
        
        with open(self.known_faces_dir / 'encodings.pkl', 'wb') as f:
            pickle.dump({
                'encodings': self.known_encodings,
                'names': self.known_names
            }, f)
        
        return {'success': True, 'name': name}
    
    def recognize_faces(self, image_path):
        """شناسایی چهره‌ها"""
        if self.use_face_recognition:
            return self._recognize_with_fr(image_path)
        return self._recognize_with_opencv(image_path)
    
    def _recognize_with_fr(self, image_path):
        """شناسایی با face_recognition"""
        import face_recognition
        
        image = face_recognition.load_image_file(image_path)
        locations = face_recognition.face_locations(image)
        encodings = face_recognition.face_encodings(image, locations)
        
        image_cv = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        results = []
        
        for (top, right, bottom, left), encoding in zip(locations, encodings):
            name = "ناشناس"
            confidence = 0
            
            if self.known_encodings:
                matches = face_recognition.compare_faces(self.known_encodings, encoding)
                distances = face_recognition.face_distance(self.known_encodings, encoding)
                
                if True in matches:
                    idx = np.argmin(distances)
                    if matches[idx]:
                        name = self.known_names[idx]
                        confidence = (1 - distances[idx]) * 100
            
            cv2.rectangle(image_cv, (left, top), (right, bottom), (0, 255, 0), 2)
            label = f"{name} ({confidence:.1f}%)" if confidence > 0 else name
            cv2.rectangle(image_cv, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
            cv2.putText(image_cv, label, (left + 6, bottom - 6),
                       cv2.FONT_HERSHEY_DUPLEX, 0.6, (255, 255, 255), 1)
            
            results.append({
                'name': name,
                'confidence': round(confidence, 2),
                'location': {'top': top, 'right': right, 'bottom': bottom, 'left': left}
            })
        
        output_file = f"recognized_{uuid.uuid4()}.jpg"
        output_path = self.tool_root / 'static' / 'results' / output_file
        cv2.imwrite(str(output_path), image_cv)
        
        return {
            'success': True,
            'faces': results,
            'output_image': f'/static/results/{output_file}'
        }
    
    def _recognize_with_opencv(self, image_path):
        """شناسایی با OpenCV"""
        image = cv2.imread(str(image_path))
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 5, minSize=(30, 30))
        
        results = []
        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(image, "Face Detected", (x, y-10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            results.append({'name': 'Detected', 'confidence': 0})
        
        output_file = f"detected_{uuid.uuid4()}.jpg"
        output_path = self.tool_root / 'static' / 'results' / output_file
        cv2.imwrite(str(output_path), image)
        
        return {
            'success': True,
            'faces': results,
            'output_image': f'/static/results/{output_file}'
        }
'''
        
        (tool_dir / 'modules' / 'face_system.py').write_text(face_module, encoding='utf-8')
        
        # Flask App
        app_code = '''# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent / 'modules'))
from face_system import FaceRecognitionSystem

app = Flask(__name__)
app.config['SECRET_KEY'] = 'face-recognition-tool'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024

TOOL_ROOT = Path(__file__).parent
face_system = FaceRecognitionSystem(TOOL_ROOT)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/recognize', methods=['POST'])
def recognize():
    if 'file' not in request.files:
        return jsonify({'error': 'فایل ارسال نشده'}), 400
    
    file = request.files['file']
    filename = secure_filename(file.filename)
    filepath = TOOL_ROOT / 'static' / 'uploads' / filename
    file.save(filepath)
    
    result = face_system.recognize_faces(str(filepath))
    return jsonify(result)

@app.route('/api/add-face', methods=['POST'])
def add_face():
    if 'file' not in request.files or 'name' not in request.form:
        return jsonify({'error': 'داده‌های ناقص'}), 400
    
    file = request.files['file']
    name = request.form['name']
    filename = secure_filename(file.filename)
    filepath = TOOL_ROOT / 'static' / 'uploads' / filename
    file.save(filepath)
    
    result = face_system.add_known_face(str(filepath), name)
    return jsonify(result)

@app.route('/static/results/<filename>')
def serve_result(filename):
    return send_from_directory(TOOL_ROOT / 'static' / 'results', filename)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=5001)
    args = parser.parse_args()
    
    print(f"🚀 Face Recognition Tool: http://localhost:{args.port}")
    app.run(debug=True, host='0.0.0.0', port=args.port)
'''
        
        (tool_dir / 'app.py').write_text(app_code, encoding='utf-8')
        
        # HTML Template
        html_template = '''<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>تشخیص چهره</title>
    <link rel="stylesheet" href="/static/css/style.css">
</head>
<body>
    <div class="container">
        <header>
            <h1>👤 ابزار تشخیص چهره</h1>
            <a href="../../index.html" class="back-btn">← بازگشت به صفحه اصلی</a>
        </header>

        <div class="tabs">
            <button class="tab active" onclick="showTab('recognize')">شناسایی چهره</button>
            <button class="tab" onclick="showTab('add')">افزودن چهره</button>
        </div>

        <div id="recognize-tab" class="tab-content">
            <div class="upload-box">
                <input type="file" id="recognizeFile" accept="image/*">
                <label for="recognizeFile">
                    <span>📸</span>
                    <p>تصویر خود را بکشید یا کلیک کنید</p>
                </label>
            </div>
            <button onclick="recognizeFace()" class="btn-primary">شناسایی چهره</button>
            <div id="recognizeResult"></div>
        </div>

        <div id="add-tab" class="tab-content" style="display:none;">
            <input type="text" id="faceName" placeholder="نام فرد">
            <div class="upload-box">
                <input type="file" id="addFile" accept="image/*">
                <label for="addFile">
                    <span>👤</span>
                    <p>تصویر چهره را آپلود کنید</p>
                </label>
            </div>
            <button onclick="addFace()" class="btn-primary">افزودن به پایگاه داده</button>
            <div id="addResult"></div>
        </div>
    </div>

    <script>
        function showTab(tab) {
            document.querySelectorAll('.tab-content').forEach(el => el.style.display = 'none');
            document.querySelectorAll('.tab').forEach(el => el.classList.remove('active'));
            
            document.getElementById(tab + '-tab').style.display = 'block';
            event.target.classList.add('active');
        }

        async function recognizeFace() {
            const file = document.getElementById('recognizeFile').files[0];
            if (!file) return alert('لطفاً تصویر را انتخاب کنید');

            const formData = new FormData();
            formData.append('file', file);

            const result = document.getElementById('recognizeResult');
            result.innerHTML = '<p>در حال پردازش...</p>';

            try {
                const response = await fetch('/api/recognize', {
                    method: 'POST',
                    body: formData
                });
                const data = await response.json();

                if (data.success) {
                    result.innerHTML = `
                        <h3>نتیجه شناسایی:</h3>
                        <img src="${data.output_image}" alt="Result">
                        <p>تعداد چهره‌ها: ${data.faces.length}</p>
                        ${data.faces.map(f => `<p>${f.name} - ${f.confidence}%</p>`).join('')}
                    `;
                } else {
                    result.innerHTML = `<p class="error">${data.error}</p>`;
                }
            } catch (error) {
                result.innerHTML = `<p class="error">خطا: ${error.message}</p>`;
            }
        }

        async function addFace() {
            const file = document.getElementById('addFile').files[0];
            const name = document.getElementById('faceName').value;
            
            if (!file || !name) return alert('لطفاً تصویر و نام را وارد کنید');

            const formData = new FormData();
            formData.append('file', file);
            formData.append('name', name);

            const result = document.getElementById('addResult');
            result.innerHTML = '<p>در حال پردازش...</p>';

            try {
                const response = await fetch('/api/add-face', {
                    method: 'POST',
                    body: formData
                });
                const data = await response.json();

                if (data.success) {
                    result.innerHTML = `<p class="success">چهره "${data.name}" با موفقیت اضافه شد!</p>`;
                } else {
                    result.innerHTML = `<p class="error">${data.error}</p>`;
                }
            } catch (error) {
                result.innerHTML = `<p class="error">خطا: ${error.message}</p>`;
            }
        }
    </script>
</body>
</html>'''
        
        (tool_dir / 'templates').mkdir(exist_ok=True)
        (tool_dir / 'templates' / 'index.html').write_text(html_template, encoding='utf-8')
        
        # CSS
        css = '''* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: Tahoma; background: #f5f5f5; padding: 20px; }
.container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; }
header { text-align: center; margin-bottom: 30px; }
.back-btn { display: inline-block; padding: 10px 20px; background: #667eea; color: white; text-decoration: none; border-radius: 5px; }
.tabs { display: flex; gap: 10px; margin-bottom: 20px; }
.tab { flex: 1; padding: 15px; background: #eee; border: none; border-radius: 5px; cursor: pointer; }
.tab.active { background: #667eea; color: white; }
.upload-box { border: 2px dashed #ccc; padding: 40px; text-align: center; margin: 20px 0; border-radius: 10px; }
.upload-box input[type="file"] { display: none; }
.upload-box label { cursor: pointer; }
.upload-box span { font-size: 3rem; }
.btn-primary { width: 100%; padding: 15px; background: #667eea; color: white; border: none; border-radius: 5px; font-size: 1.1rem; cursor: pointer; }
.btn-primary:hover { opacity: 0.9; }
input[type="text"] { width: 100%; padding: 15px; border: 1px solid #ddd; border-radius: 5px; margin-bottom: 15px; font-size: 1rem; }
#recognizeResult, #addResult { margin-top: 20px; text-align: center; }
#recognizeResult img { max-width: 100%; border-radius: 10px; margin: 20px 0; }
.error { color: red; }
.success { color: green; }'''
        
        (tool_dir / 'static' / 'css' / 'style.css').write_text(css)
        
        print("  ✓ ابزار تشخیص چهره ساخته شد")
    
    def build_audio_mastering_tool(self):
        """ساخت ابزار پردازش صدا (مستقل)"""
        print("\n🎵 ساخت ابزار پردازش صدا...")
        
        tool_dir = self.tools_dir / 'audio_mastering'
        
        # ساختار
        folders = [
            'modules',
            'static/css',
            'static/js',
            'static/uploads',
            'static/results',
            'data'
        ]
        
        for folder in folders:
            (tool_dir / folder).mkdir(parents=True, exist_ok=True)
        
        # requirements.txt
        requirements = '''flask==3.0.0
werkzeug==3.0.1
numpy==1.24.3
scipy==1.11.4
librosa==0.10.1
soundfile==0.12.1
pydub==0.25.1'''
        
        (tool_dir / 'requirements.txt').write_text(requirements)
        
        # ماژول پردازش
        audio_module = '''# -*- coding: utf-8 -*-
import numpy as np
import librosa
import soundfile as sf
from pathlib import Path
import uuid
from scipy import signal

class AudioMasteringSystem:
    """سیستم مستر کردن صدا"""
    
    def __init
