import  os
import base64

# نام فایلی که در نهایت ساخته می‌شود
OUTPUT_FILENAME = "installer.py"

# پوشه‌ها و فایل‌هایی که نباید کپی شوند (برای جلوگیری از حجم زیاد یا کپی شدن خود اسکریپت)
IGNORE_DIRS = {'.git', '__pycache__', '.replit', '.upm', 'venv', 'node_modules'}
IGNORE_FILES = {OUTPUT_FILENAME, os.path.basename(__file__), '.DS_Store'}

def create_installer():
    # شروع نوشتن محتوای فایل نصبی
    # این متغیر حاوی کدی است که قرار است در سایت مقصد اجرا شود
    installer_content = [
        "import os",
        "import base64",
        "",
        "print('--- STARTING INSTALLATION ---')",
        "",
        "# This dictionary holds all file paths and their base64 encoded content",
        "files_data = {"
    ]

    print("Reading files and packing them...")
    
    # پیمایش تمام فایل‌های پوشه فعلی
    for root, dirs, files in os.walk("."):
        # حذف پوشه‌های ممنوعه از لیست پیمایش
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        
        for file in files:
            if file in IGNORE_FILES:
                continue
                
            file_path = os.path.join(root, file)
            # مسیر نسبی فایل (بدون ./)
            rel_path = os.path.relpath(file_path, ".")
            
            try:
                # خواندن فایل به صورت باینری (برای پشتیبانی از عکس و متن)
                with open(file_path, "rb") as f:
                    file_content = f.read()
                    # تبدیل به base64 برای قرار گرفتن در کد متنی
                    encoded_content = base64.b64encode(file_content).decode('utf-8')
                    
                # اضافه کردن به دیکشنری فایل نصبی
                installer_content.append(f'    "{rel_path}": "{encoded_content}",')
                print(f"Packed: {rel_path}")
                
            except Exception as e:
                print(f"Skipped {rel_path} due to error: {e}")

    # بستن دیکشنری و اضافه کردن کدهای استخراج (Extract)
    installer_content.append("}")
    installer_content.append("")
    installer_content.append("def install():")
    installer_content.append("    count = 0")
    installer_content.append("    for file_path, encoded_data in files_data.items():")
    installer_content.append("        try:")
    installer_content.append("            # Create directories if needed")
    installer_content.append("            dir_name = os.path.dirname(file_path)")
    installer_content.append("            if dir_name:")
    installer_content.append("                os.makedirs(dir_name, exist_ok=True)")
    installer_content.append("")
    installer_content.append("            # Write file content")
    installer_content.append("            with open(file_path, 'wb') as f:")
    installer_content.append("                f.write(base64.b64decode(encoded_data))")
    installer_content.append("            ")
    installer_content.append("            print(f'Created: {file_path}')")
    installer_content.append("            count += 1")
    installer_content.append("        except Exception as e:")
    installer_content.append("            print(f'Error creating {file_path}: {e}')")
    installer_content.append("")
    installer_content.append("    print(f'\\nSuccessfully installed {count} files.')")
    installer_content.append("")
    installer_content.append("if __name__ == '__main__':")
    installer_content.append("    install()")

    # نوشتن فایل نهایی installer.py
    with open(OUTPUT_FILENAME, "w", encoding="utf-8") as f:
        f.write("\n".join(installer_content))
    
    print(f"\nDone! The file '{OUTPUT_FILENAME}' has been created.")
    print("Copy the content of 'installer.py' and run it on the destination site.")

if __name__ == "__main__":
    create_installer()
