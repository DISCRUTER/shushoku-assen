<script setup>
import { ref } from 'vue';
import axios from 'axios';
import apiClient from '../../axios';
import Button from '../Button.vue';

const success = ref(false);

const step = ref(1);
const role = ref('Student');
const email = ref('');
const password = ref('');
const showPassword = ref(false);
const confirmPassword = ref('');
const showConfirmPassword = ref(false);
const branchData = ref(null);
const academicDegreeData = ref(null);
const industryData = ref(null);

// Student Fields
const firstName = ref('');
const lastName = ref('');
const year = ref('');
const cgpa = ref('');
const branchId = ref('');
const degreeId = ref('');
const about = ref('');
const github = ref('');
const linkedin = ref('');

// Company Fields
const registeredName = ref('');
const description = ref('');
const industryId = ref('');
const location = ref('');
const contactEmail = ref('');
const contactPhone = ref('');
const website = ref('');

async function nextStep() {
    if (email.value && password.value && confirmPassword.value) {
        if (password.value === confirmPassword.value) {
            step.value = 2;
        } else {
            alert("Password and confirm password do not match.");
            return;
        }
    } else {
        alert("Please enter email and password.");
        return;
    }

    if (role.value === 'Student') {
        try {
            let response = await apiClient('api/v1/utils/branch');
            if (response.status === 200) {
                branchData.value = response.data;
            } else {
                console.log("Couldn't load branch data.");
            }
            response = await apiClient('api/v1/utils/academic-degree');
            if (response.status === 200) {
                academicDegreeData.value = response.data;
            }
        } catch (error) {
            console.error("Axios: ", error);
        }
    } else if (role.value === 'Company') {
        try {
            const response = await apiClient('api/v1/utils/industry');
            if (response.status === 200) {
                industryData.value = response.data;
            } else {
                console.log("Couldn't load industry data.");
            }
        } catch (error) {
            console.error("Axios: ", error);
        }
    }
}

async function registerUser() {
    let url = '';
    let payload = {
        email: email.value,
        password: password.value
    };

    if (role.value === 'Student') {
        if (degreeId.value === '' || branchId.value === '') {
            alert("Select a branch and academic degree.");
            return;
        }
        url = 'http://127.0.0.1:3000/api/v1/students/';
        Object.assign(payload, {
            first_name: firstName.value,
            last_name: lastName.value,
            year: parseInt(year.value),
            cgpa: parseFloat(cgpa.value),
            branch_id: branchId.value,
            academic_degree_id: degreeId.value,
            about: about.value,
            github: github.value,
            linkedin: linkedin.value
        });
    } else {
        if (industryId.value === '') {
            alert("Select an industry.");
            return;
        }
        url = 'http://127.0.0.1:3000/api/v1/company/';
        Object.assign(payload, {
            registered_name: registeredName.value,
            description: description.value,
            industry_id: industryId.value,
            location: location.value,
            contact_email: contactEmail.value,
            contact_phone: contactPhone.value,
            website: website.value
        });
    }

    try {
        const response = await axios.post(url, payload);
        if (response.status === 201) {
            success.value = true;
        }
    } catch (error) {
        console.error('Registration Error:', error);
        alert('Registration Failed: ' + (error.response?.data?.message || error.message));
    }
}
</script>

<template>
    <form @submit.prevent class="register-form" v-if="!success">
        <div v-if="step === 1" class="step-container">
            <div class="input-container">
                <label for="reg-email" class="input-label">
                    <h3>Email</h3>
                </label>
                <input type="email" id="reg-email" v-model="email" class="input-field" placeholder="Enter your email"
                    required>
            </div>
            <div class="input-container">
                <label for="reg-password" class="input-label">
                    <h3>Password</h3>
                </label>
                <input :type="showPassword ? 'text' : 'password'" id="reg-password" v-model="password"
                    class="input-field" placeholder="Enter your password" required>
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" v-if="showPassword"
                    class="show-icon" @click="showPassword = !showPassword">
                    <path d="M10 12.5a2.5 2.5 0 1 0 0-5 2.5 2.5 0 0 0 0 5Z" />
                    <path fill-rule="evenodd"
                        d="M.664 10.59a1.651 1.651 0 0 1 0-1.186A10.004 10.004 0 0 1 10 3c4.257 0 7.893 2.66 9.336 6.41.147.381.146.804 0 1.186A10.004 10.004 0 0 1 10 17c-4.257 0-7.893-2.66-9.336-6.41ZM14 10a4 4 0 1 1-8 0 4 4 0 0 1 8 0Z"
                        clip-rule="evenodd" />
                </svg>
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="show-icon" v-else
                    @click="showPassword = !showPassword">
                    <path fill-rule="evenodd"
                        d="M3.28 2.22a.75.75 0 0 0-1.06 1.06l14.5 14.5a.75.75 0 1 0 1.06-1.06l-1.745-1.745a10.029 10.029 0 0 0 3.3-4.38 1.651 1.651 0 0 0 0-1.185A10.004 10.004 0 0 0 9.999 3a9.956 9.956 0 0 0-4.744 1.194L3.28 2.22ZM7.752 6.69l1.092 1.092a2.5 2.5 0 0 1 3.374 3.373l1.091 1.092a4 4 0 0 0-5.557-5.557Z"
                        clip-rule="evenodd" />
                    <path
                        d="m10.748 13.93 2.523 2.523a9.987 9.987 0 0 1-3.27.547c-4.258 0-7.894-2.66-9.337-6.41a1.651 1.651 0 0 1 0-1.186A10.007 10.007 0 0 1 2.839 6.02L6.07 9.252a4 4 0 0 0 4.678 4.678Z" />
                </svg>
            </div>
            <div class="input-container">
                <label for="reg-c-password" class="input-label">
                    <h3>Confirm Password</h3>
                </label>
                <input :type="showConfirmPassword ? 'text' : 'password'" id="reg-c-password" v-model="confirmPassword"
                    class="input-field" placeholder="Confirm password" required>
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor"
                    v-if="showConfirmPassword" class="show-icon" @click="showConfirmPassword = !showConfirmPassword">
                    <path d="M10 12.5a2.5 2.5 0 1 0 0-5 2.5 2.5 0 0 0 0 5Z" />
                    <path fill-rule="evenodd"
                        d="M.664 10.59a1.651 1.651 0 0 1 0-1.186A10.004 10.004 0 0 1 10 3c4.257 0 7.893 2.66 9.336 6.41.147.381.146.804 0 1.186A10.004 10.004 0 0 1 10 17c-4.257 0-7.893-2.66-9.336-6.41ZM14 10a4 4 0 1 1-8 0 4 4 0 0 1 8 0Z"
                        clip-rule="evenodd" />
                </svg>
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="show-icon" v-else
                    @click="showConfirmPassword = !showConfirmPassword">
                    <path fill-rule="evenodd"
                        d="M3.28 2.22a.75.75 0 0 0-1.06 1.06l14.5 14.5a.75.75 0 1 0 1.06-1.06l-1.745-1.745a10.029 10.029 0 0 0 3.3-4.38 1.651 1.651 0 0 0 0-1.185A10.004 10.004 0 0 0 9.999 3a9.956 9.956 0 0 0-4.744 1.194L3.28 2.22ZM7.752 6.69l1.092 1.092a2.5 2.5 0 0 1 3.374 3.373l1.091 1.092a4 4 0 0 0-5.557-5.557Z"
                        clip-rule="evenodd" />
                    <path
                        d="m10.748 13.93 2.523 2.523a9.987 9.987 0 0 1-3.27.547c-4.258 0-7.894-2.66-9.337-6.41a1.651 1.651 0 0 1 0-1.186A10.007 10.007 0 0 1 2.839 6.02L6.07 9.252a4 4 0 0 0 4.678 4.678Z" />
                </svg>
            </div>
            <div class="input-container">
                <label for="filter-labels" class="input-label">
                    <h3>Role</h3>
                </label>
                <div class="filter-role-labels">
                    <div class="role-labels" :class="{ 'selected': role === 'Student' }" @click="role = 'Student'">
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 23 29">
                            <path fill="var(--role-icon)"
                                d="M0.253,28.756 L0.253,18.400 C0.253,15.269 2.716,12.730 5.755,12.730 L17.498,12.730 C20.537,12.730 23.000,15.269 23.000,18.400 L23.000,28.756 L0.253,28.756 ZM11.626,10.982 C8.825,10.982 6.554,8.642 6.554,5.754 C6.554,2.867 8.825,0.527 11.626,0.527 C14.428,0.527 16.699,2.867 16.699,5.754 C16.699,8.642 14.428,10.982 11.626,10.982 Z">
                            </path>
                        </svg>
                        <h4>Student</h4>
                    </div>
                    <div class="role-labels" :class="{ 'selected': role === 'Company' }" @click="role = 'Company'">
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 42 42">
                            <path fill="var(--role-icon)"
                                d="M36.038,32.520 L36.038,5.876 L15.483,5.876 L15.483,0.188 L41.891,0.188 L41.891,32.520 L36.038,32.520 ZM15.614,9.516 L15.483,9.643 L15.483,9.787 L11.414,13.741 L6.027,8.506 L1.825,4.423 L1.861,4.388 L1.787,4.316 L6.060,0.164 L11.829,5.769 L15.445,9.283 L15.649,9.482 L15.614,9.516 ZM6.027,35.043 L22.791,35.043 L22.791,40.731 L0.173,40.731 L0.173,13.742 L6.027,13.742 L6.027,35.043 ZM15.652,24.914 L15.652,31.990 L8.255,31.990 L8.255,24.800 L15.535,24.800 L15.652,24.800 L15.652,9.476 L31.421,9.476 L31.421,24.800 L23.479,24.800 L23.479,32.518 L23.479,32.520 L15.652,24.914 ZM31.513,32.808 L34.107,35.331 L36.934,38.078 L33.068,41.835 L32.228,41.019 L26.374,35.331 L23.778,32.808 L23.479,32.518 L27.347,28.759 L31.513,32.808 Z">
                            </path>
                        </svg>
                        <h4>Company</h4>
                    </div>
                </div>
            </div>

            <div class="auth-btn">
                <Button label="Next" @click="nextStep" class="action-btn" />
            </div>
        </div>

        <div v-else class="step-container scrollable-step">
            <div v-if="role === 'Student'" class="fields-group">
                <div class="l-half">
                    <div class="together">
                        <div class="input-container">
                            <label class="input-label">
                                <h3>First Name</h3>
                            </label>
                            <input type="text" v-model="firstName" class="input-field" required>
                        </div>
                        <div class="input-container">
                            <label class="input-label">
                                <h3>Last Name</h3>
                            </label>
                            <input type="text" v-model="lastName" class="input-field">
                        </div>
                    </div>
                    <div class="input-container">
                        <label class="input-label">
                            <h3>About</h3>
                        </label>
                        <textarea v-model="about" class="input-field textarea-field"></textarea>
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
                <div class="r-half">
                    <div class="input-container">
                        <label class="input-label">
                            <h3>Branch</h3>
                        </label>
                        <div class="label-container">
                            <span class="labels" v-for="branch in branchData" :key="branch.id"
                                :class="{ selected: branchId === branch.id }" @click="branchId === branch.id? branchId='' : branchId=branch.id">
                                {{ branch.name }}
                            </span>
                        </div>
                    </div>
                    <div class="input-container">
                        <label class="input-label">
                            <h3>Degree</h3>
                        </label>
                        <div class="label-container">
                            <span class="labels" v-for="degree in academicDegreeData" :key="degree.id"
                                :class="{ selected: degreeId === degree.id }" @click="degreeId === degree.id ? degreeId = '' : degreeId = degree.id">
                                {{ degree.name }}</span>
                        </div>
                    </div>
                    <div class="together">
                        <div class="input-container">
                            <label class="input-label">
                                <h3>Year</h3>
                            </label>
                            <input type="number" v-model="year" class="input-field" required>
                        </div>
                        <div class="input-container">
                            <label class="input-label">
                                <h3>CGPA</h3>
                            </label>
                            <input type="number" step="0.01" v-model="cgpa" class="input-field" required>
                        </div>
                    </div>
                </div>
            </div>

            <div v-if="role === 'Company'" class="fields-group">
                <div class="l-half">
                    <div class="input-container">
                        <label class="input-label"><h3>Registered Name</h3></label>
                        <input type="text" v-model="registeredName" class="input-field" required>
                    </div>
                    <div class="input-container">
                        <label class="input-label"><h3>Description</h3></label>
                        <textarea v-model="description" class="input-field textarea-field" required></textarea>
                    </div>
                    <div class="together">
                        <div class="input-container">
                            <label class="input-label"><h3>Contact Email</h3></label>
                            <input type="email" v-model="contactEmail" class="input-field" required>
                        </div>
                        <div class="input-container">
                            <label class="input-label"><h3>Contact Phone</h3></label>
                            <input type="tel" v-model="contactPhone" class="input-field" required>
                        </div>
                    </div>
                </div>
                <div class="r-half">
                    <div class="together">
                        <div class="input-container">
                            <label class="input-label"><h3>Location</h3></label>
                            <input type="text" v-model="location" class="input-field" required>
                        </div>
                        <div class="input-container">
                            <label class="input-label"><h3>Website</h3></label>
                            <input type="url" v-model="website" class="input-field" required>
                        </div>
                    </div>
                    <div class="input-container">
                        <label class="input-label"><h3>Industry</h3></label>
                        <div class="label-container">
                            <span class="labels" v-for="industry in industryData" :key="industry.id"
                                :class="{ selected: industryId === industry.id }" @click="industryId === industry.id ? industryId = '' : industryId = industry.id">
                                {{ industry.name }}
                            </span>
                        </div>
                    </div>
                </div>
            </div>

            <div class="auth-btn">
                <Button label="Back" @click="step = 1" class="action-btn secondary" />
                <Button label="Register" @click="registerUser" class="action-btn" />
            </div>
        </div>
    </form>
    <div v-else-if="success" class="register-form">
        <h2>You have successful registered!</h2>
        <h2 v-if="role==='Student'">Login to start.</h2>
        <h2 v-else-if="role==='Company'">Waiting for Admin approval.</h2>
    </div>
</template>

<style lang="css" scoped>
.register-form {
    flex-grow: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 100%;
    height: 100%;
}

.step-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 100%;
    max-height: 100%;
}

.scrollable-step {
    overflow-y: auto;
    padding: 20px 0;
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    scrollbar-width: none;
}

.scrollable-step::-webkit-scrollbar {
    display: none;
}

.fields-group {
    width: 100%;
    display: flex;
    justify-content: center;
    align-items: flex-start;
    gap: 40px;
}

.l-half {
    height: 100%;
}

.together {
    display: flex;
    gap: 20px;
}

.input-container {
    display: flex;
    flex-direction: column;
    width: 100%;
    min-width: 300px;
    max-width: 450px;
    margin-bottom: 20px;
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

.auth-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    max-width: 450px;
    margin-top: 10px;
    gap: 20px;
}

.filter-role-labels {
    margin-top: 20px;
    margin-bottom: 20px;
    --role-icon: var(--primary-highlight-color);
    display: flex;
    gap: 20px;
    width: 100%;
    justify-content: center;
}

.role-labels {
    display: inline-block;
    background-color: var(--secondary-highlight-color);
    border: var(--primary-highlight-color) 1px solid;
    margin: 2px 4px;
    padding: 5px 10px;
    border-radius: 8px;
    height: 60px;
    width: 160px;
    font-size: 1.3em;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 20px;
    transition: all 0.1s ease;
}

.role-labels:hover {
    background-color: var(--primary-highlight-color);
    color: white;
    --role-icon: var(--secondary-highlight-color);
}

.label-container {
    padding-bottom: 10px;
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

.selected,
.selected:hover {
    background-image: var(--topo-pattern);
    background-color: var(--primary-highlight-color);
    color: white;
    --role-icon: var(--accent-bar-color);
}

:deep(.action-btn) {
    width: 80%;
    height: 50px;
    font-size: 1.2em;
    font-weight: bold;
    border-radius: 8px;
    background-color: var(--accent-bar-color);
    color: white;
    border: none;
    cursor: pointer;
    transition: transform 0.1s ease, opacity 0.2s ease;
}

:deep(.action-btn.secondary) {
    background-color: #6c757d;
}

:deep(.action-btn:hover) {
    opacity: 0.9;
    transform: translateY(-1px);
}

:deep(.action-btn:active) {
    transform: translateY(1px);
}

.show-icon {
    position: absolute;
    right: 15px;
    bottom: 13px;
    width: 24px;
    height: 24px;
    cursor: pointer;
    color: #6c757d;
}

#reg-password,
#reg-c-password {
    padding-right: 45px;
}
</style>