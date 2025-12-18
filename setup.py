import os

def create_folder_with_gitkeep():
    # مسیرها
    parent_folder = 'tools'
    target_folder_name = 'دوربین تشخیص حرکت'
    keep_file_name = '.gitkeep'  # فایلی که باعث می‌شود پوشه در گیت دیده شود
    
    current_dir = os.getcwd()
    folder_path = os.path.join(current_dir, parent_folder, target_folder_name)
    file_path = os.path.join(folder_path, keep_file_name)

    try:
        # ۱. ساخت پوشه (اگر نباشد)
        os.makedirs(folder_path, exist_ok=True)
        print(f"✅ پوشه '{target_folder_name}' ساخته شد.")

        # ۲. ساخت فایل نگهدارنده داخل پوشه
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                pass # ساخت فایل خالی
            print(f"✅ فایل مخفی '{keep_file_name}' داخل پوشه ساخته شد (تا گیت پوشه را ببیند).")
        else:
            print(f"ℹ️ فایل '{keep_file_name}' از قبل وجود دارد.")

    except OSError as e:
        print(f"❌ خطا: {e}")

if __name__ == "__main__":
    create_folder_with_gitkeep()
