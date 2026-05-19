<script setup>
import { useAuthStore } from '../../stores/auth';
import Button from '../Button.vue';
import apiClient from '../../axios';

const authStore = useAuthStore();
const userRole = authStore.getUserRole();


const props = defineProps({
	studentData: Object
})

async function blacklistUser(value) {
	const payload = {
		blacklisted: value
	};

	try {
		const response = await apiClient.patch(`/api/v1/students/${props.studentData?.id}`, payload);
		if (response.status === 202) {
			Object.assign(props.studentData, response.data);
			window.location.reload();
		} else {
			console.log('Something went wrong!');
		}
	} catch (error) {
		console.error("Something went wrong");
	}
}
</script>

<template>
	<div class="company-content">
		<div class="company-info">
			<h2 class="company-name">{{ studentData.first_name }} {{ studentData.last_name }}</h2>
			<div class="academy-info">
				<h3>{{ `${studentData.academic_degree?.name} in ${studentData.branch?.name}` }}</h3>
				<h3>CGPA: {{ studentData.cgpa }}</h3>
			</div>
			<div class="about-info">
				<h3>About</h3>
				<p>{{ studentData.about }}</p>
			</div>
		</div>
		<div class="company-contact">
			<div class="info">
				<div class="contact-info">
					<h3>Links</h3>
					<span class="links">
						<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"
                            class="bi bi-github" viewBox="0 0 16 16">
                            <path
                                d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27s1.36.09 2 .27c1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.01 8.01 0 0 0 16 8c0-4.42-3.58-8-8-8" />
                        </svg>
						<h4 class="link-text">Github</h4>
						<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                            stroke="currentColor" class="size-6">
                            <path stroke-linecap="round" stroke-linejoin="round"
                                d="m4.5 19.5 15-15m0 0H8.25m11.25 0v11.25" />
                        </svg>
					</span>
					<span class="links">
						<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"
                            class="bi bi-linkedin" viewBox="0 0 16 16">
                            <path
                                d="M0 1.146C0 .513.526 0 1.175 0h13.65C15.474 0 16 .513 16 1.146v13.708c0 .633-.526 1.146-1.175 1.146H1.175C.526 16 0 15.487 0 14.854zm4.943 12.248V6.169H2.542v7.225zm-1.2-8.212c.837 0 1.358-.554 1.358-1.248-.015-.709-.52-1.248-1.342-1.248S2.4 3.226 2.4 3.934c0 .694.521 1.248 1.327 1.248zm4.908 8.212V9.359c0-.216.016-.432.08-.586.173-.431.568-.878 1.232-.878.869 0 1.216.662 1.216 1.634v3.865h2.401V9.25c0-2.22-1.184-3.252-2.764-3.252-1.274 0-1.845.7-2.165 1.193v.025h-.016l.016-.025V6.169h-2.4c.03.678 0 7.225 0 7.225z" />
                        </svg>
						<h4 class="link-text">LinkedIn</h4>
						<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                            stroke="currentColor" class="size-6">
                            <path stroke-linecap="round" stroke-linejoin="round"
                                d="m4.5 19.5 15-15m0 0H8.25m11.25 0v11.25" />
                        </svg>
					</span>
				</div>
			</div>
			<div class="info-btn" v-if="userRole === 'Admin'">
				<Button label="Unblacklist" class="apply-btn" @click="blacklistUser(false)" v-if="studentData.user?.blacklisted" />
				<Button label="Blacklist" class="apply-btn" @click="blacklistUser(true)" v-else />
			</div>
		</div>
	</div>
</template>

<style lang="css" scoped>
.company-content {
	display: flex;
	height: 100%;
	padding: 20px;
}

.company-info {
	flex-grow: 1;
}

.company-name {
	padding-bottom: 5px;
	margin-bottom: 5px;
}

.info-section {
	padding: 10px;
	margin-bottom: 5px;
	display: flex;
	gap: 10px;
	align-items: center;
}

.company-contact {
	width: 300px;
	height: 100%;
	padding: 10px 10px;
	background-color: var(--secondary-highlight-color);
	background-image: var(--topo-pattern);
	display: flex;
	flex-direction: column;
}

.info {
	flex-grow: 1;
}

.contact {
	display: flex;
	align-items: center;
	gap: 5px;
	height: 30px;
	padding: 2px 5px;
	font-size: 0.8em;
}

.contact>svg {
	display: block;
	height: 15px;
	width: 15px;
}

.info-btn {
	width: 100%;
	min-height: 15%;
	display: flex;
	flex-direction: column;
	justify-content: center;
	align-items: center;
}

.about-info {
	padding-top: 10px;
	padding-bottom: 10px;
}

.contact-info {
    flex-grow: 1;
    padding: 10px;
    border-radius: 10px;
    flex-direction: column;
    gap: 10px;
}

.links {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.3s ease;
}

.links:hover {
    background-color: rgba(255, 255, 255, 0.1);
}

.link-text {
    flex-grow: 1;
    margin: 0;
    font-weight: 600;
}

.links .size-6 {
    width: 24px;
    height: 24px;
    transition: transform 0.3s ease;
}

.links:hover .size-6 {
    transform: translateX(5px);
}

:deep(.apply-btn) {
	width: 80%;
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

.slide-up-enter-active,
.slide-up-leave-active {
	transition: all 0.25s ease-out;
}

.slide-up-enter-from {
	opacity: 0;
	transform: translateY(30px);
}

.slide-up-leave-to {
	opacity: 0;
	transform: translateY(-30px);
}
</style>