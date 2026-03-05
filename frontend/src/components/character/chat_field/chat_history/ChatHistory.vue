<script setup>
import Message from "@/components/character/chat_field/chat_history/message/Message.vue";
import {nextTick, useTemplateRef} from "vue";

const props = defineProps(
  ['history', 'friendId', 'character']
)
const scrollRef = useTemplateRef('scroll-ref')

async function scrollToBottom() {
  await nextTick()
  if (scrollRef.value) {
    scrollRef.value.scrollTop = scrollRef.value.scrollHeight
  }
}

defineExpose({
  scrollToBottom,
})
</script>

<template>
  <div ref="scroll-ref" class="flex-1 overflow-y-scroll overflow-x-hidden no-scrollbar w-full">

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