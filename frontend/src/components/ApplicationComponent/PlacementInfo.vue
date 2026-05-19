<script setup>
import { ref } from 'vue';
import dayjs from 'dayjs';
import { useAuthStore } from '../../stores/auth';
import Button from '../Button.vue';
import { download } from '../../download';

const authStore = useAuthStore();
const userRole = authStore.getUserRole();

const props = defineProps({
    show: Boolean,
    placementData: Object
});

const errorMessage = ref('');
const isLoading = ref(false);

const jobTypes = {
    "internship": "Internship",
    "part-time": "Part Time",
    "full-time": "Full Time"
}

const salaryType = {
    "internship": "Monthly",
    "part-time": "Hourly",
    "full-time": "LPA"
}
</script>

<template>
    <Transition name="modal">
        <div v-if="show" class="modal-mask" @click="$emit('close')">
            <div class="modal-container" @click.stop>

                <div class="modal-header">
                    <div class="head">
                        <h2>{{ placementData.drive?.title }}</h2>
                        <p>#OFFER ID: {{ placementData?.id }}</p>
                    </div>
                    <Button label="Close" @click="$emit('close')" />
                </div>

                <div class="content">
                    <div class="error-message" v-if="errorMessage">
                        <h3>{{ errorMessage }}</h3>
                    </div>

                    <div class="body">
                        <div class="drive">
                            <div class="info-head">
                                <h4>Applicant</h4>
                                <h3>{{ placementData.student?.first_name }} {{ placementData.student?.last_name }}</h3>
                            </div>
                            <div class="info-head">
                                <h4>Company</h4>
                                <h3>{{ placementData.company?.registered_name }}</h3>
                            </div>
                            <div class="info">
                                <div class="info-head">
                                    <h4>Job Type</h4>
                                    <h3>{{ jobTypes[placementData.drive?.job_type] }}</h3>
                                </div>
                                <div class="info-head">
                                    <h4>Salary</h4>
                                    <h3>{{ placementData.drive?.salary }}/{{ salaryType[placementData.drive?.job_type]
                                    }}</h3>
                                </div>
                            </div>
                            <div class="info-head">
                                <h4>Joining Date</h4>
                                <h3>{{ placementData.joining_date ?
                                    dayjs(placementData.joining_date).format('DD-MM-YYYY') : '' }}</h3>
                            </div>
                        </div>
                    </div>
                    <div class="options-btn">
                        <div class="download" @click="download('Placement', placementData.id)">
                            <div class="bar"></div>
                            <svg xmlns="http://www.w3.org/2000/svg" class="download-logo" viewBox="0 0 28 29">
                                <path fill-rule="evenodd" fill="currentColor"
                                    d="M20.836,14.872 L20.836,0.013 L7.162,0.013 L7.162,7.976 L13.999,14.872 L-0.006,14.872 L13.999,28.999 L28.004,14.872 L20.836,14.872 Z">
                                </path>
                            </svg>
                            Plcement Offer
                        </div>
                    </div>
                </div>
            </div>

        </div>
    </Transition>
</template>

<style lang="css" scoped>
.modal-mask {
    position: fixed;
    z-index: 9998;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    transition: opacity 0.3s ease;
}

.modal-container {
    width: 80%;
    height: 80%;
    margin: auto;
    padding: 20px 30px;
    background-color: #fff;
    border-radius: 10px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.33);
    transition: all 0.3s ease;
    display: flex;
    flex-direction: column;
}

.modal-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 12px;
    flex-shrink: 0;
}

.head {
    display: flex;
    flex-direction: column;
    gap: 2px;
}

.head h2 {
    margin: 0;
}

.head p {
    margin: 0;
    color: #888;
    font-size: 0.85em;
}

.content {
    flex-grow: 1;
    display: flex;
    flex-direction: column;
    overflow-y: auto;
    overflow-x: hidden;
    min-height: 0;
}

.body {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
    padding-top: 8px;
    height: 85%;
}

.drive,
.student {
    display: flex;
    flex-direction: column;
    gap: 6px;
}

.info {
    display: flex;
    gap: 16px;
    flex-wrap: wrap;
}

.info-head {
    margin: 5px;
}

.options-btn {
    display: flex;
    justify-content: flex-end;
    align-items: center;
    gap: 10px;
    padding-top: 14px;
    border-top: 1px solid #f0f0f0;
    flex-shrink: 0;
}

.download {
    display: flex;
    gap: 10px;
    background-color: var(--accent-bar-color);
    padding: 10px;
    padding-right: 20px;
    align-items: center;
    cursor: pointer;
    box-shadow: 1px 2px 5px var(--secondary-highlight-color);
    transition: all 0.2s ease;
}

.download:hover {
    border-radius: 10px;
    background-image: var(--topo-pattern);
}

.bar {
    background-color: var(--primary-highlight-color);
    width: 3px;
    height: 30px;
}

.download-logo {
    height: 30px;
    width: 30px;
}

.error-message {
    color: red;
    text-align: center;
}

.modal-enter-from {
    opacity: 0;
}

.modal-leave-to {
    opacity: 0;
}

.modal-enter-from .modal-container,
.modal-leave-to .modal-container {
    -webkit-transform: scale(1.1);
    transform: scale(1.1);
}
</style>
