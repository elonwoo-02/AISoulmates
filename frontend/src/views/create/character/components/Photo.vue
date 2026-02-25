<script setup>
import {onBeforeUnmount, ref, useTemplateRef, watch} from "vue";
import CameraIcon from "@/views/user/profile/compoents/icon/CameraIcon.vue";

import Croppie from 'croppie'          // 引入 Croppie 裁剪库
import 'croppie/croppie.css'           // Croppie 样式

const props = defineProps(['photo'])

const myPhoto = ref(props.photo)

watch(() => props.photo, newVal => {
  myPhoto.value = newVal
})

const fileInputRef = useTemplateRef('file-input-ref')
const modalRef = useTemplateRef('modal-ref')
const croppieRef = useTemplateRef('croppie-ref')
let croppie = null

async function openModal(photo) {
  modalRef.value.showModal()

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

async function crop(){
  if (!croppie) return

  myPhoto.value = await croppie.result({
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
  myPhoto
})

</script>

<template>
  <div class="flex justify-center">
    <div class="avatar relative">
      <div v-if="myPhoto" class="w-28 rounded-full">
        <img :src="myPhoto" alt="photo"/>
      </div>
      <div v-else class="w-28 h-28 rounded-full bg-base-200"></div>
      <div @click="fileInputRef.click()" class="w-28 h-28 rounded-full bg-black/20 absolute left-0 top-0 flex justify-center items-center cursor-pointer">
        <CameraIcon/>
      </div>
    </div>
  </div>

  <input ref="file-input-ref" type="file" class="hidden" id="image/*" @change="onFileChange"/>

  <dialog ref="modal-ref" class="modal">
    <div class="modal-box transition-none">
      <button @click="modalRef.close()" class="btn btn-sm btn-circle btn-ghost absolute top-2 right-2">✕</button>

      <div ref="croppie-ref" class="flex flex-col my-4"></div>

      <div class="modal-action">
        <button @click="modalRef.close()" class="btn">Cancel</button>
        <button @click="crop" class="btn btn-neutral">Confirm</button>
      </div>
    </div>
  </dialog>
</template>

<style scoped>

</style>