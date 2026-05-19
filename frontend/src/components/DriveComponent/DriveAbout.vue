<script setup>

import Tooltip from '../Tooltip.vue';

const props = defineProps({
    data: Object
})

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
    <div class="drive-info">
        <div class="drive-description">
            {{ data.description }}
            <div class="info-section">
                <h3>About {{ data.company.registered_name }}</h3>
                <p>{{ data.company.description }}</p>
            </div>
            <div class="info-section">
                <h3>Contact Us</h3>
                <span class="contact">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                        stroke="currentColor" class="size-6">
                        <path stroke-linecap="round" stroke-linejoin="round"
                            d="M2.25 6.75c0 8.284 6.716 15 15 15h2.25a2.25 2.25 0 0 0 2.25-2.25v-1.372c0-.516-.351-.966-.852-1.091l-4.423-1.106c-.44-.11-.902.055-1.173.417l-.97 1.293c-.282.376-.769.542-1.21.38a12.035 12.035 0 0 1-7.143-7.143c-.162-.441.004-.928.38-1.21l1.293-.97c.363-.271.527-.734.417-1.173L6.963 3.102a1.125 1.125 0 0 0-1.091-.852H4.5A2.25 2.25 0 0 0 2.25 4.5v2.25Z" />
                    </svg>
                    {{ data.company.contact_phone }}
                </span>
                <span class="contact">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                        stroke="currentColor" class="size-6">
                        <path stroke-linecap="round" stroke-linejoin="round"
                            d="M21.75 6.75v10.5a2.25 2.25 0 0 1-2.25 2.25h-15a2.25 2.25 0 0 1-2.25-2.25V6.75m19.5 0A2.25 2.25 0 0 0 19.5 4.5h-15a2.25 2.25 0 0 0-2.25 2.25m19.5 0v.243a2.25 2.25 0 0 1-1.07 1.916l-7.5 4.615a2.25 2.25 0 0 1-2.36 0L3.32 8.91a2.25 2.25 0 0 1-1.07-1.916V6.75" />
                    </svg>
                    {{ data.company.contact_email }}</span>
                <span class="contact">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                        stroke="currentColor" class="size-6">
                        <path stroke-linecap="round" stroke-linejoin="round"
                            d="M12.75 3.03v.568c0 .334.148.65.405.864l1.068.89c.442.369.535 1.01.216 1.49l-.51.766a2.25 2.25 0 0 1-1.161.886l-.143.048a1.107 1.107 0 0 0-.57 1.664c.369.555.169 1.307-.427 1.605L9 13.125l.423 1.059a.956.956 0 0 1-1.652.928l-.679-.906a1.125 1.125 0 0 0-1.906.172L4.5 15.75l-.612.153M12.75 3.031a9 9 0 0 0-8.862 12.872M12.75 3.031a9 9 0 0 1 6.69 14.036m0 0-.177-.529A2.25 2.25 0 0 0 17.128 15H16.5l-.324-.324a1.453 1.453 0 0 0-2.328.377l-.036.073a1.586 1.586 0 0 1-.982.816l-.99.282c-.55.157-.894.702-.8 1.267l.073.438c.08.474.49.821.97.821.846 0 1.598.542 1.865 1.345l.215.643m5.276-3.67a9.012 9.012 0 0 1-5.276 3.67m0 0a9 9 0 0 1-10.275-4.835M15.75 9c0 .896-.393 1.7-1.016 2.25" />
                    </svg>
                    {{ data.company.website }}
                </span>
            </div>
        </div>
        <div class="drive-aside">
            <div class="aside-info">
                <h3>Info</h3>
                <div class="info">Job Type: {{ jobTypes[data.job_type] }}</div>
                <div class="info">Salary: {{ `${data.salary}/${salaryType[data.job_type]}` }}</div>
                <div class="info">Openings: {{ data.openings }}</div>
                <div class="info">Deadline: {{ data.deadline }}</div>
            </div>
            <div class="skill-info">
                <h3>Skills Required</h3>
                <div class="skills">
                    <Tooltip v-for="skill in data.skills_required" :key="skill.id" :text="skill.description">
                        <span class="skill">
                            {{ skill.name }}
                        </span>
                    </Tooltip>
                </div>
            </div>
        </div>
    </div>
</template>

<style lang="css" scoped>
.drive-info {
    display: flex;
    gap: 5px;
    flex-grow: 1;
    height: 100%;
    overflow: hidden;
}

.drive-description {
    flex-grow: 1;
    overflow-y: auto;
    padding-right: 10px;
}

.drive-aside {
    width: 30%;
    padding: 10px 10px;
    background-color: var(--secondary-highlight-color);
    background-image: var(--topo-pattern);
    overflow-y: auto;
}

.info-section {
    margin-top: 20px;
}

.contact {
    display: flex;
    align-items: center;
    gap: 5px;
    height: 30px;
    padding: 2px 5px;
    font-size: 0.8em;
}

.contact>svg {
    display: block;
    height: 15px;
    width: 15px;
}

.aside-info {
    padding-bottom: 10px;
    margin-bottom: 10px;
    border-bottom: var(--primary-highlight-color) solid 1px;
}

.skills {
	display: flex;
	flex-wrap: wrap;
}

.skill {
    display: inline-block;
	background-color: var(--secondary-highlight-color);
	border: var(--primary-highlight-color) 1px solid;
	margin: 2px 2px;
	padding: 4px 7px;
	border-radius: 8px;
	cursor: pointer;
}
</style>