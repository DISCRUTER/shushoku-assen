<script setup>
import { onMounted, ref } from 'vue';
import apiClient from '../../axios';
import PlacementInfo from './PlacementInfo.vue';

const placementData = ref({});
const errorMessage = ref('');
const showInfo = ref(false);

const props = defineProps({
    placementId: String
})

async function fetchPlacementData() {
    try {
        const response = await apiClient.get(`/api/v1/placements/${props.placementId}`);
        placementData.value = response.data;
    } catch (error) {
        errorMessage.value = "Something went wrong!!!";
        console.error('Axios: ', error);
    }
}

onMounted(fetchPlacementData);
</script>

<template>
    <div class="student-card" @click="showInfo=true">
        <div class="arrow">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                stroke="currentColor" class="size-6">
                <path stroke-linecap="round" stroke-linejoin="round" d="m4.5 19.5 15-15m0 0H8.25m11.25 0v11.25" />
            </svg>
        </div>
        <div class="student-about">
            {{ placementData.joining_date }} <br>
            {{ placementData.company?.registered_name }}
        </div>
        <div class="drive-name">
            <h3>{{ placementData.drive?.title }}</h3>
        </div>
        <Teleport to="body">
			<PlacementInfo :show="showInfo" @close="showInfo = false" :placement-data="placementData" />
		</Teleport>
    </div>
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

.drive-name {
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    align-items: flex-start;
    padding: 5px 8px;
    border-top-left-radius: 10px;
    border-top-right-radius: 10px;
    min-height: 100px;
    width: 100%;
    box-sizing: border-box;
}

.drive-name>h3 {
    font-weight: 400;
}

.student-about {
    padding: 10px 8px;
    flex-grow: 1;
    min-width: 100%;
    box-sizing: border-box;
}
</style>