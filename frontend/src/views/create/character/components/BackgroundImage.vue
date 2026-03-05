<script setup>
import {nextTick, onBeforeUnmount, ref, useTemplateRef, watch} from "vue";
import CameraIcon from "@/views/user/profile/components/icon/CameraIcon.vue";
import TextureCard from "@/components/ui/TextureCard.vue";

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
  <TextureCard>
    <fieldset class="background-fieldset">
      <label class="background-label">Background</label>
      <div class="flex justify-center">
        <div class="avatar relative">
          <div v-if="myBackgroundImage" class="w-15 h-25 rounded-box">
            <img :src="myBackgroundImage" alt="myBackgroundImage"/>
          </div>
          <div v-else class="w-15 h-25 rounded-box bg-base-200"></div>
          <div @click="fileInputRef.click()" class="w-15 h-25 rounded-box absolute left-0 top-0 bg-black/20 flex justify-center items-center cursor-pointer">
            <CameraIcon/>
          </div>
        </div>
      </div>
      <p class="background-hint">Portrait image recommended.</p>
    </fieldset>
  </TextureCard>

  <input ref="file-input-ref" type="file" class="hidden" id="image/*" @change="onFileChange"/>

  <dialog ref="modal-ref" class="modal">
    <div class="modal-box transition-none max-2xl">
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
.background-fieldset {
  display: grid;
  gap: 10px;
}

.background-label {
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: rgba(15, 23, 42, 0.6);
}

.background-hint {
  text-align: center;
  font-size: 12px;
  color: rgba(15, 23, 42, 0.6);
}
</style>
