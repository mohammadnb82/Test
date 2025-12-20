import os
import shutil

# مسیر پوشه هدف
folder_path = "tools/doorbin-tashkhis-harekat"

# 1. عملیات پاک‌سازی (Wipe Out)
if os.path.exists(folder_path):
    # حذف تمام محتویات پوشه
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")
    print(f"All files in '{folder_path}' have been deleted.")
else:
    # اگر پوشه نبود، آن را بساز
    os.makedirs(folder_path)
    print(f"Directory '{folder_path}' created.")

# 2. ایجاد فایل جدید با کد بازنویسی شده (Clean Build)
html_file_path = os.path.join(folder_path, "index_doorbin-tashkhis-harekat.html")

html_content = r"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
    <title>Motion Detector Pro</title>
    <style>
        /* CSS Reset & Base Styles matching IMG_5701 */
        :root {
            --bg-color: #000000;
            --card-bg: #1c1c1e;
            --text-main: #ffffff;
            --text-sub: #8e8e93;
            --accent-red: #ff453a;
            --accent-green: #32d74b;
            --accent-blue: #0a84ff;
            --track-color: #3a3a3c;
        }

        body {
            background-color: var(--bg-color);
            color: var(--text-main);
            font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            margin: 0;
            padding: 15px;
            display: flex;
            flex-direction: column;
            align-items: center;
            height: 100vh;
            overflow: hidden;
            box-sizing: border-box;
        }

        /* Video Container */
        .video-box {
            width: 100%;
            max-width: 500px;
            aspect-ratio: 4/3;
            background: #111;
            border-radius: 12px;
            overflow: hidden;
            position: relative;
            margin-bottom: 15px;
            border: 1px solid #333;
            box-shadow: 0 4px 20px rgba(0,0,0,0.5);
        }

        video {
            width: 100%;
            height: 100%;
            object-fit: cover;
            display: block;
        }

        /* Red Flash Overlay */
        #alarm-flash {
            position: absolute; inset: 0;
            background: rgba(255, 69, 58, 0.4);
            display: none;
            z-index: 10;
            box-shadow: inset 0 0 50px var(--accent-red);
        }

        /* Control Card */
        .controls-card {
            width: 100%;
            max-width: 500px;
            background: var(--card-bg);
            padding: 20px;
            border-radius: 16px;
            display: flex;
            flex-
