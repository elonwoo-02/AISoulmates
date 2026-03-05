<script setup>
import {useUserStore} from "@/stores/user.js";

defineProps(['message', 'character'])
const user = useUserStore()
</script>

<template>
<div v-if="message.content">
  <div v-if="message.role === 'ai'" class="chat chat-start">
    <div class="chat-image avatar">
      <div class="w-10 rounded-full">
        <img :src="character.photo" alt=""/>
      </div>
    </div>
    <div class="chat-bubble message-bubble wrap-break-word">{{ message.content }}</div>
  </div>
  <div v-else class="chat chat-end">
    <div class="chat-image avatar">
      <div class="w-10 rounded-full">
        <img :src="user.photo" alt=""/>
      </div>
    </div>
    <div class="chat-bubble bg-green-500 message-bubble wrap-break-word">{{ message.content }}</div>
  </div>

</div>
</template>

<style scoped>
</style>