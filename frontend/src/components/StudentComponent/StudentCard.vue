<script setup>
import { ref } from 'vue';
import apiClient from '../../axios';
import StudentInfo from './StudentInfo.vue';

const studentData = ref(null);
const errorMessage = ref('');
const showInfo = ref(false);

const props = defineProps({
    data: Object
})

async function fetchStudentData(studentId) {
    try {
        const response = await apiClient.get(`/api/v1/students/${studentId}`);
        studentData.value = response.data;
        showInfo.value = true;
    } catch (error) {
        errorMessage.value = "Something went wrong!!!";
        console.error('Axios: ', error);
    }
}
</script>

<template>
    <div class="student-card" @click="fetchStudentData(data.id)">
        <div class="arrow">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                stroke="currentColor" class="size-6">
                <path stroke-linecap="round" stroke-linejoin="round" d="m4.5 19.5 15-15m0 0H8.25m11.25 0v11.25" />
            </svg>
        </div>
        <div class="student-name">
            <h3>{{ data.first_name }}</h3>
            <h3>{{ data.last_name }}</h3>
        </div>
        <div class="student-about">
            <p>{{ data.academic_degree.name }} - {{ data.year }} Year</p>
            <p>{{ data.branch.name }}</p>
        </div>
    </div>
    <Teleport to="body">
        <StudentInfo :show="showInfo" @close="showInfo = false" :student-data="studentData" />
    </Teleport>
</template>

<style scoped>
.student-card {
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
    min-height: 100px;
    max-height: 175px;
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

.student-card:hover {
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

.student-card:hover .arrow {
    transform: scale(1.3) translate(5px, -5px);
}

.student-name {
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    align-items: flex-start;
    background-color: var(--accent-bar-color);
    padding: 5px 8px;
    border-top-left-radius: 10px;
    border-top-right-radius: 10px;
    min-height: 100px;
    width: 100%;
    box-sizing: border-box;
}

.student-name>h3 {
    font-weight: 400;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    width: 100%;
}

.student-about {
    padding: 10px 8px;
    flex-grow: 1;
    width: 100%;
    align-self: stretch;
    overflow: hidden;
    box-sizing: border-box;
}

.student-about > p {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    width: 100%;
    margin: 2px 0;
}
</style>