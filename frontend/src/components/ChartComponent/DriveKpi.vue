<script setup>
import { onMounted, ref, computed } from 'vue';
import apiClient from '../../axios';
import { Bar } from 'vue-chartjs';
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js';


const activeFilter = ref('company');
const data = ref({
    job_type: [],
    job_type_value: [],
    company: [],
    company_value: []
});
const isLoading = ref(false);
const errorMessage = ref('');

async function fetchData() {
    const url = `/api/v1/analytics/drives`;
    isLoading.value = true;
    try {
        let response = await apiClient.get(`${url}`);
        data.value['job_type'] = [];
        data.value['job_type_value'] = [];
        for (const branch of response.data.data) {
            data.value['job_type'].push(branch[0]);
            data.value['job_type_value'].push(branch[1]);
        }
        response = await apiClient.get(`${url}?by_company=true`);
        data.value['company'] = [];
        data.value['company_value'] = [];
        for (const degree of response.data.data) {
            data.value['company'].push(degree[0]);
            data.value['company_value'].push(degree[1]);
        }
    } catch (error) {
        errorMessage.value = "Something went wrong";
        console.error("Axios: ", error);
    } finally {
        isLoading.value = false;
    }
}

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

const chartData = computed(() => ({
    labels: activeFilter.value === 'job_type' ? data.value.job_type : data.value.company,
    datasets: [
        {
            borderColor: '#2D2D2D', borderWidth: 0, spacing: 2,
            backgroundColor: ['#FFD700', '#FF8C00', '#3c3c3c'],
            data: activeFilter.value === 'job_type' ? data.value.job_type_value : data.value.company_value
        }
    ]
}))

const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
        legend: {
            labels: {
                color: '#3c3c3c',
            },
            position: 'bottom'
        }
    }
}

onMounted(fetchData);

</script>

<template>
    <div class="chart-container">
        <div class="chart-header">
            <h3 class="chart-title">Drives by</h3>
            <Transition name="slide-up" mode="out-in">
                <h3 class="chart-filter" v-if="activeFilter === 'job_type'" @click="activeFilter = 'company'">
                    Job Type
                </h3>
                <h3 class="chart-filter" v-else-if="activeFilter === 'company'"
                    @click="activeFilter = 'job_type'">
                    Company</h3>
            </Transition>
        </div>
        <div class="chart-wrapper">
            <Bar :data="chartData" :options="chartOptions" />
        </div>
    </div>
</template>

<style lang="css" scoped>
.chart-container {
    box-sizing: border-box;
    padding: 5px 5px;
    height: 100%;
    display: flex;
    gap: 10px;
    flex-direction: column;
}

.chart-header {
    display: flex;
    justify-content: flex-start;
    align-items: center;
    gap: 5px;
    padding: 5px 5px;
    margin-bottom: 5px;
}

.chart-title {
    color: var(--primary-highlight-color);
}

.chart-filter {
    color: var(--accent-bar-color);
    background-color: var(--primary-highlight-color);
    padding-right: 5px;
    padding-left: 5px;
    border-radius: 10px;
    font-weight: 500;
    font-size: 2em;
    cursor: pointer;
}

.chart-wrapper {
    flex-grow: 1;
    position: relative;
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