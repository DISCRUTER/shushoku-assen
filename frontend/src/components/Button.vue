<script setup>
const props = defineProps({
  label: {
    type: String,
    default: 'Apply'
  }
});
</script>

<template>
  <button class="styled-btn">
    <span class="triangle-bar"></span>
    <span class="accent-bar"></span>
    <span class="label-text">{{ label }}</span>
  </button>
</template>

<style lang="css" scoped>
.styled-btn {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 12px 40px;
  background-color: var(--primary-highlight-color);
  background-image: linear-gradient(to right, var(--primary-highlight-color) 0%, transparent 100%), var(--topo-pattern);
  background-size: 400px;
  color: white;
  border: none;
  font-family: 'Inter', sans-serif;
  font-weight: 600;
  cursor: pointer;
  overflow: hidden;
  transition: transform 0.2s ease;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
  transition: border-radius 0.3s ease;
}

.accent-bar {
  position: absolute;
  left: 8px;
  top: 20%;
  bottom: 20%;
  width: 4px;
  background-color: var(--accent-bar-color);
  border-radius: 2px;
  transition: all 1.2s cubic-bezier(0.19, 1, 0.22, 1);
}

.triangle-bar {
  position: absolute;
  left: 8px;
  top: 50%;
  transform: translateY(-50%);
  width: 0;
  height: 0;
  border-top: 10px solid transparent;
  border-bottom: 10px solid transparent;
  border-left: 0px solid var(--accent-bar-color);
  border-radius: 2px;
  transition: all 0.2s cubic-bezier(0.19, 1, 0.22, 1);
}

.styled-btn:hover {
  border-radius: 5px;
}

.styled-btn:hover .accent-bar {
  width: 1px;
  top: 40%;
  bottom: 40%;
}

.styled-btn:hover .triangle-bar {
  border-left: 10px solid var(--accent-bar-color);
}

.label-text {
  margin-left: 10px;
}
</style>