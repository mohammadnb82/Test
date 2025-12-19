import os

def apply_index_plus_foldername_convention():
print("🚀 Running naming convention fix: index_FolderName.html ...")

# Defining Paths
DIR_TOOLS = "tools"
DIR_CAMERA = "doorbin-tashkhis-harekat"

path_tools_dir = DIR_TOOLS
path_camera_dir = os.path.join(DIR_TOOLS, DIR_CAMERA)

# New File Names
NEW_CAMERA_FILE = f"index_{DIR_CAMERA}.html"  # index_doorbin-tashkhis-harekat.html
NEW_TOOLS_FILE = f"index_{DIR_TOOLS}.html"    # index_tools.html

# ---------------------------------------------------------
# 1. Fix Camera Folder (Rename index.html -> index_doorbin....html)
# ---------------------------------------------------------
print(f"\n🔹 Step 1: Fixing Camera Folder...")

if os.path.exists(path_camera_dir):
current_camera_path = os.path.join(path_camera_dir, "index.html")
target_camera_path = os.path.join(path_camera_dir, NEW_CAMERA_FILE)

if os.path.exists(current_camera_path):
try:
os.rename(current_camera_path, target_camera_path)
print(f"   ✅ Renamed: index.html -> {NEW_CAMERA_FILE}")
except Exception as e:
print(f"   ❌ Error renaming: {e}")
elif os.path.exists(target_camera_path):
print(f"   ℹ️ File already has correct name: {NEW_CAMERA_FILE}")
else:
print("   ⚠️ No index.html found in camera folder (maybe already renamed).")
else:
print(f"   ⚠️ Camera directory not found: {path_camera_dir}")

# ---------------------------------------------------------
# 2. Rebuild Tools File (index_tools.html)
# ---------------------------------------------------------
print(f"\n🔹 Step 2: Creating {NEW_TOOLS_FILE}...")

if not os.path.exists(path_tools_dir):
os.makedirs(path_tools_dir)

# Remove old confusing files
for old_file in ["index.html", "tools.html"]:
old_path = os.path.join(path_tools_dir, old_file)
if os.path.exists(old_path):
os.remove(old_path)
print(f"   🗑️ Removed old file: {old_file}")

# Correct link to camera
link_to_camera = f"{DIR_CAMERA}/{NEW_CAMERA_FILE}"

buttons_html = ""
for i in range(1, 21):
if i == 1:
buttons_html += f"""
<a href="{link_to_camera}" class="tool-btn active">
📷 دوربین تشخیص حرکت
</a>"""
else:
buttons_html += f"""
<div class="tool-btn disabled">
ابزار شماره {i}
</div>"""

tools_content = f"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>لیست ابزارها</title>
<style>
body {{ font-family: system-ui, -apple-system, sans-serif; background: #1a1a1a; color: white; padding: 20px; min-height: 100vh; display: flex; flex-direction: column; align-items: center; }}
h2 {{ margin-bottom: 30px; border-bottom: 2px solid #333; padding-bottom: 10px; }}
.grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(140px, 1fr)); gap: 15px; width: 100%; max-width: 800px; }}
.tool-btn {{ background: #333; color: #888; border: 1px solid #444; padding: 15px; border-radius: 12px; text-align: center; text-decoration: none; font-size: 14px; display: flex; align-items: center; justify-content: center; min-height: 80px; transition: 0.2s; cursor: default; }}
.tool-btn.active {{ background: #28a745; color: white; border-color: #1e7e34; cursor: pointer; font-weight: bold; font-size: 16px; box-shadow: 0 4px 10px rgba(40, 167, 69, 0.3); }}
.tool-btn.active:hover {{ background: #218838; transform: translateY(-2px); }}
.tool-btn.disabled {{ opacity: 0.5; }}
.back-link {{ margin-top: 40px; color: #aaa; text-decoration: none; padding: 10px 20px; border: 1px solid #444; border-radius: 8px; }}
.back-link:hover {{ background: #333; color: white; }}
</style>
</head>
<body>
<h2>🛠 جعبه ابزار (۲۰ آیتم)</h2>
<div class="grid">
{buttons_html}
</div>
<a href="../index.html" class="back-link">⬅️ بازگشت به صفحه اصلی</a>
</body>
</html>
"""
with open(os.path.join(path_tools_dir, NEW_TOOLS_FILE), "w", encoding="utf-8") as f:
f.write(tools_content)
print(f"   ✅ Created: {NEW_TOOLS_FILE}")


# ---------------------------------------------------------
# 3. Update Root File (index.html)
# ---------------------------------------------------------
print(f"\n🔹 Step 3: Updating Root index.html...")

# Correct link to tools
link_to_tools = f"{DIR_TOOLS}/{NEW_TOOLS_FILE}"

root_content = f"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>صفحه اصلی</title>
<style>
body {{ font-family: system-ui, -apple-system, sans-serif; background: #111; color: white; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; margin: 0; gap: 20px; }}
h1 {{ margin-bottom: 40px; }}
.menu-btn {{ background: #007bff; color: white; border: none; padding: 20px 40px; width: 80%; max-width: 300px; font-size: 20px; font-weight: bold; border-radius: 15px; cursor: pointer; text-decoration: none; display: flex; align-items: center; justify-content: center; transition: background 0.2s; box-shadow: 0 4px 15px rgba(0,123,255,0.3); }}
.menu-btn:hover {{ background: #0056b3; }}
.footer {{ margin-top: 50px; color: #666; font-size: 14px; }}
</style>
</head>
<body>
<h1>اپلیکیشن من</h1>

<a href="{link_to_tools}" class="menu-btn">
📂 ورود به ابزارها
</a>

<div class="footer">نسخه ۵.۰ - ساختار استاندارد</div>
</body>
</html>
"""
with open("index.html", "w", encoding="utf-8") as f:
f.write(root_content)
print("   ✅ Updated: Root index.html")
print("\n🎉 DONE. System is now using 'index_FolderName.html' convention.")

if __name__ == "__main__":
apply_index_plus_foldername_convention()

