import os

def create_main_dashboard():
    # مسیر ذخیره فایل ایندکس اصلی (در ریشه پوشه tools)
    base_dir = "tools"
    # اطمینان از وجود پوشه tools
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
        
    file_path = os.path.join(base_dir, "index.html")

    # محتوای HTML به صورت هاردکد شده و بدون حلقه، طبق دستور شما
    # استایل‌ها برای نمایش شبکه‌ای و زیبا در موبایل تنظیم شده‌اند
    html_content = """<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>جعبه ابزار هوشمند</title>
    <style>
        :root {
            --bg-color: #f3f4f6;
            --card-bg: #ffffff;
            --text-color: #1f2937;
            --hover-color: #3b82f6;
        }
        body {
            font-family: system-ui, -apple-system, sans-serif;
            background-color: var(--bg-color);
            margin: 0;
            padding: 20px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        h1 {
            color: var(--text-color);
            margin-bottom: 30px;
            font-size: 1.5rem;
        }
        /* گرید بندی برای نمایش منظم دکمه‌ها */
        .dashboard-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
            gap: 15px;
            width: 100%;
            max-width: 800px;
        }
        /* استایل دکمه‌ها */
        .tool-btn {
            background: var(--card-bg);
            border: 1px solid #e5e7eb;
            border-radius: 12px;
            padding: 20px 10px;
            text-align: center;
            text-decoration: none;
            color: var(--text-color);
            font-weight: 600;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            transition: all 0.2s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 60px;
        }
        /* افکت هاور و اکتیو */
        .tool-btn:hover {
            border-color: var(--hover-color);
            color: var(--hover-color);
            transform: translateY(-2px);
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        /* کلاس مخصوص برای ابزارهایی که کامل شده‌اند */
        .ready {
            border-left: 4px solid #10b981;
        }
    </style>
</head>
<body>

    <h1>🛠️ منوی انتخاب ابزار</h1>

    <div class="dashboard-grid">
        <!-- کلید ۱: ابزار فعلی (لینک دهی شد) -->
        <a href="doorbin-tashkhis-harekat/index.html" class="tool-btn ready">📷 دوربین تشخیص حرکت</a>

        <!-- کلید ۲ -->
        <a href="#" class="tool-btn">👤 دوربین تشخیص انسان</a>

        <!-- کلید ۳ -->
        <a href="#" class="tool-btn">🧮 ماشین حساب</a>

        <!-- کلید ۴ -->
        <a href="#" class="tool-btn">ابزار ۴</a>

        <!-- کلید ۵ -->
        <a href="#" class="tool-btn">ابزار ۵</a>

        <!-- کلید ۶ -->
        <a href="#" class="tool-btn">ابزار ۶</a>

        <!-- کلید ۷ -->
        <a href="#" class="tool-btn">ابزار ۷</a>

        <!-- کلید ۸ -->
        <a href="#" class="tool-btn">ابزار ۸</a>

        <!-- کلید ۹ -->
        <a href="#" class="tool-btn">ابزار ۹</a>

        <!-- کلید ۱۰ -->
        <a href="#" class="tool-btn">ابزار ۱۰</a>

        <!-- کلید ۱۱ -->
        <a href="#" class="tool-btn">ابزار ۱۱</a>

        <!-- کلید ۱۲ -->
        <a href="#" class="tool-btn">ابزار ۱۲</a>

        <!-- کلید ۱۳ -->
        <a href="#" class="tool-btn">ابزار ۱۳</a>

        <!-- کلید ۱۴ -->
        <a href="#" class="tool-btn">ابزار ۱۴</a>

        <!-- کلید ۱۵ -->
        <a href="#" class="tool-btn">ابزار ۱۵</a>

        <!-- کلید ۱۶ -->
        <a href="#" class="tool-btn">ابزار ۱۶</a>

        <!-- کلید ۱۷ -->
        <a href="#" class="tool-btn">ابزار ۱۷</a>

        <!-- کلید ۱۸ -->
        <a href="#" class="tool-btn">ابزار ۱۸</a>

        <!-- کلید ۱۹ -->
        <a href="#" class="tool-btn">ابزار ۱۹</a>

        <!-- کلید ۲۰ -->
        <a href="#" class="tool-btn">ابزار ۲۰</a>
    </div>

</body>
</html>
"""

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print(f"✅ فایل داشبورد ساخته شد: {file_path}")
    print("نکته: لینک ابزار اول به صورت خودکار به پوشه پروژه فعلی متصل شد.")

if __name__ == "__main__":
    create_main_dashboard()
