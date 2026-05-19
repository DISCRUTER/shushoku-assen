<script setup>
import { useAuthStore } from './stores/auth';
import NavBar from './components/NavBar.vue';
import HomeView from './components/LandingPage/HomeView.vue';

const authStore = useAuthStore();
</script>

<!-- Check for transition from login to dashboard -->
<template>
  <div class="layout" v-if="authStore.getUserId()">
    <NavBar />
    <RouterView v-slot="{ Component }">
      <Transition name="fade" mode="out-in">
        <component :is="Component" />
      </Transition>
    </RouterView>
  </div>
  <div class="landing" v-else>
    <HomeView />
  </div>
</template>

<style scoped>
.layout {
  display: flex;
  gap: 10px;
  width: 100vw;
  height: 100vh;
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
