<script setup>
import { ref, onMounted, toRef, watch } from 'vue';
import apiClient from '../../axios';
import Button from '../Button.vue';
import { useAuthStore } from '../../stores/auth';
import CreateDrive from '../DriveComponent/CreateDrive.vue';
import ApplicationFunnel from '../ChartComponent/ApplicationFunnel.vue';
import ApplicationCard from './ApplicationCard.vue';

const props = defineProps({
    studentId: String,
    driveId: String,
    companyId: String,
    chart: Boolean
});

const authStore = useAuthStore();
const userRole = authStore.getUserRole();

const student = toRef(props, 'studentId');
const drive = toRef(props, 'driveId');
const company = toRef(props, 'companyId');
const applicationData = ref([]);
const isLoading = ref(false);
const errorMessage = ref('');
const showInfo = ref(false);

async function fetchData() {
    isLoading.value = true;
    let url = '/api/v1/applications/';
    if (student.value) {
        url = `${url}?student_id=${student.value}`;
    } else if (drive.value) {
        url = `${url}?drive_id=${drive.value}`;
    } else if (company.value) {
        url = `${url}?company_id=${company.value}`;
    }

    try {
        const response = await apiClient.get(url);
        applicationData.value = response.data;
    } catch (error) {
        errorMessage.value = "Something went wrong!!!";
        console.error('Axios: ', error);
    } finally {
        isLoading.value = false;
    }
}

onMounted(fetchData);

watch([student, drive, company], fetchData);

async function reloadData() {
    await fetchData();
};
</script>

<template>
    <div class="content-body">
        <div class="content">
            <div class="loading" v-if="isLoading">
                <h2>Loading data...</h2>
            </div>
            <div class="loading" v-else-if="errorMessage">
                <h2>{{ errorMessage }}</h2>
                <Button label="Try again" @click="reloadData" />
            </div>
            <div class="company-content" v-else>
                <div class="loading" v-if="applicationData.length < 1">
                    <h2>No applications found.</h2>
                    <Button label="Start a Drive" @click="showInfo=true" v-if="userRole==='Company'" />
                </div>
                <template v-else>
                    <div class="company-cards-container">
                        <ApplicationCard v-for="application in applicationData" :key="application.id"
                            :application-id="application.id" class="cards" />
                    </div>
                    <div class="chart" v-if="chart === true">
                        <ApplicationFunnel :studentId="student" :driveId="drive" />
                    </div>
                </template>
            </div>
        </div>
        <Teleport to="body">
			<CreateDrive :show="showInfo" @close="showInfo = false" />
		</Teleport>
    </div>
</template>

<style lang="css" scoped>
.content-body {
    height: 100%;
    overflow-y: auto;
}

.content {
    height: 100%;
}

.company-content {
    height: 100%;
    width: 100%;
    display: flex;
    gap: 10px;
}

.company-cards-container {
    min-width: 0;
    min-height: 0;
    flex-grow: 1;
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 10px;
    padding: 10px;
    box-sizing: border-box;
    overflow-y: auto;
}

.chart {
    max-width: 30%;
    padding: 8px 15px;
    background-color: var(--secondary-highlight-color);
    background-image: var(--topo-pattern);
    background-size: 600px;
    background-position: center;
    border-radius: 10px;
    box-sizing: border-box;
    overflow-y: auto;
}
</style>