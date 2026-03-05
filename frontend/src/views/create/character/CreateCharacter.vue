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
import TextureCard from "@/components/ui/TextureCard.vue";

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
  <div class="flex justify-center px-4 py-12">
    <TextureCard class="w-full max-w-4xl">
      <template #header>
        <div class="create-header">
          <h1 class="create-title">Create character</h1>
          <p class="create-subtitle">Add a new companion to your space with a unique style and story.</p>
        </div>
      </template>

      <form @submit.prevent="handleCreate" class="create-form">
        <aside class="create-media-panel">
          <Photo ref="photo-ref" />
          <BackgroundImage ref="background-image-ref" />
        </aside>

        <section class="create-fields">
          <Name ref="name-ref" />
          <Profile ref="profile-ref" />

          <p v-if="errorMessage" class="create-error">{{ errorMessage }}</p>
        </section>
      </form>

      <template #footer>
        <div class="create-footer">
          <span>Ready to publish this character?</span>
          <button type="submit" @click="handleCreate" class="btn btn-neutral create-button">Create</button>
        </div>
      </template>
    </TextureCard>
  </div>
</template>

<style scoped>
</style>
