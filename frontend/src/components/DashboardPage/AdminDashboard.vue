<script setup>
import { useRouter } from 'vue-router';
import Header from '../Header.vue';
import StudentKpi from '../ChartComponent/StudentKpi.vue';
import CompanyKpi from '../ChartComponent/CompanyKpi.vue';
import ApplicationFunnel from '../ChartComponent/ApplicationFunnel.vue';
import DriveKpi from '../ChartComponent/DriveKpi.vue';
import CountCard from '../ChartComponent/CountCard.vue';

const router = useRouter();

function goTo(target) {
    router.push(`/${target}`)
}

</script>

<template>
    <div class="dashboard-content">
        <Header heading="Welcome Admin" />
        <div class="admin-content">
            <div class="section-left">
                <div class="big-chart">
                    <div class="drive-chart">
                        <DriveKpi />
                    </div>
                    <div class="more-info">
                        <CountCard target="application" />
                        <CountCard target="placements" />
                    </div>
                </div>
                <div class="approval-container">
                    <div class="approval" @click="goTo('company')">
                        <div class="arrow">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                                stroke="currentColor" class="size-6">
                                <path stroke-linecap="round" stroke-linejoin="round"
                                    d="m4.5 19.5 15-15m0 0H8.25m11.25 0v11.25" />
                            </svg>
                        </div>
                        <h3>Approval Required</h3>
                        <h2 class="label">COMPANY</h2>
                    </div>
                    <div class="approval" @click="goTo('drive')">
                        <div class="arrow">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                                stroke="currentColor" class="size-6">
                                <path stroke-linecap="round" stroke-linejoin="round"
                                    d="m4.5 19.5 15-15m0 0H8.25m11.25 0v11.25" />
                            </svg>
                        </div>
                        <h3>Approval Required</h3>
                        <h2 class="label">DRIVE</h2>
                    </div>
                </div>
            </div>
            <div class="section-right">
                <div class="section-r-one">
                    <div class="kpi">
                        <CompanyKpi />
                    </div>
                    <div class="kpi">
                        <StudentKpi />
                    </div>
                </div>
                <div class="section-r-two">
                    <div class="funnel">
                        <ApplicationFunnel />
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.dashboard-content {
    display: flex;
    flex-direction: column;
    height: 100vh;
}

.admin-content {
    flex-grow: 1;
    display: flex;
    padding: 10px;
    gap: 10px;
}

.section-left {
    height: 100%;
    min-width: 400px;
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.big-chart {
    flex-grow: 1;
    background-image: var(--topo-pattern);
    border-radius: 10px;
    display: flex;
    align-items: center;
    gap: 10px;
    box-sizing: border-box;
    padding: 10px 10px;
}

.drive-chart {
    width: 550px;
    height: 400px;
}

.more-info {
    flex-grow: 1;
}

.approval-container {
    display: flex;
    width: 100%;
    gap: 10px;
}

.approval {
    position: relative;
    min-height: 150px;
    width: 400px;
    line-height: 3em;
    color: var(--primary-highlight-color);
    background-color: var(--accent-bar-color);
    background-image: var(--topo-pattern);
    background-size: 800px;
    background-position: center;
    box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.125);
    border-radius: 10px;
    margin-top: 10px;
    margin-bottom: 10px;
    padding: 18px 10px;
    box-sizing: border-box;
    cursor: pointer;
    transition: background-size 1.2s cubic-bezier(0.19, 1, 0.22, 1);
}

.approval:hover {
    box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.297);
    background-size: 600px;
}

.arrow {
    position: absolute;
    top: 10px;
    right: 10px;
    height: 40px;
    width: 40px;
    z-index: 100;
    transition: transform 0.3s ease;
}

.approval:hover .arrow {
    transform: scale(1.3) translate(5px, -5px);
}

.label {
    font-weight: 700;
    font-size: 4em;
}

.section-right {
    flex-grow: 1;
    height: 100%;
    display: flex;
    gap: 10px;
}

.section-r-one {
    flex-grow: 1;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: space-around;
    gap: 10px;
}

.kpi {
    flex-grow: 1;
    min-height: 200px;
    background-color: var(--primary-highlight-color);
    background-image: var(--topo-pattern);
    border-radius: 10px;
}

.section-r-two {
    min-width: 375px;
    height: 100%;
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.kpi-f {
    height: 150px;
    background-color: var(--primary-highlight-color);
    background-image: var(--topo-pattern);
    border-radius: 10px;
}

.funnel {
    flex-grow: 1;
    background-color: var(--accent-bar-color);
    background-image: var(--topo-pattern);
    border-radius: 10px;
}
</style>