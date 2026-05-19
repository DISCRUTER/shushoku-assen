<script setup>
import { ref } from 'vue';
import apiClient from '../../axios';
import CompanyInfo from './CompanyInfo.vue';

const companyData = ref(null);
const errorMessage = ref('');
const showInfo = ref(false);

const props = defineProps({
    data: Object
})

async function fetchCompanyData(companyId) {
    try {
        const response = await apiClient.get(`http://127.0.0.1:3000/api/v1/company/${companyId}`);
        companyData.value = response.data;
        console.log(companyData.value)
    } catch (error) {
        errorMessage.value = "Something went wrong!!!";
        console.error('Axios: ', error);
    } finally {
        showInfo.value = true;
    }
}

</script>

<template>
    <div class="company-card"  @click="fetchCompanyData(data.id)">
        <div class="arrow">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                stroke="currentColor" class="size-6">
                <path stroke-linecap="round" stroke-linejoin="round" d="m4.5 19.5 15-15m0 0H8.25m11.25 0v11.25" />
            </svg>
        </div>
        <div class="company-name">
            <h3>{{ data.registered_name }}</h3>
        </div>
        <div class="company-about">
            <p>{{ data.description }}</p>
        </div>
    </div>
    <Teleport to="body">
        <CompanyInfo :show="showInfo" @close="showInfo = false" :company-data="companyData" />
    </Teleport>
</template>

<style lang="css" scoped>
.company-card {
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
    min-height: 200px;
    width: 200px;
    border-radius: 10px;
    box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.125);
    background-color: white;
    background-image: var(--topo-pattern);
    background-size: 800px;
    background-position: center;
    cursor: pointer;
    box-sizing: border-box;
    transition: background-size 1.2s cubic-bezier(0.19, 1, 0.22, 1);
}

.company-card:hover {
    box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.297);
    background-size: 600px;
}

.arrow {
    position: absolute;
    top: 10px;
    right: 10px;
    height: 25px;
    width: 25px;
    z-index: 100;
    transition: transform 0.3s ease;
}

.company-card:hover .arrow {
    transform: scale(1.3) translate(5px, -5px);
}

.company-name {
    display: flex;
    justify-content: flex-start;
    align-items: flex-end;
    background-color: var(--accent-bar-color);
    padding: 5px 8px;
    border-top-left-radius: 10px;
    border-top-right-radius: 10px;
    height: 120px;
    width: 100%;
    box-sizing: border-box;
}

.company-name>h3 {
    font-weight: 400;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    width: 100%;
}

.company-about {
    padding: 8px 10px;
    flex-grow: 1;
    width: 100%;
    align-self: stretch;
    display: flex;
    flex-direction: column;
    align-items: center;
    overflow: hidden;
    box-sizing: border-box;
}

.company-about > p {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    width: 100%;
    text-align: center;
    margin: 0;
}
</style>