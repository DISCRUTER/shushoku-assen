<script setup>
import SearchBar from './SearchBar.vue';

const props = defineProps({
    heading: String,
});
</script>

<template>
    <div class="header">
        <span class="title">
            <h1>{{ heading }}</h1>
        </span>
        <SearchBar />
    </div>
</template>

<style lang="css" scoped>
.header {
    background-color: white;
    background-image: linear-gradient(1turn, white 0%, transparent 100%), var(--topo-pattern);
    min-height: 50px;
    display: flex;
    align-items: center;
    padding: 20px 30px;
    padding-bottom: 25px;
    padding-right: 60px;
}

.title {
    flex-grow: 1;
}
</style>