<script setup>
import axios from 'axios';
import { onMounted, ref } from 'vue';

const count = ref(0);
const isLoading = ref(false);
const errorMessage = ref('');

const props = defineProps({
    target: String
})

async function fetchCount() {
    isLoading.value = true;
    const url = `/api/v1/analytics/${props.target}?all=true`;
    try {
        const response = await axios.get(url);
        count.value = response.data.data[0][1];
    } catch (error) {
        errorMessage.value = "Something went wrong";
        console.error("Axios: ", error);
    } finally {
        isLoading.value = false;
    }
}

onMounted(fetchCount);
</script>

<template>
        <div class="chart-container">
            <div class="chart-header">
                <h3 class="chart-title">{{ target.toUpperCase() }}</h3>
            </div>
            <div class="chart-wrapper">
                <h1 class="count">{{ count }}</h1>
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
    gap: 5px;
    padding: 5px 5px;
    margin-bottom: 5px;
}

.chart-title {
    color: var(--primary-highlight-color);
}

.chart-wrapper {
    max-height: 250px;
}

.count {
    font-size: 6em;
    font-weight: 800;
    display: flex;
    justify-content: flex-end;
}
</style>