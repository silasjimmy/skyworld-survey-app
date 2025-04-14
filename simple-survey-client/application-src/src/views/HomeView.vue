<template>
  <a-page-header
    title="Sky World Survey"
    style="border-bottom: 1px solid rgb(235, 237, 240)"
    :avatar="{ src: 'https://avatars1.githubusercontent.com/u/8186664?s=460&v=4' }"
  >
  </a-page-header>

  <main class="spacing">
    <div class="vertical-spacing">
      <a-typography-text>Welcome to the Sky World Survey</a-typography-text>
    </div>

    <a-card>
      <a-space direction="vertical">
        <RouterLink to="/questions">Take the survey</RouterLink>

        <RouterLink to="/responses">View responses</RouterLink>
      </a-space>
    </a-card>
  </main>
</template>

<script setup lang="ts">
import { RouterLink } from 'vue-router';
</script>

<style scoped></style>
