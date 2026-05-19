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

const studentData = ref({});
const applicationCount = ref(0);
const placementsCount = ref(0);
const isLoading = ref(false);
const errorMessage = ref('');
const currentTab = ref('PlacementView')

const tabs = {
    ApplicationView,
    PlacementView
}

async function fetchData() {
    const urls = {
        'student': `/api/v1/students/${userId}`,
        'application': `/api/v1/analytics/application?student_id=${userId}&all=true`,
        'placements': `/api/v1/analytics/placements?student_id=${userId}&all=true`
    }
    isLoading.value = true;
    try {
        const requests = Object.entries(urls).map(async ([key, value]) => {
            const response = await apiClient.get(value);
            return { key, data: response.data };
        });
        const results = await Promise.all(requests);
        results.forEach(({ key, data }) => {
            if (key === 'student') {
                studentData.value = data;
            } else if (key === 'application') {
                applicationCount.value = data.data[0][1];
            } else if (key === 'placements') {
                placementsCount.value = data.data[0][1];
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
        <Header :heading="`${studentData.first_name} ${studentData.last_name}`" />
        <div class="student-content">
            <div class="left">
                <div class="academy-info">
                    <h3>{{ `${studentData.academic_degree?.name} in ${studentData.branch?.name}` }}</h3>
                    <h3>{{ `CGPA : ${studentData.cgpa}` }}</h3>
                </div>
                <div class="about-info">
                    <h3>{{ studentData.about }}</h3>
                </div>
                <div class="contact-info">
                    <span class="links">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"
                            class="bi bi-github" viewBox="0 0 16 16">
                            <path
                                d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27s1.36.09 2 .27c1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.01 8.01 0 0 0 16 8c0-4.42-3.58-8-8-8" />
                        </svg>
                        <h4 class="link-text">Github</h4>
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                            stroke="currentColor" class="size-6">
                            <path stroke-linecap="round" stroke-linejoin="round"
                                d="m4.5 19.5 15-15m0 0H8.25m11.25 0v11.25" />
                        </svg>
                    </span>
                    <span class="links">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"
                            class="bi bi-linkedin" viewBox="0 0 16 16">
                            <path
                                d="M0 1.146C0 .513.526 0 1.175 0h13.65C15.474 0 16 .513 16 1.146v13.708c0 .633-.526 1.146-1.175 1.146H1.175C.526 16 0 15.487 0 14.854zm4.943 12.248V6.169H2.542v7.225zm-1.2-8.212c.837 0 1.358-.554 1.358-1.248-.015-.709-.52-1.248-1.342-1.248S2.4 3.226 2.4 3.934c0 .694.521 1.248 1.327 1.248zm4.908 8.212V9.359c0-.216.016-.432.08-.586.173-.431.568-.878 1.232-.878.869 0 1.216.662 1.216 1.634v3.865h2.401V9.25c0-2.22-1.184-3.252-2.764-3.252-1.274 0-1.845.7-2.165 1.193v.025h-.016l.016-.025V6.169h-2.4c.03.678 0 7.225 0 7.225z" />
                        </svg>
                        <h4 class="link-text">LinkedIn</h4>
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
                    <component :is="tabs[currentTab]" class="tab" :student-id="studentData?.id" :chart="false">
                    </component>
                </Transition>
            </div>
            <div class="right">
                <div class="approval-container">
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
                </div>
                <div class="chart">
                    <ApplicationFunnel :studentId="userId" />
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
}

.student-content {
    flex-grow: 1;
    display: flex;
    padding: 10px;
    gap: 10px;
}

.left {
    background-color: var(--secondary-highlight-color);
    background-image: var(--topo-pattern);
    border-radius: 10px;
    width: 350px;
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

.academy-info {
    padding: 20px;
    background-color: white;
    background-image: var(--topo-pattern);
    border-radius: 10px;
    min-height: 0;
    max-height: 150px;
}

.about-info {
    height: 350px;
    overflow-y: auto;
    padding: 20px;
}

.contact-info {
    flex-grow: 1;
    padding: 30px;
    background-color: var(--primary-highlight-color);
    background-image: var(--topo-pattern);
    border-radius: 10px;
    color: white;
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
</style>