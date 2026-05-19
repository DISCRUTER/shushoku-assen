<script setup>
import { ref, onMounted, toRef } from 'vue';
import { useAuthStore } from '../../stores/auth';
import apiClient from '../../axios';
import DriveList from './DriveList.vue';
import DriveInfo from './DriveInfo.vue';
import Button from '../Button.vue';
import Header from '../Header.vue';
import CreateDrive from './CreateDrive.vue';

const authStore = useAuthStore();
const userId = authStore.getUserId();
const userRole = authStore.getUserRole();

const props = defineProps({
	companyId: String
});

const company = toRef(props, 'companyId')
const pendingDrive = ref([]);
const openDrive = ref([]);
const closedDrive = ref([]);
const appliedDrive = ref(new Set());
const isLoading = ref(true);
const errorMessage = ref('');
const selectedDrive = ref(null);
const showInfo = ref(false);

async function fetchData() {
	isLoading.value = true;
	errorMessage.value = '';
	const baseUrl = "/api/v1/drives/";
	const urlMap = {};
	if (userRole === 'Student') {
		if (company.value) {
			urlMap.open = `${baseUrl}?company_id=${company.value}&status=open`;
		} else {
			urlMap.open = `${baseUrl}?status=open`
		}
		urlMap.applied = `/api/v1/applications/?student_id=${userId}`
	} else if (userRole === 'Company' || company.value) {
		const id = company.value || userId;
		urlMap.pending = `${baseUrl}?company_id=${id}&status=pending`
		urlMap.open = `${baseUrl}?company_id=${id}&status=open`
		urlMap.closed = `${baseUrl}?company_id=${id}&status=closed`
	} else if (userRole === 'Admin') {
		urlMap.pending = `${baseUrl}?status=pending`
		urlMap.open = `${baseUrl}?status=open`
		urlMap.closed = `${baseUrl}?status=closed`
	}

	try {
		for (const key in urlMap) {
			const response = await apiClient.get(urlMap[key]);
			if (key === 'pending') {
				pendingDrive.value = response.data;
			} else if (key === 'open') {
				openDrive.value = response.data;
			} else if (key === 'closed') {
				closedDrive.value = response.data;
			} else if (key === 'applied') {
				for (const app of response.data) {
					appliedDrive.value.add(app.drive_id);
				}
			}
		}
	} catch (error) {
		errorMessage.value = "Something went wrong!!!";
		console.error('Axios: ', error);
	} finally {
		isLoading.value = false;
	}
}

onMounted(fetchData);

async function reloadData() {
	await fetchData();
};

function changeDriveInfo(driveId) {
	selectedDrive.value = driveId;
}

</script>

<template>
	<div class="drive-body">
		<Header heading="Drive" v-if="!companyId" />
		<div class="content">
			<div class="loading" v-if="isLoading">
				<h2>Loading data...</h2>
			</div>
			<div class="loading" v-else-if="errorMessage">
				<h2>{{ errorMessage }}</h2>
				<Button label="Try again" @click="reloadData" />
			</div>
			<div class="loading" v-else-if="openDrive.length === 0 && closedDrive.length === 0 && pendingDrive.length === 0">
				<h2>No drives found!</h2>
				<Button label="Start a Drive" @click="showInfo=true" v-if="userRole==='Company'" />
			</div>
			<div class="drive-content" v-else>
				<DriveList :open-drive="openDrive" :pending-drive="pendingDrive" :closed-drive="closedDrive"
					@drive-selected="changeDriveInfo" />
				<DriveInfo :drive-info="selectedDrive" :applied-drive="appliedDrive" />
			</div>
		</div>
		<Teleport to="body">
			<CreateDrive :show="showInfo" @close="showInfo = false" />
		</Teleport>
	</div>
</template>

<style lang="css" scoped>
.drive-body {
	flex-grow: 1;
	display: flex;
	flex-direction: column;
	width: 100%;
	height: 100%;
	overflow: hidden;
}

.content {
	flex-grow: 1;
	overflow: hidden;
	display: flex;
	flex-direction: column;
}

.drive-content {
	flex-grow: 1;
	display: flex;
	gap: 10px;
	overflow: hidden;
}
</style>