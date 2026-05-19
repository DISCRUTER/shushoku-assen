<script setup>
import { ref, watch, computed } from 'vue';
import apiClient from '../../axios';
import { useAuthStore } from '../../stores/auth';
import { download } from '../../download';
import Button from '../Button.vue';
import DriveAbout from './DriveAbout.vue';
import ApplicationView from '../ApplicationComponent/ApplicationView.vue';
import PlacementView from '../ApplicationComponent/PlacementView.vue';


const authStore = useAuthStore();
const userId = authStore.getUserId();
const userRole = authStore.getUserRole();

const props = defineProps({
    driveInfo: [Object, String, Number],
    appliedDrive: Set
});

const driveId = computed(() => {
    if (props.driveInfo && typeof props.driveInfo === 'object') {
        return props.driveInfo.id;
    }
    return props.driveInfo;
});

const data = ref(null);
const isLoading = ref(false);
const errorMessage = ref('');
const applied = ref(false);

const currentTab = ref('DriveAbout');

const tabs = {
    DriveAbout,
    ApplicationView,
    PlacementView
}

watch(driveId, () => {
    if (driveId.value) {
        updateDriveInfo();
    }
});

async function updateDriveInfo() {
    isLoading.value = true;
    if (props.appliedDrive && props.appliedDrive.has(driveId.value)) {
        applied.value = true;
    } else {
        applied.value = false;
    }
    try {
        const response = await apiClient.get(`/api/v1/drives/${driveId.value}`);
        data.value = response.data;
    } catch (error) {
        errorMessage.value = "Something went wrong!!!";
        console.error('Axios: ', error);
    } finally {
        isLoading.value = false;
    }
}

async function changeDriveStatus(state) {
    let payload = {};
    if (state === 'approve') {
        payload = {
            status: 'open'
        }
    } else if (state === 'close') {
        payload = {
            status: 'closed'
        }
    }

    try {
        const response = await apiClient.patch(`/api/v1/drives/${driveId.value}`, payload);
        if (response.status === 200) {
            data.value = response.data;
        }
    } catch (error) {
        errorMessage.value = "Something went wrong";
        console.error("Axios: ", error);
    } finally {
        window.location.reload();
    }
}

async function applyDrive() {
    const payload = {
        drive_id: driveId.value,
        student_id: userId
    }
    try {
        const response = await apiClient.post('/api/v1/applications/', payload);
        if (response.status === 201) {
            applied.value = true;
        }
    } catch (error) {
        console.error("Axios: ", error);
    }
}

async function deleteDrive() {
    try {
        const response = await apiClient.delete(`/api/v1/drives/${driveId.value}`);
        if (response.status === 202) {
            console.log("Deleted: ", driveId.value);
            window.location.reload();
        }
    } catch (error) {
        console.error("Axios: ", error);
    }
}

</script>

<template>
    <div class="drive-info-container" v-if="data">
        <div class="drive-info-head">
            <div class="drive-title">
                <h2>{{ data.title }}</h2>
                <h3>{{ data.company.registered_name }}</h3>
            </div>
            <div class="drive-apply">
                <Button label="Approve" class="apply-btn" v-if="data.status === 'pending' && userRole === 'Admin'"
                    @click="changeDriveStatus('approve')" />
                <Button label="Reject" class="apply-btn" v-if="data.status === 'pending' && userRole === 'Admin'"
                    @click="deleteDrive" />
                <Button label="Close" class="apply-btn" v-else-if="data.status === 'open' && userRole !== 'Student'"
                    @click="changeDriveStatus('close')" />

                <Button label="Apply" class="apply-btn" v-else-if="data.status === 'open' && userRole === 'Student' && !applied" @click="applyDrive" />
                <Button label="Applied" class="apply-btn" v-else-if="data.status === 'open' && userRole === 'Student' && applied" />

                <Button label="Closed" class="apply-btn" v-else-if="data.status === 'closed' && userRole !== 'Student'" />
            </div>
        </div>
        <DriveAbout :data="data" v-if="userRole==='Student'" class="drive-content" />
        <div class="drive-content" v-else>
            <Transition name="fade" mode="out-in">
                <component :is="tabs[currentTab]" class="tab" :data="data" :drive-id="data?.id" :chart="true">
                </component>
            </Transition>
            <div class="hotbar">
                
                <span class="hotbar-icon-container" :class="{ 'active': currentTab === 'DriveAbout' }"
                    @click="currentTab = 'DriveAbout'">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 44 49"
                        class="hotbar-icon">
                        <path fill="var(--hot-bar-color)"
                            d="M17.123,48.243 L17.123,8.711 L35.000,20.840 L43.285,20.840 L43.285,36.113 L35.000,36.113 L17.123,48.243 ZM9.253,0.256 L14.966,0.256 L14.966,5.930 L9.253,5.930 L9.253,0.256 ZM0.967,0.256 L6.680,0.256 L6.680,5.930 L0.967,5.930 L0.967,0.256 ZM13.264,15.581 L6.882,15.581 L6.882,41.372 L13.264,41.372 L13.264,46.884 L1.332,46.884 L1.332,10.069 L13.264,10.069 L13.264,15.581 ZM34.848,47.434 L34.848,39.054 L43.285,39.054 L34.848,47.434 Z">
                        </path>
                    </svg>
                    <div class="options-selected"></div>
                </span>
                <span class="hotbar-icon-container" :class="{ 'active': currentTab === 'ApplicationView' }"
                    @click="currentTab = 'ApplicationView'">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 41 48" class="hotbar-icon">
                        <path fill-rule="evenodd" fill="var(--hot-bar-color)"
                            d="M5.049,47.298 L5.049,41.157 L34.758,41.157 L34.758,12.322 L40.768,12.322 L40.768,41.157 L40.768,44.969 L40.768,47.298 L5.049,47.298 ZM0.243,0.899 L24.037,0.899 C26.983,3.909 28.645,5.607 31.591,8.617 L31.591,38.231 L0.243,38.231 L0.243,0.899 ZM6.587,31.401 L25.246,31.401 L25.246,26.809 L6.587,26.809 L6.587,31.401 Z">
                        </path>
                    </svg>
                    <div class="options-selected"></div>
                </span>
                <span class="hotbar-icon-container" :class="{ 'active': currentTab === 'PlacementView' }"
                    @click="currentTab = 'PlacementView'">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 44 49"
                        class="hotbar-icon">
                        <path fill="var(--hot-bar-color)"
                            d="M43.057,48.470 L37.334,48.470 L6.667,48.470 L0.942,48.470 L0.942,40.719 L0.942,15.502 L0.941,15.502 L0.941,6.304 L0.942,6.304 L0.942,6.301 L6.667,6.301 L6.667,6.304 L9.743,6.304 L9.743,10.903 L34.526,10.903 L34.526,6.304 L37.334,6.304 L37.334,6.301 L43.058,6.301 L43.058,48.470 L43.057,48.470 ZM37.334,15.502 L6.667,15.502 L6.667,40.719 L10.448,40.719 L10.448,35.267 C10.448,32.112 12.951,29.554 16.037,29.554 L27.963,29.554 C31.049,29.554 33.551,32.112 33.551,35.267 L33.551,40.719 L37.334,40.719 L37.334,15.502 ZM22.000,27.793 C19.155,27.793 16.848,25.434 16.848,22.526 C16.848,19.617 19.155,17.259 22.000,17.259 C24.845,17.259 27.152,19.617 27.152,22.526 C27.152,25.434 24.845,27.793 22.000,27.793 ZM9.743,0.506 L34.526,0.506 L34.526,6.304 L9.743,6.304 L9.743,0.506 Z">
                        </path>
                    </svg>
                    <div class="options-selected"></div>
                </span>
                <span class="divide"></span>
                <span class="hotbar-icon-container" @click="download('Drive', driveId)">
                    <svg xmlns="http://www.w3.org/2000/svg" class="hotbar-icon" viewBox="0 0 28 29"><path fill="var(--hot-bar-download-color)" d="M20.836,14.872 L20.836,0.013 L7.162,0.013 L7.162,7.976 L13.999,14.872 L-0.006,14.872 L13.999,28.999 L28.004,14.872 L20.836,14.872 Z"></path></svg>
                </span>
            </div>
        </div>
    </div>
    <div class="no-info" v-else>
        <h2>Select a drive to view info.</h2>
    </div>
</template>

<style lang="css" scoped>
.drive-info-container {

    position: relative;
    padding: 10px 20px;
    flex-grow: 1;
    flex-shrink: 1;
    min-width: 0;
    border: var(--secondary-highlight-color) solid 2px;
    display: flex;
    flex-direction: column;
    box-sizing: border-box;
    overflow-y: auto; 
}

.drive-info-head {
    display: flex;
    height: 20%;
    margin-bottom: 20px;
    padding-bottom: 10px;
    border-bottom: var(--secondary-highlight-color) solid 2px;
}

.drive-apply {
    min-width: 25%;
    display: flex;
    justify-content: center;
    align-items: center;
}

.drive-title {
    flex-grow: 1;
}

.drive-content {
    flex-grow: 1;
}

.hotbar {
    position: absolute;
    z-index: 20;
    height: 40px;
    width: 200px;
    display: flex;
    justify-content: space-around;
    align-items: center;
    padding: 5px 5px;
    padding-top: 10px;
    box-sizing: border-box;
    top: 85%;
    left: 40%;
    background-color: var(--secondary-highlight-color); 
    box-shadow: 1px 0px 5px rgb(167, 167, 167);
    border-radius: 10px;
}

.hotbar-icon-container {
    position: relative;
    border-radius: 10px;
    padding: 5px 5px;
    cursor: pointer;
    transition: all 0.5s cubic-bezier(0.075, 0.82, 0.165, 1);
}

.hotbar-icon-container.active {
    transform: scale(1.3);
    --hot-bar-color: var(--secondary-highlight-color);
    background-color: var(--primary-highlight-color);
    bottom: 10px;
}

.hotbar-icon {
    height: 25px;
}
.divide {
    background-color: var(--primary-highlight-color);
    width: 1px;
    height: 80%;
}

.no-info {
    display: flex;
    justify-content: center;
    align-items: center;
    flex-grow: 1;
    min-width: 0;
}

.options-selected {
    position: absolute;
    height: 2px;
    left: 0%;
    right: 0%;
    border-radius: 2px;
    opacity: 0;

    transition:
        opacity 0.2s ease,
        left 0.2s ease,
        right 0.2s ease;
}

.active>.options-selected {
    opacity: 1;
    left: 20%;
    right: 20%;
    background-color: var(--accent-bar-color);
}

:deep(.apply-btn) {
    width: 80%;
    height: 50px;
    margin-left: 5px;
    font-size: 1.2em;
    font-weight: bold;
    background-color: var(--secondary-highlight-color);
    color: white;
    border: none;
    cursor: pointer;
    transition: background-color 1.2s cubic-bezier(0.19, 1, 0.22, 1);
}

:deep(.apply-btn:hover) {
    background-color: var(--accent-bar-color);
}

.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
    opacity: 0;
}
</style>