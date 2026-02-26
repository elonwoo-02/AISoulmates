<script setup>
import { nextTick, onBeforeUnmount, ref, useTemplateRef, watch } from "vue";
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
      viewport: { width: 210, height: 350 },
      boundary: { width: 400, height: 400 },
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

  myBackgroundImage.value = await croppie.result({
    type: 'base64',
    size: 'viewport',
  })

  closeModal()
}

function closeModal() {
  modalRef.value?.close()
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
  <fieldset class="space-y-3">
    <label class="text-sm font-semibold text-[var(--text)]">Background</label>

    <button type="button" @click="fileInputRef.click()" class="group relative h-28 w-20 overflow-hidden rounded-xl bg-[var(--bg-elevated)] cursor-pointer" aria-label="Upload background image">
      <img v-if="myBackgroundImage" :src="myBackgroundImage" alt="Background preview" class="h-full w-full object-cover">
      <div class="absolute inset-0 flex items-center justify-center bg-black/20 text-white transition group-hover:bg-black/35">
        <CameraIcon />
      </div>
    </button>
  </fieldset>

  <input ref="file-input-ref" type="file" class="hidden" accept="image/*" @change="onFileChange">

  <dialog ref="modal-ref" class="modal">
    <div class="modal-box max-w-2xl rounded-2xl bg-[var(--surface-strong)]">
      <button type="button" @click.stop.prevent="closeModal" class="absolute right-2 top-2 z-[120] inline-flex h-8 w-8 items-center justify-center text-[var(--muted)] transition-colors hover:text-[var(--text)]" aria-label="Close crop modal">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-5 w-5">
          <path d="M18 6L6 18"></path>
          <path d="M6 6l12 12"></path>
        </svg>
      </button>

      <div ref="croppie-ref" class="my-4 flex justify-center"></div>

      <div class="modal-action">
        <button type="button" @click="closeModal" class="btn rounded-full">Cancel</button>
        <button @click="crop" class="btn rounded-full bg-[var(--accent)] text-white hover:opacity-90">Confirm</button>
      </div>
    </div>
  </dialog>
</template>

<style scoped>
</style>

