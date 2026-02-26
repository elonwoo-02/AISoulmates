<script setup>
import { ref } from "vue";
import { useUserStore } from "@/stores/user.js";
import { useRouter } from "vue-router";
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
  <main class="page-shell flex min-h-[78vh] items-center justify-center">
    <section class="glass-panel w-full max-w-md p-6 md:p-8">
      <p class="text-xs font-semibold uppercase tracking-[0.14em] text-[var(--muted)]">Join now</p>
      <h1 class="brand-font mt-2 text-3xl">Register</h1>

      <form @submit.prevent="handleRegister" class="mt-6 space-y-4">
        <fieldset class="space-y-1.5">
          <label class="text-sm font-semibold text-[var(--text)]">Name</label>
          <input v-model="username" type="text" class="soft-input auth-input" placeholder="Name" />
        </fieldset>

        <fieldset class="space-y-1.5">
          <label class="text-sm font-semibold text-[var(--text)]">Email</label>
          <input type="email" class="soft-input auth-input" placeholder="Email" />
        </fieldset>

        <fieldset class="space-y-1.5">
          <label class="text-sm font-semibold text-[var(--text)]">Password</label>
          <input v-model="password" type="password" class="soft-input auth-input" placeholder="Password" />
        </fieldset>

        <fieldset class="space-y-1.5">
          <label class="text-sm font-semibold text-[var(--text)]">Confirm Password</label>
          <input v-model="passwordConfirmed" type="password" class="soft-input auth-input" placeholder="Password" />
        </fieldset>

        <p v-if="errorMessage" class="rounded-xl bg-[var(--accent-soft)] px-3 py-2 text-sm text-[var(--accent)]">{{ errorMessage }}</p>

        <button class="btn w-full rounded-full bg-[var(--accent)] text-white hover:opacity-90">Create account</button>
      </form>
    </section>
  </main>
</template>

<style scoped>
.auth-input:focus,
.auth-input:focus-visible {
  outline: none;
  box-shadow: none !important;
}
</style>
