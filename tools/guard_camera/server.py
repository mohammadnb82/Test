
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
