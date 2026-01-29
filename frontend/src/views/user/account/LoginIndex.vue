<script setup>
import {ref} from "vue";
import {useUserStore} from "@/stores/user.js";
import {useRouter} from "vue-router";
import api from "@/js/http/api.js";

const username = ref('')
const password = ref('')
const errorMessage = ref('')

const user = useUserStore()
const router = useRouter()

async function handlelogin() {
  errorMessage.value = '' // 清空
  if (!username.value.trim()) {
    errorMessage.value = 'Username is required.'
  } else if (!password.value.trim()) {
    errorMessage.value = 'Password is required'
  } else {
    try{
      const res = await api.post('api/user/account/login/', {
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
  <div class="flex justify-center mt-25">
      <form @submit.prevent="handlelogin" class="fieldset bg-base-200 border-base-300 rounded-box w-xs border p-4">

        <label class="label">Name</label>
        <input v-model="username" type="text" class="input" placeholder="name" />

<!--        <label class="label">Email</label>-->
<!--        <input type="email" class="input" placeholder="Email" />-->

        <label class="label">Password</label>
        <input v-model="password" type="password" class="input" placeholder="Password" />

        <p v-if="errorMessage" class="text-sm text-red-500 mt-1">{{ errorMessage }}</p>

        <button class="btn btn-neutral mt-4">Login</button>

        <div class="flex justify-end">
          <RouterLink :to="{name:'user-account-register-index'}" class="btn btn-sm btn-ghost text-gray-650">
            Have no account ? Create a account
          </RouterLink>

        </div>
      </form>
  </div>

</template>

<style scoped>

</style>