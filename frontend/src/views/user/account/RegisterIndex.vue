<script setup>
import {ref} from "vue";
import {useUserStore} from "@/stores/user.js";
import {useRouter} from "vue-router";
import api from "@/js/http/api.js";
import TextureCard from "@/components/ui/TextureCard.vue";

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
  <div class="flex justify-center px-4 py-12">
    <TextureCard class="w-full max-w-md">
      <template #header>
        <div class="register-header">
          <div class="register-pill">Cult UI</div>
          <h1 class="register-title">Create your account</h1>
          <p class="register-subtitle">Start building a new companion in seconds.</p>
        </div>
      </template>

      <form @submit.prevent="handleRegister" class="register-form">
        <label class="register-label">Username</label>
        <input v-model="username" type="text" class="input register-input" placeholder="Name" />

        <label class="register-label">Email</label>
        <input type="email" class="input register-input" placeholder="Email" />

        <label class="register-label">Password</label>
        <input v-model="password" type="password" class="input register-input" placeholder="Password" />

        <label class="register-label">Confirm Password</label>
        <input v-model="passwordConfirmed" type="password" class="input register-input" placeholder="Password" />

        <p v-if="errorMessage" class="text-sm text-red-500 mt-1">{{ errorMessage }}</p>

        <button class="btn btn-neutral register-button">Create account</button>
      </form>

      <template #footer>
        <div class="register-footer">
          <span>Already have an account?</span>
          <RouterLink :to="{name:'user-account-login-index'}" class="register-link">
            Sign in
          </RouterLink>
        </div>
      </template>
    </TextureCard>
  </div>
</template>

<style scoped>
.register-header {
  display: grid;
  gap: 8px;
}

.register-pill {
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

.register-title {
  font-family: "Fraunces", "Sora", ui-serif, Georgia, serif;
  font-size: 28px;
  font-weight: 600;
  color: #0f172a;
}

.register-subtitle {
  color: rgba(15, 23, 42, 0.7);
  font-size: 14px;
}

.register-form {
  display: grid;
  gap: 12px;
}

.register-label {
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: rgba(15, 23, 42, 0.6);
}

.register-input {
  background: rgba(255, 255, 255, 0.9);
  border-color: rgba(15, 23, 42, 0.1);
}

.register-button {
  margin-top: 8px;
  background: #0f172a;
  color: #ffffff;
  border: none;
}

.register-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  font-size: 13px;
  color: rgba(15, 23, 42, 0.7);
}

.register-link {
  color: #0f172a;
  font-weight: 600;
}
</style>
