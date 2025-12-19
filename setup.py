import os

def apply_index_plus_foldername_convention():
    print("🚀 شروع عملیات نام‌گذاری استاندارد (index_Foldername)...")

    # مسیرها و نام‌های پوشه
    DIR_TOOLS = "tools"
    DIR_CAMERA = "doorbin-tashkhis-harekat"
    
    # مسیرهای سیستمی
    path_tools_dir = DIR_TOOLS
    path_camera_dir = os.path.join(DIR_TOOLS, DIR_CAMERA)

    # نام‌های جدید فایل‌ها طبق الگوی درخواستی (index_Foldername)
    NEW_CAMERA_FILE = f"index_{DIR_CAMERA}.html"  # index_doorbin-tashkhis-harekat.html
    NEW_TOOLS_FILE = f"index_{DIR_TOOLS}.html"    # index_tools.html

    # =========================================================
    # 1. تغییر نام فایل داخل پوشه دوربین (حفظ محتوای کد)
    # =========================================================
    print(f"\n🔹 مرحله ۱: استانداردسازی نام فایل دوربین...")
    
    current_camera_path = os.path.join(path_camera_dir, "index.html")
    target_camera_path = os.path.join(path_camera_dir, NEW_CAMERA_FILE)

    # بررسی می‌کنیم فایل الان چه نامی دارد و آن را تغییر می‌دهیم
    if os.path.exists(current_camera_path):
        try:
            os.rename(current_camera_path, target_camera_path)
            print(f"   ✅ فایل تغییر نام یافت:\n      index.html -> {NEW_CAMERA_FILE}")
        except Exception as e:
            print(f"   ❌ خطا در تغییر نام: {e}")
    elif os.path.exists(target_camera_path):
        print(f"   ℹ️ فایل از قبل نام درست ({NEW_CAMERA_FILE}) را دارد.")
    else:
        # شاید قبلاً نامش چیز دیگری شده، سعی میکنیم پیدایش کنیم
        print("   ⚠️ فایل index.html یافت نشد. (اگر قبلا تغییر نام دادید نادیده بگیرید)")

    # =========================================================
    # 2. بازسازی فایل تولز (index_tools.html) با لینک‌های جدید
    # =========================================================
    print(f"\n🔹 مرحله ۲: ساخت فایل {NEW_TOOLS_FILE}...")
    
    if not os.path.exists(path_tools_dir):
        os.makedirs(path_tools_dir)

    # پاک کردن فایل‌های قدیمی و هم‌نام که باعث گیجی می‌شوند
    for old_file in ["index.html", "tools.html"]:
        old_path = os.path.join(path_tools_dir, old_file)
        if os.path.exists(old_path):
            os.remove(old_path)
            print(f"   🗑️ فایل قدیمی و تکراری '{old_file}' حذف شد.")

    # ساخت آدرس نسبی برای لینک دادن به دوربین
    # آدرس: نام پوشه دوربین / نام فایل جدید دوربین
    link_to_camera = f"{DIR_CAMERA}/{NEW_CAMERA_FILE}"

    buttons_html = ""
    for i in range(1, 21):
        if i == 1:
            buttons_html += f"""
        <!-- دکمه ۱: لینک اصلاح شده به فایل ایندکس_دوربین -->
        <a href="{link_to_camera}" class="tool-btn active">
            📷 دوربین تشخیص حرکت
        </a>"""
        else:
            buttons_html += f"""
        <div class="tool-btn disabled">
            ابزار شماره {i}
        </div>"""

    tools_content = f"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>لیست ابزارها</title>
    <style>
        body {{ font-family: system-ui, -apple-system, sans-serif; background: #1a1a1a; color: white; padding: 20px; min-height: 100vh; display: flex; flex-direction: column; align-items: center; }}
        h2 {{ margin-bottom: 30px; border-bottom: 2px solid #333; padding-bottom: 10px; }}
        .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(140px, 1fr)); gap: 15px; width: 100%; max-width: 800px; }}
        .tool-btn {{ background: #333; color: #888; border: 1px solid #444; padding: 15px; border-radius: 12px; text-align: center; text-decoration: none; font-size: 14px; display: flex; align-items: center; justify-content: center; min-height: 80px; transition: 0.2s; cursor: default; }}
        .tool-btn.active {{ background: #28a745; color: white; border-color: #1e7e34; cursor: pointer; font-weight: bold; font-size: 16px; box-shadow: 0 4px 10px rgba(40, 167, 69, 0.3); }}
        .tool-btn.active:hover {{ background: #218838; transform: translateY(-2px); }}
        .tool-btn.disabled {{ opacity: 0.5; }}
        .back-link {{ margin-top: 40px; color: #aaa; text-decoration: none; padding: 10px 20px; border: 1px solid #444; border-radius: 8px; }}
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
    # نوشتن فایل جدید tools/index_tools.html
    with open(os.path.join(path_tools_dir, NEW_TOOLS_FILE), "w", encoding="utf-8") as f:
        f.write(tools_content)
    print(f"   ✅ فایل '{NEW_TOOLS_FILE}' با موفقیت ساخته شد.")


    # =========================================================
    # 3. آپدیت فایل ریشه (index.html)
    # =========================================================
    print(f"\n🔹 مرحله ۳: آپدیت فایل اصلی سایت...")
    
    # ساخت آدرس نسبی برای لینک دادن به تولز
    # آدرس: tools / index_tools.html
    link_to_tools = f"{DIR_TOOLS}/{NEW_TOOLS_FILE}"

    root_content = f"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>صفحه اصلی</title>
    <style>
        body {{ font-family: system-ui, -apple-system, sans-serif; background: #111; color: white; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; margin: 0; gap: 20px; }}
        h1 {{ margin-bottom: 40px; }}
        .menu-btn {{ background: #007bff; color: white; border: none; padding: 20px 40px; width: 80%; max-width: 300px; font-size: 20px; font-weight: bold; border-radius: 15px; cursor: pointer; text-decoration: none; display: flex; align-items: center; justify-content: center; transition: background 0.2s; box-shadow: 0 4px 15px rgba(0,123,255,0.3); }}
        .menu-btn:hover {{ background: #0056b3; }}
        .footer {{ margin-top: 50px; color: #666; font-size: 14px; }}
    </style>
</head>
<body>
    <h1>اپلیکیشن من</h1>
    
    <!-- لینک اصلاح شده به فایل ایندکس_تولز -->
    <a href="{link_to_tools}" class="menu-btn">
        📂 ورود به ابزارها
    </a>

    <div class="footer">نسخه ۵.۰ - ساختار index_Foldername</div>
</body>
</html>
"""
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(root_content)
    print("   ✅ فایل ریشه (index.html) آپدیت شد.")

    print("\n🎉 ساختار نهایی سایت شما:")
    print(f"1. index.html  -----> لینک میدهد به -----> {link_to_tools}")
    print(f"2. {NEW_TOOLS_FILE} -- میدهد به -----> {link_to_camera}")

if __name__ == "__main__":
    apply_index_plus_foldername_convention()
```ion()

