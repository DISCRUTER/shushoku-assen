<script setup>
import { ref, watch } from 'vue';
import dayjs from 'dayjs';
import { useAuthStore } from '../../stores/auth';
import apiClient from '../../axios';
import Button from '../Button.vue';

const authStore = useAuthStore();
const userRole = authStore.getUserRole();

const props = defineProps({
    show: Boolean,
    applicationData: Object
});

const emit = defineEmits(['close', 'statusUpdated']);

const currentStatus = ref(props.applicationData?.status);
const joiningDate = ref(dayjs().format('YYYY-MM-DD'));
const errorMessage = ref('');
const isLoading = ref(false);

const printStatus = {
    "applied": 'APPLIED',
    "shortlisted": 'SHORTLISTED',
    "selected": 'SELECTED',
    "rejected": 'REJECTED',
    "offered": 'OFFERED'
}

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

watch(() => props.applicationData, (newVal) => {
    currentStatus.value = newVal?.status;
    errorMessage.value = '';
});

async function updateStatus(newStatus) {
    isLoading.value = true;
    errorMessage.value = '';

    try {
        const response = await apiClient.patch(`/api/v1/applications/${props.applicationData?.id}`, {
            status: newStatus
        });
        if (response.status === 200) {
            currentStatus.value = printStatus[newStatus];
            emit('statusUpdated', { id: props.applicationData?.id, status: printStatus[newStatus] });
        }
    } catch (error) {
        errorMessage.value = 'Failed to update status. Please try again.';
        console.error('Axios: ', error);
    } finally {
        isLoading.value = false;
    }
}

async function offerPlacement() {
    if (!joiningDate.value) {
        errorMessage.value = 'Please select a joining date.';
        return;
    }

    isLoading.value = true;
    errorMessage.value = '';

    const payload = {
        student_id: props.applicationData?.student?.id,
        company_id: props.applicationData?.drive?.company_id,
        drive_id: props.applicationData?.drive?.id,
        joining_date: joiningDate.value
    };

    try {
        const response = await apiClient.post('/api/v1/placements/', payload);
        if (response.status === 201) {
            await updateStatus('offered');
        }
    } catch (error) {
        errorMessage.value = 'Failed to create placement. Please try again.';
        console.error('Axios: ', error);
    } finally {
        isLoading.value = false;
    }
}
</script>

<template>
    <Transition name="modal">
        <div v-if="show" class="modal-mask" @click="$emit('close')">
            <div class="modal-container" @click.stop>

                <div class="modal-header">
                    <div class="head">
                        <h2>{{ applicationData.drive?.title }}</h2>
                        <p>#ID: {{ applicationData?.id }}</p>
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
                                <h4>Company</h4>
                                <h3>{{ applicationData.drive?.company?.registered_name }}</h3>
                            </div>
                            <div class="info">
                                <div class="info-head">
                                    <h4>Job Type</h4>
                                    <h3>{{ jobTypes[applicationData.drive?.job_type] }}</h3>
                                </div>
                                <div class="info-head">
                                    <h4>Salary</h4>
                                    <h3>{{ applicationData.drive?.salary }}/{{ salaryType[applicationData.drive?.job_type] }}</h3>
                                </div>
                                <div class="info-head">
                                    <h4>Openings</h4>
                                    <h3>{{ applicationData.drive?.openings }}</h3>
                                </div>
                            </div>
                            <div class="info-head">
                                <h4>About</h4>
                                <p>{{ applicationData.drive?.description }}</p>
                            </div>
                        </div>

                        <div class="student" v-if="userRole !== 'Student'">
                            <div class="info-head">
                                <h4>Applicant</h4>
                                <h3>{{ applicationData.student?.first_name }} {{ applicationData.student?.last_name }}</h3>
                            </div>
                            <div class="info-head">
                                <h4>Academics Status</h4>
                                <h3>{{ applicationData.student?.academic_degree?.name }} in {{ applicationData.student?.branch?.name }}</h3>
                            </div>
                            <div class="info">
                                <div class="info-head">
                                    <h4>CGPA</h4>
                                    <h3>{{ applicationData.student?.cgpa }}</h3>
                                </div>
                                <div class="info-head">
                                    <h4>Year</h4>
                                    <h3>{{ applicationData.student?.year }}</h3>
                                </div>
                            </div>
                            <div class="info-head">
                                <h4>Applied on</h4>
                                <h3>{{ applicationData.created_at ? dayjs(applicationData.created_at).format('DD-MM-YYYY') : '' }}</h3>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="options-btn" v-if="userRole === 'Company'">
                    <span class="status-badge">{{ currentStatus }}</span>

                    <template v-if="!isLoading">
                        <template v-if="currentStatus === 'APPLIED'">
                            <Button label="Shortlist" @click="updateStatus('shortlisted')" />
                            <Button label="Reject" @click="updateStatus('rejected')" />
                        </template>

                        <template v-else-if="currentStatus === 'SHORTLISTED'">
                            <Button label="Select" @click="updateStatus('selected')" />
                            <Button label="Reject" @click="updateStatus('rejected')" />
                        </template>

                        <template v-else-if="currentStatus === 'SELECTED'">
                            <input
                                type="date"
                                v-model="joiningDate"
                                class="input-field"
                                style="width: auto; margin-right: 10px;"
                                :min="dayjs().format('YYYY-MM-DD')"
                            />
                            <Button label="Offer Placement" @click="offerPlacement" />
                        </template>

                        <template v-else-if="currentStatus === 'OFFERED'">
                            <span class="status-final placed">Placement Offered</span>
                        </template>
                        <template v-else-if="currentStatus === 'REJECTED'">
                            <span class="status-final rejected">Rejected</span>
                        </template>
                    </template>

                    <span v-else class="loading-text">Updating…</span>
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
}

.drive, .student {
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

.status-badge {
    margin-right: auto;
    font-size: 0.85em;
    font-weight: 600;
    color: #666;
    text-transform: capitalize;
    letter-spacing: 0.03em;
}

.status-final {
    font-size: 0.9em;
    font-weight: 600;
    padding: 6px 12px;
    border-radius: 6px;
}

.status-final.placed {
    background-color: #e6f9f0;
    color: #1a7f4e;
}

.status-final.rejected {
    background-color: #fdecea;
    color: #b91c1c;
}

.loading-text {
    font-size: 0.9em;
    color: #888;
}

.input-field {
    color: var(--primary-highlight-color);
    font-size: 1em;
    padding: 10px 20px;
    box-sizing: border-box;
    border: 2px solid #ffffff;
    width: 100%;
}

.input-field:hover {
    border-color: #e0e0e0;
}

.input-field:focus {
    outline: none;
    border-color: var(--primary-highlight-color);
}

input[type="date"].input-field {
    color: #333;
    color-scheme: light;
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
