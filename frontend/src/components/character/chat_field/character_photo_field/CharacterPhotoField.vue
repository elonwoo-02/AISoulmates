<script setup>
defineProps(['character', 'isThinking'])
</script>

<template>
<div class="flex items-center gap-3 px-3 py-2 rounded-2xl bg-black/40 backdrop-blur-sm">
  <div class="avatar">
    <div class="w-8 rounded-full ring-2 ring-white/30">
      <img :src="character.photo" alt="">
    </div>
  </div>
  <div class="text-white">
    <div class="font-medium text-sm">{{ character.name }}</div>
    <div class="text-xs text-white/60">{{ isThinking ? 'Thinking...' : 'Online' }}</div>
  </div>
</div>
</template>

<style scoped>
</style>