<script setup>
import { useAuthStore } from '../../stores/auth';
import AdminDashboard from './AdminDashboard.vue';
import CompanyDashboard from './CompanyDashboard.vue';
import StudentDashboard from './StudentDashboard.vue';

const authStore = useAuthStore();
const id = authStore.getUserId();
const role = authStore.getUserRole();

</script>

<template>
    <div class="dashboard-body">
        <StudentDashboard v-if="role === 'Student'" />
        <CompanyDashboard v-else-if="role === 'Company'" />
        <AdminDashboard v-else />
    </div>
</template>

<style lang="css" scoped>
.dashboard-body {
    flex-grow: 1;
    height: 100vh;
    width: 100%;
}
</style>