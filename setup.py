import os

def create_tools_structure():
    # مسیر پوشه و فایل
    folder_name = 'tools'
    file_name = 'keep'
    
    # آدرس کامل
    current_dir = os.getcwd()
    folder_path = os.path.join(current_dir, folder_name)
    file_path = os.path.join(folder_path, file_name)

    # ۱. ساخت پوشه tools
    if not os.path.exists(folder_path):
        try:
            os.makedirs(folder_path)
            print(f"✅ پوشه '{folder_name}' با موفقیت ساخته شد.")
        except OSError as e:
            print(f"❌ خطا در ساخت پوشه: {e}")
            return
    else:
        print(f"ℹ️ پوشه '{folder_name}' از قبل وجود دارد.")

    # ۲. ساخت فایل keep
    if not os.path.exists(file_path):
        try:
            # ایجاد یک فایل خالی
            with open(file_path, 'w') as fp:
                pass 
            print(f"✅ فایل '{file_name}' داخل پوشه ساخته شد.")
        except IOError as e:
            print(f"❌ خطا در ساخت فایل: {e}")
    else:
        print(f"ℹ️ فایل '{file_name}' از قبل وجود دارد.")

if __name__ == "__main__":
    create_tools_structure()
