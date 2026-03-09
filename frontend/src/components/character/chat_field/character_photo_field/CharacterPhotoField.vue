<script setup>
import { useRouter } from 'vue-router'
defineProps(['character', 'isThinking'])
const router = useRouter()

function handleAvatarClick() {
  router.push(`/create/character/update/${character.id}/`)
}
</script>

<template>
<div class="flex items-center gap-2 px-2 py-1 rounded-xl bg-black/40 backdrop-blur-sm">
  <div class="avatar" @click="handleAvatarClick">
    <div class="w-6 rounded-full ring-2 ring-white/30 cursor-pointer hover:ring-white/50 transition-all">
      <img :src="character.photo" alt="">
    </div>
  </div>
  <div class="text-white">
    <div class="font-medium text-xs">{{ character.name }}</div>
    <div class="text-xs text-white/60">{{ isThinking ? 'Thinking...' : 'Online' }}</div>
  </div>
</div>
</template>

<style scoped>
</style>
