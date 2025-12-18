import os

def create_motion_detection_folder():
    # نام پوشه والد و هدف
    parent_folder = 'tools'
    target_folder_name = 'دوربین تشخیص حرکت'
    
    # ساخت مسیر کامل
    current_dir = os.getcwd()
    full_path = os.path.join(current_dir, parent_folder, target_folder_name)

    try:
        # ساخت پوشه (اگر پوشه tools هم نباشد، آن را می‌سازد)
        os.makedirs(full_path, exist_ok=True)
        
        print(f"✅ پوشه '{target_folder_name}' با موفقیت در داخل '{parent_folder}' ساخته شد.")
        print(f"📂 مسیر کامل: {full_path}")
        
    except OSError as e:
        print(f"❌ خطا در ساخت پوشه: {e}")

if __name__ == "__main__":
    create_motion_detection_folder()
