let video, canvas, ctx;
let blazefaceModel, posenetModel;
let isRunning = false;
let detectionCount = 0;
let savedImages = [];
let alarmEnabled = false;
let saveEnabled = false;
let sensitivity = 0.5;

async function init() {
    video = document.getElementById('video');
    canvas = document.getElementById('canvas');
    ctx = canvas.getContext('2d');

    document.getElementById('startBtn').addEventListener('click', startCamera);
    document.getElementById('stopBtn').addEventListener('click', stopCamera);
    document.getElementById('alarmToggle').addEventListener('change', (e) => {
        alarmEnabled = e.target.checked;
    });
    document.getElementById('saveToggle').addEventListener('change', (e) => {
        saveEnabled = e.target.checked;
    });
    document.getElementById('sensitivity').addEventListener('input', (e) => {
        sensitivity = parseFloat(e.target.value);
        document.getElementById('sensitivityValue').textContent = sensitivity;
    });

    await loadModels();
    loadSavedImages();
}

async function loadModels() {
    try {
        document.getElementById('systemStatus').textContent = 'در حال بارگذاری مدل‌ها...';
        blazefaceModel = await blazeface.load();
        posenetModel = await posenet.load({
            architecture: 'MobileNetV1',
            outputStride: 16,
            multiplier: 0.75
        });
        document.getElementById('systemStatus').textContent = 'آماده';
        console.log('✓ Models loaded successfully');
    } catch (error) {
        console.error('Error loading models:', error);
        document.getElementById('systemStatus').textContent = 'خطا در بارگذاری';
    }
}

async function startCamera() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({
            video: {
                facingMode: 'user',
                width: { ideal: 640 },
                height: { ideal: 480 }
            },
            audio: false
        });

        video.srcObject = stream;
        
        video.onloadedmetadata = () => {
            video.play();
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            isRunning = true;
            document.getElementById('startBtn').disabled = true;
            document.getElementById('stopBtn').disabled = false;
            document.getElementById('systemStatus').textContent = 'فعال';
            detectFrame();
        };
    } catch (error) {
        console.error('Camera error:', error);
        alert('خطا در دسترسی به دوربین!');
    }
}

function stopCamera() {
    isRunning = false;
    if (video.srcObject) {
        video.srcObject.getTracks().forEach(track => track.stop());
    }
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    document.getElementById('startBtn').disabled = false;
    document.getElementById('stopBtn').disabled = true;
    document.getElementById('systemStatus').textContent = 'غیرفعال';
}

async function detectFrame() {
    if (!isRunning) return;

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    let detectionMade = false;

    // Face Detection
    const faces = await blazefaceModel.estimateFaces(video, false);
    if (faces.length > 0) {
        faces.forEach(face => {
            if (face.probability && face.probability[0] > sensitivity) {
                const start = face.topLeft;
                const end = face.bottomRight;
                const size = [end[0] - start[0], end[1] - start[1]];

                ctx.strokeStyle = '#00ff00';
                ctx.lineWidth = 3;
                ctx.strokeRect(start[0], start[1], size[0], size[1]);

                ctx.fillStyle = '#00ff00';
                ctx.font = '16px Arial';
                ctx.fillText('👤 چهره', start[0], start[1] - 10);

                detectionMade = true;
            }
        });
    }

    // Body Detection
    const poses = await posenetModel.estimateSinglePose(video, {
        flipHorizontal: false
    });

    if (poses.score > sensitivity) {
        poses.keypoints.forEach(keypoint => {
            if (keypoint.score > sensitivity) {
                ctx.beginPath();
                ctx.arc(keypoint.position.x, keypoint.position.y, 5, 0, 2 * Math.PI);
                ctx.fillStyle = '#ff0000';
                ctx.fill();
            }
        });

        ctx.fillStyle = '#ff0000';
        ctx.font = '16px Arial';
        ctx.fillText('🚶 بدن', 10, 30);

        detectionMade = true;
    }

    if (detectionMade) {
        detectionCount++;
        document.getElementById('detectionCount').textContent = detectionCount;

        if (alarmEnabled) {
            playAlarm();
        }

        if (saveEnabled) {
            saveImage();
        }
    }

    requestAnimationFrame(detectFrame);
}

function playAlarm() {
    // Simple beep using Web Audio API
    const audioContext = new (window.AudioContext || window.webkitAudioContext)();
    const oscillator = audioContext.createOscillator();
    const gainNode = audioContext.createGain();

    oscillator.connect(gainNode);
    gainNode.connect(audioContext.destination);

    oscillator.frequency.value = 800;
    oscillator.type = 'sine';

    gainNode.gain.setValueAtTime(0.3, audioContext.currentTime);
    gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.5);

    oscillator.start(audioContext.currentTime);
    oscillator.stop(audioContext.currentTime + 0.5);
}

async function saveImage() {
    const tempCanvas = document.createElement('canvas');
    tempCanvas.width = video.videoWidth;
    tempCanvas.height = video.videoHeight;
    const tempCtx = tempCanvas.getContext('2d');
    tempCtx.drawImage(video, 0, 0);

    const imageData = tempCanvas.toDataURL('image/jpeg');
    const timestamp = new Date().toISOString();

    try {
        const response = await fetch('/save_image', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                image: imageData,
                timestamp: timestamp
            })
        });

        if (response.ok) {
            const result = await response.json();
            addImageToGallery(result.filename, timestamp);
            document.getElementById('savedCount').textContent = savedImages.length;
        }
    } catch (error) {
        console.error('Error saving image:', error);
    }
}

function addImageToGallery(filename, timestamp) {
    savedImages.push({ filename, timestamp });

    const gallery = document.getElementById('imageGallery');
    const item = document.createElement('div');
    item.className = 'gallery-item';
    item.innerHTML = `
        <img src="/saved_images/${filename}" alt="Detection">
        <button class="delete-btn" onclick="deleteImage('${filename}')">×</button>
        <div class="type-badge">${new Date(timestamp).toLocaleString('fa-IR')}</div>
    `;
    gallery.insertBefore(item, gallery.firstChild);
}

async function deleteImage(filename) {
    try {
        const response = await fetch(`/delete_image/${filename}`, {
            method: 'DELETE'
        });

        if (response.ok) {
            savedImages = savedImages.filter(img => img.filename !== filename);
            document.getElementById('savedCount').textContent = savedImages.length;
            loadSavedImages();
        }
    } catch (error) {
        console.error('Error deleting image:', error);
    }
}

async function loadSavedImages() {
    try {
        const response = await fetch('/list_images');
        const images = await response.json();
        
        const gallery = document.getElementById('imageGallery');
        gallery.innerHTML = '';
        
        images.forEach(img => {
            addImageToGallery(img.filename, img.timestamp);
        });
        
        savedImages = images;
        document.getElementById('savedCount').textContent = images.length;
    } catch (error) {
        console.error('Error loading images:', error);
    }
}

window.addEventListener('load', init);