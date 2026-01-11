<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import api from '../services/api';
import InteractiveGraph from '../components/InteractiveGraph.vue';

const router = useRouter();

// Состояние формы
const xVal = ref(0);
const yVal = ref('');
const rVal = ref(1);
const points = ref([]);
const errorMsg = ref('');

const isYValid = computed(() => {
    const y = parseFloat(yVal.value);
    return !isNaN(y) && y >= -5 && y <= 3;
});

const fetchPoints = async () => {
    try {
        const res = await api.get('/points');
        points.value = res.data;
    } catch (e) {
        console.error("Ошибка загрузки точек", e);
    }
};

const sendData = async (x, y, r) => {
    errorMsg.value = '';
    if (r <= 0) {
        errorMsg.value = "R должен быть положительным!";
        return;
    }

    try {
        const res = await api.post('/points', {
            x: parseFloat(x),
            y: parseFloat(y),
            r: parseFloat(r)
        });
        points.value.push(res.data);
    } catch (e) {
        errorMsg.value = e.response?.data || "Ошибка сервера";
    }
};

const handleFormSubmit = () => {
    if (!isYValid.value) {
        errorMsg.value = "Проверьте Y (-5 ... 3)";
        return;
    }
    sendData(xVal.value, yVal.value, rVal.value);
};

const handleGraphClick = (coords) => {
    sendData(coords.x, coords.y, rVal.value);
};

const logout = () => {
    localStorage.removeItem('jwt_token');
    router.push('/');
};

onMounted(fetchPoints);
</script>

<template>
    <div class="main-layout">
        <header class="navbar">
            <span class="brand">Lab 4: Area Check</span>
            <button @click="logout" class="logout-btn">Выход</button>
        </header>

        <div class="content">
            <div class="panel interaction-panel">
                <InteractiveGraph :r="rVal" :points="points" @graph-click="handleGraphClick" />

                <form @submit.prevent="handleFormSubmit" class="check-form">

                    <div class="form-row">
                        <label>X:</label>
                        <div class="radio-wrap">
                            <label v-for="val in [-5,-4,-3,-2,-1,0,1,2,3]" :key="val" class="radio-label">
                                <input type="radio" :value="val" v-model="xVal"> {{ val }}
                            </label>
                        </div>
                    </div>

                    <div class="form-row">
                        <label>Y (-5 ... 3):</label>
                        <input type="text" v-model="yVal" :class="{ 'error-input': !isYValid && yVal }" placeholder="-5 ... 3">
                    </div>

                    <div class="form-row">
                        <label>R:</label>
                        <div class="radio-wrap">
                            <label v-for="val in [-5,-4,-3,-2,-1,0,1,2,3]" :key="val" class="radio-label">
                                <input type="radio" :value="val" v-model="rVal"> {{ val }}
                            </label>
                        </div>
                        <small v-if="rVal <= 0" style="color:red">Выберите R > 0</small>
                    </div>

                    <div v-if="errorMsg" class="server-error">{{ errorMsg }}</div>

                    <button type="submit" class="submit-btn" :disabled="!isYValid || rVal <= 0">
                        Проверить
                    </button>
                </form>
            </div>

            <div class="panel results-panel">
                <h3>История</h3>
                <div class="table-container">
                    <table>
                        <thead>
                            <tr>
                                <th>X</th>
                                <th>Y</th>
                                <th>R</th>
                                <th>Результат</th>
                                <th>Время</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="p in points" :key="p.id">
                                <td>{{ p.x.toFixed(2) }}</td>
                                <td>{{ p.y.toFixed(2) }}</td>
                                <td>{{ p.r }}</td>
                                <td :class="p.result ? 'hit' : 'miss'">
                                    {{ p.result ? 'Попадание' : 'Промах' }}
                                </td>
                                <td>{{ new Date(p.checkedAt).toLocaleTimeString() }}</td>
                            </tr>
                            <tr v-if="points.length === 0">
                                <td colspan="5" class="empty">Нет данных</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.main-layout {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
}

.navbar {
    background: #2c3e50;
    color: white;
    padding: 1rem 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.logout-btn {
    background: #e74c3c;
    color: white;
    border: none;
    padding: 6px 12px;
    border-radius: 4px;
}

.content {
    display: flex;
    flex-wrap: wrap;
    padding: 20px;
    gap: 20px;
    justify-content: center;
}

.panel {
    background: white;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.05);
}

.form-row { margin-bottom: 15px; }
.form-row label { display: block; font-weight: bold; margin-bottom: 5px; }
.radio-wrap { display: flex; flex-wrap: wrap; gap: 8px; }
.radio-label { background: #eee; padding: 4px 8px; border-radius: 4px; font-size: 0.9em; cursor: pointer; }

input[type="text"] {
    width: 100%;
    padding: 8px;
    border: 1px solid #ccc;
    border-radius: 4px;
}
input.error-input { border-color: red; background: #fff5f5; }

.submit-btn {
    width: 100%;
    padding: 12px;
    background: #3498db;
    color: white;
    border: none;
    border-radius: 4px;
    font-size: 1rem;
}
.submit-btn:disabled { background: #bdc3c7; cursor: not-allowed; }

.server-error { color: red; margin-bottom: 10px; text-align: center; }

.table-container { overflow-x: auto; }
table { width: 100%; border-collapse: collapse; font-size: 0.9em; }
th, td { padding: 10px; border-bottom: 1px solid #eee; text-align: center; }
th { background: #f8f9fa; }
.hit { color: #2ecc71; font-weight: bold; }
.miss { color: #e74c3c; font-weight: bold; }
.empty { color: #999; padding: 20px; }


@media (min-width: 1203px) {
    .interaction-panel { width: 400px; }
    .results-panel { flex: 1; max-width: 800px; }
    .content { align-items: flex-start; }
}

@media (max-width: 1202px) and (min-width: 669px) {
    .content { flex-direction: column; align-items: center; }
    .panel { width: 80%; }
}

@media (max-width: 668px) {
    .content { flex-direction: column; padding: 10px; }
    .panel { width: 100%; }
    .radio-wrap { justify-content: center; }
}
</style>