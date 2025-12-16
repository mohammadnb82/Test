import os

# Define the base directory for the project
base_dir = "tools/face_detection_camera"

# Create necessary directories
os.makedirs(os.path.join(base_dir, "css"), exist_ok=True)
os.makedirs(os.path.join(base_dir, "js"), exist_ok=True)

# ---------------------------------------------------------
# 1. HTML (index.html)
# ---------------------------------------------------------
html_content = """<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>تشخیص هوشمند چهره و بدن</title>
    
    <!-- CSS Styles -->
    <link rel="stylesheet" href="css/style.css">

    <!-- TensorFlow.js and Models (CDNs) -->
    <!-- Using specific versions for stability -->
    <script src="https://cdn.jsdelivr.net/npm/@tensorflow/tfjs@3.11.0/dist/tf.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@tensorflow-models/blazeface@0.0.7/dist/blazeface.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@tensorflow-models/posenet@2.2.2/dist/posenet.min.js"></script>
</head>
<body>

<div class="container">
    <header>
        <h1>📷 دوربین هوشمند</h1>
        <div id="status" class="status-badge">در انتظار شروع...</div>
    </header>

    <!-- Main Camera View -->
    <div class="camera-wrapper">
        <video id="video" autoplay playsinline muted></video>
        <canvas id="canvas"></canvas> <!-- Overlay for bounding boxes -->
    </div>

    <!-- Controls -->
    <div class="controls">
        <button id="startBtn" class="btn btn-primary">▶ شروع دوربین</button>
        <button id="stopBtn" class="btn btn-danger" disabled>⏹ توقف</button>
        <button id="clearBtn" class="btn btn-secondary">🗑 پاک کردن لیست</button>
    </div>

    <!-- Settings Toggles -->
    <div class="settings">
        <label class="toggle-switch">
            <input type="checkbox" id="saveToggle">
            <span class="slider"></span>
            <span class="label-text">💾 ذخیره تصاویر</span>
        </label>
        
        <label class="toggle-switch">
            <input type="checkbox" id="alarmToggle">
            <span class="slider"></span>
            <span class="label-text">🔔 صدای آژیر</span>
        </label>
    </div>

    <!-- Detection List -->
    <div class="gallery-section">
        <h3>مارد شناسایی شده</h3>
        <div id="facesList" class="gallery-grid">
            <!-- Detected items will appear here -->
        </div>
    </div>
</div>

<!-- Local Logic -->
<script src="js/app.js"></script>

</body>
</html>"""

# ---------------------------------------------------------
# 2. CSS (css/style.css)
# ---------------------------------------------------------
css_content = """/* General Reset */
* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

body {
    background-color: #f0f2f5;
    color: #333;
    padding: 20px;
    direction: rtl;
}

.container {
    max-width: 800px;
    margin: 0 auto;
    background: white;
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
}

header {
    text-align: center;
    margin-bottom: 20px;
}

h1 {
    font-size: 1.8rem;
    margin-bottom: 10px;
    color: #2c3e50;
}

/* Status Badge */
.status-badge {
    display: inline-block;
    padding: 6px 12px;
    border-radius: 20px;
    background-color: #e2e8f0;
    font-size: 0.9rem;
    color: #64748b;
    font-weight: bold;
}

/* Camera Area */
.camera-wrapper {
    position: relative;
    width: 100%;
    max-width: 640px;
    margin: 0 auto 20px;
    background: #000;
    border-radius: 12px;
    overflow: hidden;
    aspect-ratio: 4/3; /* Keeps a nice shape */
}

video {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
}

canvas {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none; /* Let clicks pass through */
}

/* Controls */
.controls {
    display: flex;
    justify-content: center;
    gap: 10px;
    margin-bottom: 20px;
    flex-wrap: wrap;
}

.btn {
    padding: 10px;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    font-size: 1rem;
    font-weight: bold;
    transition: transform 0.1s, opacity 0.2s;
}

.btn:active {
    transform: scale(0.96);
}

.btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

.btn-primary { background-color: #3b82f6; color: white; }
.btn-danger
