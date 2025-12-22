
let video = document.getElementById('video');
let canvas = document.getElementById('overlay');
let ctx = canvas.getContext('2d');
let alarm = document.getElementById('alarm');
let alarmOn = true;
let currentFacing = "user";
let knownFaces = [];

async function loadModels() {
  await faceapi.nets.tinyFaceDetector.loadFromUri('models');
  await faceapi.nets.faceLandmark68Net.loadFromUri('models');
  await faceapi.nets.faceRecognitionNet.loadFromUri('models');
}

async function startCamera() {
  let stream = await navigator.mediaDevices.getUserMedia({
    video: { facingMode: currentFacing }
  });
  video.srcObject = stream;
}

function toggleAlarm() {
  alarmOn = !alarmOn;
  if(!alarmOn) alarm.pause();
}

function switchCamera() {
  currentFacing = currentFacing === "user" ? "environment" : "user";
  startCamera();
}

async function detect() {
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;

  const detections = await faceapi
    .detectAllFaces(video, new faceapi.TinyFaceDetectorOptions())
    .withFaceLandmarks()
    .withFaceDescriptors();

  ctx.clearRect(0,0,canvas.width,canvas.height);

  if(detections.length > 0 && alarmOn){
    alarm.play();
  }

  detections.forEach(det => saveFace(det));
}

function saveFace(det){
  const box = det.detection.box;
  const faceCanvas = document.createElement('canvas');
  faceCanvas.width = box.width;
  faceCanvas.height = box.height;
  faceCanvas.getContext('2d').drawImage(
    video,
    box.x, box.y, box.width, box.height,
    0,0,box.width,box.height
  );

  let img = document.createElement('img');
  img.src = faceCanvas.toDataURL();
  document.getElementById('faces').appendChild(img);
}

video.addEventListener('play', () => {
  setInterval(detect, 700);
});

loadModels().then(startCamera);
