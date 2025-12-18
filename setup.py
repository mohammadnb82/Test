import os
import requests

def download_file(url, folder, filename):
    """دانلود فایل و ذخیره با نمایش وضعیت"""
    file_path = os.path.join(folder, filename)
    
    # اگر فایل قبلاً وجود داشت، دوباره دانلود نکن (صرفه‌جویی در وقت)
    if os.path.exists(file_path):
        print(f"✅ فایل {filename} از قبل موجود است.")
        return

    print(f"⬇️ در حال دانلود {filename} ...")
    try:
        response = requests.get(url, stream=True, timeout=30)
        if response.status_code == 200:
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            print(f"   با موفقیت ذخیره شد.")
        else:
            print(f"❌ خطا: سرور پاسخ داد {response.status_code}")
    except Exception as e:
        print(f"❌ خطای ارتباطی: {e}")

def setup_offline_assets():
    # مسیر پایه پروژه
    base_dir = "tools/doorbin-tashkhis-harekat"
    assets_dir = os.path.join(base_dir, "assets")
    
    # مسیرهای دقیق
    js_dir = os.path.join(assets_dir, "js")
    # مدل Blazeface (تشخیص چهره سریع)
    model_dir = os.path.join(assets_dir, "models", "blazeface")

    # 1. ایجاد پوشه‌ها
    os.makedirs(js_dir, exist_ok=True)
    os.makedirs(model_dir, exist_ok=True)

    # 2. لیست فایل‌های حیاتی
    # نکته مهم: ما نسخه tfjs-core و backend-webgl را جدا نمی‌کنیم
    # بلکه از نسخه Union (tf.min.js) استفاده می‌کنیم که همه چیز را دارد
    # تا نیاز به دانلود داینامیک وابستگی‌ها نباشد.
    
    files = [
        # --- موتور اصلی تنسورفلو (نسخه کامل شامل WebGL) ---
        {
            "url": "https://cdn.jsdelivr.net/npm/@tensorflow/tfjs/dist/tf.min.js",
            "folder": js_dir,
            "name": "tf.min.js"
        },
        # --- کتابخانه کمکی Blazeface (فقط رپر JS) ---
        {
            "url": "https://cdn.jsdelivr.net/npm/@tensorflow-models/blazeface/dist/blazeface.min.js",
            "folder": js_dir,
            "name": "blazeface.min.js"
        },
        # --- فایل‌های مدل هوش مصنوعی (مغز سیستم) ---
        # فایل JSON که ساختار شبکه عصبی را توضیح می‌دهد
        {
            "url": "https://storage.googleapis.com/tfjs-models/savedmodel/blazeface/model.json",
            "folder": model_dir,
            "name": "model.json"
        },
        # فایل باینری که وزن‌های ریاضی شبکه عصبی در آن است (قسمت اصلی)
        {
            "url": "https://storage.googleapis.com/tfjs-models/savedmodel/blazeface/group1-shard1of1.bin",
            "folder": model_dir,
            "name": "group1-shard1of1.bin"
        }
    ]

    print("🚀 شروع عملیات دانلود منابع آفلاین...")
    for item in files:
        download_file(item["url"], item["folder"], item["name"])

    print("\n✅ عملیات تمام شد.")
    print("ساختار فایل‌ها برای ارجاع در HTML:")
    print(f"   JS Core:  assets/js/tf.min.js")
    print(f"   JS Model: assets/js/blazeface.min.js")
    print(f"   AI Model: assets/models/blazeface/model.json")

if __name__ == "__main__":
    setup_offline_assets()
