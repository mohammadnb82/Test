import os
import shutil

def remove_persian_folder():
    parent_folder = 'tools'
    folder_to_remove = 'دوربین تشخیص حرکت' # نام پوشه قدیمی فارسی
    
    current_dir = os.getcwd()
    path_to_remove = os.path.join(current_dir, parent_folder, folder_to_remove)

    if os.path.exists(path_to_remove):
        try:
            # دستور rmtree کل پوشه و محتویات داخلش را پاک می‌کند
            shutil.rmtree(path_to_remove)
            print(f"✅ پوشه قدیمی '{folder_to_remove}' با موفقیت و کامل حذف شد.")
        except OSError as e:
            print(f"❌ خطا در حذف پوشه: {e}")
    else:
        print(f"ℹ️ پوشه '{folder_to_remove}' وجود ندارد (شاید قبلاً پاک شده است).")

if __name__ == "__main__":
    remove_persian_folder()
