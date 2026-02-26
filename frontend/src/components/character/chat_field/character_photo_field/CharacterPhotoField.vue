<script setup>
defineProps(['character'])
</script>

<template>
  <div class="inline-flex w-fit items-center gap-2 rounded-full   bg-black/30 px-2.5 py-1 text-white backdrop-blur-md">
    <div class="avatar">
      <div class="w-8 rounded-full ring-1 ring-white/40">
        <img :src="character.photo" alt="character avatar">
      </div>
    </div>
    <div class="max-w-36 truncate text-sm font-medium">
      {{ character.name }}
    </div>
  </div>
</template>

<style scoped>
</style>

