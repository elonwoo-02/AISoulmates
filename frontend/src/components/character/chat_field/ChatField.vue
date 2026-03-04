<script setup>
import {computed, nextTick, ref, useTemplateRef} from 'vue'
import InputField from '@/components/character/chat_field/input_field/InputField.vue'
import CharacterPhotoField from '@/components/character/chat_field/character_photo_field/CharacterPhotoField.vue'

const props = defineProps(['friend'])
const modalRef = useTemplateRef('modal-ref')
const inputRef = useTemplateRef('input-ref')
const history = ref(null)

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
  }
  return {}
})

defineExpose({
  showModal,
})
</script>

<template>
  <dialog ref="modal-ref" class="modal" @click.stop>
    <div class="modal-box w-11/12 max-w-2xl h-[85vh] sm:h-5/6 max-h-[600px] flex flex-col" :style="modalStyle">
      <!-- Header: Character Info + Close Button -->
      <div class="flex justify-between items-start mb-2">
        <CharacterPhotoField v-if="friend" :character="friend.character" />
        <button @click.stop="modalRef.close()" class="btn btn-sm btn-circle btn-ghost bg-black/30 text-white hover:bg-black/50">✕</button>
      </div>

      <!-- Message Area Placeholder -->
      <div class="flex-1 overflow-y-auto py-4">
        <!-- TODO: Add message list component here -->
      </div>

      <!-- Footer: Input Field -->
      <InputField
          v-if="friend"
          ref="input-ref"
          :friendId="friend.id"
      />
    </div>
  </dialog>
</template>

<style scoped>
</style>
