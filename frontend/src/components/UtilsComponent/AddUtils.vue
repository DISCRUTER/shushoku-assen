<script setup>
import { ref } from 'vue';
import apiClient from '../../axios';
import Button from '../Button.vue';

const props = defineProps({
	addUtilData: Object,
	show: Boolean
});

const emit = defineEmits(['close']);

const name = ref('');
const description = ref('');

async function addUtil() {
	const payload = {
		'name': name.value,
		'description': description.value
	}

	try {
		const response = await apiClient.post(props.addUtilData.url, payload);
		if (response.status === 201) {
			console.log("created");
			name.value = '';
			description.value = '';
			emit('close');
		} else {
			console.log("failed");
		}
	} catch (error) {
		console.log("Axios: ", error);
	}
}

</script>

<template>
	<Transition name="modal">
		<div v-if="show" class="modal-mask" @click="$emit('close')">
			<div class="modal-container" @click.stop>
				<div class="options-btn">
					<Button label="Close" @click="$emit('close')" />
				</div>
				<div class="content">
					<h2>Add a {{ addUtilData['name'] }}</h2>
					<form @submit.prevent="addUtil" class="form-content">
						<label for="name" class="label-text">Name</label>
						<input type="text" name="name" id="name" v-model="name" class="input-text input-field">
						<label for="description" class="label-text">Description</label>
						<textarea name="description" id="description" v-model="description"
							class="input-textarea input-field"></textarea>
					</form>
				</div>
				<div class="options-btn">
					<Button label="Add" class="apply-btn" @click="addUtil" />
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

.form-content {
	margin-top: 10px;
	display: flex;
	flex-direction: column;
	gap: 10px;
}

.label-text {
	font-size: 1.2em;
}

.input-text {
	height: 50px;
	width: 50%;
	border-radius: 10px;
	background-color: var(--secondary-highlight-color);
}

.input-field {
	color: var(--primary-highlight-color);
	font-size: 1em;
	padding: 10px 20px;
	box-sizing: border-box;
	border: 2px solid #ffffff;
}

.input-field:hover {
	border-color: #e0e0e0;
}

.input-field:focus {
	outline: none;
	border-color: var(--primary-highlight-color);
}

.input-textarea {
	height: 250px;
	font: Roboto;
	border-radius: 10px;
	background-color: var(--secondary-highlight-color);
}


.options-btn {
	display: flex;
	justify-content: flex-end;
	align-items: center;
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

.fade-enter-active,
.fade-leave-active {
	transition: opacity 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
	opacity: 0;
}
</style>