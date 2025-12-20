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
            flex-direction: column;
            gap: 15px;
        }

        /* 1. Motion Graph Area */
        .graph-wrapper {
            position: relative;
            height: 45px; /* Taller for better visibility */
            background: #2c2c2e;
            border-radius: 8px;
            overflow: hidden;
            margin-bottom: 5px;
        }

        .motion-bar {
            height: 100%;
            width: 0%; /* Dynamic */
            background: var(--accent-green);
            transition: width 0.1s linear; /* Smooth movement */
            opacity: 0.8;
        }

        .threshold-line {
            position: absolute;
            top: 0; bottom: 0;
            width: 4px;
            background: var(--accent-red);
            box-shadow: 0 0 8px rgba(255, 69, 58, 0.8);
            z-index: 5;
            transform: translateX(-50%); /* Center perfectly on value */
            left: 40%; /* Dynamic */
        }

        /* Ruler/Scale Numbers */
        .ruler {
            display: flex;
            justify-content: space-between;
            color: var(--text-sub);
            font-size: 11px;
            padding: 0 2px;
            margin-top: -10px;
            font-weight: 500;
        }

        /* 2. Stats Row */
        .stats-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-weight: 700;
            font-size: 15px;
        }
        .stat-left { color: var(--accent-red); }
        .stat-right { color: var(--accent-green); }

        /* 3. Slider */
        .slider-container {
            display: flex;
            flex-direction: column;
            gap: 8px;
        }
        .slider-label {
            color: var(--text-sub);
            font-size: 13px;
        }
        
        /* Custom Range Slider Styling */
        input[type=range] {
            -webkit-appearance: none;
            width: 100%;
            background: transparent;
        }
        input[type=range]:focus { outline: none; }
        
        /* The Track */
        input[type=range]::-webkit-slider-runnable-track {
            width: 100%;
            height: 6px;
            background: var(--accent-blue);
            border-radius: 3px;
            cursor: pointer;
        }
        /* The Thumb (Handle) */
        input[type=range]::-webkit-slider-thumb {
            -webkit-appearance: none;
            height: 24px;
            width: 24px;
            border-radius: 50%;
            background: #ffffff;
            cursor: pointer;
            margin-top: -9px; /* Centers thumb on track */
            box-shadow: 0 2px 6px rgba(0,0,0,0.4);
        }

        /* 4. Action Buttons */
        .buttons-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 12px;
            margin-top: 10px;
        }

        .btn {
            border: none;
            padding: 16px;
            border-radius: 12px;
            font-size: 15px;
            font-weight: 600;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            transition: transform 0.1s;
        }
        .btn:active { transform: scale(0.98); }

        .btn-grey {
            background: #3a3a3c;
            color: white;
        }
        
        .btn-red {
            background: #3a3a3c; /* Default OFF state */
            color: #ccc;
            border: 1px solid #444;
        }
        
        /* Active Siren State */
        .btn-red.active {
            background: var(--accent-red);
            color: white;
            border: none;
            box-shadow: 0 0 15px rgba(255, 69, 58, 0.4);
        }

        .back-link {
            margin-top: auto;
            color: var(--text-sub);
            text-decoration: none;
            font-size: 13px;
            padding-bottom: 20px;
        }

        /* Hidden processing canvas */
        canvas { display: none; }

    </style>
</head>
<body>

    <!-- VIDEO SECTION -->
    <div class="video-box">
        <video id="webcam" autoplay playsinline muted></video>
        <div id="alarm-flash"></div>
    </div>
    
    <!-- Hidden Canvas for Pixel Processing -->
    <canvas id="proc-canvas"></canvas>

    <!-- CONTROLS SECTION -->
    <div class="controls-card">
        
        <!-- Graph -->
        <div>
            <div class="graph-wrapper">
                <div id="bar-motion" class="motion-bar"></div>
                <div id="line-thresh" class="threshold-line"></div>
            </div>
            <div class="ruler">
                <span>0</span><span>20</span><span>40</span><span>60</span><span>80</span><span>100</span>
            </div>
        </div>

        <!-- Stats -->
        <div class="stats-row">
            <span class="stat-left">Threshold: <span id="txt-thresh">40</span></span>
            <span class="stat-right">Motion: <span id="txt-motion">0</span></span>
        </div>

        <!-- Slider -->
        <div class="slider-container">
            <span class="slider-label">Threshold Adjustment</span>
            <input type="range" id="input-slider" min="0" max="100" value="40">
        </div>

        <!-- Buttons -->
        <div class="buttons-grid">
            <button class="btn btn-grey" onclick="rotateCamera()">
                🔄 Rotate Cam
            </button>
            <button id="btn-siren" class="btn btn-red" onclick="toggleSiren()">
                🔕 Siren OFF
            </button>
        </div>

    </div>

    <a href="../index_tools.html" class="back-link">← Back to Tools</a>

    <!-- LOGIC ENGINE -->
    <script>
        /**
         * GLOBAL CONFIGURATION
         */
        const CONF = {
            procWidth: 64,  // Low resolution for fast processing
            procHeight: 48,
            pixelDiffThreshold: 15, // Sensitivity per pixel (Lower = more sensitive in dark)
            motionGain: 4,  // Multiplier to make bar fill up easier
        };

        // DOM Elements
        const video = document.getElementById('webcam');
        const canvas = document.getElementById('proc-canvas');
        const ctx = canvas.getContext('2d', { willReadFrequently: true });
        const alarmFlash = document.getElementById('alarm-flash');
        
        // UI Elements
        const barMotion = document.getElementById('bar-motion');
        const lineThresh = document.getElementById('line-thresh');
        const txtThresh = document.getElementById('txt-thresh');
        const txtMotion = document.getElementById('txt-motion');
        const slider = document.getElementById('input-slider');
        const btnSiren = document.getElementById('btn-siren');

        // State
        let stream = null;
        let facingMode = 'environment'; // Start with back camera
        let lastFrameData = null;
        let isSirenActive = false;
        let isLoopRunning = false;
        
        // Audio Context
        let audioCtx = null;

        // --- 1. INITIALIZATION ---
        
        function init() {
            canvas.width = CONF.procWidth;
            canvas.height = CONF.procHeight;
            updateThresholdUI(slider.value); // Sync initial state
            startCamera();
        }

        // --- 2. CAMERA LOGIC ---

        async function startCamera() {
            // Stop existing stream
            if (stream) {
                stream.getTracks().forEach(track => track.stop());
            }

            try {
                stream = await navigator.mediaDevices.getUserMedia({
                    video: { 
                        facingMode: facingMode,
                        width: { ideal: 640 },
                        height: { ideal: 480 }
                    },
                    audio: false
                });
                video.srcObject = stream;
                
                // Clear memory so we don't compare new camera frame with old camera frame
                lastFrameData = null;

                if (!isLoopRunning) {
                    isLoopRunning = true;
                    requestAnimationFrame(processLoop);
                }

            } catch (err) {
                console.error("Camera Error:", err);
                alert("Error accessing camera. Please allow permissions.");
            }
        }

        function rotateCamera() {
            facingMode = (facingMode === 'environment') ? 'user' : 'environment';
            lastFrameData = null; // Important: Reset baseline
            startCamera();
        }

        // --- 3. CORE PROCESSING LOOP (The Engine) ---

        function processLoop() {
            if (video.readyState === 4) {
                try {
                    // Draw video to small canvas
                    ctx.drawImage(video, 0, 0, CONF.procWidth, CONF.procHeight);
                    
                    // Get raw pixel data
                    const frame = ctx.getImageData(0, 0, CONF.procWidth, CONF.procHeight);
                    const data = frame.data;
                    const dataLength = data.length;

                    if (lastFrameData) {
                        const prevData = lastFrameData.data;
                        let changedPixels = 0;
                        let r, g, b, pr, pg, pb, diff;

                        // Loop through pixels (R, G, B, A) - Step by 4
                        for (let i = 0; i < dataLength; i += 4) {
                            r = data[i]; g = data[i+1]; b = data[i+2];
                            pr = prevData[i]; pg = prevData[i+1]; pb = prevData[i+2];

                            // Calculate difference sum
                            diff = Math.abs(r - pr) + Math.abs(g - pg) + Math.abs(b - pb);

                            // If difference exceeds threshold, count it as motion
                            if (diff > CONF.pixelDiffThreshold) {
                                changedPixels++;
                            }
                        }

                        // Calculate Motion Score (0 - 100)
                        const totalPixels = CONF.procWidth * CONF.procHeight;
                        let rawPercentage = (changedPixels / totalPixels) * 100;
                        
                        // Apply Gain (Amplification)
                        // Because raw motion is usually 1-5%, we multiply to make it visible on 0-100 scale
                        let displayScore = Math.floor(rawPercentage * CONF.motionGain);
                        
                        // Clamp between 0 and 100
                        if (displayScore > 100) displayScore = 100;

                        // UPDATE UI
                        updateMotionUI(displayScore);

                        // CHECK ALARM
                        checkAlarm(displayScore);
                    }

                    // Save current frame as next reference
                    lastFrameData = frame;

                } catch (e) {
                    console.warn("Frame skipped", e);
                    lastFrameData = null; // Reset on error
                }
            }
            
            // Repeat
            requestAnimationFrame(processLoop);
        }

        // --- 4. UI SYNC & ALARM LOGIC ---

        // Called when slider moves
        slider.addEventListener('input', (e) => {
            updateThresholdUI(e.target.value);
        });

        function updateThresholdUI(val) {
            // Visual Sync: Slider 50 = Line at 50%
            lineThresh.style.left = val + '%';
            txtThresh.innerText = val;
        }

        function updateMotionUI(score) {
            // Visual Sync: Motion 50 = Bar width 50%
            barMotion.style.width = score + '%';
            txtMotion.innerText = score;
        }

        function checkAlarm(motionScore) {
            const threshold = parseInt(slider.value);
            
            // Logic: If Motion >= Threshold -> TRIGGER
            if (motionScore >= threshold && threshold > 0) {
                // Visual Trigger
                barMotion.style.background = '#ff453a'; // Red bar
                if (isSirenActive) {
                    alarmFlash.style.display = 'block';
                    playSirenSound();
                }
            } else {
                // Normal State
                barMotion.style.background = '#32d74b'; // Green bar
                alarmFlash.style.display = 'none';
            }
        }

        // --- 5. AUDIO SYSTEM (Self-Contained) ---

        function toggleSiren() {
            if (!audioCtx) {
                audioCtx = new (window.AudioContext || window.webkitAudioContext)();
            }
            
            if (audioCtx.state === 'suspended') {
                audioCtx.resume();
            }

            isSirenActive = !isSirenActive;

            if (isSirenActive) {
                btnSiren.classList.add('active');
                btnSiren.innerHTML = "🔔 Siren ON";
                // Play a short chirp to confirm
                playSirenSound(0.1); 
            } else {
                btnSiren.classList.remove('active');
                btnSiren.innerHTML = "🔕 Siren OFF";
                alarmFlash.style.display = 'none';
            }
        }

        // Generate a digital beep using Web Audio API
        function playSirenSound(duration = 0.15) {
            if (!audioCtx) return;

            const osc = audioCtx.createOscillator();
            const gainNode = audioCtx.createGain();

            osc.type = 'square'; // Harsh sound for alarm
            osc.frequency.setValueAtTime(800, audioCtx.currentTime);
            osc.frequency.linearRampToValueAtTime(1200, audioCtx.currentTime + duration); // Pitch up

            gainNode.gain.setValueAtTime(0.1, audioCtx.currentTime);
            gainNode.gain.linearRampToValueAtTime(0, audioCtx.currentTime + duration);

            osc.connect(gainNode);
            gainNode.connect(audioCtx.destination);

            osc.start();
            osc.stop(audioCtx.currentTime + duration);
        }

        // Start App
        init();

    </script>
</body>
</html>"""

# نوشتن فایل
try:
    with open(html_file_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Success: File created at {html_file_path}")
except Exception as e:
    print(f"Error writing file: {e}")
