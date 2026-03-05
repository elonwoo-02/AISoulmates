<script setup>
import Photo from "@/views/create/character/components/Photo.vue";
import BackgroundImage from "@/views/create/character/components/BackgroundImage.vue";
import Name from "@/views/create/character/components/Name.vue";
import Profile from "@/views/create/character/components/Profile.vue";
import {onMounted, ref, useTemplateRef} from "vue";
import {base64ToFile} from "@/js/utils/base64_to_file.js";
import api from "@/js/http/api.js";
import {useRoute, useRouter} from "vue-router";
import {useUserStore} from "@/stores/user.js";
import TextureCard from "@/components/ui/TextureCard.vue";

const user = useUserStore()
const router = useRouter()
const route = useRoute()
const characterId = route.params.character_id
const character = ref(null)

onMounted( async () => {
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
  // } else if (!backgroundImage) {
  //   errorMessage.value = 'BackgroundImage image is required'
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
  <div v-if="character" class="flex justify-center px-4 py-12">
    <TextureCard class="w-full max-w-4xl">
      <template #header>
        <div class="update-header">
          <h1 class="update-title">Update character</h1>
          <p class="update-subtitle">Refine details, refresh visuals, and keep your character profile in sync.</p>
        </div>
      </template>

      <form @submit.prevent="handleUpdate" class="update-form">
        <aside class="update-media-panel">
          <Photo ref="photo-ref" :photo="character.photo" />
          <BackgroundImage ref="background-image-ref" :backgroundImage="character.background_image" />
        </aside>

        <section class="update-fields">
          <Name ref="name-ref" :name="character.name" />
          <Profile ref="profile-ref" :profile="character.profile" />

          <p v-if="errorMessage" class="update-error">{{ errorMessage }}</p>
        </section>
      </form>

      <template #footer>
        <div class="update-footer">
          <span>Save your edits and return to your space.</span>
          <button type="submit" @click="handleUpdate" class="btn btn-neutral update-button">Save changes</button>
        </div>
      </template>
    </TextureCard>
  </div>

</template>

<style scoped>

</style>
