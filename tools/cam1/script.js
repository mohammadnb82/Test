const slider = document.getElementById("slider");
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
