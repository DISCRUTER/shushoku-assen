<script setup>
import apiClient from '../../axios';
import { useAuthStore } from '../../stores/auth';
import Button from '../Button.vue';

const authStore = useAuthStore();
const userRole = authStore.getUserRole();

const props = defineProps({
    show: Boolean,
    userId: String,
    userRole: String
});

async function deleteAccount() {
    let url = '';
    if (props.userRole === 'Student') {
        url = `/api/v1/students/${props.userId}`;
    } else if (props.userRole === 'Company') {
        url = `/api/v1/company/${props.userId}`;
    }

    try {
        const response = await apiClient.delete(url);
        if (response.status === 204) {
            authStore.logout();
        }
    } catch (error) {
        console.error("Axios: ", error);
    }
}
</script>

<template>
    <Transition name="modal">
        <div v-if="show" class="modal-mask" @click="$emit('close')">
            <div class="modal-container" @click.stop>

                <div class="modal-header">
                    <div class="head">
                        <h2>Delete Account</h2>
                    </div>
                    <Button label="Close" @click="$emit('close')" />
                </div>

                <div class="content">
                    <h3>Are you sure?</h3>
                </div>
                <div class="options-btn" v-if="userRole !== 'Admin'">
                    <Button label="Delete" class="apply-btn" @click="deleteAccount" />
                </div>
            </div>
        </div>
    </Transition>
</template>

<style lang="css" scoped>
.modal-mask {
    position: fixed;
    z-index: 9998;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    transition: opacity 0.3s ease;
}

.modal-container {
    width: 60%;
    height: 40%;
    margin: auto;
    padding: 20px 30px;
    background-color: #fff;
    border-radius: 10px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.33);
    transition: all 0.3s ease;
    display: flex;
    flex-direction: column;
}

.modal-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 12px;
    flex-shrink: 0;
}

.head {
    display: flex;
    flex-direction: column;
    gap: 2px;
}

.head h2 {
    margin: 0;
}

.head p {
    margin: 0;
    color: #888;
    font-size: 0.85em;
}

.content {
    flex-grow: 1;
    display: flex;
    flex-direction: column;
    overflow-y: auto;
    overflow-x: hidden;
    min-height: 0;
}

.options-btn {
    display: flex;
    justify-content: flex-end;
    align-items: center;
    gap: 10px;
    padding-top: 14px;
    border-top: 1px solid #f0f0f0;
    flex-shrink: 0;
}

:deep(.apply-btn) {
	width: 250px;
	height: 50px;
	font-size: 1.2em;
	font-weight: bold;
	background-color: var(--secondary-highlight-color);
	color: white;
	border: none;
	cursor: pointer;
	transition: background-color 1.2s cubic-bezier(0.19, 1, 0.22, 1);
	margin-bottom: 5px;
}

:deep(.apply-btn:hover) {
	background-color: var(--accent-bar-color);
}

.modal-enter-from {
    opacity: 0;
}

.modal-leave-to {
    opacity: 0;
}

.modal-enter-from .modal-container,
.modal-leave-to .modal-container {
    -webkit-transform: scale(1.1);
    transform: scale(1.1);
}
</style>
