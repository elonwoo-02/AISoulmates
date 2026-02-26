<script setup>
import { computed, useTemplateRef } from 'vue'
import InputField from '@/components/character/chat_field/input_field/InputField.vue'
import CharacterPhotoField from '@/components/character/chat_field/character_photo_field/CharacterPhotoField.vue'

const props = defineProps(['friend'])
const modalRef = useTemplateRef('modal-ref')

function showModal() {
  modalRef.value?.showModal()
}

function closeModal() {
  if (modalRef.value?.open) {
    modalRef.value.close()
  }
}

function handleBackdropClick(event) {
  if (event.target === modalRef.value) {
    closeModal()
  }
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
  closeModal,
})
</script>

<template>
  <dialog ref="modal-ref" class="modal layer-modal" @click="handleBackdropClick">
    <div class="modal-box relative h-[80vh] w-11/12 max-w-3xl overflow-hidden rounded-3xl p-0" :style="modalStyle" @click.stop>
      <div class="absolute inset-0 bg-gradient-to-t from-black/55 via-black/20 to-black/30"></div>

      <button
        type="button"
        @click.stop.prevent="closeModal"
        class="absolute right-3 top-3 z-[120] inline-flex h-10 w-10 items-center justify-center rounded-full bg-black/20 text-white/90 transition-colors hover:bg-black/35 hover:text-white"
        aria-label="Close chat"
      >
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-5 w-5">
          <path d="M18 6L6 18"></path>
          <path d="M6 6l12 12"></path>
        </svg>
      </button>

      <div class="relative z-10 flex h-full flex-col justify-between p-4 sm:p-5">
        <CharacterPhotoField v-if="friend" :character="friend.character" />
        <InputField />
      </div>
    </div>
  </dialog>
</template>

<style scoped>
</style>
