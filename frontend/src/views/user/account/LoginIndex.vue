<script setup>
import {ref} from "vue";
import {useUserStore} from "@/stores/user.js";
import {useRouter} from "vue-router";
import api from "@/js/http/api.js";
import TextureCard from "@/components/ui/TextureCard.vue";

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
  <div class="flex justify-center px-4 py-12">
    <TextureCard class="w-full max-w-md">
      <template #header>
        <div class="login-header">
          <div class="login-pill">Cult UI</div>
          <h1 class="login-title">Welcome back</h1>
          <p class="login-subtitle">Log in to continue your story.</p>
        </div>
      </template>

      <form @submit.prevent="handlelogin" class="login-form">
        <label class="login-label">Username</label>
        <input v-model="username" type="text" class="input login-input" placeholder="Name" />

        <label class="login-label">Password</label>
        <input v-model="password" type="password" class="input login-input" placeholder="Password" />

        <p v-if="errorMessage" class="text-sm text-red-500 mt-1">{{ errorMessage }}</p>

        <button class="btn btn-neutral login-button">Login</button>
      </form>

      <template #footer>
        <div class="login-footer">
          <span>New here?</span>
          <RouterLink :to="{name:'user-account-register-index'}" class="login-link">
            Create an account
          </RouterLink>
        </div>
      </template>
    </TextureCard>
  </div>

</template>

<style scoped>
.login-header {
  display: grid;
  gap: 8px;
}

.login-pill {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: fit-content;
  padding: 4px 10px;
  border-radius: 999px;
  background: rgba(15, 23, 42, 0.08);
  color: rgba(15, 23, 42, 0.7);
  font-size: 12px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.login-title {
  font-family: "Fraunces", "Sora", ui-serif, Georgia, serif;
  font-size: 28px;
  font-weight: 600;
  color: #0f172a;
}

.login-subtitle {
  color: rgba(15, 23, 42, 0.7);
  font-size: 14px;
}

.login-form {
  display: grid;
  gap: 12px;
}

.login-label {
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: rgba(15, 23, 42, 0.6);
}

.login-input {
  background: rgba(255, 255, 255, 0.9);
  border-color: rgba(15, 23, 42, 0.1);
}

.login-button {
  margin-top: 8px;
  background: #0f172a;
  color: #ffffff;
  border: none;
}

.login-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  font-size: 13px;
  color: rgba(15, 23, 42, 0.7);
}

.login-link {
  color: #0f172a;
  font-weight: 600;
}
</style>
