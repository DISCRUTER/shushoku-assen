<script setup>

const props = defineProps({
    data: Object
})

</script>

<template>
    <div class="util-card">
        <div class="company-name">
            <h3>{{ data.name }}</h3>
        </div>
        <div class="company-about">
            <p>{{ data.description }}</p>
        </div>
    </div>
</template>

<style lang="css" scoped>
.util-card {
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
    min-height: 150px;
    width: 350px;
    border-radius: 10px;
    box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.125);
    background-color: white;
    background-image: var(--topo-pattern);
    background-size: 800px;
    background-position: center;
    cursor: pointer;
    box-sizing: border-box;
    transition: all 1.2s cubic-bezier(0.19, 1, 0.22, 1);
}

.util-card:hover {
    box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.297);
    background-size: 600px;
}

.company-name {
    display: flex;
    justify-content: flex-start;
    align-items: flex-end;
    background-color: var(--primary-highlight-color);
    color: var(--accent-bar-color);
    padding: 5px 8px;
    border-top-left-radius: 10px;
    border-top-right-radius: 10px;
    height: 120px;
    width: 100%;
    box-sizing: border-box;
}

.company-name>h3 {
    font-weight: 400;
}

.company-about {
    flex-grow: 1;
    text-align: center;
    height: 100%;
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 15px;
    box-sizing: border-box;
}
</style>