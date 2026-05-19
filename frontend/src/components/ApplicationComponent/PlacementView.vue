<script setup>
import { ref, onMounted, toRef, watch } from 'vue';
import apiClient from '../../axios';
import Button from '../Button.vue';
import PlacementCard from './PlacementCard.vue';

const props = defineProps({
    studentId: String,
    driveId: String,
    companyId: String
});


const student = toRef(props, 'studentId');
const drive = toRef(props, 'driveId');
const company = toRef(props, 'companyId');
const placementData = ref([]);
const isLoading = ref(false);
const errorMessage = ref('');

async function fetchData() {
    isLoading.value = true;
    let url = '/api/v1/placements/';
    if (student.value) {
        url = `${url}?student_id=${student.value}`;
    } else if (drive.value) {
        url = `${url}?drive_id=${drive.value}`;
    } else if (company.value) {
        url = `${url}?company_id=${company.value}`;
    }
    
    try {
        const response = await apiClient.get(url);
        placementData.value = response.data;
    } catch (error) {
        errorMessage.value = "Something went wrong!!!";
        console.error('Axios: ', error);
    } finally {
        isLoading.value = false;
    }
}

watch([student, drive, company], fetchData);

onMounted(fetchData);

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
                <div class="loading" v-if="placementData.length < 1">
                    <h2>No placements found.</h2>
                </div>
                <div class="company-cards-container" v-else>
                    <PlacementCard v-for="placement in placementData" :key="placement.id" :placement-id="placement.id" />
                </div>
            </div>
        </div>
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
    width: 100%;
    display: flex;
    justify-content: flex-start;
    flex-wrap: wrap;
    gap: 20px;
    padding: 10px;
    box-sizing: border-box;
    overflow-y: auto;
}


.approval-required {
    padding-bottom: 10px;
    margin-bottom: 10px;
    border-bottom: var(--secondary-highlight-color) 2px solid;
}

.section-title {
    margin-bottom: 5px;
}

.chart {
    min-width: 350px;
    padding: 8px 15px;
    background-color: var(--secondary-highlight-color);
    background-image: var(--topo-pattern);
    background-size: 600px;
    background-position: center;
    border-radius: 10px;
    box-sizing: border-box;
    overflow-y: auto;
}

.filter-heading {
    display: flex;
    gap: 10px;
    align-items: center;
}

.filter-icon {
    height: auto;
    width: 40px;
}

.label-container {
    padding-bottom: 10px;
}

.border {
    padding-bottom: 5px;
    border-bottom: var(--primary-highlight-color) 1px solid;
}

.label-text {
    color: var(--primary-highlight-color);
    margin-bottom: 5px;
}

.labels {
    display: inline-block;
    background-color: var(--secondary-highlight-color);
    border: var(--primary-highlight-color) 1px solid;
    margin: 2px 2px;
    padding: 5px 8px;
    border-radius: 8px;
    cursor: pointer;
    transition: border 0.1s ease;
}

.labels:hover {
    background-color: var(--primary-highlight-color);
    color: white;
}

.selected {
    background-image: var(--topo-pattern);
    background-color: var(--primary-highlight-color);
    color: white;
}
</style>