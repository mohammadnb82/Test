import os

def create_web_ready_folder():
    parent_folder = 'tools'
    # نام فینگلیش و استاندارد برای URL (با خط تیره)
    target_folder_name = 'doorbin-tashkhis-harekat'
    file_name = 'README.md'
    
    # مسیر کامل
    current_dir = os.getcwd()
    folder_path = os.path.join(current_dir, parent_folder, target_folder_name)
    file_path = os.path.join(folder_path, file_name)

    try:
        # ۱. ساخت پوشه فینگلیش
        os.makedirs(folder_path, exist_ok=True)
        print(f"✅ پوشه '{target_folder_name}' با موفقیت ساخته شد.")

        # ۲. ساخت فایل README.md
        # محتوایی داخلش می‌نویسیم تا خالی نباشد
        content = (
            f"# {target_folder_name}\n\n"
            "محل قرارگیری فایل‌های پروژه دوربین تشخیص حرکت.\n"
            "This folder contains the Motion Detection Camera project files.\n"
        )
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print(f"✅ فایل '{file_name}' ایجاد شد (پوشه اکنون توسط گیت شناسایی می‌شود).")

    except OSError as e:
        print(f"❌ خطا در عملیات: {e}")

if __name__ == "__main__":
    create_web_ready_folder()
