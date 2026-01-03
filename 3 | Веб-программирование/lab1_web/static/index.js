document.addEventListener('DOMContentLoaded', () => {

    const urlParamsOnLoad = new URLSearchParams(window.location.search);
    const isDebugOnLoad = urlParamsOnLoad.get('debug') === 'true';
    if (isDebugOnLoad) {
        document.body.classList.add('debug-mode');
    }


    const form = document.getElementById('shot-form');
    const xButtonsContainer = document.getElementById('x-buttons');
    const yValueInput = document.getElementById('y-value');
    const errorMessageElement = document.getElementById('error-message');
    const resultsTableBody = document.getElementById('results-table-body');
    const LOCAL_STORAGE_KEY = 'shotHistory';
    let selectedX = null;
    const resetButton = document.getElementById('reset-btn');

    const canvas = document.getElementById('graph-canvas');
    if (!canvas) {
        console.error("Canvas element not found!");
        return;
    }
    const ctx = canvas.getContext('2d');
    const rRadiosContainer = document.getElementById('r-radios');
    const rDisplay = document.getElementById('current-r-display');

    const DISPLAY_RANGE = 5;
    const canvasSize = canvas.width;
    const center = canvasSize / 2;
    const pixelsPerUnit = canvasSize / (DISPLAY_RANGE * 2 + 1);

    let currentR = null;

    xButtonsContainer.addEventListener('click', (event) => {
        if (event.target.tagName === 'BUTTON') {
            xButtonsContainer.querySelectorAll('button').forEach(btn => btn.classList.remove('selected'));
            event.target.classList.add('selected');
            selectedX = event.target.dataset.value;
        }
    });

    rRadiosContainer.addEventListener('change', (event) => {
        if (event.target.name === 'r') {
            currentR = event.target.value;
            if(rDisplay) rDisplay.textContent = currentR;
            drawGraph(currentR);
        }
    });

    form.addEventListener('submit', async (event) => {
        event.preventDefault();
        clearErrors();

        if (!validateForm()) {
            return;
        }

        const yValue = yValueInput.value.replace(',', '.');
        const rValue = currentR;

        const formData = new URLSearchParams();
        formData.append('x', selectedX);
        formData.append('y', yValue);
        formData.append('r', rValue);

        const urlParams = new URLSearchParams(window.location.search);
        const isDebug = urlParams.get('debug') === 'true';

        const fetchHeaders = {
            'Content-Type': 'application/x-www-form-urlencoded',
        };

        let fetchUrl = '/fcgi-bin/lab1_web.jar';

        if (isDebug) {
            fetchHeaders['X-Debug-Token'] = 'secret';
            fetchUrl += '?debug=true';
        }

        try {
            const response = await fetch(fetchUrl, {
                method: 'POST',
                headers: fetchHeaders,
                body: formData
            });

            const responseText = await response.text();
            if (!responseText) {
                throw new Error('Сервер вернул пустой ответ.');
            }
            const resultsData = JSON.parse(responseText);

            if (!response.ok) {
                throw new Error(resultsData.reason || `Ошибка сервера: ${response.status}`);
            }

            addRowToTable(resultsData, true);
            saveResult(resultsData);

            drawGraph(currentR);

        } catch (error) {
            showError(`Произошла ошибка: ${error.message}`);
            console.error('Fetch error:', error);
        }
    });

    if (resetButton) {
        resetButton.addEventListener('click', () => {
            localStorage.removeItem(LOCAL_STORAGE_KEY);

            resultsTableBody.innerHTML = '';

            drawGraph(currentR);

            clearErrors();
        });
    }


    function validateForm() {
        if (selectedX === null) {
            showError("Пожалуйста, выберите значение X.");
            return false;
        }

        const yStr = yValueInput.value.trim().replace(',', '.');
        if (yStr === '') {
            showError("Пожалуйста, введите значение Y.");
            return false;
        }
        const yNum = parseFloat(yStr);
        if (isNaN(yNum)) {
            showError("Y должен быть числом.");
            return false;
        }

        if (yNum <= -5 || yNum >= 5) {
            showError("Y должен быть в диапазоне (-5, 5).");
            return false;
        }

        if (currentR === null) {
            showError("Пожалуйста, выберите значение R.");
            return false;
        }
        return true;
    }

    function addRowToTable(res, prepend = false) {
        const row = document.createElement('tr');

        const hitClass = res.result ? 'hit-true' : 'hit-false';
        const hitText = res.result ? 'Попадание' : 'Промах';

        const xVal = typeof res.x !== 'undefined' ? res.x : '-';
        const yVal = typeof res.y !== 'undefined' ? res.y : '-';
        const rVal = typeof res.r !== 'undefined' ? res.r : '-';

        const debug = res.debug || {};
        const validationTime = debug.validationTimeNs || '-';
        const calcTime = debug.calcTimeNs || '-';
        const memoryUsed = debug.memoryUsedBytes || '-';
        const threadId = debug.threadId || '-';

        row.innerHTML = `
            <td>${xVal}</td>
            <td>${yVal}</td>
            <td>${rVal}</td>
            <td>${res.now || '-'}</td>
            <td>${res.time || '-'}</td>
            <td class="${hitClass}">${hitText}</td>
            <td class="debug-col">${validationTime}</td>
            <td class="debug-col">${calcTime}</td>
            <td class="debug-col">${memoryUsed}</td>
            <td class="debug-col">${threadId}</td>
        `;

        if (prepend) {
            resultsTableBody.prepend(row);
        } else {
            resultsTableBody.appendChild(row);
        }
    }

    function loadResultsFromStorage() {
        const resultsJson = localStorage.getItem(LOCAL_STORAGE_KEY);
        if (resultsJson) {
            try {
                const results = JSON.parse(resultsJson);
                resultsTableBody.innerHTML = '';
                results.forEach(res => {
                    addRowToTable(res, false);
                });
                drawGraph(currentR);
            } catch (e) {
                console.error("Ошибка парсинга localStorage:", e);
                localStorage.removeItem(LOCAL_STORAGE_KEY);
            }
        }
    }

    function saveResult(newResult) {
        const resultsJson = localStorage.getItem(LOCAL_STORAGE_KEY);
        let results = [];
        if (resultsJson) {
            try {
                results = JSON.parse(resultsJson);
            } catch (e) {
                console.error("Ошибка парсинга localStorage:", e);
                results = [];
            }
        }
        results.push(newResult);
        localStorage.setItem(LOCAL_STORAGE_KEY, JSON.stringify(results));
    }

    function showError(message) {
        errorMessageElement.textContent = message;
    }

    function clearErrors() {
        errorMessageElement.textContent = '';
    }

    function toPixelX(x) { return center + x * pixelsPerUnit; }
    function toPixelY(y) { return center - y * pixelsPerUnit; }
    function toGraphX(px) { return (px - center) / pixelsPerUnit; }
    function toGraphY(py) { return (center - py) / pixelsPerUnit; }

    function drawGraph(rValue) {
        if (!ctx) return;

        ctx.clearRect(0, 0, canvasSize, canvasSize);
        ctx.fillStyle = "rgba(0, 0, 139, 0.5)";

        if (rValue) {
            const rPx = rValue * pixelsPerUnit;
            const rHalfPx = (rValue / 2) * pixelsPerUnit;

            ctx.beginPath();
            ctx.moveTo(toPixelX(0), toPixelY(0));
            ctx.lineTo(toPixelX(rValue), toPixelY(0));
            ctx.lineTo(toPixelX(0), toPixelY(rValue / 2));
            ctx.closePath();
            ctx.fill();

            ctx.beginPath();
            ctx.rect(toPixelX(-rValue), toPixelY(rValue / 2), rPx, rHalfPx);
            ctx.fill();

           ctx.beginPath();
           ctx.moveTo(toPixelX(0), toPixelY(0));

           ctx.arc(toPixelX(0), toPixelY(0), rHalfPx, Math.PI / 2, Math.PI);

           ctx.closePath();
           ctx.fill();

        }

        ctx.strokeStyle = "#333";
        ctx.lineWidth = 1;
        ctx.beginPath();

        ctx.moveTo(0, center); ctx.lineTo(canvasSize, center);
        ctx.lineTo(canvasSize - 10, center - 5);
        ctx.moveTo(canvasSize, center); ctx.lineTo(canvasSize - 10, center + 5);

        ctx.moveTo(center, canvasSize); ctx.lineTo(center, 0);
        ctx.lineTo(center - 5, 10);
        ctx.moveTo(center, 0); ctx.lineTo(center + 5, 10);
        ctx.stroke();

        ctx.fillStyle = "#333";
        ctx.font = "10px Arial";
        ctx.textAlign = "center";
        ctx.textBaseline = "middle";

        for (let i = -DISPLAY_RANGE; i <= DISPLAY_RANGE; i++) {
            if (i === 0) continue;

            ctx.fillText(i, toPixelX(i), center + 15);
            ctx.beginPath();
            ctx.moveTo(toPixelX(i), center - 4); ctx.lineTo(toPixelX(i), center + 4); ctx.stroke();

            ctx.fillText(i, center - 15, toPixelY(i));
            ctx.beginPath();
            ctx.moveTo(center - 4, toPixelY(i)); ctx.lineTo(center + 4, toPixelY(i)); ctx.stroke();
        }

        drawPoints();
    }

    function drawPoints() {
        if (!ctx) return;
        const resultsJson = localStorage.getItem(LOCAL_STORAGE_KEY);
        if (!resultsJson) return;

        try {
            const results = JSON.parse(resultsJson);
            results.forEach(res => {
                const x = parseFloat(res.x);
                const y = parseFloat(res.y);
                if (isNaN(x) || isNaN(y)) return;

                ctx.beginPath();
                ctx.arc(toPixelX(x), toPixelY(y), 4, 0, Math.PI * 2);
                ctx.fillStyle = res.result ? '#388e3c' : '#d32f2f';
                ctx.fill();
                ctx.strokeStyle = "#fff";
                ctx.lineWidth = 1;
                ctx.stroke();
            });
        } catch(e) {
            console.error("Ошибка отрисовки точек:", e);
        }
    }

    if(canvas) {
        canvas.addEventListener('mousemove', (event) => {
            drawGraph(currentR);

            const rect = canvas.getBoundingClientRect();
            const mouseX = event.clientX - rect.left;
            const mouseY = event.clientY - rect.top;

            ctx.strokeStyle = '#aaa';
            ctx.setLineDash([3, 3]);
            ctx.lineWidth = 0.5;
            ctx.beginPath();
            ctx.moveTo(mouseX, 0); ctx.lineTo(mouseX, canvasSize);
            ctx.moveTo(0, mouseY); ctx.lineTo(canvasSize, mouseY);
            ctx.stroke();
            ctx.setLineDash([]);

            const graphX = toGraphX(mouseX);
            const graphY = toGraphY(mouseY);
            const coordText = `X: ${graphX.toFixed(2)}, Y: ${graphY.toFixed(2)}`;
            ctx.fillStyle = 'black';
            ctx.font = '12px Arial';
            ctx.fillText(coordText, mouseX + 10, mouseY - 10);
        });

        canvas.addEventListener('mouseleave', () => {
            drawGraph(currentR);
        });
    }

    loadResultsFromStorage();
    drawGraph(null);
});