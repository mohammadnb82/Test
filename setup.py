import os

target_file_path = "tools/doorbin-tashkhis-harekat/index_doorbin-tashkhis-harekat.html"

html_content = r"""<!DOCTYPE html>
<html lang="en" dir="ltr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
    <title>Smart Motion Camera</title>
    <style>
        body { 
            background-color: #121212; 
            color: white; 
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; 
            display: flex; 
            flex-direction: column; 
            align-items: center; 
            margin: 0; 
            padding: 10px; 
            height: 100vh;
            overflow: hidden;
        }

        .video-container {
            width: 100%;
            max-width: 600px;
            aspect-ratio: 4/3;
            background: #000;
            border-radius: 10px;
            overflow: hidden;
            position: relative;
            margin-bottom: 10px;
            border: 1px solid #333;
        }
        video { width: 100%; height: 100%; object-fit: cover; }
        canvas { display: none; }
        
        #alarmLayer {
            position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(255, 0, 0, 0.3);
            display: none; pointer-events: none; z-index: 5;
            box-shadow: inset 0 0 50px red;
        }

        .control-panel {
            width: 100%;
            max-width: 600px;
            background: #1e1e1e;
            padding: 15px;
            border-radius: 12px;
            box-sizing: border-box;
        }

        .motion-graph-wrapper {
            position: relative;
            margin-bottom: 5px;
        }
        
        .motion-track {
            height: 24px;
            background: #2c2c2e;
            position: relative;
            border-radius: 4px;
            overflow: hidden;
            border: 1px solid #333;
        }
        
        .motion-fill {
            height: 100%;
            width: 0%;
            background: #32d74b;
            transition: width 0.1s linear; /* Slightly smoother transition */
        }

        .threshold-line {
            position: absolute;
            top: 0;
            bottom: 0;
            width: 3px;
            background: #ff453a;
            z-index: 10;
            box-shadow: 0 0 4px rgba(255, 69, 58, 0.8);
        }

        .scale-numbers {
            display: flex;
            justify-content: space-between;
            color: #8e8e93;
            font-size: 11px;
            margin-top: 4px;
            padding: 0 2px;
        }

        .stats-row {
            display: flex;
            justify-content: space-between;
            margin: 12px 0;
            font-size: 15px;
            font-weight: bold;
        }
        .stat-item { display: flex; align-items: center; gap: 6px; }
        .text-red { color: #ff453a; }
        .text-green { color: #32d74b; }

        .slider-container {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 20px;
        }
        .slider-label { font-size: 14px; color: #aeaeb2; min-width: 80px; }
        
        input[type=range] {
            flex-grow: 1;
            height: 6px;
            border-radius: 3px;
            background: #3a3a3c;
            outline: none;
            -webkit-appearance: none;
        }
        input[type=range]::-webkit-slider-thumb {
            -webkit-appearance: none;
            width: 24px;
            height: 24px;
            background: white;
            border-radius: 50%;
            cursor: pointer;
            margin-top: -9px; 
            box-shadow: 0 2px 6px rgba(0,0,0,0.4);
        }
        input[type=range]::-webkit-slider-runnable-track {
            width: 100%;
            height: 6px;
            background: #0a84ff;
            border-radius: 3px;
        }

        .buttons-row {
            display: flex;
            gap: 12px;
        }

        .btn {
            padding: 14px;
            border: none;
            border-radius: 10px;
            font-size: 15px;
            font-weight: 600;
            cursor: pointer;
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            flex: 1;
        }

        .btn-cam { background: #3a3a3c; } 
        
        .btn-siren { background: #3a3a3c; color: #aaa; border: 1px solid #444; }
        .btn-siren.active { 
            background: #ff453a; 
            color: white; 
            border: none;
            animation: pulse-red 1.5s infinite;
        }

        @keyframes pulse-red {
            0% { box-shadow: 0 0 0 0 rgba(255, 69, 58, 0.4); }
            70% { box-shadow: 0 0 0 10px rgba(255, 69, 58, 0); }
            100% { box-shadow: 0 0 0 0 rgba(255, 69, 58, 0); }
        }

        .back-link {
            margin-top: 25px;
            color: #636366;
            text-decoration: none;
            font-size: 13px;
        }
    </style>
</head>
<body>

    <div class="video-container">
        <video id="video" autoplay playsinline muted></video>
        <div id="alarmLayer"></div>
    </div>
    <canvas id="canvas"></canvas>

    <div class="control-panel">
        
        <div class="motion-graph-wrapper">
            <div class="motion-track">
                <div id="motionFill" class="motion-fill"></div>
                <div id="threshLine" class="threshold-line" style="left: 20%;"></div>
            </div>
            <div class="scale-numbers">
                <span>0</span><span>20</span><span>40</span><span>60</span><span>80</span><span>100</span>
            </div>
        </div>

        <div class="stats-row">
            <span class="stat-item text-red">Threshold: <span id="threshText">20</span></span>
            <span class="stat-item text-green">Motion: <span id="motionText">0</span></span>
        </div>

        <div class="slider-container">
            <span class="slider-label">Sensitivity:</span>
            <input type="range" id="sensitivitySlider" min="1" max="100" value="20">
        </div>

        <div class="buttons-row">
            <button class="btn btn-cam" onclick="switchCamera()">
                🔄 Rotate Cam
            </button>
            <button id="sirenBtn" class="btn btn-siren" onclick="toggleSiren()">
                🔕 Siren OFF
            </button>
        </div>
    </div>

    <a href="../index_tools.html" class="back-link">← Back to Tools</a>

    <script>
        const video = document.getElementById('video');
        const canvas = document.getElementById('canvas');
        const ctx = canvas.getContext('2d');
        const alarmLayer = document.getElementById('alarmLayer');
        
        const motionFill = document.getElementById('motionFill');
        const threshLine = document.getElementById('threshLine');
        const threshText = document.getElementById('threshText');
        const motionText = document.getElementById('motionText');
        const slider = document.getElementById('sensitivitySlider');
        const sirenBtn = document.getElementById('sirenBtn');

        let stream = null;
        let facingMode = 'environment';
        let lastFrameData = null;
        let isSirenActive = false;
        
        // Audio System
        let audioCtx = null;
        let oscillator = null;
        let gainNode = null;
        let isBeeping = false;

        function initAudio() {
            if (!audioCtx) {
                audioCtx = new (window.AudioContext || window.webkitAudioContext)();
                oscillator = audioCtx.createOscillator();
                gainNode = audioCtx.createGain();
                oscillator.type = 'square';
                oscillator.frequency.value = 800; 
                gainNode.gain.value = 0;
                oscillator.connect(gainNode);
                gainNode.connect(audioCtx.destination);
                oscillator.start();
            }
            if (audioCtx.state === 'suspended') audioCtx.resume();
        }

        function startBeep() {
            if (gainNode && !isBeeping) {
                gainNode.gain.setTargetAtTime(0.3, audioCtx.currentTime, 0.05);
                oscillator.frequency.setValueAtTime(800, audioCtx.currentTime);
                oscillator.frequency.linearRampToValueAtTime(1200, audioCtx.currentTime + 0.1);
                isBeeping = true;
            }
        }

        function stopBeep() {
            if (gainNode && isBeeping) {
                gainNode.gain.setTargetAtTime(0, audioCtx.currentTime, 0.1);
                isBeeping = false;
            }
        }

        function toggleSiren() {
            isSirenActive = !isSirenActive;
            initAudio();
            if (isSirenActive) {
                sirenBtn.classList.add('active');
                sirenBtn.innerHTML = "🔔 Siren ON";
                startBeep(); setTimeout(stopBeep, 150);
            } else {
                sirenBtn.classList.remove('active');
                sirenBtn.innerHTML = "🔕 Siren OFF";
                stopBeep();
            }
        }

        slider.addEventListener('input', updateThreshold);

        function updateThreshold() {
            const val = parseInt(slider.value);
            threshText.innerText = val;
            threshLine.style.left = val + '%';
        }
        updateThreshold();

        async function startCamera() {
            if (stream) {
                stream.getTracks().forEach(t => t.stop());
            }
            try {
                stream = await navigator.mediaDevices.getUserMedia({ 
                    video: { facingMode: facingMode } 
                });
                video.srcObject = stream;
                // CRITICAL FIX: Reset frame memory to prevent crash on camera switch
                lastFrameData = null;
            } catch (err) {
                console.log("Camera Error: " + err);
                alert("Please enable camera access.");
            }
        }

        function switchCamera() {
            // Toggle camera mode
            facingMode = (facingMode === 'environment') ? 'user' : 'environment';
            // Force reset memory before starting new stream
            lastFrameData = null; 
            startCamera();
        }

        function processFrame() {
            if (video.readyState === 4) {
                try {
                    const w = 64; 
                    const h = 48;
                    // Ensure canvas is always set to correct size
                    if (canvas.width !== w) canvas.width = w;
                    if (canvas.height !== h) canvas.height = h;
                    
                    ctx.drawImage(video, 0, 0, w, h);
                    const currentData = ctx.getImageData(0, 0, w, h);
                    const data = currentData.data;

                    if (lastFrameData && lastFrameData.data.length === data.length) {
                        const oldData = lastFrameData.data;
                        let changedPixels = 0;
                        
                        for (let i = 0; i < data.length; i += 4) {
                            const rDiff = Math.abs(data[i] - oldData[i]);
                            const gDiff = Math.abs(data[i+1] - oldData[i+1]);
                            const bDiff = Math.abs(data[i+2] - oldData[i+2]);
                            
                            // Night Vision Threshold
                            if ((rDiff + gDiff + bDiff) > 20) {
                                changedPixels++;
                            }
                        }

                        const totalPixels = w * h;
                        // Calculate raw percentage
                        let rawPercent = (changedPixels / totalPixels) * 100;
                        
                        // Apply Sensitivity Multiplier (Boost)
                        // This allows small movements to register as high values
                        let finalScore = rawPercent * 6; 
                        
                        // Clamp to 0-100
                        if (finalScore > 100) finalScore = 100;
                        if (finalScore < 0) finalScore = 0;
                        
                        // Round for display
                        let displayVal = Math.floor(finalScore);

                        // SYNC FIX: Ensure Text and Graph are identical
                        motionText.innerText = displayVal;
                        motionFill.style.width = displayVal + '%';

                        const thresholdVal = parseInt(slider.value);
                        
                        if (displayVal > thresholdVal) {
                            alarmLayer.style.display = "block";
                            motionFill.style.background = "#ff453a"; 
                            if (isSirenActive) startBeep();
                        } else {
                            alarmLayer.style.display = "none";
                            motionFill.style.background = "#32d74b";
                            stopBeep();
                        }
                    }
                    lastFrameData = currentData;
                } catch(e) {
                    // Prevent loop crash
                    console.error("Frame skip:", e);
                    lastFrameData = null; 
                }
            }
            requestAnimationFrame(processFrame);
        }

        startCamera();
        video.addEventListener('play', processFrame);

    </script>
</body>
</html>"""

try:
    with open(target_file_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print("Success: Fixed sync mismatch and camera switch crash.")
except Exception as e:
    print("Error updating file: " + str(e))
