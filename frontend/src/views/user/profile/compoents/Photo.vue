<script setup>
import {nextTick, onBeforeMount, ref, useTemplateRef, watch} from "vue";
import CameraIcon from "@/views/user/profile/compoents/icon/CameraIcon.vue";

import Croppie from 'croppie'
import 'croppie/croppie.css'

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
  await nextTick()

  if (!croppie) {
    croppie = new Croppie(croppieRef.value,  {
      viewport: {width: 200, height: 200, type: 'square'},
      boundary: {width: 300, height: 300},
      enableOrientation: true,
      enforceBoundary: true,
    })
  }

  croppie.bind({
    url: photo,
  })
}

async function crop() {
  if(!croppie) return

  myPhoto.value = await croppie.result({
    type: 'base64',
    size: 'viewport',
  })

  modalRef.value.close()
}

function onFileChange(e) {
  const file = e.target.files[0]
  e.target.value=''
  if (!file) return

  const reader = new FileReader()
  reader.onload = () => {
    openModal(reader.result)
  }
  reader.readAsDataURL(file)
}

onBeforeMount(() => {
  croppie?.destroy() // 截断操作：return null if croppie is null, else destroy.
})

defineExpose({ // 暴露组件，使得父组件可以调用
  myPhoto,
})
</script>

<template>
  <div class="flex justify-center">
    <div class="avatar relative">
      <div class="w-25 rounded-full">
        <img :src="myPhoto" alt="avatar">
      </div>
      <div @click="fileInputRef.click()" class="absolute left-0 top-0 w-25 h-25 flex justify-center items-center bg-black/20 rounded-full cursor-pointer">
        <CameraIcon/>
      </div>
    </div>
  </div>

  <input ref="file-input-ref" type="file" accept="image/*" class="hidden" @change="onFileChange">

  <dialog ref="modal-ref" class="modal">
    <div class="modal-box transition-none">
      <button @click="modalRef.close()" class="btn btn-circle btn-xs btn-ghost absolute right-2 top-2">✕</button>

      <div ref="croppie-ref" class="flex flex-col justify-center my-4"></div>
      <div class="modal-action">
        <div @click="modalRef.close()" class="btn">Cancel</div>
        <div @click="crop" class="btn btn-neutral">Confirm</div>
      </div>
    </div>

  </dialog>
</template>

<style scoped>

</style>