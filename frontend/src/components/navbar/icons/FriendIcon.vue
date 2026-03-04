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
    <!-- 两个人头像 -->
    <circle cx="7" cy="6" r="3" />
    <circle cx="17" cy="6" r="3" />
    <!-- 下方身体 -->
    <path d="M2 19c0-2 2.5-4 5-4s5 2 5 4" />
    <path d="M12 19c0-2 2.5-4 5-4s5 2 5 4" />
  </svg>
</template>

<style scoped>

</style>