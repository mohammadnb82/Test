import os

def overwrite_root_index():
    filename = "index.html"
    
    # محتوای HTML جدید (صفحه اصلی سایت)
    html_content = """<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>سامانه هوشمند</title>
    <style>
        :root {
            --primary-color: #3b82f6;
            --bg-color: #f8fafc;
            --text-color: #1e293b;
            --white: #ffffff;
        }

        body {
            font-family: system-ui, -apple-system, sans-serif;
            background-color: var(--bg-color);
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            text-align: center;
        }

        .container {
            background: var(--white);
            padding: 40px 30px;
            border-radius: 20px;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1);
            width: 90%;
            max-width: 500px;
        }

        h1 {
            color: var(--text-color);
            margin-bottom: 10px;
            font-size: 2rem;
        }

        p.subtitle {
            color: #64748b;
            margin-bottom: 40px;
            font-size: 1.1rem;
        }

        .button-stack {
            display: flex;
            flex-direction: column;
            gap: 15px;
        }

        .btn {
            display: block;
            text-decoration: none;
            padding: 18px;
            border-radius: 12px;
            font-weight: bold;
            font-size: 1.1rem;
            transition: transform 0.2s, box-shadow 0.2s;
        }

        /* دکمه اصلی: ورود به ابزارها */
        .btn-primary {
            background-color: var(--primary-color);
            color: var(--white);
            box-shadow: 0 4px 6px -1px rgba(59, 130, 246, 0.4);
        }

        .btn-primary:hover {
            background-color: #2563eb;
            transform: translateY(-2px);
            box-shadow: 0 10px 15px -3px rgba(59, 130, 246, 0.4);
        }

        /* دکمه‌های فرعی */
        .btn-secondary {
            background-color: var(--white);
            color: var(--text-color);
            border: 2px solid #e2e8f0;
        }

        .btn-secondary:hover {
            border-color: var(--primary-color);
            color: var(--primary-color);
        }

        .footer {
            margin-top: 30px;
            font-size: 0.9rem;
            color: #94a3b8;
        }
    </style>
</head>
<body>

    <div class="container">
        <h1>خوش آمدید</h1>
        <p class="subtitle">پرتال جامع خدمات هوشمند</p>

        <div class="button-stack">
            <!-- لینک به پوشه tools -->
            <a href="tools/index.html" class="btn btn-primary">
                🚀 ورود به بخش ابزارها
            </a>

            <a href="#" class="btn btn-secondary">درباره ما</a>
            <a href="#" class="btn btn-secondary">ارتباط با پشتیبانی</a>
        </div>

        <div class="footer">
            نسخه ۱.۰.۰
        </div>
    </div>

</body>
</html>
"""

    # بررسی وجود فایل قدیمی صرفاً جهت اطلاع
    if os.path.exists(filename):
        print(f"⚠️ فایل {filename} موجود است. محتوای قبلی در حال پاک‌سازی است...")
    else:
        print(f"✨ فایل {filename} وجود نداشت. فایل جدید ساخته می‌شود...")

    # حالت 'w' (Write) فایل قبلی را خالی کرده و محتوای جدید را می‌نویسد
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print(f"✅ فایل {filename} با موفقیت به‌روزرسانی شد.")

if __name__ == "__main__":
    overwrite_root_index()
