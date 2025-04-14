<template>
  <RouterView />
</template>

<script setup lang="ts">
import { RouterView } from 'vue-router'
</script>

<style>
.vertical-spacing {
    margin: 10px 0;
}

.horizontal-spacing {
    margin: 0 10px;
}

.spacing {
  padding: 10px;
}
</style>
