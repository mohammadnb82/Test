
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
