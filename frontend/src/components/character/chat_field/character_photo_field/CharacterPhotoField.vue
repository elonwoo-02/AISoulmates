<script setup>
import { useRouter } from 'vue-router'
defineProps(['character', 'isThinking'])
const router = useRouter()

function handleAvatarClick() {
  router.push(`/create/character/update/${character.id}/`)
}
</script>

<template>
<div class="flex items-center gap-3 px-3 py-2 rounded-2xl bg-black/40 backdrop-blur-sm">
  <div class="avatar" @click="handleAvatarClick">
    <div class="w-8 rounded-full ring-2 ring-white/30 cursor-pointer hover:ring-white/50 transition-all">
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