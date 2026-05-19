<script setup>
import { onMounted, ref } from 'vue';
import Button from '../Button.vue';
import apiClient from '../../axios';

const props = defineProps({
    show: Boolean,
    userId: String,
    userRole: String
});

// Student Fields
const cgpa = ref('');
const about = ref('');
const github = ref('');
const linkedin = ref('');

// Company Fields
const description = ref('');
const location = ref('');
const contactEmail = ref('');
const contactPhone = ref('');
const website = ref('');

async function fetchData() {
    let url ='';
    if (props.userRole === 'Student') {
        url = `/api/v1/students/${props.userId}`;
    } else if (props.userRole === 'Company') {
        url = `/api/v1/company/${props.userId}`;
    }

    try {
        const response = await apiClient.get(url);
        const data = response.data;
        if (props.userRole === 'Student') {
            cgpa.value = data.cgpa;
            about.value = data.about;
            github.value = data.github;
            linkedin.value = data.linkedin;
        } else if (props.userRole === 'Company') {
            description.value = data.description;
            location.value = data.location;
            website.value = data.website;
            contactEmail.value = data.contact_email;
            contactPhone.value = data.contact_phone;
        }
    } catch (error) {
        console.error("Axios: ", error);
    }
}

async function UpdateProfile() {
    let url ='';
    let payload = {}
    if (props.userRole === 'Student') {
        url = `/api/v1/students/${props.userId}`;
        Object.assign(payload, {
            cgpa: parseFloat(cgpa.value),
            about: about.value,
            github: github.value,
            linkedin: linkedin.value
        });
        if (cgpa.value !== '' && !isNaN(parseFloat(cgpa.value))) {
            payload.cgpa = parseFloat(cgpa.value);
        }
        payload.about = about.value;
        payload.github = github.value || null;
        payload.linkedin = linkedin.value || null;
    } else if (props.userRole === 'Company') {
        url = `/api/v1/company/${props.userId}`;
        Object.assign(payload, {
            description: description.value,
            location: location.value,
            contact_email: contactEmail.value,
            contact_phone: contactPhone.value,
            website: website.value
        });
    } 

    try {
        const response = await apiClient.patch(url, payload);
        if (response.status === 202) {
            window.location.reload();
        }
    } catch (error) {
        console.error("Axios: ", error);
    }
}
onMounted(fetchData);
</script>

<template>
    <Transition name="modal">
        <div v-if="show" class="modal-mask" @click="$emit('close')">
            <div class="modal-container" @click.stop>

                <div class="modal-header">
                    <div class="head">
                        <h2>Update Profile</h2>
                    </div>
                    <Button label="Close" @click="$emit('close')" />
                </div>

                <div class="fields-group">
                    <template v-if="userRole==='Student'">
                        <div class="l-half">
                            <div class="input-container">
                                <div class="input-container">
                                    <label class="input-label">
                                        <h3>CGPA</h3>
                                    </label>
                                    <input type="number" step="0.01" v-model="cgpa" class="input-field" required>
                                </div>
                                <div class="input-container">
                                    <label class="input-label">
                                        <h3>About</h3>
                                    </label>
                                    <textarea v-model="about" class="input-field textarea-field"></textarea>
                                </div>
                            </div>
                            <div class="together">
                                <div class="input-container">
                                    <label class="input-label">
                                        <h3>Github</h3>
                                    </label>
                                    <input type="url" v-model="github" class="input-field">
                                </div>
                                <div class="input-container">
                                    <label class="input-label">
                                        <h3>LinkedIn</h3>
                                    </label>
                                    <input type="url" v-model="linkedin" class="input-field">
                                </div>
                            </div>
                        </div>
                    </template>
                    <template v-if="userRole==='Company'">
                        <div class="l-half">
                            <div class="input-container">
                                <div class="input-container">
                                    <label class="input-label">
                                        <h3>Location</h3>
                                    </label>
                                    <input type="text" v-model="location" class="input-field" required>
                                </div>
                                <div class="input-container">
                                    <label class="input-label">
                                        <h3>Description</h3>
                                    </label>
                                    <textarea v-model="description" class="input-field textarea-field"></textarea>
                                </div>
                            </div>
                            <div class="together">
                                <div class="input-container">
                                    <label class="input-label">
                                        <h3>Contact Email</h3>
                                    </label>
                                    <input type="email" v-model="contactEmail" class="input-field">
                                </div>
                                <div class="input-container">
                                    <label class="input-label">
                                        <h3>Contact Phone</h3>
                                    </label>
                                    <input type="tel" v-model="contactPhone" class="input-field">
                                </div>
                                <div class="input-container">
                                    <label class="input-label">
                                        <h3>Website</h3>
                                    </label>
                                    <input type="url" v-model="website" class="input-field">
                                </div>
                            </div>
                        </div>
                    </template>
                    <div class="options-btn" v-if="userRole !== 'Admin'">
                        <Button label="Update" class="apply-btn" @click="UpdateProfile" />
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

.fields-group {
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 40px;
}

.l-half {
    height: 100%;
}

.together {
    display: flex;
    gap: 10px;
}

.input-container {
    display: flex;
    flex-direction: column;
    width: 100%;
    min-width: 300px;
    max-width: 450px;
    margin-bottom: 10px;
    position: relative;
}

.input-label {
    font-size: 1.2em;
    margin-bottom: 8px;
    font-weight: 600;
    color: #333;
    align-self: flex-start;
}

.input-field {
    height: 50px;
    width: 100%;
    box-sizing: border-box;
    border: 2px solid #e0e0e0;
    border-radius: 8px;
    color: #333;
    background-color: #f8f9fa;
    padding-left: 15px;
    font-size: 1em;
    transition: all 0.3s ease;
}

.textarea-field {
    height: 130px;
    width: 600px;
    padding-top: 10px;
    resize: vertical;
}

.input-field:hover {
    border-color: var(--accent-bar-color);
    background-color: #fff;
}

.input-field:focus {
    outline: none;
    border-color: var(--accent-bar-color);
    background-color: #fff;
    box-shadow: 0 0 0 4px rgba(0, 0, 0, 0.1);
}

:deep(.apply-btn) {
	width: 250px;
	height: 50px;
	font-size: 1.2em;
	font-weight: bold;
	background-color: var(--secondary-highlight-color);
	color: white;
	border: none;
	cursor: pointer;
	transition: background-color 1.2s cubic-bezier(0.19, 1, 0.22, 1);
	margin-bottom: 5px;
}

:deep(.apply-btn:hover) {
	background-color: var(--accent-bar-color);
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
