<script setup>
import { ref } from 'vue';
import Button from '../Button.vue';
import StudentProfile from './StudentProfile.vue';
import ApplicationView from '../ApplicationComponent/ApplicationView.vue';
import PlacementView from '../ApplicationComponent/PlacementView.vue';

const props = defineProps({
	show: Boolean,
	studentData: Object
})

const currentTab = ref('StudentProfile')

const tabs = {
	StudentProfile,
	ApplicationView,
	PlacementView
}

const tabNames = {
	'StudentProfile': "About",
	'ApplicationView': "Applications",
	'PlacementView': "Placements",
}

</script>

<template>
	<Transition name="modal">
		<div v-if="show" class="modal-mask" @click="$emit('close')">
			<div class="modal-container" @click.stop>
				<div class="options-btn">
					<div class="options">
						<span v-for="(_, tab) in tabs" :key="tab" :class="['options-label', { active: currentTab === tab }]"
							@click="currentTab = tab">
							<h3>{{ tabNames[tab] }}</h3>
							<div class="options-selected"></div>
						</span>
					</div>
					<Button label=" Close" @click="$emit('close')" />
				</div>
				<div class="content">
					<Transition name="fade" mode="out-in">
						<component :is="tabs[currentTab]" class="tab" :student-data="studentData" :student-id="studentData?.id" :chart="true" v-if="studentData">
						</component>
					</Transition>
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


.options-btn {
	display: flex;
	justify-content: space-between;
	align-items: flex-end;
}

.options {
	display: flex;
	align-items: flex-end;
}

.options-label {
	position: relative;
	margin: 5px;
	padding: 2px 5px;
	cursor: pointer;
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