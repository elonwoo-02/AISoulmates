<script setup>
import {nextTick, onBeforeUnmount, ref, useTemplateRef, watch} from "vue";
import CameraIcon from "@/views/user/profile/components/icon/CameraIcon.vue";

import Croppie from 'croppie'
import 'croppie/croppie.css'

const props = defineProps(['backgroundImage'])
const myBackgroundImage = ref(props.backgroundImage)

watch(() => props.backgroundImage, newVal => {
  myBackgroundImage.value = newVal
})


const fileInputRef = useTemplateRef('file-input-ref')
const modalRef = useTemplateRef('modal-ref')
const croppieRef = useTemplateRef('croppie-ref')
let croppie = null

async function openModal(photo) {
  modalRef.value.showModal()
  await nextTick()

  if (!croppie) {
    croppie = new Croppie(croppieRef.value, {
      viewport: { width: 210, height: 350},
      boundary: { width: 400, height: 400 },
      enableOrientation: true,
      enforceBoundary: true,
    })
  }

  croppie.bind({
    url: photo,
  })
}

async function crop(){
  if (!croppie) return

  myBackgroundImage.value = await croppie.result({
    type: 'base64',
    size: 'viewport',
  })

  modalRef.value.close()
}

function onFileChange(event) {
  const file = event.target.files[0]
  event.target.value = ''
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
  myBackgroundImage
})
</script>

<template>
  <div class="flex justify-center">
    <div class="relative">
      <div v-if="myBackgroundImage" class="h-24 w-16 rounded-box ring-2 ring-base-300">
        <img :src="myBackgroundImage" alt="background" class="object-cover" />
      </div>
      <div v-else class="h-24 w-16 rounded-box bg-base-200 ring-2 ring-base-300"></div>
      <button
        type="button"
        @click="fileInputRef.click()"
        class="absolute inset-0 flex items-center justify-center rounded-box bg-black/35 text-white transition hover:bg-black/45 cursor-pointer"
      >
        <CameraIcon />
      </button>
    </div>
  </div>

  <input ref="file-input-ref" type="file" accept="image/*" class="hidden" @change="onFileChange"/>

  <dialog ref="modal-ref" class="modal">
    <div class="modal-box transition-none max-w-2xl">
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
