<script setup>
import { ref, onMounted, watch } from 'vue';

const props = defineProps({
    r: { type: Number, required: true },
    points: { type: Array, default: () => [] }
});

const emit = defineEmits(['graph-click']);
const canvasRef = ref(null);
const CANVAS_SIZE = 300;

const draw = () => {
    const canvas = canvasRef.value;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const w = canvas.width;
    const h = canvas.height;

    ctx.clearRect(0, 0, w, h);

    const currentR = props.r > 0 ? props.r : 3;

    const pixelsPerUnit = (w / 2) / 6;

    const rPx = currentR * pixelsPerUnit;
    const halfRPx = (currentR / 2) * pixelsPerUnit;

    ctx.save();
    ctx.translate(w / 2, h / 2);

    ctx.fillStyle = '#4da6ff';

    ctx.beginPath();
    ctx.fillRect(0, -rPx, rPx, rPx);

    ctx.beginPath();
    ctx.moveTo(0, 0);
    ctx.arc(0, 0, rPx, Math.PI, 1.5 * Math.PI);
    ctx.fill();

    ctx.beginPath();
    ctx.moveTo(0, 0);
    ctx.lineTo(-halfRPx, 0);
    ctx.lineTo(0, rPx);
    ctx.fill();

    ctx.strokeStyle = '#000';
    ctx.lineWidth = 1;
    ctx.fillStyle = '#000';
    ctx.font = '12px Arial';

    ctx.beginPath();
    ctx.moveTo(-w / 2 + 10, 0);
    ctx.lineTo(w / 2 - 10, 0);
    ctx.stroke();

    ctx.beginPath();
    ctx.moveTo(w / 2 - 10, 0);
    ctx.lineTo(w / 2 - 15, -3);
    ctx.lineTo(w / 2 - 15, 3);
    ctx.fill();
    ctx.fillText("x", w / 2 - 10, 15);

    ctx.beginPath();
    ctx.moveTo(0, h / 2 - 10);
    ctx.lineTo(0, -h / 2 + 10);
    ctx.stroke();

    ctx.beginPath();
    ctx.moveTo(0, -h / 2 + 10);
    ctx.lineTo(-3, -h / 2 + 15);
    ctx.lineTo(3, -h / 2 + 15);
    ctx.fill();
    ctx.fillText("y", 5, -h / 2 + 15);

    const drawTickX = (x, label) => {
        ctx.beginPath();
        ctx.moveTo(x, -3);
        ctx.lineTo(x, 3);
        ctx.stroke();
        ctx.textAlign = "center";
        ctx.textBaseline = "top";
        ctx.fillText(label, x, 5);
    };

    const drawTickY = (y, label) => {
        ctx.beginPath();
        ctx.moveTo(-3, y);
        ctx.lineTo(3, y);
        ctx.stroke();
        ctx.textAlign = "left";
        ctx.textBaseline = "middle";
        ctx.fillText(label, 5, y);
    };

    if (props.r > 0) {
        drawTickX(rPx, "R");
        drawTickX(halfRPx, "R/2");
        drawTickX(-rPx, "-R");
        drawTickX(-halfRPx, "-R/2");

        drawTickY(-rPx, "R");
        drawTickY(-halfRPx, "R/2");
        drawTickY(rPx, "-R");
        drawTickY(halfRPx, "-R/2");
    } else {
        ctx.textAlign = "center";
        ctx.fillText("R не задан", 0, -h/2 + 40);
    }

    props.points.forEach(p => {
        const px = p.x * pixelsPerUnit;
        const py = -p.y * pixelsPerUnit;

        ctx.beginPath();
        ctx.arc(px, py, 4, 0, 2 * Math.PI);
        ctx.fillStyle = p.result ? '#2ecc71' : '#e74c3c';
        ctx.fill();
        ctx.strokeStyle = '#222';
        ctx.stroke();
    });

    ctx.restore();
};

const handleClick = (event) => {
    if (props.r <= 0) {
        alert("Выберите корректный радиус R перед кликом!");
        return;
    }

    const canvas = canvasRef.value;
    const rect = canvas.getBoundingClientRect();
    const xClick = event.clientX - rect.left;
    const yClick = event.clientY - rect.top;

    const w = canvas.width;
    const h = canvas.height;
    const pixelsPerUnit = (w / 2) / 6;

    let x = (xClick - w / 2) / pixelsPerUnit;
    let y = -(yClick - h / 2) / pixelsPerUnit;

    x = parseFloat(x.toFixed(3));
    y = parseFloat(y.toFixed(3));

    emit('graph-click', { x, y });
};

watch(() => [props.r, props.points], draw, { deep: true });
onMounted(draw);
</script>

<template>
    <div class="canvas-wrapper">
        <canvas
            ref="canvasRef"
            :width="CANVAS_SIZE"
            :height="CANVAS_SIZE"
            @click="handleClick"
        ></canvas>
    </div>
</template>

<style scoped>
.canvas-wrapper {
    display: flex;
    justify-content: center;
    margin-bottom: 20px;
}
canvas {
    background-color: white;
    cursor: crosshair;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
</style>