<script setup>
defineProps(['character'])
</script>

<template>
<div class="absolute left-2 top-6 h-10 r-22 w-fit rounded-full bg-black/50 flex items-center gap-2 px-2">
  <div class="avatar">
    <div class="w-8 rounded-full">
      <img :src="character.photo" alt="">
    </div>
  </div>
  <div class="text-white text-sm">
    {{ character.name}}
  </div>
</div>
</template>

<style scoped>

</style>