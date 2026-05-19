<script setup>
import { ref, onMounted } from 'vue';
import apiClient from '../../axios';
import Header from '../Header.vue';
import Button from '../Button.vue';
import StudentCard from './StudentCard.vue';

const props = defineProps({
    action: Boolean
});

const studentData = ref([]);
const academicDegree = ref([]);
const branchData = ref([]);
const branchSet = ref(new Set())
const degreeSet = ref(new Set())
const isLoading = ref(true);
const errorMessage = ref('');

async function fetchData() {
    isLoading.value = true;
    errorMessage.value = '';
    const urlMap = {
        students: "/api/v1/students/?blacklisted=false",
        branch: "/api/v1/utils/branch",
        academicDegree: "/api/v1/utils/academic-degree"
    };

    if (props.action) {
        urlMap.students = "/api/v1/students/?blacklisted=true";
    }

    try {
        for (const key in urlMap) {
            const response = await apiClient.get(urlMap[key]);
            if (key === 'students') {
                studentData.value = response.data;
            } else if (key === 'branch') {
                branchData.value = response.data;
            } else if (key === 'academicDegree') {
                academicDegree.value = response.data;
            }
        }
    } catch (error) {
        errorMessage.value = "Something went wrong!!!";
        console.error('Axios: ', error);
    } finally {
        isLoading.value = false;
    }
}

async function applyFilter(branch = null, degree = null) {
    if (branch) {
        if (branchSet.value.has(branch)) {
            branchSet.value.delete(branch);
        } else {
            branchSet.value.add(branch);
        }
    }
    if (degree) {
        if (degreeSet.value.has(degree)) {
            degreeSet.value.delete(degree);
        } else {
            degreeSet.value.add(degree);
        }
    }

    let url = "/api/v1/students/?blacklisted=false";
    if (props.action) {
        url = "/api/v1/students/?blacklisted=true";
    }

    branchSet.value.forEach((branchId) => {
        url = `${url}&branch_id=${branchId}`;
    });
    degreeSet.value.forEach((degreeId) => {
        url = `${url}&academic_degree_id=${degreeId}`;
    });

    try {
        const response = await apiClient.get(url);
        studentData.value = response.data;
    } catch (error) {
        errorMessage.value = "Something went wrong!!!";
        console.error('Axios: ', error);
    }
}

onMounted(fetchData);

async function reloadData() {
    await fetchData();
};
</script>

<template>
    <div class="content-body">
        <Header heading="Students" v-if="!action" />
        <div class="content">
            <div class="loading" v-if="isLoading">
                <h2>Loading data...</h2>
            </div>
            <div class="loading" v-else-if="errorMessage">
                <h2>{{ errorMessage }}</h2>
                <Button label="Try again" @click="reloadData" />
            </div>
            <div class="company-content" v-else>
                <div class="loading" v-if="studentData.length < 1">
                    <h2>No results found.</h2>
                </div>
                <div class="company-cards-container" v-else>
                    <StudentCard v-for="student in studentData" :key="student.id" :data="student" />
                </div>
                <div class="filter-labels">
                    <div class="filter-heading">
                        <span>
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                                stroke="currentColor" class="filter-icon">
                                <path stroke-linecap="round" stroke-linejoin="round"
                                    d="M10.5 6h9.75M10.5 6a1.5 1.5 0 1 1-3 0m3 0a1.5 1.5 0 1 0-3 0M3.75 6H7.5m3 12h9.75m-9.75 0a1.5 1.5 0 0 1-3 0m3 0a1.5 1.5 0 0 0-3 0m-3.75 0H7.5m9-6h3.75m-3.75 0a1.5 1.5 0 0 1-3 0m3 0a1.5 1.5 0 0 0-3 0m-9.75 0h9.75" />
                            </svg>
                        </span>
                        <h2>Filters</h2>
                    </div>
                    <div class="label-container">
                        <h3 class="label-text">Branch</h3>
                        <span class="labels" v-for="branch in branchData" :key="branch.id"
                            :class="{ selected: branchSet.has(branch.id) }" @click="applyFilter(branch.id)">
                            {{ branch.name }}
                        </span>
                    </div>
                    <div class="border"></div>
                    <div class="label-container">
                        <h3 class="label-text">Academic Degree</h3>
                        <span class="labels" v-for="degree in academicDegree" :key="degree.id"
                            :class="{ selected: degreeSet.has(degree.id) }" @click="applyFilter(null, degree.id)">
                            {{ degree.name }}</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style lang="css" scoped>
.company-content {
    height: 100%;
    width: 100%;
    display: flex;
    gap: 10px;
}

.company-cards-container {
    width: 100%;
    display: flex;
    justify-content: flex-start;
    flex-wrap: wrap;
    gap: 20px;
    padding: 10px;
    box-sizing: border-box;
    overflow-y: auto;
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
    max-width: 350px;
    padding: 8px 15px;
    background-color: var(--secondary-highlight-color);
    background-image: var(--topo-pattern);
    border-radius: 10px;
    box-sizing: border-box;
    overflow-y: auto;
}

.filter-heading {
    display: flex;
    gap: 10px;
    align-items: center;
}

.filter-icon {
    height: auto;
    width: 40px;
}

.label-container {
    padding-bottom: 10px;
}

.border {
    padding-bottom: 5px;
    border-bottom: var(--primary-highlight-color) 1px solid;
}

.label-text {
    color: var(--primary-highlight-color);
    margin-bottom: 5px;
}

.labels {
    display: inline-block;
    background-color: var(--secondary-highlight-color);
    border: var(--primary-highlight-color) 1px solid;
    margin: 2px 2px;
    padding: 5px 8px;
    border-radius: 8px;
    cursor: pointer;
    transition: border 0.1s ease;
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