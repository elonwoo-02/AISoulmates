<script setup>
defineOptions({
  inheritAttrs: false
})
</script>

<template>
  <svg
    xmlns="http://www.w3.org/2000/svg"
    v-bind="$attrs"
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    stroke-width="1.8"
    stroke-linecap="round"
    stroke-linejoin="round"
  >
    <!-- 聊天气泡 -->
    <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
    <!-- 消息线条 -->
    <path d="M8 10h8" />
    <path d="M8 14h4" />
  </svg>
</template>

<style scoped>
</style>
