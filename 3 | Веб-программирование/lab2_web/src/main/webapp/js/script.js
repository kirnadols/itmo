const canvas = document.getElementById('graphCanvas');
const ctx = canvas.getContext('2d');
const rInput = document.getElementById('r-value');
const yInput = document.getElementById('y-value');
const errorMessage = document.getElementById('error-message');

const width = canvas.width;
const height = canvas.height;
const center = width / 2;

const scale = 25;

function drawGraph() {
    ctx.clearRect(0, 0, width, height);

    let rRaw = rInput.value.replace(',', '.');
    let r = parseFloat(rRaw);

    if (!isNaN(r) && r > 2 && r < 5) {
        drawAreas(r);
    }

    drawAxes();
    drawPoints();
}

function drawAxes() {
    ctx.strokeStyle = "black";
    ctx.lineWidth = 1;
    ctx.font = "12px Arial";
    ctx.fillStyle = "black";

    ctx.beginPath();
    ctx.moveTo(0, center);
    ctx.lineTo(width, center);
    ctx.stroke();

    ctx.beginPath();
    ctx.moveTo(width - 10, center - 5);
    ctx.lineTo(width, center);
    ctx.lineTo(width - 10, center + 5);
    ctx.stroke();
    ctx.fillText("X", width - 15, center - 10);

    ctx.beginPath();
    ctx.moveTo(center, height);
    ctx.lineTo(center, 0);
    ctx.stroke();

    ctx.beginPath();
    ctx.moveTo(center - 5, 10);
    ctx.lineTo(center, 0);
    ctx.lineTo(center + 5, 10);
    ctx.stroke();
    ctx.fillText("Y", center + 10, 15);

    const tickSize = 4;
    for (let i = 1; i * scale < width / 2 - 10; i++) {

        ctx.beginPath(); ctx.moveTo(center + i * scale, center - tickSize); ctx.lineTo(center + i * scale, center + tickSize); ctx.stroke();
        ctx.beginPath(); ctx.moveTo(center - i * scale, center - tickSize); ctx.lineTo(center - i * scale, center + tickSize); ctx.stroke();

        ctx.beginPath(); ctx.moveTo(center - tickSize, center - i * scale); ctx.lineTo(center + tickSize, center - i * scale); ctx.stroke();
        ctx.beginPath(); ctx.moveTo(center - tickSize, center + i * scale); ctx.lineTo(center + tickSize, center + i * scale); ctx.stroke();
    }
}

function drawAreas(r) {
    ctx.fillStyle = "rgba(0, 121, 107, 0.5)";
    ctx.beginPath();

    ctx.moveTo(center, center);
    ctx.arc(center, center, (r/2) * scale, -Math.PI/2, 0, false);

    ctx.rect(center - r * scale, center - r * scale, r * scale, r * scale);

    ctx.moveTo(center, center);
    ctx.lineTo(center - r * scale, center);
    ctx.lineTo(center, center + (r/2) * scale);

    ctx.fill();

    ctx.fillStyle = "black";
    ctx.font = "11px Arial";
    ctx.fillText("R", center + r * scale - 3, center - 10);
    ctx.fillText("-R", center - r * scale - 6, center - 10);
    ctx.fillText("R", center + 10, center - r * scale + 3);
    ctx.fillText("-R/2", center + 10, center + (r/2) * scale + 3);
}

function drawPoints() {
    if (typeof historyPoints === 'undefined') return;

    historyPoints.forEach(p => {
        let xCoord = center + p.x * scale;
        let yCoord = center - p.y * scale;

        ctx.beginPath();
        ctx.arc(xCoord, yCoord, 3, 0, 2 * Math.PI);
        ctx.fillStyle = p.hit ? "#388e3c" : "#d32f2f";
        ctx.fill();
        ctx.strokeStyle = "white";
        ctx.stroke();
    });
}

canvas.addEventListener('click', function(event) {
    let rRaw = rInput.value.replace(',', '.');
    let r = parseFloat(rRaw);

    if (isNaN(r) || r <= 2 || r >= 5) {
        alert("Для клика по графику R должен быть СТРОГО больше 2 и меньше 5");
        return;
    }

    const rect = canvas.getBoundingClientRect();
    const xClick = event.clientX - rect.left;
    const yClick = event.clientY - rect.top;

    let xVal = (xClick - center) / scale;
    let yVal = (center - yClick) / scale;

    window.location.href = `controller?x=${xVal}&y=${yVal}&r=${r}`;
});

function validateForm() {
    errorMessage.textContent = "";

    let r = parseFloat(rInput.value.replace(',', '.'));
    let y = parseFloat(yInput.value.replace(',', '.'));
    let xRadios = document.getElementsByName('x');
    let xSelected = false;

    for (let radio of xRadios) {
        if (radio.checked) xSelected = true;
    }

    if (!xSelected) {
        errorMessage.textContent = "Выберите значение X.";
        return false;
    }

    if (isNaN(y) || y <= -3 || y >= 5) {
        errorMessage.textContent = "Y должен быть строго больше -3 и меньше 5.";
        return false;
    }

    if (isNaN(r) || r <= 2 || r >= 5) {
        errorMessage.textContent = "R должен быть строго больше 2 и меньше 5.";
        return false;
    }
    return true;
}

window.onload = drawGraph;