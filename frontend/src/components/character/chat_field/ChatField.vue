<script setup>
import {computed, nextTick, ref, useTemplateRef} from 'vue'
import InputField from '@/components/character/chat_field/input_field/InputField.vue'
import CharacterPhotoField from '@/components/character/chat_field/character_photo_field/CharacterPhotoField.vue'
import ChatHistory from "@/components/character/chat_field/chat_history/ChatHistory.vue";

const props = defineProps(['friend'])
const modalRef = useTemplateRef('modal-ref')
const inputRef = useTemplateRef('input-ref')
const chatHistoryRef = useTemplateRef('chat-history-ref')
const history = ref([])

async function showModal() {
  modalRef.value.showModal()

  await nextTick()
  inputRef.value.focus()
}

const modalStyle = computed(() => {
  if (props.friend) {
    return {
      backgroundImage: `url(${props.friend.character.background_image})`,
      backgroundSize: 'cover',
      backgroundPosition: 'center',
      backgroundRepeat: 'no-repeat',
    }
  } else {
    return {}
  }
})

function handlePushBackMessage(msg) {
  history.value.push(msg)
  chatHistoryRef.value.scrollToBottom()
}

function handleAddToLastMessage(delta) {
  history.value.at(-1).content += delta
  chatHistoryRef.value.scrollToBottom()
}

function handlePushFrontMessage(msg) {
  history.value.unshift(msg)
}

defineExpose({
  showModal,
})
</script>

<template>
  <dialog ref="modal-ref" class="modal" @click.stop>
    <div class="modal-box p-2 max-w-sm aspect-3/5 flex flex-col" :style="modalStyle">
      <!-- Header: Character Info + Close Button -->
      <div class="flex justify-between items-start mb-2">
        <CharacterPhotoField v-if="friend" :character="friend.character" />
        <button @click.stop="modalRef.close()" class="btn btn-sm btn-circle btn-ghost bg-black/30 text-white hover:bg-black/50">✕</button>
      </div>

      <!-- Message Area Placeholder -->
      <ChatHistory
          ref="chat-history-ref"
          v-if="friend"
          :history="history"
          :friendId="friend.id"
          :character="friend.character"
          @pushBackFrontMessage="handlePushFrontMessage"
      />

      <!-- Footer: Input Field -->
      <InputField
          v-if="friend"
          ref="input-ref"
          :friendId="friend.id"
          @pushBackMessage="handlePushBackMessage"
          @addToLastMessage="handleAddToLastMessage"
      />
    </div>
  </dialog>
</template>

<style scoped>
</style>
