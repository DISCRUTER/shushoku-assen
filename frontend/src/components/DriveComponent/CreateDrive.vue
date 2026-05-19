<script setup>
import { onMounted, ref } from 'vue';
import dayjs from 'dayjs';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../../stores/auth';
import apiClient from '../../axios';
import Button from '../Button.vue';
import Tooltip from '../Tooltip.vue';

const authStore = useAuthStore();
const userId = authStore.getUserId();

const router = useRouter();

const props = defineProps({
	show: Boolean
})

const openings = ref(1);
const title = ref('');
const jobType = ref('full-time');
const description = ref('');
const salary = ref(0);
const deadline = ref(dayjs().format('YYYY-MM-DD'));
const errorMessage = ref('');
const skillData = ref([]);
const skillsRequired = ref([]);

const salaryType = {
	"internship": "Monthly",
	"part-time": "Hourly",
	"full-time": "LPA"
}

function toggleSkill(skill) {
	if (skillsRequired.value.some(s => s.id === skill.id)) {
		skillsRequired.value = skillsRequired.value.filter(s => s.id !== skill.id);
	} else {
		skillsRequired.value.push({ id: skill.id, name: skill.name, description: skill.description });
	}
}

async function createDrive() {
	if (title.value.length < 5 || title.value.length > 100) {
		errorMessage.value = "Title must be between 5 and 100 characters";
		return;
	}

	if (openings.value < 1) {
		errorMessage.value = "Openings must be at least 1";
		return;
	}

	if (!jobType.value) {
		errorMessage.value = "Job Type is required";
		return;
	}

	if (dayjs(deadline.value).isBefore(dayjs(), 'day')) {
		errorMessage.value = "Deadline must be today or in the future";
		return;
	}

	const payload = {
		openings: openings.value,
		company_id: userId,
		title: title.value,
		job_type: jobType.value,
		description: description.value,
		salary: salary.value,
		deadline: deadline.value,
		skills_required: skillsRequired.value
	};

	try {
		const response = await apiClient.post('api/v1/drives/', payload);
		if (response.status === 201) {
			window.location.reload();
		} else {
			errorMessage.value = 'Something went wrong!!!';
		}
	} catch (error) {
		errorMessage.value = 'Something went wrong!!!';
		console.log("Axios: ", error);
	}
}

async function fetchSkills() {
	try {
		const response = await apiClient.get('/api/v1/utils/skills');
		skillData.value = response.data;
	} catch (error) {
		errorMessage.value = "couldn't fetch skill data.";
		console.error("Axios :", error);
	}
}

onMounted(fetchSkills);

</script>

<template>
	<Transition name="modal">
		<div v-if="show" class="modal-mask" @click="$emit('close')">
			<div class="modal-container" @click.stop>
				<div class="options-btn">
					<Button label="Close" @click="$emit('close')" />
				</div>
				<div class="content">
					<div class="error-message" v-if="errorMessage">
						<h3>{{ errorMessage }}</h3>
					</div>
					<h2>Create drive</h2>
					<form @submit.prevent="createDrive" class="form-content">
						<div class="right">
							<div class="input-container">
								<label for="title" class="label-text">Title</label>
								<input type="text" name="title" id="title" v-model="title"
									class="input-text input-field">
							</div>
							<div class="input-container">
								<label for="description" class="label-text">Description</label>
								<textarea name="description" id="description" v-model="description"
									class="input-textarea input-field"></textarea>
							</div>
						</div>
						<div class="left">
							<div class="input-container">
								<label class="label-text">Job Type</label>
								<div class="label-container">
									<span class="labels" :class="{ selected: jobType === 'internship' }"
										@click="jobType === 'internship' ? jobType = '' : jobType = 'internship'">Internship</span>
									<span class="labels" :class="{ selected: jobType === 'part-time' }"
										@click="jobType === 'part-time' ? jobType = '' : jobType = 'part-time'">Part
										Time</span>
									<span class="labels" :class="{ selected: jobType === 'full-time' }"
										@click="jobType === 'full-time' ? jobType = '' : jobType = 'full-time'">Full
										Time</span>
								</div>
							</div>
							<div class="input-container">
								<label for="openings" class="label-text">Openings</label>
								<input type="number" name="openings" id="openings" v-model="openings"
									class="input-text input-field">
							</div>
							<div class="input-container">
								<label for="salary" class="label-text">Salary - {{ salaryType[jobType] }}</label>
								<input type="number" name="salary" id="salary" v-model="salary"
									class="input-text input-field">
							</div>
							<div class="input-container">
								<label for="deadline" class="label-text">Deadline</label>
								<input type="date" name="deadline" id="deadline" v-model="deadline"
									class="input-text input-field">
							</div>
						</div>
						<div class="l-left">
							<div class="input-container">
								<label class="label-text">Skills Required</label>
								<div class="skills">
									<Tooltip v-for="skill in skillData" :key="skill.id" :text="skill.description">
										<span class="labels"
											:class="{ selected: skillsRequired.some(s => s.id === skill.id) }"
											@click="toggleSkill(skill)">
											{{ skill.name }}
										</span>
									</Tooltip>
								</div>
							</div>
						</div>
					</form>
				</div>
				<div class="options-btn">
					<Button label="Create" class="apply-btn" @click="createDrive" />
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

.content {
	flex-grow: 1;
	display: flex;
	flex-direction: column;
	overflow-y: auto;
	overflow-x: hidden;
	min-height: 0;
}

.form-content {
	margin-top: 10px;
	display: grid;
	grid-template-columns: 3fr 1fr 2fr;
	gap: 20px;
	flex-grow: 1;
}

.right {
	display: flex;
	flex-direction: column;
}

.skills {
	display: flex;
	flex-wrap: wrap;
}

.label-text {
	font-size: 1.2em;
}

.input-text {
	height: 50px;
	width: 100%;
	border-radius: 10px;
	background-color: var(--secondary-highlight-color);
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

.input-textarea {
	flex-grow: 1;
	height: 240px;
	width: 580px;
	font: Roboto;
	overflow-y: auto;
	border-radius: 10px;
	background-color: var(--secondary-highlight-color);
}

input[type="date"].input-field {
	color: #333;
	color-scheme: light;
}

.options-btn {
	display: flex;
	justify-content: flex-end;
	align-items: center;
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

.error-message {
	color: red;
	text-align: center;
}
</style>