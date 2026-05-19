<script setup>
import { ref } from 'vue';
import { useAuthStore } from '../../stores/auth';
import Header from '../Header.vue';
import UpdateProfile from './UpdateProfile.vue';
import DeleteAccount from './DeleteAccount.vue';
import CompanyView from '../CompanyComponent/CompanyView.vue';
import StudentView from '../StudentComponent/StudentView.vue';

const authStore = useAuthStore();
const userId = authStore.getUserId();
const userRole = authStore.getUserRole();

const showUpdate = ref(false);
const showDelete = ref(false);

const currentTab = ref('CompanyView')

const tabs = {
    CompanyView,
    StudentView
}

const tabNames = {
    'CompanyView': "Blacklisted Company",
    'StudentView': "Blacklisted Students"
}

</script>

<template>
    <div class="action-content">
        <Header heading="Action Center" />
        <div class="content-menu">
            <div class="users" v-if="userRole !== 'Admin'">
                <span class="links" @click="showUpdate = true">
                    <h3 class="link-text">Update Profile</h3>
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                        stroke="currentColor" class="size-6">
                        <path stroke-linecap="round" stroke-linejoin="round"
                            d="m4.5 19.5 15-15m0 0H8.25m11.25 0v11.25" />
                    </svg>
                </span>
                <span class="links" @click="showDelete = true">
                    <h3 class="link-text">Delete Account</h3>
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                        stroke="currentColor" class="size-6">
                        <path stroke-linecap="round" stroke-linejoin="round"
                            d="m4.5 19.5 15-15m0 0H8.25m11.25 0v11.25" />
                    </svg>
                </span>
            </div>
            <div class="users" v-if="userRole === 'Admin'">
                <div class="options-btn">
                    <div class="options">
                        <span v-for="(_, tab) in tabs" :key="tab"
                            :class="['options-label', { active: currentTab === tab }]" @click="currentTab = tab">
                            <h3>{{ tabNames[tab] }}</h3>
                            <div class="options-selected"></div>
                        </span>
                    </div>
                </div>
                <Transition name="fade" mode="out-in">
                    <component :is="tabs[currentTab]" class="tab" :action="true">
                    </component>
                </Transition>
            </div>
        </div>
        <Teleport to="body">
            <UpdateProfile :show="showUpdate" @close="showUpdate = false" :user-id="userId" :user-role=userRole />
            <DeleteAccount :show="showDelete" @close="showDelete = false" :user-id="userId" :user-role="userRole" />
        </Teleport>
    </div>
</template>

<style lang="css" scoped>
.action-content {
    height: 100vh;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    width: 100%;
}

.content-menu {
    flex: 1;
    min-width: 0;
    overflow-y: auto;
    display: flex;
    justify-content: center;
    padding: 5px 16px;
}

.users {
    display: flex;
    flex-direction: column;
    gap: 8px;
    width: 100%;
    /* max-width: 480px; */
}

.links {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 14px 16px;
    border-radius: 8px;
    cursor: pointer;
    transition: background-color 0.3s ease;
}

.links:hover {
    background-color: var(--secondary-highlight-color);
}

.link-text {
    flex-grow: 1;
    margin: 0;
}

.size-6 {
    width: 24px;
    height: 24px;
    flex-shrink: 0;
    transition: transform 0.3s ease;
}

.links:hover .size-6 {
    transform: translateX(5px);
}

.options-btn {
	display: flex;
	justify-content: space-between;
	align-items: flex-end;
}

.options {
	display: flex;
	align-items: flex-end;
}

.options-label {
	position: relative;
	margin: 5px;
	padding: 2px 5px;
	cursor: pointer;
}

.options-selected {
	position: absolute;
	height: 2px;
	left: 0%;
	right: 0%;
	border-radius: 2px;
	opacity: 0;

	transition:
		opacity 0.2s ease,
		left 0.2s ease,
		right 0.2s ease;
}

.active>.options-selected {
	opacity: 1;
	left: 20%;
	right: 20%;
	background-color: var(--accent-bar-color);
}

.fade-enter-active,
.fade-leave-active {
	transition: opacity 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
	opacity: 0;
}
</style>