<script setup>

import Photo from "@/views/create/character/components/Photo.vue";
import BackgroundImage from "@/views/create/character/components/BackgroundImage.vue";
import Name from "@/views/create/character/components/Name.vue";
import Profile from "@/views/create/character/components/Profile.vue";
import {ref, useTemplateRef} from "vue";
import {base64ToFile} from "@/js/utils/base64_to_file.js";
import api from "@/js/http/api.js";
import {useRouter} from "vue-router";
import {useUserStore} from "@/stores/user.js";

const user = useUserStore()
const router = useRouter()

const photoRef = useTemplateRef('photo-ref')
const nameRef = useTemplateRef('name-ref')
const profileRef = useTemplateRef('profile-ref')
const backgroundImageRef = useTemplateRef('background-image-ref')
const errorMessage = ref('')

async function handleCreate() {
  const photo = photoRef.value.myPhoto
  const name = nameRef.value.myName?.trim()
  const profile = profileRef.value.myProfile?.trim()
  const backgroundImage = backgroundImageRef.value.myBackgroundImage

  errorMessage.value = ''
  if (!photo) {
    errorMessage.value = 'Photo is required'
  } else if (!name) {
    errorMessage.value = 'Name is required'
  } else if (!profile) {
    errorMessage.value = 'Profile is required'
  // } else if (!backgroundImage) {
  //   errorMessage.value = 'BackgroundImage image is required'
  } else {
    const formData = new FormData()
    formData.append('name', name)
    formData.append('profile', profile)
    formData.append('photo', base64ToFile(photo, 'photo.png'))
    if (backgroundImage) {
      formData.append('background_image', base64ToFile(backgroundImage, 'background_image.png'))
    }

    try {
      const res = await api.post('/api/create/character/create/', formData)
      const data = res.data
      if (data.result === 'success') {
        await router.push({
          name: 'user-space-index',
          params: { user_id: user.id }
        })
      } else {
        errorMessage.value = data.result
      }
    } catch (err) {
    }
  }
}
</script>

<template>
  <div class="mx-auto w-full max-w-5xl px-4 py-6 md:px-6 lg:px-8">
    <section class="overflow-hidden rounded-3xl border border-base-300 bg-base-100 shadow-sm">
      <div class="border-b border-base-300 bg-base-200/60 px-5 py-4 md:px-8">
        <h1 class="text-2xl font-bold tracking-tight">Create character</h1>
        <p class="mt-1 text-sm text-base-content/70">Add a new companion to your space with a unique style and story.</p>
      </div>

      <div class="grid gap-6 p-5 md:grid-cols-[260px_1fr] md:gap-8 md:p-8">
        <aside class="rounded-2xl border border-base-300 bg-base-200/40 p-4 space-y-4">
          <Photo ref="photo-ref" />
          <p class="text-center text-xs text-base-content/65">Upload a square image for best results.</p>
          <BackgroundImage ref="background-image-ref" />
          <p class="text-center text-xs text-base-content/65">Upload a portrait image for best results.</p>
        </aside>

        <main class="space-y-4">
          <Name ref="name-ref" />
          <Profile ref="profile-ref" />

          <p v-if="errorMessage" class="rounded-lg border border-error/30 bg-error/10 px-3 py-2 text-sm text-error-content">
            {{ errorMessage }}
          </p>

          <div class="flex justify-center pt-2">
            <button type="submit" @click="handleCreate" class="btn btn-neutral px-6">Create</button>
          </div>
        </main>
      </div>
    </section>
  </div>
</template>

<style scoped>
</style>
