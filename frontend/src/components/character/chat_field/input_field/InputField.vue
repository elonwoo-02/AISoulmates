<script setup>

import SendIcon from "@/components/character/icons/SendIcon.vue";
import MicIcon from "@/components/character/icons/MicIcon.vue";
import {useTemplateRef} from "vue";

const inputRef = useTemplateRef('input-ref')

function focus() {
  inputRef.value.focus()
}

defineExpose({focus})
</script>

<template>
  <div class="absolute bottom-4 left-1/2 -translate-x-1/2 h-12 w-86 flex items-center">
    <input
        ref="input-ref"
        class="input bg-black/30 backdrop-blur-sm text-white text-base w-full h-full rounded-2xl focus:outline-none focus:border-none focus:ring-0"
        type="text"
        placeholder="type here...">
    <div class="absolute right-2 w-8 h-8 flex justify-center items-center cursor-pointer">
      <SendIcon/>
    </div>
    <div class="absolute right-8 w-8 h-8 flex justify-center items-center cursor-pointer">
      <MicIcon/>
    </div>
  </div>
</template>

<style scoped>

</style>