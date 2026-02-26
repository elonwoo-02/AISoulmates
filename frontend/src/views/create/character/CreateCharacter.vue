<script setup>
import Photo from "@/views/create/character/components/Photo.vue";
import BackgroundImage from "@/views/create/character/components/BackgroundImage.vue";
import Name from "@/views/create/character/components/Name.vue";
import Profile from "@/views/create/character/components/Profile.vue";
import { ref, useTemplateRef } from "vue";
import { base64ToFile } from "@/js/utils/base64_to_file.js";
import api from "@/js/http/api.js";
import { useRouter } from "vue-router";
import { useUserStore } from "@/stores/user.js";

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
  <main class="page-shell pb-12">
    <section class="glass-panel mx-auto max-w-3xl p-6 md:p-8">
      <h1 class="brand-font text-3xl text-[var(--text)]">Create Character</h1>
      <p class="mt-2 text-sm text-[var(--muted)]">Build a distinct persona with custom look and profile.</p>

      <div class="mt-6 grid gap-5 md:grid-cols-[220px_1fr]">
        <div class="space-y-5">
          <Photo ref="photo-ref" />
          <BackgroundImage ref="background-image-ref" />
        </div>

        <div class="space-y-5">
          <Name ref="name-ref" />
          <Profile ref="profile-ref" />

          <p v-if="errorMessage" class="rounded-xl   bg-rose-500/10 px-3 py-2 text-sm text-rose-500">{{ errorMessage }}</p>

          <div class="flex justify-end">
            <button @click="handleCreate" class="btn rounded-full  bg-[var(--accent)] px-8 text-white hover:opacity-90">Create</button>
          </div>
        </div>
      </div>
    </section>
  </main>
</template>

<style scoped>
</style>

