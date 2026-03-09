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
import {computed} from "vue";
import MobilePageHeader from "@/components/navbar/MobilePageHeader.vue";

const user = useUserStore()
const router = useRouter()
const route = useRoute()
const characterId = route.params.character_id
const character = ref(null)
const backTarget = computed(() => {
  if (user.id) {
    return {
      name: "user-space-index",
      params: { user_id: user.id },
    }
  }

  return { name: "character-list" }
})

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
  <div v-if="character" class="mx-auto w-full max-w-5xl px-4 pb-6 pt-0 md:px-6 md:py-6 lg:px-8">
    <MobilePageHeader
      title="Update character"
      :fallback-route="backTarget"
    />

    <section class="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm">
      <div class="border-b border-base-300 bg-base-200/60 px-5 py-4 md:px-8">
        <h1 class="text-2xl font-bold tracking-tight">Update character</h1>
        <p class="mt-1 text-sm text-base-content/70">Refine details, refresh visuals, and keep your character profile in sync.</p>
      </div>

      <div class="grid gap-6 p-5 md:grid-cols-[260px_1fr] md:gap-8 md:p-8">
        <aside class="rounded-2xl border border-slate-200 bg-slate-50 p-4 space-y-4">
          <Photo ref="photo-ref" :photo="character.photo" />
          <p class="text-center text-xs text-base-content/65">Upload a square image for best results.</p>
          <BackgroundImage ref="background-image-ref" :backgroundImage="character.background_image" />
          <p class="text-center text-xs text-base-content/65">Upload a portrait image for best results.</p>
        </aside>

        <main class="space-y-4">
          <Name ref="name-ref" :name="character.name" />
          <Profile ref="profile-ref" :profile="character.profile" />

          <p v-if="errorMessage" class="rounded-lg border border-error/30 bg-error/10 px-3 py-2 text-sm text-error-content">
            {{ errorMessage }}
          </p>

          <div class="flex justify-center pt-2">
            <button type="submit" @click="handleUpdate" class="btn btn-neutral px-6">Save changes</button>
          </div>
        </main>
      </div>
    </section>
  </div>

</template>

<style scoped>

</style>
