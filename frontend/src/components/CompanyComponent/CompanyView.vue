<script setup>
import { ref, onMounted } from 'vue';
import { useAuthStore } from '../../stores/auth';
import axios from 'axios';
import Header from '../Header.vue';
import CompanyCard from './CompanyCard.vue';
import Button from '../Button.vue';

const authStore = useAuthStore();
const userRole = authStore.getUserRole();

const props = defineProps({
    action: Boolean
});

const companyData = ref([]);
const pendingCompanyData = ref([]);
const industryData = ref([]);
const industrySet = ref(new Set());
const isLoading = ref(true);
const errorMessage = ref('');

async function fetchData() {
    isLoading.value = true;
    errorMessage.value = '';
    const urlMap = {
        approved: "/api/v1/company/?status=approved&blacklisted=false",
        industry: "/api/v1/utils/industry"
    };

    if (props.action) {
        urlMap.approved = "/api/v1/company/?status=approved&blacklisted=true";
    }

    if (userRole === 'Admin' && !props.action) {
        urlMap.pending = "/api/v1/company/?status=pending&blacklisted=false";
    }

    try {
        for (const key in urlMap) {
            const response = await axios.get(urlMap[key]);
            if (key === 'pending') {
                pendingCompanyData.value = response.data;
            } else if (key === 'approved') {
                companyData.value = response.data;
            } else if (key === 'industry') {
                industryData.value = response.data;
            }
        }
    } catch (error) {
        errorMessage.value = "Something went wrong!!!";
        console.error('Axios: ', error);
    } finally {
        isLoading.value = false;
    }
}

async function reloadData() {
    await fetchData();
};

async function applyFilter(industry = null) {
    if (industry) {
        if (industrySet.value.has(industry)) {
            industrySet.value.delete(industry);
        } else {
            industrySet.value.add(industry);
        }
    }

    let url = "/api/v1/company/?status=approved&blacklisted=false";

    industrySet.value.forEach((industryId) => {
        url = `${url}&industry_id=${industryId}`;
    });

    try {
        const response = await axios.get(url);
        companyData.value = response.data;
    } catch (error) {
        errorMessage.value = "Something went wrong!!!";
        console.error('Axios: ', error);
    } 
}

onMounted(fetchData);
</script>

<template>
    <div class="content-body">
            <Header heading="Company" v-if="!action" />
        <div class="content">
            <div class="loading" v-if="isLoading">
                <h2>Loading data...</h2>
            </div>
            <div class="loading" v-else-if="errorMessage">
                <h2>{{ errorMessage }}</h2>
                <Button label="Try again" @click="reloadData" />
            </div>
            <div class="loading" v-else-if="pendingCompanyData.length === 0 && companyData.length === 0">
                <h2>No results found.</h2>
            </div>
            <div class="company-content" v-else>
                <div class="approval-required" v-if="userRole === 'Admin' && pendingCompanyData.length > 0">
                    <h3 class="section-title">Approval Required</h3>
                    <div class="company-cards-container">
                        <CompanyCard v-for="company in pendingCompanyData" :key="company.id" :data="company" />
                    </div>
                </div>
                <h3 class="section-title" v-if="userRole==='Admin' && !action">Browse Company</h3>
                <div class="filter-labels">
                    <span class="labels" v-for="industry in industryData" :key="industry.id" :class="{ selected : industrySet.has(industry.id) }" @click="applyFilter(industry.id)">{{ industry.name }}</span>
                </div>
                <div class="company-cards-container">
                    <CompanyCard v-for="company in companyData" :key="company.id" :data="company" />
                </div>
            </div>
        </div>
    </div>
</template>

<style lang="css" scoped>
.content-body {
    height: 100vh;
    overflow-y: auto;
}

.company-content {
    height: 100%;
    width: 100%;
    overflow-y: auto;
}

.company-cards-container {
    width: 100%;
    display: flex;
    justify-content: flex-start;
    flex-wrap: wrap;
    gap: 20px;
    padding: 10px;
    box-sizing: border-box;
}


.approval-required {
    padding-bottom: 10px;
    margin-bottom: 10px;
    border-bottom: var(--secondary-highlight-color) 2px solid;
}

.section-title {
    margin-bottom: 5px;
}

.filter-labels {
    margin-top: 20px;
    margin-bottom: 20px;
}

.labels {
    display: inline-block;
    background-color: var(--secondary-highlight-color);
    border: var(--primary-highlight-color) 1px solid;
    margin: 2px 4px;
    padding: 5px 8px;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.1s ease;
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