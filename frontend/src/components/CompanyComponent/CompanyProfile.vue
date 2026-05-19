<script setup>
import { ref } from 'vue';
import { useAuthStore } from '../../stores/auth';
import Button from '../Button.vue';
import apiClient from '../../axios';

const authStore = useAuthStore();
const userId = authStore.getUserId();
const userRole = authStore.getUserRole();


const props = defineProps({
	companyData: Object
})

async function changeStatus() {
	const payload = {
		status: 'approved'
	};

	try {
		const response = await apiClient.patch(`/api/v1/company/${props.companyData?.id}`, payload);
		if (response.status === 202) {
			Object.assign(props.companyData, response.data);
		} else {
			console.log('Something went wrong!');
		}
	} catch (error) {
		console.error("Axios: ", error);
	}
}

async function rejectCompany() {
	try {
		const response = await apiClient.delete(`/api/v1/company/${props.companyData?.id}`);
		if (response.status === 202) {
			window.location.reload()
		} else {
			console.log('Something went wrong!');
		}
	} catch (error) {
		console.error("Axios: ", error);
	}
}

async function blacklistUser(value) {
	const payload = {
		blacklisted: value
	};

	try {
		const response = await apiClient.patch(`/api/v1/company/${props.companyData?.id}`, payload);
		if (response.status === 202) {
			Object.assign(props.companyData, response.data);
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
			<h2 class="company-name">{{ companyData.registered_name }}</h2>
			<p>{{ companyData.description }}</p>
		</div>
		<div class="company-contact">
			<div class="info">
				<div class="info-section">
					<h3>Industry</h3>
					{{ companyData.industry.name }}
				</div>
				<div class="info-section">
					<h3>Contact Us</h3>
					<span class="contact">
						<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
							stroke="currentColor" class="size-6">
							<path stroke-linecap="round" stroke-linejoin="round"
								d="M2.25 6.75c0 8.284 6.716 15 15 15h2.25a2.25 2.25 0 0 0 2.25-2.25v-1.372c0-.516-.351-.966-.852-1.091l-4.423-1.106c-.44-.11-.902.055-1.173.417l-.97 1.293c-.282.376-.769.542-1.21.38a12.035 12.035 0 0 1-7.143-7.143c-.162-.441.004-.928.38-1.21l1.293-.97c.363-.271.527-.734.417-1.173L6.963 3.102a1.125 1.125 0 0 0-1.091-.852H4.5A2.25 2.25 0 0 0 2.25 4.5v2.25Z" />
						</svg>
						{{ companyData.contact_phone }}
					</span>
					<span class="contact">
						<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
							stroke="currentColor" class="size-6">
							<path stroke-linecap="round" stroke-linejoin="round"
								d="M21.75 6.75v10.5a2.25 2.25 0 0 1-2.25 2.25h-15a2.25 2.25 0 0 1-2.25-2.25V6.75m19.5 0A2.25 2.25 0 0 0 19.5 4.5h-15a2.25 2.25 0 0 0-2.25 2.25m19.5 0v.243a2.25 2.25 0 0 1-1.07 1.916l-7.5 4.615a2.25 2.25 0 0 1-2.36 0L3.32 8.91a2.25 2.25 0 0 1-1.07-1.916V6.75" />
						</svg>
						{{ companyData.contact_email }}</span>
					<span class="contact">
						<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
							stroke="currentColor" class="size-6">
							<path stroke-linecap="round" stroke-linejoin="round"
								d="M12.75 3.03v.568c0 .334.148.65.405.864l1.068.89c.442.369.535 1.01.216 1.49l-.51.766a2.25 2.25 0 0 1-1.161.886l-.143.048a1.107 1.107 0 0 0-.57 1.664c.369.555.169 1.307-.427 1.605L9 13.125l.423 1.059a.956.956 0 0 1-1.652.928l-.679-.906a1.125 1.125 0 0 0-1.906.172L4.5 15.75l-.612.153M12.75 3.031a9 9 0 0 0-8.862 12.872M12.75 3.031a9 9 0 0 1 6.69 14.036m0 0-.177-.529A2.25 2.25 0 0 0 17.128 15H16.5l-.324-.324a1.453 1.453 0 0 0-2.328.377l-.036.073a1.586 1.586 0 0 1-.982.816l-.99.282c-.55.157-.894.702-.8 1.267l.073.438c.08.474.49.821.97.821.846 0 1.598.542 1.865 1.345l.215.643m5.276-3.67a9.012 9.012 0 0 1-5.276 3.67m0 0a9 9 0 0 1-10.275-4.835M15.75 9c0 .896-.393 1.7-1.016 2.25" />
						</svg>
						<a :href="companyData.website">{{ companyData.website }}</a>
					</span>
					<span class="contact">
						<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
							stroke="currentColor" class="size-6">
							<path stroke-linecap="round" stroke-linejoin="round"
								d="M15 10.5a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
							<path stroke-linecap="round" stroke-linejoin="round"
								d="M19.5 10.5c0 7.142-7.5 11.25-7.5 11.25S4.5 17.642 4.5 10.5a7.5 7.5 0 1 1 15 0Z" />
						</svg>
						{{ companyData.location }}
					</span>
				</div>
			</div>
			<div class="info-btn" v-if="userRole === 'Admin'">
				<template v-if="companyData.status === 'PENDING'">
					<Button label="Approve" class="apply-btn" @click="changeStatus" />
					<Button label="Reject" class="apply-btn" @click="rejectCompany" />
				</template>
				<Button label="Unblacklist" class="apply-btn" @click="blacklistUser(false)" v-else-if="companyData.user?.blacklisted" />
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
	padding-bottom: 5px;
	margin-bottom: 5px;
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