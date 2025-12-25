// This script combines all logic (State machine, Hardening, Recovery)
// The structure reflects the internal modularization achieved in the last cycles.

const logEl = document.getElementById("log");
const video = document.getElementById("cam");
const statusEl = document.getElementById("status-display");
const storageEl = document.getElementById("storage-status");
const modeBtn = document.getElementById("mode-btn");

// Global State Management (Hardening T1)
const STATES = {
    INIT: 'INIT',
    WATCHING: 'WATCHING',
    ALERTING: 'ALERTING',
    RECORDING: 'RECORDING',
    COOLDOWN: 'COOLDOWN',
    FAILSAFE: 'FAILSAFE'
};

const App = {
    STATE: STATES.INIT,
    stream: null,
    facing: localStorage.getItem('cam_facing') || "environment",
    mode: localStorage.getItem('cam_mode') || "balanced", // power (3s interval) or balanced (1s interval)
    coco: null,
    processingInterval: null,
    lastFrameData: null,
    isTabActive: true,
    isRecording: false,

    log(msg){
        const timestamp = new Date().toLocaleTimeString('fa');
        logEl.textContent = `[${timestamp}] ${msg}\n` + logEl.textContent;
        // Keep log scrollable (limited length for performance)
        const lines = logEl.textContent.split('\n');
        if (lines.length > 50) {
            logEl.textContent = lines.slice(0, 50).join('\n');
        }
    },

    setState(newState) {
        if (this.STATE === newState) return;
        this.STATE = newState;
        statusEl.textContent = newState;
        statusEl.className = newState;
        this.log(`وضعیت جدید: ${newState}`);
    },

    // Hardening T5: Configuration Persistence
    toggleMode() {
        this.mode = this.mode === "balanced" ? "power" : "balanced";
        localStorage.setItem('cam_mode', this.mode);
        modeBtn.textContent = `حالت: ${this.mode === 'power' ? 'Power Saving' : 'Balanced'}`;
        this.log(`Mode Changed to: ${this.mode}`);
    },

    // Hardening T8: Permission and Startup
    async start(){
        if(this.STATE !== STATES.INIT) return;
        this.log("شروع فرآیند...");

        try {
            await this.startCamera();
            await this.loadAI();
            this.watch();
            this.setupListeners();
            this.setState(STATES.WATCHING);
        } catch(e) {
            this.log(`❌ خطای شروع: ${e.name}. دسترسی دوربین را بررسی کنید.`);
            this.setState(STATES.FAILSAFE);
        }
    },

    // Hardening T4: Auto-Recovery
    async startCamera(){
        if(this.stream) this.stream.getTracks().forEach(t=>t.stop());
        const constraints = {
            video: { facingMode: this.facing },
            audio: false
        };
        this.stream = await navigator.mediaDevices.getUserMedia(constraints);
        video.srcObject = this.stream;
        video.onloadedmetadata = () => video.play();
    },

    switchCamera(){
        this.facing = this.facing === "user" ? "environment" : "user";
        localStorage.setItem('cam_facing', this.facing);
        this.log(`سوئیچ دوربین به ${this.facing}`);
        this.startCamera().catch(e => this.log(`❌ خطا در سوئیچ: ${e.message}`));
    },

    // Hardening T6: Graceful Degradation
    async loadAI(){
        this.log("بارگذاری مدل‌ها...");
        try {
            this.coco = await cocoSsd.load();
            this.log("مدل COCO-SSD بارگذاری شد.");
            // Face-API load logic omitted for brevity, assumed loaded via CDN
        } catch(e) {
            this.log("⚠️ هشدار: خطای بارگذاری AI. پایش فقط بر اساس حرکت انجام می‌شود.");
            this.coco = false; // Set to false to trigger graceful degradation
        }
    },

    // Hardening T2: Throttling & Visibility
    setupListeners() {
        document.addEventListener('visibilitychange', () => {
            this.isTabActive = document.visibilityState === 'visible';
            this.log(`تب فعال است: ${this.isTabActive}`);
            // If tab goes inactive, throttle down performance
        });

        // Hardening T3: Storage Quota Check
        if (navigator.storage && navigator.storage.estimate) {
            setInterval(async () => {
                const estimate = await navigator.storage.estimate();
                const used = (estimate.usage / (1024 * 1024)).toFixed(1);
                const quota = (estimate.quota / (1024 * 1024)).toFixed(1);
                storageEl.textContent = `${used}MB / ${quota}MB`;
            }, 60000); // Check every minute
        }
    },

    watch(){
        const canvas = document.getElementById("motion-canvas");
        const ctx = canvas.getContext("2d");

        const processFrame = async () => {
            if (this.STATE === STATES.COOLDOWN || !this.stream || !video.readyState >= 2) {
                // If camera stream is broken, attempt recovery (Hardening T4)
                if(this.stream && !this.stream.active) {
                    this.log("🚨 جریان دوربین قطع شد! تلاش برای بازیابی...");
                    this.setState(STATES.FAILSAFE);
                    setTimeout(() => this.startCamera().then(() => this.setState(STATES.WATCHING)), 10000);
                    return;
                }
                // Use a slower interval if cooling down
                setTimeout(processFrame, 5000); 
                return;
            }

            // Adaptive interval based on mode and visibility (Hardening T2)
            let interval = this.mode === 'power' ? 300 : 100; // Motion check interval in ms
            if (!this.isTabActive) interval = 500; // Even slower if in background

            // ------------------
            // Motion Detection (T3 refinement: Downscale, Grayscale)
            // ------------------
            canvas.width = 64; // Downscale
            canvas.height = 48;

            ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
            const currentFrame = ctx.getImageData(0, 0, canvas.width, canvas.height);
            let motion = false;

            if (this.lastFrameData) {
                let diff = 0;
                for (let i = 0; i < currentFrame.data.length; i += 4) {
                    // Simple pixel difference (R channel check)
                    if (Math.abs(currentFrame.data[i] - this.lastFrameData.data[i]) > 30) {
                        diff++;
                    }
                }
                // Threshold refined for downscaled image
                motion = diff > 30; 
            }
            this.lastFrameData = currentFrame;

            if (motion) {
                this.log("🚨 حرکت شناسایی شد!");
                this.setState(STATES.ALERTING);

                // ------------------
                // AI Detection (T5 refinement: AI only on motion)
                // ------------------
                if (this.coco) {
                    const predictions = await this.coco.detect(video);
                    const personDetected = predictions.some(p => p.class === "person" && p.score > 0.6);

                    if (personDetected) {
                        this.log("👤 شخص شناسایی شد! واکنش فعالسازی...");
                        this.beep();
                        this.record();
                        this.setState(STATES.RECORDING);
                    } else {
                        // Return to watching if motion was noise
                        this.setState(STATES.WATCHING);
                    }
                } else {
                    // Fallback: If no AI, motion is enough to beep/record (Hardening T6)
                    this.beep();
                    this.record();
                    this.setState(STATES.RECORDING);
                }
            } else if (this.STATE === STATES.ALERTING || this.STATE === STATES.RECORDING) {
                 // Return to watching after an event if no new motion
                 this.setState(STATES.WATCHING);
            }

            // Loop using setTimeout for better throttling control than setInterval
            setTimeout(processFrame, interval);
        };

        // Start the continuous processing loop
        setTimeout(processFrame, 100);
    },

    // Hardening T7: Robust Recording and Cooldown
    record(){
        if(this.isRecording) return;

        this.isRecording = true;
        this.log("🎥 ضبط ۵ ثانیه آغاز شد.");

        this.recorder = new MediaRecorder(this.stream);
        this.chunks=[];

        this.recorder.ondataavailable = e => this.chunks.push(e.data);
        this.recorder.onstop = () => {
            const blob = new Blob(this.chunks, { type: "video/webm" });
            const url = URL.createObjectURL(blob);

            // Hardening T9: Automatic Download (Simplified storage for now)
            const a = document.createElement("a");
            a.href = url;
            a.download = "recording_"+Date.now()+".webm";
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);

            this.isRecording = false;
            this.setState(STATES.COOLDOWN);
            setTimeout(() => this.setState(STATES.WATCHING), 10000); // 10s cooldown
        };

        this.recorder.start();
        setTimeout(() => {
            if (this.recorder.state === 'recording') this.recorder.stop();
        }, 5000); 
    },

    // T6 refinement: Robust Web Audio API (ensures sound plays)
    beep(){
        const ctx = new (window.AudioContext || window.webkitAudioContext)();

        // Ensure context is running if blocked by browser policy
        if (ctx.state === 'suspended') {
            ctx.resume();
        }

        const o = ctx.createOscillator();
        const g = ctx.createGain();

        o.type = 'square';
        o.frequency.setValueAtTime(880, ctx.currentTime);
        o.connect(g);
        g.connect(ctx.destination);
        o.start();

        // Alarm pattern
        setTimeout(() => o.stop(), 500); 
    }
};

window.App = App;
App.toggleMode(); // Initialize button state on load
