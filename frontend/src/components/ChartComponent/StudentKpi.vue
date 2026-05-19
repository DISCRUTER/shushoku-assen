<script setup>
import { onMounted, ref, computed } from 'vue';
import apiClient from '../../axios';
import { Pie, Radar } from 'vue-chartjs';
import { 
  Chart as ChartJS, 
  Title, Tooltip, Legend, 
  ArcElement 
} from 'chart.js'

const activeFilter = ref('branch');
const data = ref({
    branch_label: [],
    branch_data: [],
    degree_label: [],
    degree_data: []
});
const isLoading = ref(false);
const errorMessage = ref('');

async function fetchData() {
    const url = `/api/v1/analytics/students`;
    isLoading.value = true;
    try {
        let response = await apiClient.get(`${url}?branch=true`);
        data.value['branch_label'] = [];
        data.value['branch_data'] = [];
        for (const branch of response.data.data) {
            data.value['branch_label'].push(branch[0]);
            data.value['branch_data'].push(branch[1]);
        }
        response = await apiClient.get(`${url}?academic_degree=true`);
        data.value['degree_label'] = [];
        data.value['degree_data'] = [];
        for (const degree of response.data.data) {
            data.value['degree_label'].push(degree[0]);
            data.value['degree_data'].push(degree[1]);
        }
    } catch (error) {
        errorMessage.value = "Something went wrong";
        console.error("Axios: ", error);
    } finally {
        isLoading.value = false;
    }
}

ChartJS.register(Title, Tooltip, Legend, ArcElement)

const chartData = computed(() => ({
    labels: activeFilter.value === 'branch' ? data.value.branch_label : data.value.degree_label,
    datasets: [
        {
            borderColor: '#2D2D2D', borderWidth: 0, spacing: 2,
            backgroundColor: ['#FFD700', '#FF8C00', '#F5F5F5'],
            data: activeFilter.value === 'branch' ? data.value.branch_data : data.value.degree_data
        }
    ]
}))

const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
        legend: {
            labels: {
                color: '#fff',
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
            <h3 class="chart-title">Student by</h3>
            <Transition name="slide-up" mode="out-in">
                <h3 class="chart-filter" v-if="activeFilter === 'branch'" @click="activeFilter = 'academic_degree'">
                    Branch
                </h3>
                <h3 class="chart-filter" v-else-if="activeFilter === 'academic_degree'"
                    @click="activeFilter = 'branch'">
                    Academic Degree</h3>
            </Transition>
        </div>
        <div class="chart-wrapper">
            <Pie :data="chartData" :options="chartOptions" />
        </div>
    </div>
</template>

<style lang="css" scoped>
.chart-container {
    box-sizing: border-box;
    padding: 5px 5px;
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
    color: white;
}

.chart-filter {
    color: var(--accent-bar-color);
    font-weight: 500;
    font-size: 2em;
    cursor: pointer;
}

.chart-wrapper {
    max-height: 250px;
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