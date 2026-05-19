<script setup>
import { shallowRef, ref, computed, watchEffect, toRef } from 'vue'
import apiClient from '../../axios'
import { Chart as ChartJS, Title, Tooltip, Legend, CategoryScale, LinearScale } from 'chart.js'
import { FunnelController, TrapezoidElement } from 'chartjs-chart-funnel'
import { Chart } from 'vue-chartjs'
import Button from '../Button.vue'

ChartJS.register(Title, Tooltip, Legend, CategoryScale, LinearScale, FunnelController, TrapezoidElement)

const chartComponent = shallowRef(Chart)

const data = ref({
    status: [],
    count: []
});
const isLoading = ref(false);
const errorMessage = ref('');

const props = defineProps({
    studentId: String,
    driveId: String,
    companyId: String
})

const student = toRef(props, 'studentId');
const company = toRef(props, 'companyId');
const drive = toRef(props, 'driveId');

async function fetchData() {
    let url = `/api/v1/analytics/application?by_status=true`;
    if (student.value) {
        url = `${url}&student_id=${student.value}`;
    } else if (drive.value) {
        url = `${url}&drive_id=${drive.value}`;
    } else if (company.value) {
        url = `${url}&company_id=${company.value}`;
    }
    isLoading.value = true;
    errorMessage.value = '';
    try {
        const response = await apiClient.get(url);
        const status = [];
        const count = [];
        for (const branch of response.data.data) {
            status.push(branch[0]);
            count.push(branch[1]);
        }
        data.value = { status, count };
    } catch (error) {
        errorMessage.value = "Something went wrong";
        console.error("Axios: ", error);
    } finally {
        isLoading.value = false;
    }
}

const chartData = computed(() => ({
  labels: data.value.status,
  datasets: [
    {
      label: 'Sales Funnel',
      backgroundColor: [
        '#ffffff',
        "#e5e5e5",
        '#B3B3B3',
        '#7D7D7D',
        '#3c3c3c'
      ],
      data: data.value.count,
      type: 'funnel'
    }
  ]
}))

const chartOptions = {
  indexAxis: 'y',
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { display: false },
    tooltip: {
      backgroundColor: '#1a1a1a',
      titleColor: '#FFD700',
      bodyColor: '#FFFFFF',
      borderColor: '#FFD700',
      borderWidth: 0
    }
  },
  scales: {
    x: { display: false },
    y: {
      ticks: { color: '#FFFFFF', font: { size: 14 } },
      grid: { display: false }
    }
  }
}

watchEffect(fetchData);

</script>

<template>
    <div class="chart-container">
        <div class="chart-header">
            <h3 class="chart-title">Application by</h3>
            <h3 class="chart-filter">Status</h3>
        </div>
        <div class="chart-wrapper">
            <div v-if="isLoading" class="message-container">
                <h3>Loading...</h3>
            </div>
            <div v-else-if="errorMessage" class="message-container">
                <h3>{{ errorMessage }}</h3>
                <Button label="Try again" @click="fetchData" />
            </div>
            <div v-else-if="data.status.length === 0" class="message-container">
                <h3>No data found</h3>
            </div>
            <component v-else :is="chartComponent" type="funnel" :data="chartData" :options="chartOptions" />
        </div>
    </div>
</template>

<style lang="css" scoped>
.chart-container {
    box-sizing: border-box;
    padding: 5px 5px;
    height: 100%;
    display: flex;
    flex-direction: column;
}

.chart-header {
    display: flex;
    justify-content: flex-start;
    align-items: center;
    gap: 5px;
    padding: 5px 5px;
}

.chart-title {
    color: var(--primary-highlight-color);
}

.chart-filter {
    color: var(--primary-highlight-color);
    font-weight: 600;
    font-size: 2em;
    cursor: pointer;
}

.chart-wrapper {
    padding: 10px 10px;
    box-sizing: border-box;
    flex-grow: 1;
    position: relative;
}

.message-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100%;
    color: var(--primary-highlight-color);
}
</style>