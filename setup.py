import os

def create_homepage():
    # محتوای HTML صفحه اصلی با ۴ دکمه و استایل زیبا
    html_content = """
    <!DOCTYPE html>
    <html lang="fa" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>سایت تست - کنترل پنل</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background-color: #f4f4f9;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                height: 100vh;
                margin: 0;
            }
            h1 {
                color: #333;
                margin-bottom: 30px;
            }
            .button-container {
                display: grid;
                grid-template-columns: 1fr 1fr; /* دو ستون */
                gap: 20px;
            }
            .btn {
                background-color: #4CAF50; /* رنگ سبز */
                border: none;
                color: white;
                padding: 20px 40px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 18px;
                margin: 4px 2px;
                cursor: pointer;
                border-radius: 12px;
                transition: background-color 0.3s, transform 0.2s;
                width: 200px;
            }
            .btn:hover {
                background-color: #45a049;
                transform: scale(1.05); /* کمی بزرگنمایی هنگام موس */
            }
            .btn-blue { background-color: #008CBA; }
            .btn-red { background-color: #f44336; }
            .btn-orange { background-color: #ff9800; }
        </style>
    </head>
    <body>

        <h1>کنترل پنل سایت Test</h1>

        <div class="button-container">
            <!-- دکمه اول -->
            <button class="btn" onclick="alert('دکمه ۱ کلیک شد!')">دکمه شماره ۱</button>
            
            <!-- دکمه دوم -->
            <button class="btn btn-blue" onclick="alert('دکمه ۲ کلیک شد!')">دکمه شماره ۲</button>
            
            <!-- دکمه سوم -->
            <button class="btn btn-red" onclick="alert('دکمه ۳ کلیک شد!')">دکمه شماره ۳</button>
            
            <!-- دکمه چهارم -->
            <button class="btn btn-orange" onclick="alert('دکمه ۴ کلیک شد!')">دکمه شماره ۴</button>
        </div>

    </body>
    </html>
    """

    # ایجاد و ذخیره فایل index.html
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("✅ صفحه اصلی (index.html) با ۴ دکمه ساخته شد.")

def ensure_tools_folder():
    # ساخت پوشه tools و فایل keep برای جلوگیری از حذف
    folder_name = "tools"
    keep_file = ".keep"
    file_path = os.path.join(folder_name, keep_file)

    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    
    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            pass 

if __name__ == "__main__":
    # ۱. اطمینان از وجود پوشه tools
    ensure_tools_folder()
    
    # ۲. ساختن صفحه اصلی با دکمه‌ها
    create_homepage()
    
    print("🚀 تمام عملیات با موفقیت انجام شد.")
