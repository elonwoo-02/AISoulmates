<script setup>
import Photo from '@/views/user/profile/components/Photo.vue'
import Username from '@/views/user/profile/components/Username.vue'
import Profile from '@/views/user/profile/components/Profile.vue'

import { useUserStore } from '@/stores/user.js'
import { ref, useTemplateRef } from 'vue'
import { base64ToFile } from '@/js/utils/base64_to_file.js'
import api from '@/js/http/api.js'

const user = useUserStore()

const photoRef = useTemplateRef('photo-ref')
const profileRef = useTemplateRef('profile-ref')
const usernameRef = useTemplateRef('username-ref')

const errorMessage = ref('')

async function handleUpdate() {
  const photo = photoRef.value.myPhoto
  const username = usernameRef.value.myUsername.trim()
  const profile = profileRef.value.myProfile.trim()

  errorMessage.value = ''

  if (!photo) {
    errorMessage.value = 'avatar is required'
  } else if (!username) {
    errorMessage.value = 'username is required'
  } else if (!profile) {
    errorMessage.value = 'profile is required'
  } else {
    const formData = new FormData()
    formData.append('username', username)
    formData.append('profile', profile)

    if (photo !== user.photo) {
      formData.append('photo', base64ToFile(photo, 'photo.png'))
    }

    try {
      const res = await api.post('/api/user/profile/update', formData)
      const data = res.data

      if (data.result === 'success') {
        user.setUserInfo(data)
      } else {
        errorMessage.value = data.result
      }
    } catch {
      errorMessage.value = 'Failed to update profile'
    }
  }
}
</script>

<template>
  <div class="mx-auto w-full max-w-screen-lg px-4 py-6 md:px-6 lg:px-8">
    <section class="overflow-hidden rounded-3xl border border-base-300 bg-base-100 shadow-sm">
      <div class="border-b border-base-300 bg-base-200/60 px-5 py-4 md:px-8">
        <h1 class="text-2xl font-bold tracking-tight">Channel profile</h1>
        <p class="mt-1 text-sm text-base-content/70">Customize how your profile appears in your space.</p>
      </div>

      <div class="grid gap-6 p-5 md:grid-cols-[260px_1fr] md:gap-8 md:p-8">
        <aside class="rounded-2xl border border-base-300 bg-base-200/40 p-4">
          <Photo ref="photo-ref" :photo="user.photo" />
          <p class="mt-4 text-center text-xs text-base-content/65">Upload a square image for best results.</p>
        </aside>

        <main class="space-y-4">
          <Username ref="username-ref" :username="user.username" />
          <Profile ref="profile-ref" :profile="user.profile" />

          <p v-if="errorMessage" class="rounded-lg border border-error/30 bg-error/10 px-3 py-2 text-sm text-error-content">
            {{ errorMessage }}
          </p>

          <div class="flex justify-end pt-2">
            <button @click="handleUpdate" class="btn btn-neutral rounded-full px-6">Save changes</button>
          </div>
        </main>
      </div>
    </section>
  </div>
</template>

<style scoped>
</style>
