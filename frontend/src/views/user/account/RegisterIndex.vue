<script setup>
import {ref} from "vue";
import {useUserStore} from "@/stores/user.js";
import {useRouter} from "vue-router";
import api from "@/js/http/api.js";

const username = ref('')
const password = ref('')
const passwordConfirmed = ref('')
const errorMessage = ref('')

const user = useUserStore()
const router = useRouter()

async function handleRegister() {
  errorMessage.value = ''
  if (!username.value.trim()) {
    errorMessage.value = 'Username is required.'
  } else if (!password.value.trim()) {
    errorMessage.value = 'Password is required'
  } else if (password.value.trim() !== passwordConfirmed.value.trim()) {
    errorMessage.value = 'Passwords do not match'
  } else {
    try {
      const res = await api.post('/api/user/account/register/', {
        username: username.value,
        password: password.value,
      })
      const data = res.data
      if (data.result === 'success') {
        user.setAccessToken(data.access)
        user.setUserInfo(data)
        await router.push({
          name: 'homepage-index'
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
  <div class="flex justify-center mt-10">
    <form @submit.prevent="handleRegister" class="fieldset bg-base-200 border-base-300 rounded-box w-xs border p-4">
      <label class="label">Name</label>
      <input v-model="username" type="text" class="input" placeholder="Name" />

      <label class="label">Email</label>
      <input type="email" class="input" placeholder="Email" />

      <label class="label">Password</label>
      <input v-model="password" type="password" class="input" placeholder="Password" />

      <label class="label">Confirm Password</label>
      <input v-model="passwordConfirmed" type="password" class="input" placeholder="Password" />

      <p v-if="errorMessage" class="text-sm text-red-500 mt-1">{{ errorMessage }}</p>

      <button class="btn btn-neutral mt-4">Create account</button>
    </form>
  </div>

</template>

<style scoped>

</style>