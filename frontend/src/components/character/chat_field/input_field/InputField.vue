<script setup>

import SendIcon from "@/components/character/icons/SendIcon.vue";
import MicIcon from "@/components/character/icons/MicIcon.vue";
import {ref, useTemplateRef} from "vue";
import streamApi from "@/js/http/streamApi.js";

const props = defineProps(['friendId'])
const emit = defineEmits(['pushBackMessage', 'addToLastMessage', 'updateProcessing'])
const inputRef = useTemplateRef('input-ref')
const message = ref('')
const processing = ref(false)

function focus() {
  inputRef.value.focus()
}

async function handleSend() {
  if (processing.value) return
  processing.value = true
  emit('updateProcessing', true)

  const content = message.value.trim()
  if (!content) {
    processing.value = false
    emit('updateProcessing', false)
    return
  }
  message.value = ''

  emit('pushBackMessage', {role: 'user', content: content, id: crypto.randomUUID() })
  emit('pushBackMessage', {role: 'ai', content: '', id: crypto.randomUUID() })

  try {
    await streamApi('/api/friend/message/chat/', {
      body: {
        friend_id: props.friendId,
        message: content,
      },
      onmessage(data, isDone) {
        if (isDone) {
          processing.value = false
          emit('updateProcessing', false)
        } else if (data.content) {
          emit('addToLastMessage', data.content)
        }
      },
      onerror(err) {
        processing.value = false
        emit('updateProcessing', false)
      }
    })
  } catch (err) {
    processing.value = false
    emit('updateProcessing', false)
  }


}

defineExpose({
  focus,
})
</script>

<template>
  <form @submit.prevent="handleSend" class="flex items-center gap-2 h-12 px-2">
    <input
        ref="input-ref"
        v-model="message"
        class="input bg-black/30 backdrop-blur-sm text-white text-base w-full h-full rounded-2xl focus:outline-none focus:border-none focus:ring-0"
        type="text"
        placeholder="type here...">
    <div class="flex items-center gap-1">
      <div class="w-8 h-8 flex justify-center items-center cursor-pointer hover:bg-white/10 rounded-full transition-colors">
        <MicIcon/>
      </div>
      <div @click="handleSend" class="w-8 h-8 flex justify-center items-center cursor-pointer hover:bg-white/10 rounded-full transition-colors">
        <SendIcon/>
      </div>
    </div>
  </form>
</template>

<style scoped>

</style>