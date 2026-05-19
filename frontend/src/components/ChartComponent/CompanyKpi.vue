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
    industry: [],
    count: [],
});
const isLoading = ref(false);
const errorMessage = ref('');

async function fetchData() {
    const url = `/api/v1/analytics/company`;
    isLoading.value = true;
    try {
        const response = await apiClient.get(url);
        const industry = [];
        const count = [];
        for (const branch of response.data.data) {
            industry.push(branch[0]);
            count.push(branch[1]);
        }
        data.value = { industry, count };
    } catch (error) {
        errorMessage.value = "Something went wrong";
        console.error("Axios: ", error);
    } finally {
        isLoading.value = false;
    }
}

ChartJS.register(Title, Tooltip, Legend, ArcElement)

const chartData = computed(() => ({
    labels: data.value.industry,
    datasets: [
        {
            borderColor: '#2D2D2D', borderWidth: 0, spacing: 2,
            backgroundColor: ['#FFD700', '#FF8C00', '#F5F5F5'],
            data: data.value.count
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
            <h3 class="chart-title">Company by</h3>
            <h3 class="chart-filter">Industry</h3>
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
</style>