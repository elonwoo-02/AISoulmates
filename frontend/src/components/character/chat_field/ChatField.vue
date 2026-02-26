<script setup>
import { computed, useTemplateRef } from 'vue'
import InputField from '@/components/character/chat_field/input_field/InputField.vue'
import CharacterPhotoField from '@/components/character/chat_field/character_photo_field/CharacterPhotoField.vue'

const props = defineProps(['friend'])
const modalRef = useTemplateRef('modal-ref')

function showModal() {
  modalRef.value.showModal()
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
    <div class="modal-box w-11/12 max-w-2xl h-5/6 max-h-600px" :style="modalStyle">
      <div class="flex justify-between items-center mb-4">
        <button @click.stop="modalRef.close()" class="btn btn-sm btn-circle btn-ghost absolute bg-transparent right-1 top-1">✕</button>
        <InputField />
        <CharacterPhotoField v-if="friend" :character="friend.character" />
      </div>
    </div>
  </dialog>
</template>

<style scoped>
</style>
