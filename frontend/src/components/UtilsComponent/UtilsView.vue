<script setup>
import { onMounted, ref } from 'vue';
import Header from '../Header.vue';
import apiClient from '../../axios';
import UtilsCard from './UtilsCard.vue';
import AddUtils from './AddUtils.vue';
import Button from '../Button.vue';

const isLoading = ref(false);
const errorMessage = ref('');
const utilsData = ref([]);
const addUtils = ref(false);
const addUtilData = ref({});

const urls = {
    'Branch': '/api/v1/utils/branch',
    'Academic Degree': '/api/v1/utils/academic-degree',
    'Industry': '/api/v1/utils/industry',
    'Skills': '/api/v1/utils/skills'
}

async function fetchData() {
    isLoading.value = true;
    try {
        const requests = Object.entries(urls).map(async ([label, endpoint]) => {
            const response = await apiClient.get(endpoint);
            return { [label]: response.data };
        });
        const results = await Promise.all(requests);
        utilsData.value = results;
    } catch (error) {
        errorMessage.value = "Something went wrong!!!";
        console.log("Axios: ", error);
    } finally {
        isLoading.value = false;
    }
}

function addRequest(category) {
    addUtilData.value['name'] = category;
    addUtilData.value['url'] = urls[category];

    addUtils.value = true;
}

function reloadData() {
    errorMessage.value = '';
    fetchData();
}

onMounted(fetchData);
</script>


<template>
    <div class="content-body">
        <Header heading="Utils" />
        <div class="content">
            <div class="loading" v-if="isLoading">
                <h2>Loading data...</h2>
            </div>
            <div class="loading" v-else-if="errorMessage">
                <h2>{{ errorMessage }}</h2>
                <Button label="Try again" @click="reloadData" />
            </div>
            <div class="utils-content" v-else>
                <div class="utils-container" v-for="(item, index) in utilsData" :key="index">
                    <template v-for="(list, category) in item" :key="category">
                        <div class="utils-header">
                            <h3 class="section-title">{{ category }}</h3>
                            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="var(--add-icon-color)"
                                class="add-utils" @click="addRequest(category)">
                                <path
                                    d="M10.75 4.75a.75.75 0 0 0-1.5 0v4.5h-4.5a.75.75 0 0 0 0 1.5h4.5v4.5a.75.75 0 0 0 1.5 0v-4.5h4.5a.75.75 0 0 0 0-1.5h-4.5v-4.5Z" />
                            </svg>
                        </div>
                        <div class="utils-cards-container">
                            <UtilsCard v-for="util in list" :key="util.id" :data="util" />
                        </div>
                    </template>
                </div>
            </div>
        </div>
        <Teleport to="body">
            <AddUtils :show="addUtils" @close="addUtils = false" :add-util-data="addUtilData" />
        </Teleport>
    </div>
</template>

<style lang="css" scoped>
.content-body {
    height: 100vh;
    overflow-y: auto;
}

.utils-content {
    height: 100%;
    width: 100%;
    overflow-y: auto;
}

.utils-cards-container {
    width: 100%;
    display: flex;
    justify-content: flex-start;
    flex-wrap: wrap;
    gap: 20px;
    padding: 10px;
    box-sizing: border-box;
}

.add-utils {
    height: 35px;
    padding: 5px;
    cursor: pointer;
    --add-icon-color: var(--primary-highlight-color);
    transition: all 0.2s ease;
}

.add-utils:hover {
    --add-icon-color: var(--accent-bar-color);
    transform: scale(1.5) rotate(0.125turn);
}

.utils-header {
    display: flex;
    gap: 5px;
    align-items: center;
}


.utils-container {
    padding-bottom: 10px;
    margin-bottom: 10px;
    border-bottom: var(--secondary-highlight-color) 2px solid;
}

.section-title {
    font-size: 2em;
    font-weight: 400;
}
</style>