import os

def create_simple_camera_app():
    tool_dir = "tools/doorbin-tashkhis-harekat"
    file_path = os.path.join(tool_dir, "app.js")

    js_content = """
// انتخاب المان‌های صفحه
const video = document.getElementById('video');
const switchBtn = document.getElementById('switch-camera');
const statusElement = document.getElementById('status');

// متغیرهای وضعیت
let currentStream = null;
let facingMode = 'environment'; // پیش‌فرض: دوربین پشت (environment) - برای سلفی: 'user'

// تابع اصلی روشن کردن دوربین
async function startCamera() {
    // نمایش وضعیت به کاربر
    statusElement.innerText = 'در حال راه‌اندازی دوربین...';
    statusElement.style.color = 'yellow';

    // اگر قبلاً دوربینی روشن است، آن را خاموش کن (برای سوییچ کردن)
    if (currentStream) {
        currentStream.getTracks().forEach(track => {
            track.stop();
        });
    }

    // تنظیمات درخواست دوربین
    const constraints = {
        audio: false, // صدا نمی‌خواهیم
        video: {
            facingMode: facingMode, // جلو یا عقب
            width: { ideal: 640 },  // رزولوشن بهینه
            height: { ideal: 480 }
        }
    };

    try {
        // درخواست دسترسی به دوربین
        const stream = await navigator.mediaDevices.getUserMedia(constraints);
        currentStream = stream;
        video.srcObject = stream;
        
        // پخش ویدیو
        video.play();
        
        statusElement.innerText = 'دسترسی تأیید شد - دوربین فعال ✅';
        statusElement.style.color = '#0f0'; // سبز

    } catch (err) {
        console.error("Error accessing camera: ", err);
        statusElement.innerText = '❌ خطا: دسترسی به دوربین داده نشد یا موجود نیست.';
        statusElement.style.color = 'red';
        
        // جزئیات خطا برای دیباگ
        alert("خطا: " + err.name + " - " + err.message);
    }
}

// رویداد دکمه تغییر دوربین
switchBtn.addEventListener('click', () => {
    // تغییر حالت بین user و environment
    if (facingMode === 'user') {
        facingMode = 'environment';
    } else {
        facingMode = 'user';
    }
    
    // راه‌اندازی مجدد با حالت جدید
    startCamera();
});

// شروع خودکار برنامه هنگام لود شدن صفحه
window.addEventListener('load', () => {
    startCamera();
});
"""

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(js_content)

    print(f"✅ فایل app.js برای تست ساده دوربین ساخته شد.")

if __name__ == "__main__":
    create_simple_camera_app()
