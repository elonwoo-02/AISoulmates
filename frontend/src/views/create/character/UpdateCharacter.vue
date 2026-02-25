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
  //   errorMessage.value = 'Background image is required'
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
  <div v-if="character" class="flex justify-center">
    <div class="card w-120 bg-base-200 shadow-sm mt-1">
      <div class="card-body">
        <h3 class="text-lg font-bold my-4">Update character</h3>
        <Photo ref="photo-ref" :photo="character.photo"/>
        <Name ref="name-ref" :name="character.name"/>
        <Profile ref="profile-ref" :profile="character.profile"/>
        <BackgroundImage ref="background-image-ref" :backgroundImage="character.background_image"/>

        <p v-if="errorMessage" class="text-sm text-red-500"> {{ errorMessage }}</p>

        <div class="flex justify-center">
          <div @click="handleUpdate" class="btn btn-neutral w-60 mt-2">Update</div>
        </div>
      </div>
    </div>
  </div>

</template>

<style scoped>

</style>