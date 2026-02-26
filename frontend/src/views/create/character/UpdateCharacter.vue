<script setup>
import Photo from "@/views/create/character/components/Photo.vue";
import BackgroundImage from "@/views/create/character/components/BackgroundImage.vue";
import Name from "@/views/create/character/components/Name.vue";
import Profile from "@/views/create/character/components/Profile.vue";
import { onMounted, ref, useTemplateRef } from "vue";
import { base64ToFile } from "@/js/utils/base64_to_file.js";
import api from "@/js/http/api.js";
import { useRoute, useRouter } from "vue-router";
import { useUserStore } from "@/stores/user.js";

const user = useUserStore()
const router = useRouter()
const route = useRoute()
const characterId = route.params.character_id
const character = ref(null)

onMounted(async () => {
  try {
    const res = await api.get(`/api/create/character/get_single/`, {
      params: {
        character_id: characterId
      }
    })
    const data = res.data
    if (data.result === 'success') {
      character.value = data.character
    }
  } catch (err) {
  }
})

const photoRef = useTemplateRef('photo-ref')
const nameRef = useTemplateRef('name-ref')
const profileRef = useTemplateRef('profile-ref')
const backgroundImageRef = useTemplateRef('background-image-ref')
const errorMessage = ref('')

async function handleUpdate() {
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
    formData.append('character_id', characterId)
    formData.append('name', name)
    formData.append('profile', profile)

    if (photo !== character.value.photo) {
      formData.append('photo', base64ToFile(photo, 'photo.png'))
    }

    if (!backgroundImage || backgroundImage && backgroundImage !== character.value.background_image) {
      formData.append('background_image', base64ToFile(backgroundImage, 'background_image.png'))
    }

    try {
      const res = await api.post('/api/create/character/update/', formData)
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
    <section v-if="character" class="glass-panel mx-auto max-w-3xl p-6 md:p-8">
      <h1 class="brand-font text-3xl text-[var(--text)]">Update Character</h1>
      <p class="mt-2 text-sm text-[var(--muted)]">Polish profile details while keeping your audience context.</p>

      <div class="mt-6 grid gap-5 md:grid-cols-[220px_1fr]">
        <div class="space-y-5">
          <Photo ref="photo-ref" :photo="character.photo" />
          <BackgroundImage ref="background-image-ref" :backgroundImage="character.background_image" />
        </div>

        <div class="space-y-5">
          <Name ref="name-ref" :name="character.name" />
          <Profile ref="profile-ref" :profile="character.profile" />

          <p v-if="errorMessage" class="rounded-xl   bg-rose-500/10 px-3 py-2 text-sm text-rose-500">{{ errorMessage }}</p>

          <div class="flex justify-end">
            <button @click="handleUpdate" class="btn rounded-full  bg-[var(--accent)] px-8 text-white hover:opacity-90">Update</button>
          </div>
        </div>
      </div>
    </section>
  </main>
</template>

<style scoped>
</style>

