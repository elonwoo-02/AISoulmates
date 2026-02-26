<script setup>
import { nextTick, onBeforeUnmount, ref, useTemplateRef, watch } from 'vue'
import CameraIcon from '@/views/user/profile/components/icon/CameraIcon.vue'
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

  closeModal()
}

function closeModal() {
  modalRef.value?.close()
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
      <div class="h-28 w-28 rounded-full bg-[var(--surface-strong)] p-0.5">
        <img :src="myPhoto" alt="avatar" class="rounded-full object-cover" />
      </div>

      <button
        type="button"
        @click="fileInputRef.click()"
        class="absolute inset-0 flex items-center justify-center rounded-full bg-black/28 text-white transition hover:bg-black/38 cursor-pointer"
        aria-label="Upload avatar"
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
    <div class="modal-box rounded-2xl bg-[var(--surface-strong)]">
      <button type="button" @click.stop.prevent="closeModal" class="absolute right-2 top-2 z-[120] inline-flex h-8 w-8 items-center justify-center text-[var(--muted)] transition-colors hover:text-[var(--text)]" aria-label="Close crop modal">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-5 w-5">
          <path d="M18 6L6 18"></path>
          <path d="M6 6l12 12"></path>
        </svg>
      </button>

      <div ref="croppie-ref" class="my-4 flex flex-col justify-center"></div>

      <div class="modal-action">
        <button type="button" @click="closeModal" class="btn rounded-full">Cancel</button>
        <button @click="crop" class="btn rounded-full bg-[var(--accent)] text-white">Confirm</button>
      </div>
    </div>
  </dialog>
</template>

<style scoped>
</style>

