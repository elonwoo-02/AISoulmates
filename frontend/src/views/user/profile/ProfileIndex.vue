<script setup>

import Photo from "@/views/user/profile/compoents/Photo.vue";
import Username from "@/views/user/profile/compoents/Username.vue";
import Profile from "@/views/user/profile/compoents/Profile.vue";
import {useUserStore} from "@/stores/user.js";
import {ref, useTemplateRef} from "vue";
import {base64ToFile} from "@/js/utils/base64_to_file.js";
import api from "@/js/http/api.js";

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
      formData.append('photo',base64ToFile(photo, 'photo.png'))
    }
    // 给后端发请求
    try {
      const res = await api.post('/api/user/profile/update', formData)
      const data = res.data
      if (data.result === 'success') {
        user.setUserInfo(data)
      } else {
        errorMessage.value = data.result
      }
    } catch (err) {
      // console.log(err)
    }
  }
}
</script>

<template>
  <div class="flex justify-center">
    <div class="card w-120 bg-base-200 shadow-sm mt-0">
      <div class="card-body">
        <h3 class="text-lg font-bold my-4">Edit Profile</h3>
        <Photo ref="photo-ref" :photo="user.photo"/>
        <Username ref="username-ref" :username="user.username"/>
        <Profile ref="profile-ref" :profile="user.profile"/>

        <p v-if="errorMessage" class="text-sm text-red-500">{{ errorMessage }}</p>
        <div class="flex justify-center">
          <button @click="handleUpdate" class="btn btn-neutral w-60 mt-2">Commit</button>
        </div>
      </div>
    </div>
  </div>

</template>

<style scoped>

</style>