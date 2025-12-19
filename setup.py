import re
import os

def quick_fix_direction():
    path = "tools/doorbin-tashkhis-harekat/index.html"
    
    if not os.path.exists(path):
        print("فایل پیدا نشد.")
        return

    with open(path, "r", encoding="utf-8") as f:
        html = f.read()

    # پیدا کردن استایل #motion-bar-container و اضافه کردن direction: ltr به انتهای آن
    # این کد دنبال آکولاد بسته } در استایل مربوطه می‌گردد و خط جدید را قبل از آن اضافه می‌کند
    pattern = r"(#motion-bar-container\s*\{[^}]*)(\})"
    replacement = r"\1    direction: ltr;\n        \2"
    
    new_html = re.sub(pattern, replacement, html)

    with open(path, "w", encoding="utf-8") as f:
        f.write(new_html)

    print("✅ فقط جهت نوار سبز (motion-bar) به چپ-به-راست تغییر کرد.")

if __name__ == "__main__":
    quick_fix_direction()
