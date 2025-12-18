import os
import shutil

def clean_project():
    # مسیر جاری (ریشه پروژه)
    root_dir = os.getcwd()
    
    # نام همین فایل اسکریپت تا خودش را پاک نکند
    script_name = os.path.basename(__file__)

    # لیست سفید ریشه (چیزهایی که نباید پاک شوند)
    root_whitelist = [
        '.github',
        'tools',
        'index.html',
        script_name.lower()
    ]

    # لیست سفید داخل پوشه tools
    tools_whitelist = ['keep']

    print("🧹 شروع عملیات پاک‌سازی خودکار (بدون پرسش)...")

    # -----------------------------------------------------
    # 1. پاک‌سازی ریشه پروژه (Root)
    # -----------------------------------------------------
    for item_name in os.listdir(root_dir):
        item_path = os.path.join(root_dir, item_name)
        lower_name = item_name.lower()

        # بررسی استثنا برای فایل‌های Readme
        is_readme = lower_name.startswith('readme')
        
        # اگر جزو لیست سفید یا ریدمی است، رد شو
        if lower_name in root_whitelist or is_readme:
            print(f"   ✅ نگهداری شد: {item_name}")
            continue

        # حذف آیتم (فایل یا پوشه)
        try:
            if os.path.isfile(item_path) or os.path.islink(item_path):
                os.remove(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
            print(f"   🗑️ حذف شد: {item_name}")
        except Exception as e:
            print(f"   ❌ خطا در حذف {item_name}: {e}")

    # -----------------------------------------------------
    # 2. پاک‌سازی داخل پوشه tools
    # -----------------------------------------------------
    tools_dir = os.path.join(root_dir, 'tools')
    
    if os.path.exists(tools_dir) and os.path.isdir(tools_dir):
        print("\n📂 در حال پاک‌سازی پوشه tools...")
        for item_name in os.listdir(tools_dir):
            item_path = os.path.join(tools_dir, item_name)
            lower_name = item_name.lower()

            # اگر نام فایل keep است، نگه دار
            if lower_name in tools_whitelist:
                print(f"   ✅ نگهداری شد (در tools): {item_name}")
                continue

            # حذف آیتم‌های داخل tools
            try:
                if os.path.isfile(item_path) or os.path.islink(item_path):
                    os.remove(item_path)
                elif os.path.isdir(item_path):
                    shutil.rmtree(item_path)
                print(f"   🗑️ حذف شد (از tools): {item_name}")
            except Exception as e:
                print(f"   ❌ خطا در حذف {item_name}: {e}")
    else:
        print("\n⚠️ پوشه tools پیدا نشد.")

    print("\n✨ عملیات پاک‌سازی تمام شد.")

if __name__ == "__main__":
    # در محیط گیت‌هاب اکشن، سوال پرسیدن باعث ارور EOFError می‌شود
    # بنابراین تابع را مستقیم صدا می‌زنیم.
    clean_project()
