<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import apiClient from '../../axios';
import { useAuthStore } from '../../stores/auth';
import Button from '../Button.vue';

const router = useRouter();

const authStore = useAuthStore();

const email = ref('');
const password = ref('');
const errorMessage = ref(null);
const showPassword = ref(false);


async function userLogin() {
    const url = "/auth/v1/login";
    const payload = {
        email: email.value,
        password: password.value
    };
    try {
        const response = await apiClient.post(url, payload, { noCsrf: true });
        if (response.status === 200) {
            authStore.setUser(response.data.id, response.data.role);
            router.replace('/dashboard');            
        }
    } catch (error) {
        errorMessage.value = error.response?.data?.message || "Something went wrong!!!";
        console.error('Axios: ', error);
    }
}
</script>

<template>
    <form @submit.prevent class="login-form">
        <div v-if="errorMessage" class="error-msg">
            {{ errorMessage }}
        </div>
        <div class="input-container">
            <label for="user-email" class="input-label"><h3>Email</h3></label>
            <input type="email" id="user-email" v-model="email" class="input-field" placeholder="Enter your email"
                required>
        </div>
        <div class="input-container">
            <label for="user-password" class="input-label"><h3>Password</h3></label>
            <input :type="showPassword ? 'text' : 'password'" id="user-password" v-model="password" class="input-field"
                placeholder="Enter your password" minlength="8" required>
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor"
                v-if="showPassword" class="show-icon" @click="showPassword=!showPassword" >
                <path d="M10 12.5a2.5 2.5 0 1 0 0-5 2.5 2.5 0 0 0 0 5Z" />
                <path fill-rule="evenodd"
                    d="M.664 10.59a1.651 1.651 0 0 1 0-1.186A10.004 10.004 0 0 1 10 3c4.257 0 7.893 2.66 9.336 6.41.147.381.146.804 0 1.186A10.004 10.004 0 0 1 10 17c-4.257 0-7.893-2.66-9.336-6.41ZM14 10a4 4 0 1 1-8 0 4 4 0 0 1 8 0Z"
                    clip-rule="evenodd" />
            </svg>
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="show-icon" v-else @click="showPassword=!showPassword" >
                <path fill-rule="evenodd"
                    d="M3.28 2.22a.75.75 0 0 0-1.06 1.06l14.5 14.5a.75.75 0 1 0 1.06-1.06l-1.745-1.745a10.029 10.029 0 0 0 3.3-4.38 1.651 1.651 0 0 0 0-1.185A10.004 10.004 0 0 0 9.999 3a9.956 9.956 0 0 0-4.744 1.194L3.28 2.22ZM7.752 6.69l1.092 1.092a2.5 2.5 0 0 1 3.374 3.373l1.091 1.092a4 4 0 0 0-5.557-5.557Z"
                    clip-rule="evenodd" />
                <path
                    d="m10.748 13.93 2.523 2.523a9.987 9.987 0 0 1-3.27.547c-4.258 0-7.894-2.66-9.337-6.41a1.651 1.651 0 0 1 0-1.186A10.007 10.007 0 0 1 2.839 6.02L6.07 9.252a4 4 0 0 0 4.678 4.678Z" />
            </svg>
        </div>
        <div class="auth-btn">
            <Button label="Login" @click="userLogin" class="login-btn" />
        </div>
    </form>
</template>

<style scoped>
.login-form {
    flex-grow: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 100%;
}

.input-container {
    display: flex;
    flex-direction: column;
    width: 100%;
    max-width: 450px;
    margin-bottom: 20px;
    position: relative;
}

.input-label {
    font-size: 1.2em;
    margin-bottom: 8px;
    font-weight: 600;
    color: #333;
    align-self: flex-start;
}

.input-field {
    height: 50px;
    width: 100%;
    box-sizing: border-box;
    border: 2px solid #e0e0e0;
    border-radius: 8px;
    color: #333;
    background-color: #f8f9fa;
    padding-left: 15px;
    font-size: 1em;
    transition: all 0.3s ease;
}

.input-field:hover {
    border-color: var(--accent-bar-color);
    background-color: #fff;
}

.input-field:focus {
    outline: none;
    border-color: var(--accent-bar-color);
    background-color: #fff;
    box-shadow: 0 0 0 4px rgba(0, 0, 0, 0.1);
}

.auth-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    max-width: 450px;
    margin-top: 10px;
}

/* Override Button Component Style */
:deep(.login-btn) {
    width: 80%;
    height: 50px;
    font-size: 1.2em;
    font-weight: bold;
    border-radius: 8px;
    background-color: var(--accent-bar-color);
    color: white;
    border: none;
    cursor: pointer;
    transition: transform 0.1s ease, opacity 0.2s ease;
}

:deep(.login-btn:hover) {
    opacity: 0.9;
    transform: translateY(-1px);
}

:deep(.login-btn:active) {
    transform: translateY(1px);
}

.show-icon {
    position: absolute;
    right: 15px;
    bottom: 13px;
    width: 24px;
    height: 24px;
    cursor: pointer;
    color: #6c757d;
}

#user-password {
    padding-right: 45px;
}

.error-msg {
    color: #d9534f;
    background-color: #fdf7f7;
    border: 1px solid #d9534f;
    padding: 10px;
    border-radius: 5px;
    margin-bottom: 20px;
    width: 100%;
    max-width: 450px;
    text-align: center;
}
</style>