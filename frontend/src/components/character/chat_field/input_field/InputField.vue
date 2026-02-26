<script setup>
import SendIcon from "@/components/character/icons/SendIcon.vue";
import MicIcon from "@/components/character/icons/MicIcon.vue";
</script>

<template>
  <div class="mx-auto w-full max-w-2xl">
    <div class="relative flex h-12 items-center rounded-2xl   bg-black/35 px-3 text-white backdrop-blur-md">
      <input
        class="h-full w-full bg-transparent text-sm text-white placeholder:text-white/70 focus:outline-none"
        type="text"
        placeholder="Type your message..."
      >

      <button class="flex h-9 w-9 items-center justify-center rounded-full text-white/85 transition hover:bg-white/20 hover:text-white" aria-label="Voice input">
        <MicIcon />
      </button>
      <button class="flex h-9 w-9 items-center justify-center rounded-full text-white/85 transition hover:bg-white/20 hover:text-white" aria-label="Send message">
        <SendIcon />
      </button>
    </div>
  </div>
</template>

<style scoped>
</style>

