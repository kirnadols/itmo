<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import api from '../services/api';

const username = ref('');
const password = ref('');
const router = useRouter();
const message = ref('');
const isError = ref(false);

const handleLogin = async () => {
    try {
        const response = await api.post('/auth/login', {
            username: username.value,
            password: password.value
        });
        localStorage.setItem('jwt_token', response.data);
        router.push('/main');
    } catch (e) {
        isError.value = true;
        message.value = "Ошибка входа: неверные данные";
    }
};

const handleRegister = async () => {
    try {
        await api.post('/auth/register', {
            username: username.value,
            password: password.value
        });
        isError.value = false;
        message.value = "Регистрация успешна! Теперь войдите.";
    } catch (e) {
        isError.value = true;
        message.value = e.response?.data || "Ошибка регистрации (возможно, логин занят)";
    }
}
</script>

<template>
    <div class="auth-container">
        <header class="header-info">
            <h1>Web Lab 4</h1>
            <p>Студент: Иванов И.И.</p>
            <p>Группа: P32xx | Вариант: 12345</p>
        </header>

        <div class="auth-card">
            <h2>Авторизация</h2>
            <form @submit.prevent="handleLogin">
                <div class="input-group">
                    <input v-model="username" type="text" placeholder="Логин" required />
                </div>
                <div class="input-group">
                    <input v-model="password" type="password" placeholder="Пароль" required />
                </div>

                <div class="btn-group">
                    <button type="submit" class="btn-login">Войти</button>
                    <button type="button" @click="handleRegister" class="btn-register">Регистрация</button>
                </div>

                <p v-if="message" :class="{ 'error-msg': isError, 'success-msg': !isError }">
                    {{ message }}
                </p>
            </form>
        </div>
    </div>
</template>

<style scoped>
.auth-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
}

.header-info {
    text-align: center;
    background: #2c3e50;
    color: white;
    padding: 1rem 3rem;
    border-radius: 8px;
    margin-bottom: 2rem;
}

.auth-card {
    background: white;
    padding: 2rem;
    width: 300px;
    border-radius: 8px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.1);
}

.input-group input {
    width: 100%;
    padding: 10px;
    margin-bottom: 15px;
    border: 1px solid #ddd;
    border-radius: 4px;
}

.btn-group {
    display: flex;
    gap: 10px;
}

.btn-login {
    flex: 1;
    padding: 10px;
    background-color: #3498db;
    color: white;
    border: none;
    border-radius: 4px;
}

.btn-register {
    flex: 1;
    padding: 10px;
    background-color: #95a5a6;
    color: white;
    border: none;
    border-radius: 4px;
}

.error-msg { color: #e74c3c; margin-top: 10px; text-align: center; font-size: 0.9em; }
.success-msg { color: #2ecc71; margin-top: 10px; text-align: center; font-size: 0.9em; }
</style>