<script setup>
import { nextTick, onBeforeUnmount, ref, useTemplateRef, watch } from 'vue'
import CameraIcon from '@/views/user/profile/compoents/icon/CameraIcon.vue'

import Croppie from 'croppie'
import 'croppie/croppie.css'

const props = defineProps(['photo'])
const myPhoto = ref(props.photo)

watch(
  () => props.photo,
  newVal => {
    myPhoto.value = newVal
  },
)

const fileInputRef = useTemplateRef('file-input-ref')
const modalRef = useTemplateRef('modal-ref')
const croppieRef = useTemplateRef('croppie-ref')

let croppie = null

async function openModal(photo) {
  modalRef.value.showModal()
  await nextTick()

  if (!croppie) {
    croppie = new Croppie(croppieRef.value, {
      viewport: { width: 200, height: 200, type: 'square' },
      boundary: { width: 300, height: 300 },
      enableOrientation: true,
      enforceBoundary: true,
    })
  }

  croppie.bind({
    url: photo,
  })
}

async function crop() {
  if (!croppie) return

  myPhoto.value = await croppie.result({
    type: 'base64',
    size: 'viewport',
  })

  modalRef.value.close()
}

function onFileChange(e) {
  const file = e.target.files[0]
  e.target.value = ''
  if (!file) return

  const reader = new FileReader()
  reader.onload = () => {
    openModal(reader.result)
  }
  reader.readAsDataURL(file)
}

onBeforeUnmount(() => {
  croppie?.destroy()
})

defineExpose({
  myPhoto,
})
</script>

<template>
  <div class="flex justify-center">
    <div class="avatar relative">
      <div class="h-28 w-28 rounded-full ring-2 ring-base-300">
        <img :src="myPhoto" alt="avatar" class="object-cover" />
      </div>

      <button
        type="button"
        @click="fileInputRef.click()"
        class="absolute inset-0 flex items-center justify-center rounded-full bg-black/35 text-white transition hover:bg-black/45 cursor-pointer"
      >
        <CameraIcon />
      </button>
    </div>
  </div>

  <input
    ref="file-input-ref"
    type="file"
    accept="image/*"
    class="hidden"
    @change="onFileChange"
  />

  <dialog ref="modal-ref" class="modal">
    <div class="modal-box transition-none">
      <button @click="modalRef.close()" class="btn btn-circle btn-xs btn-ghost absolute right-2 top-2">x</button>

      <div ref="croppie-ref" class="my-4 flex flex-col justify-center"></div>

      <div class="modal-action">
        <button @click="modalRef.close()" class="btn">Cancel</button>
        <button @click="crop" class="btn btn-neutral">Confirm</button>
      </div>
    </div>
  </dialog>
</template>

<style scoped>
</style>