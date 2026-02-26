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
  <main class="page-shell pb-12">
    <section class="glass-panel overflow-hidden">
      <div class=" px-5 py-4 md:px-8">
        <h1 class="brand-font text-3xl tracking-tight">Channel Profile</h1>
        <p class="mt-1 text-sm text-[var(--muted)]">Customize how your profile appears in your space.</p>
      </div>

      <div class="grid gap-6 p-5 md:grid-cols-[260px_1fr] md:gap-8 md:p-8">
        <aside class="rounded-2xl bg-[var(--surface)] p-4">
          <Photo ref="photo-ref" :photo="user.photo" />
          <p class="mt-4 text-center text-xs text-[var(--muted)]">Upload a square image for best results.</p>
        </aside>

        <main class="space-y-4">
          <Username ref="username-ref" :username="user.username" />
          <Profile ref="profile-ref" :profile="user.profile" />

          <p v-if="errorMessage" class="rounded-xl   bg-rose-500/10 px-3 py-2 text-sm text-rose-500">
            {{ errorMessage }}
          </p>

          <div class="flex justify-end pt-2">
            <button @click="handleUpdate" class="btn rounded-full  bg-[var(--accent)] px-6 text-white">Save changes</button>
          </div>
        </main>
      </div>
    </section>
  </main>
</template>

<style scoped>
</style>


