<template>
  <div class="tooltip-wrapper" @mouseenter="onEnter" @mouseleave="show = false">
    <slot></slot>

    <Teleport to="body">
      <Transition name="fade">
        <div v-if="show" class="tooltip-box" :style="tooltipStyle">
          {{ text }}
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';

const props = defineProps({
  text: { type: String, required: true },
  position: { type: String, default: 'top' } // top, bottom, left, right
});

const show = ref(false);
const coords = ref({ top: 0, left: 0, placement: 'top' });

function onEnter(e) {
  const rect = e.currentTarget.getBoundingClientRect();
  const GAP = 8;

  let top, left;
  const placement = props.position;

  if (placement === 'bottom') {
    top = rect.bottom + GAP + window.scrollY;
    left = rect.left + rect.width / 2 + window.scrollX;
  } else if (placement === 'left') {
    top = rect.top + rect.height / 2 + window.scrollY;
    left = rect.left - GAP + window.scrollX;
  } else if (placement === 'right') {
    top = rect.top + rect.height / 2 + window.scrollY;
    left = rect.right + GAP + window.scrollX;
  } else {
    // default: top
    top = rect.top - GAP + window.scrollY;
    left = rect.left + rect.width / 2 + window.scrollX;
  }

  coords.value = { top, left, placement };
  show.value = true;
}

const tooltipStyle = computed(() => {
  const { top, left, placement } = coords.value;
  const base = { top: `${top}px`, left: `${left}px` };

  if (placement === 'bottom') {
    return { ...base, transform: 'translateX(-50%)' };
  } else if (placement === 'left') {
    return { ...base, transform: 'translate(-100%, -50%)' };
  } else if (placement === 'right') {
    return { ...base, transform: 'translateY(-50%)' };
  } else {
    // top
    return { ...base, transform: 'translate(-50%, -100%)' };
  }
});
</script>

<style scoped>
.tooltip-wrapper {
  position: relative;
  display: inline-block;
}

.tooltip-box {
  position: fixed;
  background-color: #1a1a1a;
  color: #fff;
  min-width: 200px;
  max-width: 300px;
  max-height: 400px;
  padding: 8px 12px;
  border-radius: 4px;
  font-size: 12px;
  z-index: 9999;
  overflow-y: auto;
  border: 1px solid #444;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.5);
  pointer-events: none;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>