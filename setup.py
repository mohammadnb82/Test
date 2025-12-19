import os

def fix_navigation_full():
    print("🚀 شروع عملیات بازسازی کامل ناوبری سایت...")

    # ==========================================
    # 1. بازسازی فایل ریشه (Root index.html)
    # وظیفه: فقط یک دروازه ورود به پوشه tools باشد
    # ==========================================
    root_html_content = """<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>صفحه اصلی</title>
    <style>
        body {
            font-family: system-ui, -apple-system, sans-serif;
            background: #111;
            color: white;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
            margin: 0;
            gap: 20px;
        }
        h1 { margin-bottom: 40px; }
        .menu-btn {
            background: #007bff;
            color: white;
            border: none;
            padding: 20px 40px;
            width: 80%;
            max-width: 300px;
            font-size: 20px;
            font-weight: bold;
            border-radius: 15px;
            cursor: pointer;
            text-decoration: none;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: background 0.2s;
            box-shadow: 0 4px 15px rgba(0,123,255,0.3);
        }
        .menu-btn:hover { background: #0056b3; }
        .footer {
            margin-top: 50px;
            color: #666;
            font-size: 14px;
        }
    </style>
</head>
<body>

    <h1>اپلیکیشن من</h1>

    <!-- لینک اصلی به پوشه تولز -->
    <a href="tools/index.html" class="menu-btn">
        📂 ورود به ابزارها
    </a>

    <div class="footer">نسخه ۲.۰ - بازسازی کامل</div>

</body>
</html>
"""
    try:
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(root_html_content)
        print("✅ مرحله ۱: فایل اصلی (index.html) بازسازی شد.")
    except Exception as e:
        print(f"❌ خطا در مرحله ۱: {e}")


    # ==========================================
    # 2. بازسازی فایل تولز (tools/index.html)
    # وظیفه: ۲۰ دکمه داشته باشد، دکمه ۱ به دوربین برود
    # ==========================================
    
    # اطمینان از وجود پوشه tools
    if not os.path.exists("tools"):
        os.makedirs("tools")
    
    # ساخت لیست ۲۰ دکمه
    buttons_html = ""
    for i in range(1, 21):
        if i == 1:
            # دکمه اول: فعال و سبز رنگ (لینک به دوربین)
            buttons_html += f"""
        <a href="doorbin-tashkhis-harekat/index.html" class="tool-btn active">
            📷 دوربین تشخیص حرکت
        </a>"""
        else:
            # دکمه‌های بعدی: غیرفعال یا رزرو
            buttons_html += f"""
        <div class="tool-btn disabled">
            ابزار شماره {i} (خالی)
        </div>"""

    tools_html_content = f"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>لیست ابزارها</title>
    <style>
        body {{
            font-family: system-ui, -apple-system, sans-serif;
            background: #1a1a1a;
            color: white;
            padding: 20px;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
        }}
        h2 {{ margin-bottom: 30px; border-bottom: 2px solid #333; padding-bottom: 10px; }}
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
            gap: 15px;
            width: 100%;
            max-width: 800px;
        }}
        .tool-btn {{
            background: #333;
            color: #888;
            border: 1px solid #444;
            padding: 15px;
            border-radius: 12px;
            text-align: center;
            text-decoration: none;
            font-size: 14px;
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 80px;
            transition: 0.2s;
            cursor: default;
        }}
        /* استایل دکمه فعال (دوربین) */
        .tool-btn.active {{
            background: #28a745;
            color: white;
            border-color: #1e7e34;
            cursor: pointer;
            font-weight: bold;
            font-size: 16px;
            box-shadow: 0 4px 10px rgba(40, 167, 69, 0.3);
        }}
        .tool-btn.active:hover {{ background: #218838; transform: translateY(-2px); }}
        
        /* استایل دکمه‌های غیرفعال */
        .tool-btn.disabled {{
            opacity: 0.5;
        }}
        
        .back-link {{
            margin-top: 40px;
            color: #aaa;
            text-decoration: none;
            padding: 10px 20px;
            border: 1px solid #444;
            border-radius: 8px;
        }}
        .back-link:hover {{ background: #333; color: white; }}
    </style>
</head>
<body>

    <h2>🛠 جعبه ابزار (۲۰ آیتم)</h2>

    <div class="grid">
        {buttons_html}
    </div>

    <a href="../index.html" class="back-link">⬅️ بازگشت به صفحه اصلی</a>

</body>
</html>
"""

    try:
        with open("tools/index.html", "w", encoding="utf-8") as f:
            f.write(tools_html_content)
        print("✅ مرحله ۲: فایل لیست ابزارها (tools/index.html) با ۲۰ دکمه بازسازی شد.")
        print("   -> دکمه ۱ به 'doorbin-tashkhis-harekat/index.html' لینک شد.")
    except Exception as e:
        print(f"❌ خطا در مرحله ۲: {e}")

if __name__ == "__main__":
    fix_navigation_full()
