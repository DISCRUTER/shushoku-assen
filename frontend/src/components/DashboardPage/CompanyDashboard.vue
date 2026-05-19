<script setup>
import { ref, onMounted } from 'vue';
import apiClient from '../../axios';
import Header from '../Header.vue';
import { useAuthStore } from '../../stores/auth';
import ApplicationView from '../ApplicationComponent/ApplicationView.vue';
import PlacementView from '../ApplicationComponent/PlacementView.vue';
import ApplicationFunnel from '../ChartComponent/ApplicationFunnel.vue';

const authStore = useAuthStore();
const userId = authStore.getUserId();

const companyData = ref({});
const applicationCount = ref(0);
const placementsCount = ref(0);
const isLoading = ref(false);
const errorMessage = ref('');
const currentTab = ref('ApplicationView');

const tabs = {
    ApplicationView,
    PlacementView
}

async function fetchData() {
    const urls = {
        'company': `/api/v1/company/${userId}`,
        'application': `/api/v1/analytics/application?company_id=${userId}&all=true`,
        'placements': `/api/v1/analytics/placements?company_id=${userId}&all=true`
    }
    isLoading.value = true;
    try {
        const requests = Object.entries(urls).map(async ([key, value]) => {
            const response = await apiClient.get(value);
            return { key, data: response.data };
        });
        const results = await Promise.all(requests);
        results.forEach(({ key, data }) => {
            if (key === 'company') {
                companyData.value = data;
            } else if (key === 'application') {
                applicationCount.value = data.data ? data.data[0][1] : 0;
            } else if (key === 'placements') {
                placementsCount.value = data.data ? data.data[0][1] : 0;
            }
        });
    } catch (error) {
        errorMessage.value = "Something went wrong";
        console.error("Axios: ", error);
    } finally {
        isLoading.value = false;
    }
}

onMounted(fetchData);
</script>

<template>
    <div class="dashboard-content">
        <Header :heading="companyData.registered_name" />
        <div class="company-content">
            <div class="left">
                <div class="company-info-top">
                    <div class="industry">
                        <h4>Industry</h4>
                        <h3>{{ companyData.industry?.name }}</h3>
                    </div>
                    <div class="industry">
                        <h4>Location</h4>
                        <h3>{{ companyData.location }}</h3>
                    </div>
                </div>
                <div class="about-info">
                    <h3>{{ companyData.description }}</h3>
                </div>
                <div class="contact-info">
                    <span class="links" v-if="companyData.website">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"
                            class="bi bi-globe" viewBox="0 0 16 16">
                            <path
                                d="M0 8a8 8 0 1 1 16 0A8 8 0 0 1 0 8m7.5-6.923c-.67.204-1.335.82-1.887 1.855A7.97 7.97 0 0 1 5.145 4H7.5zM4.09 4a9.267 9.267 0 0 1 .64-1.539 6.7 6.7 0 0 1 .597-.933A7.025 7.025 0 0 0 2.255 4zm-.582 3.5c.03-.877.138-1.718.312-2.5H1.674a6.958 6.958 0 0 0-.656 2.5zM4.847 5a12.5 12.5 0 0 0-.338 2.5H7.5V5zM8.5 5v2.5h2.99a12.495 12.495 0 0 0-.337-2.5zM4.51 8.5a12.5 12.5 0 0 0 .337 2.5H7.5V8.5zm3.99 0V11h2.653c.187-.765.306-1.608.338-2.5zM5.145 12c.138.386.295.744.468 1.068.552 1.035 1.218 1.65 1.887 1.855V12zm.182 2.472a6.696 6.696 0 0 1-.597-.933A9.268 9.268 0 0 1 4.09 12H2.255a7.024 7.024 0 0 0 3.072 2.472M3.82 11a13.652 13.652 0 0 1-.312-2.5h-2.49c.062.89.291 1.733.656 2.5zm6.853 3.472A7.024 7.024 0 0 0 13.745 12H11.91a9.27 9.27 0 0 1-.64 1.539 6.688 6.688 0 0 1-.597.933M8.5 12v2.923c.67-.204 1.335-.82 1.887-1.855.173-.324.33-.682.468-1.068z" />
                        </svg>
                        <h4 class="link-text">Website</h4>
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                            stroke="currentColor" class="size-6">
                            <path stroke-linecap="round" stroke-linejoin="round"
                                d="m4.5 19.5 15-15m0 0H8.25m11.25 0v11.25" />
                        </svg>
                    </span>
                    <span class="links" v-if="companyData.contact_email">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"
                            class="bi bi-envelope" viewBox="0 0 16 16">
                            <path
                                d="M0 4a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2zm2-1a1 1 0 0 0-1 1v.217l7 4.2 7-4.2V4a1 1 0 0 0-1-1zm13 2.383-4.708 2.825L15 11.105zm-.034 6.876-5.64-3.471L8 9.583l-1.326-.795-5.64 3.47A1 1 0 0 0 2 13h12a1 1 0 0 0 .966-.741M1 11.105l4.708-2.897L1 5.383z" />
                        </svg>
                        <h4 class="link-text">Email</h4>
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                            stroke="currentColor" class="size-6">
                            <path stroke-linecap="round" stroke-linejoin="round"
                                d="m4.5 19.5 15-15m0 0H8.25m11.25 0v11.25" />
                        </svg>
                    </span>
                </div>
            </div>
            <div class="center">
                <Transition name="fade" mode="out-in">
                    <component :is="tabs[currentTab]" class="tab" :company-id="companyData?.id" :chart="false">
                    </component>
                </Transition>
            </div>
            <div class="right">
                <div class="approval-container">
                    <div class="approval" @click="currentTab = 'ApplicationView'"
                        :class="{ selected: currentTab === 'ApplicationView' }">
                        <div class="arrow">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                                stroke="currentColor" class="size-6">
                                <path stroke-linecap="round" stroke-linejoin="round"
                                    d="m4.5 19.5 15-15m0 0H8.25m11.25 0v11.25" />
                            </svg>
                        </div>
                        <h2 class="label">{{ applicationCount }}</h2>
                        <h3>APPLICATIONS</h3>
                    </div>
                    <div class="approval" @click="currentTab = 'PlacementView'"
                        :class="{ selected: currentTab === 'PlacementView' }">
                        <div class="arrow">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                                stroke="currentColor" class="size-6">
                                <path stroke-linecap="round" stroke-linejoin="round"
                                    d="m4.5 19.5 15-15m0 0H8.25m11.25 0v11.25" />
                            </svg>
                        </div>
                        <h2 class="label">{{ placementsCount }}</h2>
                        <h3>PLACEMENTS</h3>
                    </div>
                </div>
                <div class="chart">
                    <ApplicationFunnel :company-id="userId" />
                </div>
            </div>
        </div>
    </div>
</template>

<style lang="css" scoped>
.dashboard-content {
    display: flex;
    flex-direction: column;
    height: 100vh;
    width: 100%;
}

.company-content {
    flex-grow: 1;
    display: flex;
    padding: 10px;
    gap: 10px;
}

.left {
    background-color: var(--secondary-highlight-color);
    background-image: var(--topo-pattern);
    border-radius: 10px;
    min-width: 350px;
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.center {
    border-radius: 10px;
    flex-grow: 1;
    min-height: 0;
    overflow-y: auto;
}

.right {
    border-radius: 10px;
    width: 300px;
    display: flex;
    flex-direction: column;
    height: 100%;
}

.approval-container {
    width: 100%;
}

.approval {
    position: relative;
    height: 120px;
    width: 100%;
    line-height: 3em;
    background-color: var(--primary-highlight-color);
    color: white;
    background-image: var(--topo-pattern);
    background-size: 800px;
    background-position: center;
    box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.125);
    border-radius: 10px;
    margin-top: 10px;
    margin-bottom: 10px;
    padding: 20px 10px;
    box-sizing: border-box;
    cursor: pointer;
    transition: background-size 1.2s cubic-bezier(0.19, 1, 0.22, 1);
}

.approval:hover {
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

.approval:hover .arrow {
    transform: scale(1.3) translate(5px, -5px);
}

.label {
    font-weight: 700;
    font-size: 4em;
}

.selected {
    color: var(--primary-highlight-color);
    background-color: var(--accent-bar-color);
}

.chart {
    flex-grow: 1;
    background-image: var(--topo-pattern);
    background-color: var(--accent-bar-color);
    border-radius: 10px;
}

.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
    opacity: 0;
}

.company-info-top {
    padding: 20px;
    background-color: white;
    background-image: var(--topo-pattern);
    border-radius: 10px;
    min-height: 0;
    max-height: 150px;
}

.about-info {
    height: 320px;
    overflow-y: auto;
    min-width: 0;
    padding: 20px;
}

.contact-info {
    flex-grow: 1;
    padding: 30px;
    background-color: var(--primary-highlight-color);
    background-image: var(--topo-pattern);
    border-radius: 10px;
    color: white;
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.links {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.3s ease;
}

.links:hover {
    background-color: rgba(255, 255, 255, 0.1);
}

.link-text {
    flex-grow: 1;
    margin: 0;
    font-weight: 600;
}

.links .size-6 {
    width: 24px;
    height: 24px;
    transition: transform 0.3s ease;
}

.links:hover .size-6 {
    transform: translateX(5px);
}

.industry {
    line-height: 1.2;
    padding-bottom: 5px;
}
</style>