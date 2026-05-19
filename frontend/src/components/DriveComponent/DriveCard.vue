<script setup>

const props = defineProps({
	drive: Object,
	active: Boolean,
});

const jobTypes = {
	"internship": "Internship",
	"part-time": "Part Time",
	"full-time": "Full Time"
}
</script>

<template>
	<div class="drive-selected" :class="{ active: active }"></div>
	<div class="drive-avatar">
		<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 41 50">
			<path fill="var(--drive-active-color)"
				d="M23.312,44.301 L18.497,49.105 L12.435,43.800 L17.195,43.800 L17.195,41.198 L17.195,38.997 L12.435,38.997 L17.542,34.527 L18.497,33.692 L18.757,33.952 L19.966,35.157 L20.654,35.844 L23.312,38.496 L25.259,38.496 L35.436,38.496 L36.242,38.496 L36.948,38.496 L37.859,38.496 L40.277,38.496 L40.791,38.496 L40.791,44.301 L23.312,44.301 ZM36.948,36.085 L36.242,36.085 L24.317,36.085 L20.214,31.986 L19.966,31.739 L19.966,23.492 L20.306,23.294 L30.347,17.513 L36.948,21.315 L40.729,23.492 L40.729,36.085 L39.626,36.085 L36.948,36.085 ZM30.347,24.808 C27.763,24.808 25.668,26.898 25.668,29.470 C25.668,32.048 27.763,34.137 30.347,34.137 C32.926,34.137 35.021,32.048 35.021,29.470 C35.021,26.898 32.926,24.808 30.347,24.808 ZM30.347,14.731 L29.139,15.424 L18.757,21.402 L17.542,22.101 L17.542,31.318 L16.904,31.875 L10.842,37.179 L6.249,41.198 L0.002,41.198 L0.002,0.895 L27.651,0.895 C31.283,4.518 33.316,6.546 36.948,10.169 L36.948,18.527 L31.556,15.424 L30.347,14.731 ZM7.898,4.605 L3.720,4.605 L3.720,8.765 L7.898,8.765 L7.898,4.605 ZM13.947,4.605 L9.776,4.605 L9.776,8.765 L13.947,8.765 L13.947,4.605 Z">
			</path>
		</svg>
	</div>
	<div class="drive-info">
		<div class="drive-title">{{ drive.title }}</div>
		<div class="drive-extra">
			<span class="drive-extra-info">
				<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="var(--drive-active-color)" class="size-5">
					<path fill-rule="evenodd"
						d="M6 3.75A2.75 2.75 0 0 1 8.75 1h2.5A2.75 2.75 0 0 1 14 3.75v.443c.572.055 1.14.122 1.706.2C17.053 4.582 18 5.75 18 7.07v3.469c0 1.126-.694 2.191-1.83 2.54-1.952.599-4.024.921-6.17.921s-4.219-.322-6.17-.921C2.694 12.73 2 11.665 2 10.539V7.07c0-1.321.947-2.489 2.294-2.676A41.047 41.047 0 0 1 6 4.193V3.75Zm6.5 0v.325a41.622 41.622 0 0 0-5 0V3.75c0-.69.56-1.25 1.25-1.25h2.5c.69 0 1.25.56 1.25 1.25ZM10 10a1 1 0 0 0-1 1v.01a1 1 0 0 0 1 1h.01a1 1 0 0 0 1-1V11a1 1 0 0 0-1-1H10Z"
						clip-rule="evenodd" />
					<path
						d="M3 15.055v-.684c.126.053.255.1.39.142 2.092.642 4.313.987 6.61.987 2.297 0 4.518-.345 6.61-.987.135-.041.264-.089.39-.142v.684c0 1.347-.985 2.53-2.363 2.686a41.454 41.454 0 0 1-9.274 0C3.985 17.585 3 16.402 3 15.055Z" />
				</svg>
				{{ jobTypes[drive.job_type] }}
			</span>
			<span class="drive-extra-info">
				<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="var(--drive-active-color)" class="size-5">
					<path
						d="M10 9.25a.75.75 0 0 0-.75.75v.01c0 .414.336.75.75.75h.01a.75.75 0 0 0 .75-.75V10a.75.75 0 0 0-.75-.75H10ZM6 13.25a.75.75 0 0 0-.75.75v.01c0 .414.336.75.75.75h.01a.75.75 0 0 0 .75-.75V14a.75.75 0 0 0-.75-.75H6ZM8 13.25a.75.75 0 0 0-.75.75v.01c0 .414.336.75.75.75h.01a.75.75 0 0 0 .75-.75V14a.75.75 0 0 0-.75-.75H8ZM9.25 14a.75.75 0 0 1 .75-.75h.01a.75.75 0 0 1 .75.75v.01a.75.75 0 0 1-.75.75H10a.75.75 0 0 1-.75-.75V14ZM12 11.25a.75.75 0 0 0-.75.75v.01c0 .414.336.75.75.75h.01a.75.75 0 0 0 .75-.75V12a.75.75 0 0 0-.75-.75H12ZM12 13.25a.75.75 0 0 0-.75.75v.01c0 .414.336.75.75.75h.01a.75.75 0 0 0 .75-.75V14a.75.75 0 0 0-.75-.75H12ZM13.25 12a.75.75 0 0 1 .75-.75h.01a.75.75 0 0 1 .75.75v.01a.75.75 0 0 1-.75.75H14a.75.75 0 0 1-.75-.75V12ZM11.25 10.005c0-.417.338-.755.755-.755h2a.755.755 0 1 1 0 1.51h-2a.755.755 0 0 1-.755-.755ZM6.005 11.25a.755.755 0 1 0 0 1.51h4a.755.755 0 1 0 0-1.51h-4Z" />
					<path fill-rule="evenodd"
						d="M5.75 2a.75.75 0 0 1 .75.75V4h7V2.75a.75.75 0 0 1 1.5 0V4h.25A2.75 2.75 0 0 1 18 6.75v8.5A2.75 2.75 0 0 1 15.25 18H4.75A2.75 2.75 0 0 1 2 15.25v-8.5A2.75 2.75 0 0 1 4.75 4H5V2.75A.75.75 0 0 1 5.75 2Zm-1 5.5c-.69 0-1.25.56-1.25 1.25v6.5c0 .69.56 1.25 1.25 1.25h10.5c.69 0 1.25-.56 1.25-1.25v-6.5c0-.69-.56-1.25-1.25-1.25H4.75Z"
						clip-rule="evenodd" />
				</svg>
				{{ drive.deadline }}
			</span>
		</div>
	</div>
</template>

<style lang="css" scoped>
.drive-avatar {
	margin-left: 15px;
}

.drive-avatar>svg {
	display: block;
	height: 40px;
	width: 40px;
}

.drive-info {
	flex-grow: 1;
	padding: 10px 10px;
}

.drive-selected {
	position: absolute;
	left: 8px;
	top: 20%;
	bottom: 20%;
	background-color: var(--primary-highlight-color);
	border-radius: 2px;
	width: 5px;

	transition:
		top 0.2s ease,
		bottom 0.2s ease;
}

.drive-selected.active {
	top: 30%;
	bottom: 30%;
	background-color: var(--accent-bar-color);
}

.drive-title {
	font-size: 1.2em;
	font-weight: 500;
	padding: 2px 0px;
}

.drive-extra {
	display: flex;
	justify-content: space-around;
}

.drive-extra-info {
	display: flex;
	align-items: center;
	gap: 5px;
}

.drive-extra-info>svg {
	display: block;
	height: 20px;
	width: 20px;
}
</style>