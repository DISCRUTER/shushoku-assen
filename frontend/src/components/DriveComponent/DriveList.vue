<script setup>
import { ref, computed } from 'vue';
import { useAuthStore } from '../../stores/auth';
import DriveCard from './DriveCard.vue';

const authStore = useAuthStore();
const userRole = authStore.getUserRole();

const activeDriveId = ref(null);
const activeFilter = ref(null);

const props = defineProps({
	pendingDrive: Array,
	openDrive: Array,
	closedDrive: Array
});

const emit = defineEmits(['drive-selected']);

function driveSelected(driveId) {
	activeDriveId.value = driveId;
	emit('drive-selected', driveId);
}

const filters = [
	{ label: 'Internship', value: 'internship' },
	{ label: 'Part Time', value: 'part-time' },
	{ label: 'Full Time', value: 'full-time' }
];

function filterDrive(filterType) {
	if (activeFilter.value === filterType) {
		activeFilter.value = null;
	} else {
		activeFilter.value = filterType;
	}
}

const filteredPendingDrives = computed(() => {
	if (!activeFilter.value) return props.pendingDrive;
	return props.pendingDrive.filter(drive => drive.job_type === activeFilter.value);
});

const filteredOpenDrives = computed(() => {
	if (!activeFilter.value) return props.openDrive;
	return props.openDrive.filter(drive => drive.job_type === activeFilter.value);
});

const filteredClosedDrives = computed(() => {
	if (!activeFilter.value) return props.closedDrive;
	return props.closedDrive.filter(drive => drive.job_type === activeFilter.value);
});
</script>

<template>
	<div class="drive-list">
		<div class="filter-labels">
			<span class="labels" :class="{ active: activeFilter === null }" @click="filterDrive(null)">All</span>
			<span class="labels" v-for="filter in filters" :key="filter.value"
				:class="{ active: activeFilter === filter.value }" @click="filterDrive(filter.value)">
				{{ filter.label }}
			</span>
		</div>
		<template v-if="(userRole !== 'Student') && (filteredPendingDrives.length > 0)">
			<h3 class="section-title">Approval Required</h3>
			<div class="drive-card" :class="{ isActive: activeDriveId === drive.id }" v-for="drive in filteredPendingDrives"
				:key="drive.id" @click="driveSelected(drive.id)">
				<DriveCard :drive="drive" :active="activeDriveId === drive.id" />
			</div>
		</template>
		<template v-if="filteredOpenDrives.length > 0">
			<h3 class="section-title" v-if="userRole !== 'Student'">Ongoing</h3>
			<div class="drive-card" :class="{ isActive: activeDriveId === drive.id }" v-for="drive in filteredOpenDrives"
				:key="drive.id" @click="driveSelected(drive.id)">
				<DriveCard :drive="drive" :active="activeDriveId === drive.id" />
			</div>
		</template>
		<template v-if="!(userRole === 'Student') && (filteredClosedDrives.length > 0)">
			<h3 class="section-title" v-if="userRole !== 'Student'">Closed</h3>
			<div class="drive-card" :class="{ isActive: activeDriveId === drive.id }" v-for="drive in filteredClosedDrives"
				:key="drive.id" @click="driveSelected(drive.id)">
				<DriveCard :drive="drive" :active="activeDriveId === drive.id" />
			</div>
		</template>
	</div>
</template>

<style lang="css" scoped>

.drive-list {
    width: 450px;
    padding-right: 5px;
    flex-shrink: 0;
    align-self: stretch;
    min-height: 0;
    overflow-y: auto;
    box-sizing: border-box;
}

.drive-card {
	position: relative;
	display: flex;
	align-items: center;
	margin: 10px 0px;
	box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.125);
	cursor: pointer;
	--drive-active-color: var(--primary-highlight-color);
	background-position: center;
	background-size: 700px;
	transition:
		all 0.2s ease,
		background-size 1.2s cubic-bezier(0.19, 1, 0.22, 1);
}

.drive-card:hover {
	background-image: linear-gradient(to right, white 0%, transparent 100%), var(--topo-pattern);
	background-size: 500px;
	box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.297);
}

.drive-card.isActive {
	box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.559);
	border-radius: 10px;
	color: white;
	background-color: var(--primary-highlight-color);
	background-image: linear-gradient(to right, var(--primary-highlight-color) 30%, transparent 100%), var(--topo-pattern);
	--drive-active-color: var(--secondary-highlight-color);
}

.filter-labels {
	position: sticky;
	top: 0;
	z-index: 100;
	background-color: white;
	padding: 10px 0px;
}

.section-title {
	margin-bottom: 5px;
}

.labels {
    display: inline-block;
    background-color: var(--secondary-highlight-color);
    border: var(--primary-highlight-color) 1px solid;
    margin: 2px 4px;
    padding: 5px 8px;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.1s ease;
}

.labels:hover {
    background-color: var(--primary-highlight-color);
    color: white;
}

.labels.active {
    background-image: var(--topo-pattern);
    background-color: var(--primary-highlight-color);
    color: white;
}
</style>