<script setup>
import Message from "@/components/character/chat_field/chat_history/message/Message.vue";

const props = defineProps(
  ['history', 'friendId', 'character']
)

</script>

<template>
  <div class="flex-1 overflow-y-scroll no-scrollbar">
    <Message
        v-for="message in history"
        :key="message.id"
        :message="message"
        :character="character"
    />
  </div>

</template>

<style scoped>

</style>