import os

BASE_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "tools",
    "cam1"
)

os.makedirs(BASE_DIR, exist_ok=True)

# ---------- index.html ----------
html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Motion Threshold Test</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="stylesheet" href="style.css">
</head>
<body>

  <h2>Motion Threshold</h2>

  <div class="graph">
    <div class="motion-bar"></div>
    <div class="threshold-line" id="thresholdLine"></div>
  </div>

  <div class="controls">
    <input id="slider" type="range" min="0" max="100" value="50">
    <div class="value">
      Threshold: <span id="thresholdValue">50</span>
    </div>
  </div>

  <script src="script.js"></script>
</body>
</html>
"""

# ---------- style.css ----------
css = """* {
  box-sizing: border-box;
}

body {
  font-family: Arial, sans-serif;
  padding: 20px;
}

.graph {
  position: relative;
  width: 100%;
  max-width: 400px;
  height: 30px;
  background: #ddd;
  margin: 20px 0;
  border-radius: 6px;
  overflow: hidden;
}

.motion-bar {
  position: absolute;
  top: 0;
  left: 0;
  height: 100%;
  width: 100%;
  background: #4caf50;
  opacity: 0.4;
}

.threshold-line {
  position: absolute;
  top: 0;
  bottom: 0;
  width: 4px;
  background: red;
  left: 50%;
  transform: translateX(-50%);
  z-index: 10;
}

.controls {
  max-width: 400px;
}

input[type="range"] {
  width: 100%;
}
"""

# ---------- script.js ----------
js = """const slider = document.getElementById("slider");
const line = document.getElementById("thresholdLine");
const valueText = document.getElementById("thresholdValue");

function updateThreshold(val) {
  line.style.left = val + "%";
  valueText.textContent = val;
}

slider.addEventListener("input", e => {
  updateThreshold(e.target.value);
});

updateThreshold(slider.value);
"""

with open(os.path.join(BASE_DIR, "index.html"), "w", encoding="utf-8") as f:
    f.write(html)

with open(os.path.join(BASE_DIR, "style.css"), "w", encoding="utf-8") as f:
    f.write(css)

with open(os.path.join(BASE_DIR, "script.js"), "w", encoding="utf-8") as f:
    f.write(js)

print("✅ Base HTML rebuild complete at tools/cam1")
